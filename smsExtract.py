'''
Author: Cesar Murillas
CS6963 Digital Forensics
Professor Joel Fernandez
Final Project Fall 2013
Android SMS
'''
import argparse
import sys
import os 
import time
import sqlite3
import itertools
import pickle

rootpath = ""

class SMSmsg:
	'''This class will hold the basic structure of a regular SMS message on an Android device'''

	def __init__(self, iD, threadID, PhoneNum, datetime, rec, msg):
		self.uniqueID = str(iD)
		self.iD = str(threadID)
		self.Num = str(PhoneNum)
		self.date = float(datetime)
		self.recieved = int(rec)
		self.body = msg.encode("utf-8")
		
	def getNum(self):
		return self.Num
		
	def getiD(self):
		return self.iD
		
	def getuniID(self):
		return self.uniqueID
		
	def getStatus(self):
		return self.recieved
		
	def getDate(self):
		return self.date

	def convertTime(self):
	#Convert EPOCH time to regular time in Y-M-D format
		self.date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((self.date/1000)))
		
	def display(self):
		if self.recieved == 1:
			print 'FROM: '+self.Num 
		else:
			print 'TO: '+self.Num
		print 'DATE: '+self.date+'\n\t'+self.body+'\n'
		
	def writeOut(self,filey):
		
		if self.recieved == 1:
			line =  'FROM: '+self.Num+'\n'
			filey.write(line )
		else:
			line = 'TO: '+self.Num+'\n'
			filey.write(line)
		rest = 'DATE: '+self.date+'\n\t'+self.body+'\n\n'
		filey.write(rest) 
		
	

class SMSconvo:
	'''This class will hold the SMS messages that are meant for the same Phone Number, effectively modeling a conversation on a mobile device'''
	
	def __init__(self, obj):
		self.uiD = obj.getuniID()
		self.convoiD = obj.getiD()
		self.name = obj.getNum()
		self.__msgs = []
		self.__msgs.append(obj)
		self.total = 0
		
	def display(self):
		print "**NEW CONVO**"
		count = 0
		for i in self.__msgs:
			count+=1
			i.display()
		print "TOTAL amount of msgs: "+str(count)
		print "*****END OF CONVERSATION*****"
		
	def getUnique(self):
		return self.uiD
	
	def getconviD(self):
		return self.convoiD
		
	def getName(self):
		return self.name
		
	def getTotal(self):
		return self.total
	
	def addMsg(self, obj):
		if self.convoiD == obj.getiD() and self.uiD != obj.getuniID():
			self.__msgs.append(obj)
		else:
			#NOT THE SAME CONVO
			print " "
			
	def writeOut(self,filey):
		for i in self.__msgs:
			i.writeOut(filey)
	
	def writeStats(self,filey):
		sent = 0
		rec = 0
		total = 0
		for i in self.__msgs:
			if i.getStatus() == 1:
				rec +=1
			else:
				sent+=1
			total +=1
		self.total = total				
		line = "***STATISTICS FOR THIS CONVERSATION***\n\n"
		line1 = "TOTAL AMOUNT OF MESSAGES SENT: "+str(sent)+'\n\n'
		line2 = "TOTAL AMOUNT OF MESSAGES RECIEVED: "+str(rec)+'\n\n'
		line3 = "TOTAL AMOUNT OF MESSAGES: "+str(total)+'\n\n'
		line4 = "RANGING FROM: "+self.__msgs[0].getDate()+'\n\n'
		line5 = "TO: "+self.__msgs[total-1].getDate()+'\n\n'
		seq = line+line1+line2+line3+line4+line5
		filey.write(seq)
		
class MMSmessage:
	'''This class will hold the basic MMS message structure on an Android Device, for the purpose of this project, we limit this to just PNG and JPEG images'''

	def __init__(self, iD, image):
		self.mID = iD
		self.image = image
	def getmID(self):
		return self.mID
	def getImage(self):
		return self.image
class MMSconvo:
	'''This class will hold the MMS messages in PNG/JPEG format associated with the same Phone Number'''
	def __init__(self, obj):
		self.__mms = []
		self.__mms.append(obj)
		
		
def main():

	rootpath = sys.argv[1]
##POPULATE SMS MESSAGES AND CONVERSATIONS FROM ANDROID DEVICE data/data/com.android.providers.telephony/databases/mmssms.db (sqlite DB)
	messages = []
	convos = {}
	conn = sqlite3.connect(rootpath+'mmssms.db')
	c = conn.cursor()
	c.execute('SELECT _id, thread_id, address, date, type, body FROM sms')
	results = c.fetchall()
	for result in results:
			h = SMSmsg(result[0], result[1], result[2], result[3], result[4], result[5])
			h.convertTime()
			messages.append(h)			
			
	conn.close()	
	print "Messages: "+str(len(messages))
	
	# SORT OUT ALL MESSAGES INTO CONVERSATIONS
	for i in messages:
			if i.getiD() in convos:
				#THIS MESSAGE BELONGS TO A CONVERSATION, LET'S ADD IT
				convos.get(i.getiD()).addMsg(i)
			else:
				#MESSAGE BELONGS IN A NEW CONVERSATION
				conv = SMSconvo(i)
				convos[i.getiD()] = conv
				
##WRITE OUT ALL CONVERSATIONS INTO SMSCONVOS FOLDER		
	convoStats = rootpath+'SMSCONVOSTATS.TXT'
	filey = open(convoStats,'w')
	line = "*****SMS CONVERSATION HISTOGRAM*****\n\n DISPLAYS\n\n NUMBER:AMOUNT OF SMS MESSAGES\n\n"
	filey.write(line)
	for key in convos:
		smsOutput = '{0}/SMSCONVOS/{1}'.format(os.path.dirname(os.path.abspath(__file__)),convos[key].getName())
		if not os.path.exists(smsOutput): os.makedirs(smsOutput)
		smsOutputFile = smsOutput+'/'+convos[key].getName()+'.txt'
		stats = smsOutput+'/Statistics'+'.txt'
		filey1 = open(smsOutputFile,'w')
		filey2 = open(stats,'w')
		convos[key].writeOut(filey1)
		convos[key].writeStats(filey2)
		line = convos[key].getName()+': '+str(convos[key].getTotal())+'\n\n'
		filey.write(line)
		filey1.close()
		filey2.close()
	filey.close()
		
if __name__ == "__main__":
    main()