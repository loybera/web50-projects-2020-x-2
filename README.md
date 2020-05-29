Web Programming with Python and JavaScript
# Project 2

This is a chat program without database, just has object list to save the messages, 
user and channels in memory and user flask.io sockets to create, join and send messages to rooms. 
First, you have to enter your nickname and you can join the existent channels with the message 
history in it, or create your own channels. 
It's possible leave channels.  If you logout and go inside again, the app will join the joined
 channels again.

Video url: 
#----------------------------------------------------------------------------------------
Contain
#----------------------------------------------------------------------------------------
templates:
login.htm (has login at chat -without password-)
chat.htm (has the visualization of channels and chats)
layout.htm (has the menu)
about.htm (read this file)

Css:
/static/css/chat.css

Js:
/static/js/chat.jss
contain all logic for send and receive sockets messages and update the htm for show channels 
and messages,  Join, create channels, send and receive messages

Application.py
the server side with sockets processing and object channel, users and channels listing in memory

Model.py
The class model used in project2
#----------------------------------------------------------------------------------------

Objectives: 
- Learn to use JavaScript to run code server-side.
- Become more comfortable with building web user interfaces.
- Gain experience with Socket.IO to communicate between clients and servers.

Milestones:
- Complete the Display Name, Channel Creation, and Channel List steps.
# done
- Complete the Messages View and Sending Messages steps.
# done
- Complete the Remembering the Channel and Personal Touch steps.
# done

Requirements
Alright, it’s time to actually build your web application! Here are the requirements:

Display Name: When a user visits your web application for the first time, they should be 
prompted to type in a display name that will eventually be associated with every message 
the user sends. If a user closes the page and returns to your app later, the display name 
should still be remembered.
# login.htm 
- whitout password, you just have to choose your nickname

Channel Creation: Any user should be able to create a new channel, so long as its name doesn’t 
conflict with the name of an existing channel.
# chat.htm button New

Channel List: Users should be able to see a list of all current channels, and selecting one 
should allow the user to view the channel. We leave it to you to decide how to display such a list.
# chat.htm button Join

Messages View: Once a channel is selected, the user should see any messages that have already 
been sent in that channel, up to a maximum of 100 messages. Your app should only store the 
100 most recent messages per channel in server-side memory.
# ok

Sending Messages: Once in a channel, users should be able to send text messages to others 
the channel. When a user sends a message, their display name and the timestamp of the message 
should be associated with the message. All users in the channel should then see the new message 
(with display name and timestamp) appear on their channel page. Sending and receiving messages 
should NOT require reloading the page.
# ok

Remembering the Channel: If a user is on a channel page, closes the web browser window, and goes 
back to your web application, your application should remember what channel the user was on 
previously and take the user back to that channel.
# ok

Personal Touch: Add at least one additional feature to your chat application of your choosing! 
Feel free to be creative, but if you’re looking for ideas, possibilities include: supporting 
deleting one’s own messages, supporting use attachments (file uploads) as messages, or supporting 
private messaging between two users.
# no ok

In README.md, include a short writeup describing your project, what’s contained in each file, and 
(optionally) any other additional information the staff should know about your project. Also, 
include a description of your personal touch and what you chose to add to the project.
If you’ve added any Python packages that need to be installed in order to run your web application, 
be sure to add them to requirements.txt!