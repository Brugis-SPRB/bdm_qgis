# -*- coding: utf8 -*-
# plugin deployement to local repository

import os
import socket
from datetime import datetime
import  sys
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

sys.path.append("C:/scripts/custom")

import zipfile
from time import strftime


################################################################################
def zipdir(path, ziph):
	# Iterate all the directories and files
	for root, dirs, files in os.walk(path):
		# Create a prefix variable with the folder structure inside the path folder. 
		# So if a file is at the path directory will be at the root directory of the zip file
		# so the prefix will be empty. If the file belongs to a containing folder of path folder 
		# then the prefix will be that folder.
		if root.replace(path,'') == '':
			prefix = ''
		else:
			# Keep the folder structure after the path folder, append a '/' at the end 
			# and remome the first character, if it is a '/' in order to have a path like 
			# folder1/folder2/file.txt
			prefix = root.replace(path, '') + '/'
			if (prefix[0] == '/'):
				prefix = prefix[1:]
		for filename in files:
			actual_file_path = root + '/' + filename
			zipped_file_path = prefix + filename
			zipf.write( actual_file_path, zipped_file_path)

def doLog(myLine, myFile):
	print myLine
	if myLine is None:
		myFile.write("{}\n".format(datetime.today()) )
	else:
		myFile.write("{} : {}\n".format(datetime.today(),myLine) )

if __name__ == "__main__":
	repodir = "//xxxx/xxx/"
	version = "0.1"
	downloadsubdir = "xxx/"
	custom_config_dir = "C:/scripts/custom/"
	updatetime = strftime("%Y-%m-%dT%H:%M:%S")	
	listplugins = ["bdmEditor","bdmAdmin"]
	operator = "x. xxx (xxx)"
	about = "Brugis data management plugin (Web Access)"
	homepage = "http://www.xxx.xxx.be/xxx/xxx/"
	
	
	logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.now().strftime('%d_%m_%Y'))
	with open(os.path.join(os.path.dirname(__file__), logFileName), 'a') as logFile:
		doLog('Startup deploy BDM Pluggin ', logFile)

		###################
		## Generate and upload plugins
		for plugName in listplugins:
	
			zipfilename = os.path.join(os.path.dirname(__file__),'{}.{}.zip'.format(plugName,version))
			uploaddir = os.path.join(repodir,downloadsubdir) 
			targetzipfilename = os.path.join(repodir,'{}.{}.zip'.format(plugName,version))
			
			if os.path.exists(zipfilename):
				os.remove(zipfilename)
				doLog('Zip file removed', logFile)
			if os.path.exists(targetzipfilename):
				os.remove(targetzipfilename)
				doLog('Target Zip file removed', logFile)
			
			
			zipf = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED)
			zipdir(os.path.join(os.path.dirname(__file__), plugName), zipf)
			zipf.close()
			
			shutil.copyfile(zipfilename, targetzipfilename)
		
		###############################
		## Update repository xml

		xmltemplatefilename = os.path.join(os.path.dirname(__file__),'plugins_template.xml')
		xmlfilename = os.path.join(os.path.dirname(__file__),'plugins.xml')
		targetxmlfilename = os.path.join(repodir,'plugins.xml')

		tempf = open(xmltemplatefilename, 'r') 
		tempcontent = tempf.read()
		tempcontent = tempcontent.replace("[VERSION]",version)
		tempcontent = tempcontent.replace("[DOWNLOAD_DIR]",downloadsubdir)
		tempcontent = tempcontent.replace("[UPD_DATETIME]",updatetime)
		tempcontent = tempcontent.replace("[OPERATOR]",operator)
		tempcontent = tempcontent.replace("[ABOUT]",about)
		tempcontent = tempcontent.replace("[REPOSITORY]",repodir)
		tempcontent = tempcontent.replace("[HOMEPAGE]",homepage)





		tempf.close()
		if os.path.exists(xmlfilename):
			os.remove(xmlfilename)
			doLog('Local xml file removed', logFile)

		with open(xmlfilename, 'w+') as xmlf:  
			xmlf.write(tempcontent)

		if os.path.exists(targetxmlfilename):
			os.remove(targetxmlfilename)
			doLog('Target xml file removed', logFile)
		shutil.copyfile(xmlfilename, targetxmlfilename)
		doLog('Done', logFile)



		
					
			






