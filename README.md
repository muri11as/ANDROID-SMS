**ANDROID SMS AND MMS RETRIEVAL**
========================================================================================================================

    Requirements to run this tool:
	  -python 2.7
	  -sqlite3 for python
	
    Resources Used:
    	-SQLite Database Browser 2.0 for MacOSX: [http://sourceforge.net/projects/sqlitebrowser/]
    		This was mainly used to graphically inspect the database file.
    		I found many of the attributes in the tables which would be useful to construct this tool.
    		Having this tool, made it much easier for me to visually see and put together specifically what I needed
    		
    		For example: 
    			-Getting the numbers the MMS messages were associated with wasn't spelled out anywhere. 
    			Using the same message id from two different tables I was able to construct a relationship.
    			-Finding the right attributes to properly display a message as an object.
    	-

========================================================================================================================

    There are numerous methods in which to root android devices, and how to access the file system.
    The method I chose was to download a rootkit, apply it to the device and then copy over the necessary files over SSH.
    
    If an image of the filesystem was available:
    	-Recover the file:
    		/data/data/com.android.providers.telephony/databases/mmssms.db
    	-Recover the folder:
    		/data/data/com.android.providers.telephony/app_parts/
    
    The first file is the database in which all sms and mms messages are stored.
    The second is the folder in which all of the media files sent and recieved via MMS messages are stored.(ACTUAL FILES)

========================================================================================================================

    This tool recovers all SMS messages and organizes them
    into SMS Conversations with statistics provided.
    
    	Individual Conversation Statistic file:
    		Statistics.txt:
    			TOTAL AMOUNT OF MESSAGES SENT: Total amount of messages sent in conversation.
    			TOTAL AMOUNT OF MESSAGES RECIEVED: Total amount of messages received in conversation.
    			TOTAL AMOUNT OF MESSAGES: Total amount of messages in conversation.
    			RANGING FROM: Date of first message in conversation.
    			TO: Date of latest message in conversation.
    	Statistics for all SMS Conversations:
    		SMSHISTOGRAM.TXT:
    			-Displays Histogram showing what numbers were contacted and their frequency, highest at top.	
    				Format:
    					Phone Number:Amount of total messages
    				At the end:
    					Total amount of messages in device.
========================================================================================================================
    This tool also recovers all MMS messages and organizes them into MMS Conversations,
    with the respective files from app_parts inside of the folder.(Clicking a file
    within a MMS Conversation yields the actual file) this tool places JPG,PNG,AUDIO/3GPP,
    and VCARD Contact Information inside of an MMS Conversation.
    	
    	Statistics for all MMS Conversations:
    		MMSHISTOGRAM.TXT:
    			-Displays Histogram showing the amount of MMS messages associated with a specific
    			 Phone Number, and the amount of messages associated. The number with the most
    			 messsages will most likely be the number of the device you are examining.
    			 All other fields are effectively sent MMS messages.
    				Format:
    					Phone Number: Amount of messages and corresponding files associated.
    				At the end:
    					Total amount of messages & files in device.	
    					
========================================================================================================================

		1. Root android device
		2. Install && open SSHDroid (ssh server)
			-Make note of the Address field inside SSHDroid we will need this.
			-Make sure SSHDroid is running
		3. Download SMSMMS folder from github: https://github.com/muri11as/ANDROID-SMS
		4. open terminal 
			-Copy over app_parts folder from android device with the following command:
				scp -r root@192.168.1.4:/data/data/com.android.providers.telephony/app_parts path/to/ANDROID-SMS/
				Enter password: (Default is set to admin)
			-Copy over mmssms.db from android device with the following command:
				scp root@192.168.1.4:/data/data/com.android.providers.telephony/databases/mmssms.db path/to/ANDROID-SMS/
				Enter password: (Default is set to admin)
		5. Now you should have the messageExtract.py script, the mmssms.db file, and the app_parts folder all in the same place. 
