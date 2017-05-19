# Aaron Epstein
# Pymessagedroid
# Mac desktop app that sends imessage messages to phone or email (works
#	well for android users)

#using sqlite3
import sqlite3
from message import Message

import datetime
from datetime import timedelta
from os.path import expanduser

import time
import smtplib
import getpass

# Import the email modules we'll need
from email.mime.text import MIMEText

#connects to database
def sqliteConnect():
	path = expanduser("~") + '/Library/Messages/chat.db'
	return sqlite3.connect(path)

def main():
	info = login()
	user_address = getUserAddress()

	connection = sqliteConnect()
	c = connection.cursor()
	print("Reading last message")
	lastMessage = getLastMessage(c);

	idleTime = 10
	while True:
		idle(idleTime)
		print("Checking for new messages...")

		if getLastMessage(c).text != lastMessage.text:
			idleTime = 10
			lastMessage = getLastMessage(c)
			sendMessage(lastMessage, info[0], info[1], user_address)
		else:
			idleTime *= 1.5
			if idleTime > 6000:
				idleTime = 3000

	connection.close()

#gets last message in database
#returns Message object
#parameter: cursor object (for db)
def getLastMessage(c):

	lastText = ""
	number = ""
	groupName = ""

	#get last message
	c.execute("SELECT * FROM message WHERE ROWID = (SELECT MAX(ROWID) FROM message);");
	for row in c:
		message_id = row[0]
		date = row[15]
		lastText = row[2]
		handleid = row[6]

	#get number
	sql_handle = "SELECT * FROM handle WHERE ROWID='%s'" % (handleid)
	c.execute(sql_handle)
	for entry in c:
		number = handle[1]

	#get group of message
	sql_chat = "SELECT * FROM chat_message_join WHERE message_id='%s'" % (message_id)
	c.execute(sql_chat)
	for line in c:
		chatid = line[0]

	sql_group = "SELECT * FROM chat WHERE ROWID='%s'" % (chatid)
	for r in c:
		groupName = row[13]
		groupName = groupName.encode('ascii','ignore')

	d = datetime.datetime.strptime("01-01-2001", "%m-%d-%Y")
	date = (d-datetime.timedelta(hours=4)+datetime.timedelta(seconds=date)).strftime("%a, %d %b %Y %H:%M:%S EST")
	lastMessage = Message(lastText, number, groupName, date)
	return lastMessage

#makes the app sleep for 'idleTime'
def idle(idleTime):
	time.sleep(idleTime)

#sends message from given email to given user address
def sendMessage(Message, email, password, user_address):
	print("sending new message")
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(email, password)

	content = "Sender: %s, Date: %s, Group: %s, Message: %s" % (Message.number,Message.date,Message.groupName,Message.text)

	msg = MIMEText(content, 'plain')

	msg['Subject'] = "New iMessage From %s" % (Message.number)
	msg['From'] = email
	msg['To'] = user_address

	server.sendmail(email, user_address, msg.as_string())
	server.quit()

#logs into email
def login():
	print("Welcome to pymessagedroid. Please enter a gmail account and password below.")
	loggedin = False
	while loggedin == False:
		email = raw_input('Email: ')
		password = getpass.getpass()
		try:
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(email, password)
			loggedin = True
		#change the exception
		except smtplib.SMTPException:
			loggedin = False
			print("Unsuccesful. Try again.")

	server.quit()	
	print("Succesful.")
	info = [email,password]
	return info

#gets user address from user
def getUserAddress():
	print("Input your phone number as an email address, or an email address to send messages to.")
	print("Example: 11231231234@mymetropcs.com")
	user_address = raw_input("User address: ")
	return user_address

if __name__ == '__main__':
	main()