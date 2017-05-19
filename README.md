# Aaron Epstein
Copyright 2017

# pymessagedroid
A python desktop app for Macs to send imessages to Android phone

# Background
This app accesses your macs iMessages via the chat.db sqlite3 database in the route ~/Library/Messages.

# Guide to database
Messages table
	-holds all messages
	-each message contains valuable info like 'text', 'date', 'handle_id'

Handle Table (holds numbers that send messages to you)
	- each handle contains its id and the corresponding number

chat_message_join table
	-contains 'chat_id' and 'message_id'
	-gives relation between each message and chat (i.e. what group is each message in)

chat table
	-contains each group message
	-group name is stored under 'display_name'

Other references - https://github.com/mjbrisebois/pymessage

# How it works
Logs into your gmail account and stores the address to send messages to.
Loads in most recent message from the database. Checks at a certain interval for new messages.
When a new message is recieved an email is sent from your email to the given address that contains
the message, its group, the number its from and the date.

# How to use
Use command 'python app.py'

# Phone Carrier Domains
http://www.emailtextmessages.com/

