#using sqlite3
import sqlite3
#import our classes
from conversation import Conversation
from message import Message
from person import Person

import datetime
from os.path import expanduser

import time
import smtplib

#connect to database, read in info
#when first opened, load past 10 messages in each group/conversation
#then check at a certain rate for new messages in each group

#order of stuff
#get conversations - chat_message_join table and create conversations
#load people in each conversation - add people to conversation objects
#load messages in each convo - store date and content

def sqliteConnect():
	path = expanduser("~") + '/Library/Messages/chat.db'
	return sqlite3.connect(path)

def main():
	connection = sqliteConnect()
	c = connection.cursor()

	c.execute("SELECT * FROM chat");
	conversations = []
	groupidlist = []
	for row in c:
		group_name = row[13]
		group_id = row[0]
		group_name_edited = group_name.encode('ascii','ignore')
		conversations.append(Conversation(group_name_edited,[],[],group_id))
		groupidlist.append(group_id)

	#load all messages with each chat
	lastMessage = ""
	message_id_list = []
	for i in groupidlist:
		sql_statement = "SELECT * FROM chat_message_join WHERE chat_id='%s'" % (groupidlist[i])
		c.execute(sql_statement)
		for row in c:
			message_id = row[1]
			groupid = row[0]
			sql = "SELECT * FROM message WHERE ROWID='%s'" % (message_id)
			c.execute(sql)
			for line in c:
				messageinfo = line
			date = messageinfo[15]
			lastMessage = messageinfo[2]
			for j in range(0,len(conversations)):
				if (conversations[j].id == groupid):
					handleid = messageinfo[6]
					sql_handle = "SELECT * FROM handle WHERE ROWID='%s'" (handleid)
					c.execute(sql_handle)
					handle = c
					number = handle[1]
					#to add: import contacts
					#need to remove duplicate members
					conversations[j].members.append(Person('Unkown',number)) #add people
					conversations[j].messages.prepend(Message(messageinfo[2], Person('Unkown', number), groupid,date)) #add messages
	connection.close()

	while True:
		if checkForNew():
			connection = sqliteConnect()
			c = connection.cursor()
			c.execute("SELECT * FROM message")
			for row in c:
				while row[2] != lastMessage:
					m = Message()
					sqlnew = "SELECT chat_id FROM chat_message_join WHERE message_id = %s" (row[0])
					c.execute(sqlnew)
					gid = c
					sqlhandle = "SELECT * FROM handle WHERE ROWID='%s'" (row[6])
					c.execute(sqlhandle)
					m = Message(row[2], Person('Unknown',c[1]), gid, row[15])
					for k in range(0,len(conversations)):
						if (conversations[k].id == m.group_id):
							conversations[k].members.append(Person('Unknown', c[1]))
							conversations[k].messages.prepend(m)
					sendMessage(m)


def checkForNew(lastMessage):
	time.sleep(60)
	connection = sqliteConnect()
	c = connection.cursor()
	messages = []
	c.execute("SELECT text FROM message")
	for row in c:
		messages.prepend(row)
	if messages[0] == lastMessage:
		return False
	else:
		return True

def sendMessage(Message):
	email = raw_input('Email:')
	password = raw_input('Password:')

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(email, password)

	connection = sqliteConnect()
	c = connection.cursor()

	sql = "SELECT display_name FROM chat WHERE ROWID = '%s'" (Message.groupid)
	c.execute(sql);
	connection.close()

	msg = "Sender: %s, Date: %s, Group: %s, Message: %s" (Message.person.number,Message.date,c,Message.text)
	server.sendmail(email, "19784605861@mymetropcs.com", msg)


if __name__ == '__main__':
	main()
	server.quit()