Web Programming with Python and JavaScript
# Project 2

This is a chat program without database, just has object list to save the messages, 
user and channels in memory and user flask.io sockets to create, join and send messages to rooms. 
First, you have to enter your nickname and you can join the existent channels with the message 
history in it, or create your own channels. 
It's possible leave channels.  If you logout and go inside again, the app will join the joined
 channels again.

Model: channel, user, channeluser, messages
All channels are keep it in the object channel lists called list_channels
Each channel of the list_channels has a messages (messages) list and an users connected list (users).
When the users leave the channel I kickoff him from the channel.users list
Also, I have a list_users who has all the users created, active o not active (logout the site). Each user has too a channel list for initialize when he login and see your joined channels, publics or private (user to user)


Video url:  https://youtu.be/4v1z3atA7Ag
0' a  17''   login (user1)
18'' 37'' user1 join to public room (created previusly by server at start)
39'' login second user (user2)
40''to 48'' user2 join public group with previusly messages loaded and chat with user 1
0'50'' a 0'1:03'' chat between users
1'04'' user2 create new channel
1'16'' user2 join to many groups
2'09'' join to private room (user to user) clicking on ingoing message name's (has a red hover efect) at public room
2'57'' user2 filter your joined channels through the search box
3'04'' user1 logout and login keeping yours channels joined and messages loaded
3'12'' user1 join to channel created by user2
3'40'' user2 close the browser and open it again, login and keep his channels joined and messages

############################################
# Contain
############################################
templates:
login.htm (has login at chat -without password-)
chat.htm (has the visualization of channels and chats)
layout.htm (has the menu)
about.htm (read this file)

Css:
/static/css/chat.css
/static/css/chat.scss


Js:
/static/js/chat.jss
contain all logic for send and receive sockets messages and update the htm for show channels 
and messages,  Join, create channels, send and receive messages

Application.py
the server side with sockets processing and object channel, users and channels listing in memory

Model.py
The class model used in project2
####----------------------------------------###

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
- whitout password, you just have to choose your nickname. 
plus: the system asign random profile image to users and channels

Channel Creation: Any user should be able to create a new channel, so long as its name doesn’t 
conflict with the name of an existing channel.
# chat.htm 
- clic in button New
- if channel name exists don't create another

Channel List: Users should be able to see a list of all current channels, and selecting one 
should allow the user to view the channel. We leave it to you to decide how to display such a list.
# chat.htm button 
- clic in button Join open a channel modal window

Messages View: Once a channel is selected, the user should see any messages that have already 
been sent in that channel, up to a maximum of 100 messages. Your app should only store the 
100 most recent messages per channel in server-side memory.
# application.py
def addMessageToChannel
store all input messaggse and start to purgue the oldest message when they are over 100 messages by each channel


Sending Messages: Once in a channel, users should be able to send text messages to others 
the channel. When a user sends a message, their display name and the timestamp of the message 
should be associated with the message. All users in the channel should then see the new message 
(with display name and timestamp) appear on their channel page. Sending and receiving messages 
should NOT require reloading the page.
# chat.js
throw js the app show messages in channel joined without reload page, even if it a private channel show the new chat room with the other user automatically without reload the page

Remembering the Channel: If a user is on a channel page, closes the web browser window, and goes 
back to your web application, your application should remember what channel the user was on 
previously and take the user back to that channel.
# ok
- the server keep a user list and the channel list by each user are still joined. If the user join to one channel and leave it, when he login again he didn't see this channel in his channel joined list when the page load


Personal Touch: Add at least one additional feature to your chat application of your choosing! 
Feel free to be creative, but if you’re looking for ideas, possibilities include: supporting 
deleting one’s own messages, supporting use attachments (file uploads) as messages, or supporting 
private messaging between two users.
# plus: user can clic over the name at message in a channel public to text a private user (like whatsapp). By this way the create a private room between users

In README.md, include a short writeup describing your project, what’s contained in each file, and 
(optionally) any other additional information the staff should know about your project. Also, 
include a description of your personal touch and what you chose to add to the project.
If you’ve added any Python packages that need to be installed in order to run your web application, 
be sure to add them to requirements.txt!