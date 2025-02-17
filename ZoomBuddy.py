import webbrowser, subprocess, requests, json, csv, sys

from os import system, name, path, rename
from datetime import datetime
from time import sleep

VERSION = "1.0.5"
URL = "https://github.com/MNThomson/ZoomBuddy"
API_URL = 'https://api.github.com/repos/mnthomson/zoombuddy/releases/latest'
Update_URL = 'https://github.com/MNThomson/ZoomBuddy/releases/latest'

def main():
	figlet()
	update()
        while(True):    
            auto()
            sleep(5)

def figlet():
	#Figlet for ZoomBuddy
	print("\
 _____                     ____            _     _\n\
|__  /___   ___  _ __ ___ | __ ) _   _  __| | __| |_   _\n\
  / // _ \\ / _ \\| '_ ` _ \\|  _ \\| | | |/ _` |/ _` | | | |\n\
 / /| (_) | (_) | | | | | | |_) | |_| | (_| | (_| | |_| |\n\
/____\\___/ \\___/|_| |_| |_|____/ \\__,_|\\__,_|\\__,_|\\__, |")
	print("v" + VERSION, end ="")
	for i in range(1,41-len(VERSION)):
		print(" ", end ="")
	print("MNThomson |___/")

#Check for updates
def update():
	try:
		response = requests.get(API_URL).text
	except:
		return
	data = json.loads(response)
	CURRENT_VERSION = data['tag_name'].split("v")[1]

	if (int(VERSION.replace('.','')) < int(CURRENT_VERSION.replace('.',''))):
		print("Downloaded Version: v" + VERSION)
		print("Current Version:    v" + CURRENT_VERSION)
		Choice = input('Would you like to update ZoomBuddy? (Y/N)')
		if Choice.lower() == 'yes' or Choice.lower() == 'y':
			#Yes to update
			if getattr(sys, 'frozen', False):
				print('Redircting...')
				webbrowser.open(Update_URL)
				sys.exit(0)
			else:
				print("Either run a git pull or reclone this repo.")
				Choice = input('Would you like to be redirected to the Github page? (Y/N)')
				if Choice.lower() == 'yes' or Choice.lower() == 'y':
					#Yes to update
					print('Redircting...')
					webbrowser.open(Update_URL)
					sys.exit(0)
		system("cls||clear")
		figlet()

#Open the ZoomData file with exceptions
def open_data():
	#Open the ZoomData csv file and skip first line (since it's the formatting)
	try:
		file = open('ZoomData.csv', 'r')
		csvfile = csv.reader(file)
		next(csvfile)
		return file, csvfile
	except FileNotFoundError:
		if path.isfile('EXAMPLE_ZoomData.csv'):
			print("Found file named: EXAMPLE_ZoomData.csv")
			Choice = input('Would you like to rename it to ZoomData.csv? (Y/N)')
			if Choice.lower() == 'yes' or Choice.lower() == 'y':
				print('Renaming...')
				rename("EXAMPLE_ZoomData.csv", "ZoomData.csv")
				print("Finished renaming. Please rerun ZoomBuddy!")
		else:
			print("ZoomData.csv Does Not Exist!")
			print("Please read the setup instructions for ZoomData.csv")
			Choice = input('Would you like to be redirected to the instructions page? (Y/N)')
			if Choice.lower() == 'yes' or Choice.lower() == 'y':
				print('Redircting...')
				webbrowser.open(URL)
		sleep(1)
		sys.exit(0)

#Automatically join a meeting that is +-15 minutes
def auto():
	#Open the ZoomData
	file, csvfile = open_data()

	#Get time and date
	day = datetime.today().weekday()
	time = int(datetime.now().strftime("%H"))*60 + int(datetime.now().strftime("%M"))

	#Iterate through ZoomData.csv to find the specified class
	for row in csvfile:
		try:
			classtime = int(row[day+4].split(":")[0]) * 60 + int(row[day+4].split(":")[1])
			if (time>classtime-5) and (time<classtime+15):
				meetingID=row[2]
				#Check if password exists
				try:
					passWD=row[3]
				except:
					passWD=""
				connect(meetingID, passWD)
		except ValueError:
			pass
	print("No meetinges found for this time!")

#Show a popup to choose which meeting to join
def manual():
	#Open the ZoomData
	file, csvfile = open_data()

	#Print out each possible option
	print("Choose an option below:")
	for row in csvfile:
		print(row[0] + " [" + row[1] + "]")
	file.seek(1)

	#Get intended meeting
	meetingname = input("Enter a Meeting: ")

	#Find the specified meeting
	for row in csvfile:
		if (meetingname==row[1]):
			meetingID=row[2]
			#Check if password exists
			try:
				passWD=row[3]
			except:
				passWD=""
			break

	#Check if the input is not in the list
	try:
		meetingID
	except NameError:
		print("Input Invalid")
		Choice = input('Try again? (Y/N)')
		if Choice.lower() == 'yes' or Choice.lower() == 'y':
			#Yes to update
			system("cls||clear")
			figlet()
			manual()
		else:
			sys.exit(0)
		sys.exit(1)
	connect(meetingID, passWD)

#Connect to the meeting
def connect(meetingID, passWD):
	#Command to join zoom meeting from Zoom binary
	if sys.platform == "linux" or sys.platform == "linux2":
		command = "/opt/zoom/zoom --url=zoommtg://zoom.us/join?confno=" + meetingID + "&pwd=" + passWD
		print("Linux is currently under developement. Please open a Github issue if an error occurs")
	elif sys.platform == "darwin":
		command = "open zoommtg://zoom.us/join?confno=" + meetingID + "&pwd=" + passWD
		print("MacOS is currently under developement. Please open a Github issue if an error occurs")
	elif sys.platform == "win32":
		command = "%appdata%\\Zoom\\bin\\Zoom.exe --url=zoommtg://zoom.us/join?confno=" + meetingID + "^&pwd=" + passWD
	else:
		print("Operating System unknown. Please manually set this is the python file")
		sleep(5)
		sys.exit(1)

	#Execute command
	try:
		subprocess.run(command.split(), shell=True, timeout=1)
	except subprocess.TimeoutExpired:
		pass
	sys.exit(0)

if __name__ == "__main__":
	main()
