**ANDROID SMS AND MMS RETRIEVAL**
========================================================================================================================
**SET-UP AND LOGISTICS**


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

========================================================================================================================
**PURPOSE AND INSIGHT**

	This tool was built with the purpose of extracting SMS and MMS messages from a ROOTED Android device.
	The tool takes a single database file found in the Android Filesystem, which is only accessible by rooting
	the device, and extracts its contents in SMS and MMS form. MMS are multimedia messages which include pictures,
	audio, video, and contact Vcards. SMS are regular text messages. It would be used for example, if a device
	is cosmetically damaged and does not allow investigators to physically see messages on the device itself.
	If the mmssms.db-journal file is available, deleted SMS and MMS messages might be possible to view, using this tool.




========================================================================================================================
    There are numerous methods in which to root android devices, and how to access the file system.
    The method I chose was to download a rootkit, apply it to the device and then copy over the necessary files over SSH.
    
    If an image of the filesystem was available:
    	-Recover the file:
    		/data/data/com.android.providers.telephony/databases/mmssms.db
    	-Recover the folder:
    		/data/data/com.android.providers.telephony/app_parts/
    
    The first file is the database in which all sms and mms messages are stored.
    The second is the folder in which all of the media files sent and received via MMS messages are stored.(ACTUAL FILES)

========================================================================================================================

    This tool recovers all SMS messages and organizes them
    into SMS Conversations with statistics provided.
    
    	Individual Conversation Statistic file:
    		Statistics.txt:
    			TOTAL AMOUNT OF MESSAGES SENT: Total amount of messages sent in conversation.
    			TOTAL AMOUNT OF MESSAGES RECEIVED: Total amount of messages received in conversation.
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
    			 messages will most likely be the number of the device you are examining.
    			 All other fields are effectively sent MMS messages.
    				Format:
    					Phone Number: Amount of messages and corresponding files associated.
    				At the end:
    					Total amount of messages & files in device.	
    					
========================================================================================================================
**RUNNING THE TOOL**

		1. Root android device
			-Method of your choice.
			-Tons of options.

		2. Install && open SSHDroid (ssh server)
			-Make note of the Address field inside SSHDroid we will need this.
			-Make sure SSHDroid is running

		3. Download SMSMMS folder from github:
			-git clone https://github.com/muri11as/ANDROID-SMS

		4. Open a new Terminal window
			-Copy over app_parts folder from android device with the following command:
			-In my case, my phone's SSH server address is 192.168.1.4 and the user is root
				Usage: scp -r user@address:folder/to/fetch path/to/new/location

				scp -r root@192.168.1.4:/data/data/com.android.providers.telephony/app_parts path/to/ANDROID-SMS/app_parts
				Enter password: (Default is set to admin)
				**If there are alot of files here, this might take a while**

			-Copy over mmssms.db from android device with the following command:
				Usage: scp user@address:/path/to/file /path/to/new/location
				
				scp root@192.168.1.4:/data/data/com.android.providers.telephony/databases/mmssms.db path/to/ANDROID-SMS/
				Enter password: (Default is set to admin)
			
			 **Now you should have the messageExtract.py script, the mmssms.db file, and the app_parts
			 folder all in the same place.**
			 
		5. Run messageExtract.py
			Usage: python path/to/ANDROID-SMS/messageExtract.py path/to/ANDROID-SMS 
========================================================================================================================
**FUTURE EXPLORATIONS**
	
	-Was not able to find the mmssms.db-journal file in which deleted messages would be stored.
	More thorough research in this topic would be needed. If this file was found, we could run this tool,
	changing the name of the database to mmssms.db-journal, and the same results would be expected,
	this time with deleted SMS and MMS messages.
	
	-Perhaps running the app_parts folder through an exif analyzing tool would give forensic examiners
	a more thorough insight into the image files being sent and received from the device. This could be
	an extension to this project, although for the purpose of retrieving SMS and MMS messages it was not
	essential to this project. 
	
	
