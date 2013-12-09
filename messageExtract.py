'''
Author: Cesar Murillas
CS6963 Digital Forensics
Professor Joel Fernandez
Final Project Fall 2013
ANDROID-SMS-MMS-EXTRACTOR

USAGE: messageExtract.py /path/to/SMSMMS folder
'''
import operator
import sys
import os 
import time
import sqlite3
import subprocess
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
	
	def getconviD(self):
		return self.convoiD
		
	def getName(self):
		return self.name
		
	def getTotal(self):
		return self.total
	
	def addMsg(self, obj):
		if self.convoiD == obj.getiD() and self.uiD != obj.getuniID():
			self.__msgs.append(obj)
			
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
		line2 = "TOTAL AMOUNT OF MESSAGES RECEIVED: "+str(rec)+'\n\n'
		line3 = "TOTAL AMOUNT OF MESSAGES: "+str(total)+'\n\n'
		line4 = "RANGING FROM: "+self.__msgs[0].getDate()+'\n\n'
		line5 = "TO: "+self.__msgs[total-1].getDate()+'\n\n'
		seq = line+line1+line2+line3+line4+line5
		filey.write(seq)
		
class MMSmsg:
	'''This class will hold the basic MMS message structure on an Android Device, for the purpose of this project, we limit this to just PNG and JPEG images, Audo3GPP, and Contact Vcard files'''

	def __init__(self, iD, img):
		self.mID = iD
		self.number = 0
		self.image = str(img)
		
	def getmID(self):
		return self.mID
		
	def getImage(self):
		return self.image
		
	def addNum(self, number):
		self.number = number
		
	def getName(self):
		return self.number
	
	
class MMSconvo:
	'''This class will hold the MMS messages in PNG/JPEG format associated with the same Phone Number'''
	
	def __init__(self, obj):
		self.__mms = []
		self.__mms.append(obj)
		self.name = obj.getmID()
		self.num = obj.getName()
		self.total = 0
		self.imgs = []
	def getName(self):
		return self.name
		
	def getImages(self):
		for i in self.__mms:
			if not i.getImage() in self.imgs:
				self.imgs.append(i.getImage())
		return self.imgs
		
	def getNum(self):
		return self.num
	
	def addMsg(self,obj):
		self.__mms.append(obj)
		
	def setTotal(self):
		for i in self.__mms:
			self.total+=1
	def getTotal(self):
		return self.total				
		
class MMSExtractor:
	'''This class takes care of extracting and outputting the MMS messages found. ONLY .jpg, png, audio3gpp, and contact vcards are supported'''
	
	def __init__(self, path):
		self.path = path
		self.messages =[]
		self.convos={}
		self.total = 0
		
	def run(self):
		# POPULATE MMS MESSAGES AND CONVERSATIONS FROM ANDROID DEVICE data/data/com.android.providers.telephony/databases/mmssms.db (sqlite DB)
		conn = sqlite3.connect(self.path+'mmssms.db')
		c = conn.cursor()
		c.execute('SELECT mid, ct, _data from part')
		results = c.fetchall()
		for result in results:
			if (result[1] == "image/jpeg" or result[1] == "image/png" or result[1] == "audio/3gpp" or result[1] == "text/x-vcard"):
				img = result[2]
				new = img[53:]
				m = MMSmsg(result[0], new)
				self.messages.append(m)		
		c.execute('SELECT msg_id, address from addr')
		results = c.fetchall()
		for result in results:
			for i in self.messages:
				if i.getmID() == result[0] and result[1]!= "insert-address-token":
					i.addNum(result[1])
		conn.close()
		self.sort()
		self.output()
		
	def sort(self):
		# SORT OUT ALL MESSAGES INTO CONVERSATIONS
		for i in self.messages:
			if i.getName() in self.convos:
				#THIS MESSAGE BELONGS TO A CONVERSATION, LET'S ADD IT
				self.convos.get(i.getName()).addMsg(i)
			else:
				#MESSAGE BELONGS IN A NEW CONVERSATION
				conv = MMSconvo(i)
				self.convos[i.getName()] = conv
		
	def output(self):
		# WRITE EVERYTHING OUT. MMS MESSAGES WILL BE AVAILABLE FOR VIEWING IN THE CURRENT WORKING DIR. THEY WILL BE COPIED FROM THE app_parts FOLDER, TO THE RESPECTIVE MMS CONVO
		convoStats = self.path+'MMSHISTOGRAM.TXT'
		filey = open(convoStats,'w')
		line = "*****MMS CONVERSATION HISTOGRAM*****\n\n DISPLAYS:\n\n NUMBER:AMOUNT OF MMS MESSAGES\n\n"
		line1 ="***THIS DISPLAYS JPG, PNG, AUDIO3GPP, and CONTACT VCARD FILES***\n\n***THE FIRST NUMBER IS PROBABLY THE NUMBER OF THIS DEVICE, IT USUALLY HAS THE HIGHEST COUNT BECAUSE THE INCOMING MMS MESSAGES ARE STORED THERE***\n\n"
		lin = line+line1
		filey.write(lin)
		
		dic = {}
		for key in self.convos:
			self.convos[key].setTotal()
			mmsOutput = '{0}/MMSCONVOS/{1}'.format(os.path.dirname(os.path.abspath(__file__)),self.convos[key].getNum())
			if not os.path.exists(mmsOutput):
				 os.makedirs(mmsOutput)	
			liss = self.convos[key].getImages()	
			self.total += self.convos[key].getTotal()
			dic[self.convos[key].getNum()] = self.convos[key].getTotal()
			if len(liss) != 0:
				for i in liss:
					cmd = 'cp '+self.path+'app_parts/'+i+' '+mmsOutput+'/'
					subprocess.call(cmd,shell=True)
		sdic = sorted(dic.items(), key=operator.itemgetter(1))
		reverse = sdic[::-1]
		for i in reverse:
			line =  i[0]+': '+str(i[1])+'\n\n'
			filey.write(line)
		line2 = "TOTAL AMOUNT OF MESSAGES IN DEVICE: "+str(self.total)
		filey.write(line2)
		filey.close()			
					
