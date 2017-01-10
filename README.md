# pymessagedroid
A python desktop app for Macs to send imessages to Android phone

# Background
This app accesses your macs iMessages via the chat.db sqlite3 database in the route ~/Library/Messages.

# Guide to database
All messages are stored in message table. Each message contains valuable information like text, date, handle_id.
Handle_id tells you the rowid in the handle table of the 'handle'. Each handle contains the number of the person who sent the message.
The rowid of the message can be used to find out information about the group it belongs to. Use the rowid to find the chat_id in the chat_message_join table, which relates the chats (groups) to the messages.
Using the chat_id as the rowid in the chat table you can get the group name and information. The group name is labeled as the display name in the chat table.

# Structure of the app
Loads in all messages. Stores messages in 'conversations' which contain people and messages. Each message contains info about the message like the text, date, groupid, and sender. Each person object contains name and number. Then checks for new messages every minute and sends these to mobile number via email. Need to change mobile number for personal use. 

# How to use
Change mobile number/email address to go with it based off of phone service. Run app.py on local computer. Input email and password.

# Other
Still under development. All people are currently 'Unknown' names. Considering use google api to import contacts.