class SMSExtractor:
	'''This class takes care of extracting and outputting all SMS messages into SMS conversations'''
	def __init__(self, path):
		self.messages = []
		self.convos = {}
		self.path = path
		self.total = 0
	
	def run(self):
		##POPULATE SMS MESSAGES AND CONVERSATIONS FROM ANDROID DEVICE data/data/com.android.providers.telephony/databases/mmssms.db (sqlite DB)
		conn = sqlite3.connect(self.path+'mmssms.db')
		c = conn.cursor()
		c.execute('SELECT _id, thread_id, address, date, type, body FROM sms')
		results = c.fetchall()
		for result in results:
				h = SMSmsg(result[0], result[1], result[2], result[3], result[4], result[5])
				h.convertTime()
				self.messages.append(h)				
		conn.close()
		self.sort()
		self.output()
			
	def sort(self):
		# SORT OUT ALL MESSAGES INTO CONVERSATIONS
		for i in self.messages:
			if i.getiD() in self.convos:
				#THIS MESSAGE BELONGS TO A CONVERSATION, LET'S ADD IT
				self.convos.get(i.getiD()).addMsg(i)
			else:
				#MESSAGE BELONGS IN A NEW CONVERSATION
				conv = SMSconvo(i)
				self.convos[i.getiD()] = conv
				
	def output(self):
		##WRITE OUT ALL CONVERSATIONS && STATISTICS
		convoStats = self.path+'SMSHISTOGRAM.TXT'
		filey = open(convoStats,'w')
		line = "*****SMS CONVERSATION HISTOGRAM*****\n\n DISPLAYS\n\n NUMBER:AMOUNT OF SMS MESSAGES\n\n"
		filey.write(line)
		dic = {}
		for key in self.convos:
			smsOutput = '{0}/SMSCONVOS/{1}'.format(os.path.dirname(os.path.abspath(__file__)),self.convos[key].getName())
			if not os.path.exists(smsOutput): os.makedirs(smsOutput)
			smsOutputFile = smsOutput+'/'+self.convos[key].getName()+'.txt'
			stats = smsOutput+'/Statistics'+'.txt'
			filey1 = open(smsOutputFile,'w')
			filey2 = open(stats,'w')
			self.convos[key].writeOut(filey1)
			self.convos[key].writeStats(filey2)
			dic[self.convos[key].getName()] = self.convos[key].getTotal()
			self.total += self.convos[key].getTotal()
			filey1.close()
			filey2.close()
		sdic = sorted(dic.items(), key=operator.itemgetter(1))
		r = sdic[::-1]
		for i in r:
			line =  i[0]+': '+str(i[1])+'\n\n'
			filey.write(line)
		line2 = "TOTAL AMOUNT OF MESSAGES IN DEVICE: "+str(self.total)
		filey.write(line2)
		filey.close()
		
def main():

	rootpath = sys.argv[1]
	ex = SMSExtractor(rootpath)
	ex.run()
	mex = MMSExtractor(rootpath)
	mex.run()
			
if __name__ == "__main__":
    main()