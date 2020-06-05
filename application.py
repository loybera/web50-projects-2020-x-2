import datetime
import re
from datetime import date
from flask_socketio import SocketIO, Namespace, emit, send, join_room, leave_room, close_room, rooms, disconnect
from model import *
from flask import request, redirect, make_response
from flask_session import Session
from flask import Flask, session, render_template,jsonify, url_for, flash
from socketio import Namespace as _Namespace
from threading import Lock
from functools import wraps

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'memcached'
app.config["JSON_SORT_KEYS"] = False
app.config["SECRET_KEY"] = "secret key debug"

# socketio = SocketIO(app)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


list_channel = set()
list_user = set()
list_messages = []
list_channeluser = []

forbbiden_usernames = ['admin', 'administrator', 'root']

def validateUser(username):
    print(f"Validate {username}")

    result = True

    if (forbbiden_usernames.count(username.lower())>0):
        result = "username reserved, please choose another"
    else:
        if (len(list_user)>0):
            for item in list_user:
                if (item.id == username):
                    if (item.active == True):
                        result = "username already connected, please choose another"
                    
    print (result)
    return result

# add channel number to channel list of user connected
def addChannelToUser(username, channel, channel_label,  channel_type, user_to, user_from):

    print(f"--Add channel {channel} to user {username} --")
    if (channel_type=='PRIVATE'):
        image= getChannelImage(user_to, channel_type)
    else:
        image = getChannelImage(channel, channel_type)

    newChannel = ChannelUser(channel, channel_label, image, channel_type, user_to, user_from)
    print(newChannel)
    userInChannel = False

    if (len(list_user)>0):
        for item in list_user:
            if (item.id == username):
                # validate if channel exists in user list's
                for chn in item.channels:
                    if (chn.id == channel):
                        userInChannel = True

                if (userInChannel == False):
                    item.add_channel(newChannel)
                # user and channels
                print(item.id, item.channels)
    else:
        print(f"Error....Add user {username}")
        addUser(username)



    # TODO: may be must to save json
    session['users'] = list_user

def addUser(username, username_label):
    createUser=True
    usr = User(username, username_label)
    for item in list_user:
        if (item.id == username.lower()):
            createUser = False
            item.active = True
            return item

    if (createUser):
        list_user.add(usr)
        print(repr(usr))

    return usr

def addChannel(channel, name, owner, channel_type):
    createChannel  = True
    for item in list_channel:
        if (item.id == channel.lower()):
            createChannel = False
            break

    if (createChannel):
        chn = Channel(channel, name, owner, channel_type)
        list_channel.add(chn)
        chn.print_info()


def removeChannelFromUser(channel, username):
    print(f"--Remove channel  {channel} from user {username} --")

    # remove user from channel list
    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel.lower()):
                if (item.users.count(username)>0):
                    item.users.remove(username)
                    print(f"Remove user  {username} from channel list {channel}" )
                    pass
                item.print_info()

    else:
        print("Error, removing user from channel list")

    # remove channel from user list
    if (len(list_user)>0):
        for item in list_user:
            if (item.id == username.lower()):
                # validate if channel exists in user list's
                for chn in item.channels:
                    if (chn.id == channel.lower()):
                        item.channels.remove(chn)
                        print(f"Remove channel {channel} from user list {username}" )

 
                print(item.id, item.channels)
    else:
        print(f"Error....removing channel from user {username}")
        addUser(username)

    #update sessions variables
    session['channels'] = list_channel
    session['users'] = list_user



def addUserToChannel(channel, username):
    print(f"--Add user {username} to channel {channel}--")

    # add user to list_user of channel element
    user=username

    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel.lower()):
                print(f"Add user {user} to channel {channel}")
                if (item.users.count(user)==0):
                    item.add_user(user)

                item.print_info()
                break
    else:
        print("Error, channel list doesnt exists")

    session['channels'] = list_channel

def addMessageToChannel(channel, user_from, user_to, image, time, msg):
    print(f"--add msg {msg} to channel {channel}--")

    msg = Message(channel=channel, user_from= user_from, user_to= user_to,  time= getDay(time), post= msg, user_from_img= image)
    # backup users messages
    list_messages.append(repr(msg))

    # Don't keep the broadcast messages at channel
    if (user_from.lower() !='admin'):
        for item in list_channel:
            if (item.id == channel.lower()):
                if (len(item.messages)>99):
                    print("remove first message")
                    # remove first message to put the new message (max 100 per channel)
                    item.messages.pop(0)
                # put new message in channel 
                item.add_message(msg)
                item.print_info()
                break

    return msg

def validateUserBychannel(username, channel):
    print(f"--Validate {username} in {channel}--")

    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel.lower()):
                if (len(item.users)>0):
                    item.print_info()
                    for item2 in item.users:
                        if (item2.id == username.lower()):
                            print("not valid")
                            return False
    
    print("valid")
    return True

def getChannel(channel):

    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel.lower()):
                return item

    # default the channel
    return None

def getChannelLabel(channel):

    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel.lower()):
                return item.name

    # default the channel
    return channel

def getChannelImage(channel, channel_type):
    if (channel_type == 'PUBLIC'):
        if (len(list_channel)>0):
            for item in list_channel:
                if (item.id == channel.lower()):
                    return item.image
    else:
        if (len(list_user)>0):
            for item in list_user:
                if (item.id == channel.lower()):
                    return item.image
    
    return 'new-channel'

def getMessagesByChannel(channel):
    
    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel.lower()):
                return item.messages
    
    return None


def getUsersByChannel(channel):
    
    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel.lower()):
                return item.users
    
    return None

def getChannelsByUser(username):
    listResult = []
    if (len(list_user)>0):
        for item in list_user:
            if (item.id == username.lower()):
                print(f"load channels {item.channels} for user {username}")
                if (len(item.channels)>0):
                    for chn in item.channels:
                        listResult.append(chn)
    
    return listResult


def findChannel(channel, user_to, user_from):

    separator = "__to__"
    channelusers = channel.split(separator)
    
    if (len(channelusers)>1):
        if (len(list_channel)>0):
            for item in list_channel:
                if (item.channel_type == 'PRIVATE'):
                    if (item.name == channelusers[0]+separator+channelusers[1]):
                        return item.name
                    if (item.name == channelusers[1]+separator+channelusers[0]):
                        return item.name

    # if dont find channel return the input
    return channel        

def getUserImage(username):

    if (len(list_user)>0):
     for item in list_user:
            if (item.id == username.lower()):
                print(f"load image {item.image} for user {username}")
                return item.image

    return 'user-profile'

def leaveRoomByUser(username):

    list_channeluser = getChannelsByUser(username)
    print(f"list channels to leave {list_channel}")

    for item in list_channeluser:
        print(f"leave channel {item.id}")
        # leave_room(item.id)
        print(f"remove channel {item.id}")
        removeChannelFromUser(item.id, username)


def login_required(f):
    @wraps(f)
    def decorated_funtion(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_funtion

@app.route('/login', methods= ['GET', 'POST'] )
def login():
        print("login ")
        existUser = False

        if request.method == 'GET':
            print("login get")
            return render_template('login.htm', messages=list_messages, channels = list_channel)
        else:
            if request.method == 'POST':
                
                username_label = request.form['form-username']
                print(username_label)
                username = re.sub('[^A-Za-z0-9]', '', username_label).lower()
                print(username + " "+ username_label)
                result = validateUser(username)
                if (result == True):                
                    user= addUser(username, username_label)
                    # TODO: push user to clients
                else:
                    return render_template('login.htm', errorAlert= result,   username= username)
 
 
                session.permanent = True
                session['dateLogin'] = datetime.datetime.today().replace(microsecond=0)
                session['username'] = user.id
                session['username_label'] = user.name
                session['username_image'] = user.image

                session['today'] = datetime.datetime.today().replace(microsecond=0)
                
                now = datetime.datetime.today().replace(microsecond=0)

                print(f"login load to list_channeluser: {list_channeluser}    ")
       
                return redirect(url_for('home'))


 

@app.route('/logout', methods=['GET'])
def logout():
    
    # delete the session variables
    if ('username' in session):
        username= session['username']

        # TODO: enviar a todos los grupos el aviso de logout
        print (f"disconect user {username}")
        socketio.emit('my_response',
             {'data': 'User '+username+' Disconnected!', 'count': 0},
                      namespace='/chat')
        

        del session ['username'] 
        del session ['username_label'] 

        try:
            if (len(list_user)>0):
                for item in list_user:
                    if (item.id == username):
                        item.active = False
                        print(f"logout user: {item.name}")
        except:
            print("error to inactive user from user list")

    if ('channel' in session):
        del session ['channel'] 
 
        
    return redirect(url_for('home')) 


@app.route('/about', methods=['GET'])
def about():
    
    filename = "README.md"
    f = open(filename, encoding='utf-8')
    content = f.read()
    
    return render_template('about.htm', content=content)

@app.route('/chat', methods= ['GET', 'POST'] )
@login_required
def chat():

    # iniatilize defaults channels 
    print(f"N° Channels: {len(list_channel)}")
    if (len(list_channel) == 0):
        addChannel(channel="things", name="Things", owner="Admin", channel_type='PUBLIC')
        addChannel(channel="otherthings", name="Other Things", owner="Admin", channel_type='PUBLIC')
        addChannel(channel="barfriends", name="Bar Friends", owner="Admin", channel_type='PUBLIC')
        addChannel(channel="soccermondays", name="Soccer Mondays", owner="Admin", channel_type='PUBLIC')
        addChannel(channel="university", name="University", owner="Admin", channel_type='PUBLIC')
        addChannel(channel="cs50pythoncourse", name="Cs50 Python course", owner="Admin", channel_type='PUBLIC')

    print(f"N° Channels: {len(list_channel)}")
    print(list_channel)
    username = session['username']
    list_channeluser = getChannelsByUser(username)
    print(f"list channels {list_channel}")

    list_channel2 = list_channel.copy()
    for item2 in list_channeluser:
        for item in list_channel:
            if (item.id == item2.id):
                try:
                    list_channel2.remove(item)
                except: 
                    print("channel already removed")

    print(f"list channels {list_channel}")
    print(f"list user {list_user}")
    print(f"list canales user {list_channeluser}")

    return render_template('chat.htm',  username=session['username'], username_label=session['username_label'], username_image=session['username_image'], list_usr_channel=list_channeluser, list_channel=list_channel2, list_user=list_user)


@app.route('/')
def home():

   

    if ('username' not in session):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('chat'))


def getDay(my_date):

    if (my_date.date() == date.today()):
        return (f"Today {my_date.time().replace(microsecond=0)}")
    if (my_date.date() == date.today() - timedelta(days=1)):
        return (f"Yesterday {my_date.time().replace(microsecond=0)}")
    if (my_date.date() > date.today() - timedelta(days=5)):
        return (f"{date.strftime('%A')} {my_date.time().replace(microsecond=0)}")
    else:
        return (f"{my_date.date()} {my_date.time().replace(microsecond=0)}")


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(100000)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/chat')

class MyNamespace(Namespace):

    def on_my_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        try:
            username = session['username']
        except:
            username = 'not logued'

        msg = f"{datetime.datetime.today().replace(microsecond=0)} {username}: {message['data']}"
        message['data'] = msg

        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']})

    def on_my_broadcast_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1

        msg = f"{datetime.datetime.today().replace(microsecond=0)}  {session['username']}: {message['data']}"
        message['data'] = msg

        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']},
             broadcast=True)

    def on_join(self, message):

        username = session['username']
        room = message['room']
        room_type = message['room_type']
        create_room = False
        try:
            create_room = message['create_room']
            room_type = message['room_type']
            if (create_room):
                addChannel(room, message['data'], username, room_type)
        except:
            print("room already existing, just join it")

        print(f"Join Room: {message['room']} User: {session['username']}")        
        # add user connected to channel list
        addUserToChannel(room, username)
        # add channel to user profile for next login
        addChannelToUser(username=username, channel=room, channel_label=getChannelLabel(room), channel_type=room_type, user_to= room, user_from = username)

        # join user to room  
        join_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        
        # get message list from channel to send html client
        channel_msg_list = getMessagesByChannel(room)
        print (f"list msg channel: {channel_msg_list}")

        emit('my_response',
             {'data': username + ' has entered ' + ' , '.join(rooms()),
              'room': room, 'messages': channel_msg_list,'count': session['receive_count']})
        
    def on_join_user(self, message):
        
        
        username = session['username']
        room = message['room']
        print(f"join user {username} to channel {room}")
        room_type = message['room_type']
        try:
            user_from = message['user_from']
            user_to = message['user_to']
        except:
            chn = getChannel(room)
            if (chn == None):
                print(f"Error, channel {room} not exists or there is inconsistent")
                return False
            else:
                if (chn.channel_type =='PRIVATE' and len(chn.users)==2):
                    if (user_from == chn.users[0]):
                        user_to = chn.users[1]
                    else: 
                        user_to = chn.users[0]
                else:
                    print(f"Error, channel {room} not exists or there are not users inside")
                    return False     

        create_room = False
        try:
            create_room = message['create_room']
        except:
            print("warning: room already existing, just join it")
        try:
            room_type = message['room_type']
        except:
            print("warning: room private withot parameter")

        channel = findChannel(room, user_to, user_from)

        if (create_room == 'True'):
            addChannel(channel, room, 'Single_Chat', room_type)
            # TODO: push channel to clients or don't create private room in channel list

        print(f"Join user: {message['room']} User: {session['username']}")        
        # add user connected to channel list
        addUserToChannel(channel, user_from)
        # add channel to user profile for next login
        addChannelToUser(username=user_from, channel=channel, channel_label=user_to, channel_type=room_type, user_to= user_to, user_from = user_from)

        # do the same with the destination user
        addUserToChannel(channel, user_to)
        addChannelToUser(username=user_to, channel=channel, channel_label=user_from, channel_type=room_type, user_to= user_from, user_from = user_to)

        # join user to room  
        join_room(channel)
        session['receive_count'] = session.get('receive_count', 0) + 1
        
        # get message list from channel to send html client
        channel_msg_list = getMessagesByChannel(channel)
        print (f"list msg channel: {channel_msg_list}")

        emit('my_response_user',
             {'data': user_from + ' has joined with ' +  user_to +' , '.join(rooms()),
              'room': channel, 'original_room': room , 'user_from': user_from, 'user_to':user_to, 'messages': channel_msg_list,'count': session['receive_count']})
      
    def on_leave(self, message):

        username = session['username']
        room = message['room']
        removeChannelFromUser(room, username)
        
        leave_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'In rooms: ' + ', '.join(rooms()), 'count': session['receive_count']})

        

    def on_close_room(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                             'count': session['receive_count']},
             room=message['room'])
        close_room(message['room'])

    # event for PUBLIC rooms
    def on_my_room_event(self, message):
        
        time = datetime.datetime.now()
        # message['data'] = msg
        room = message['room']
        user_from = message['user_from']
        user_to = message['user_to']
        room_type = message['room_type']

        print("user:"+ user_from)
        
        user_image = getUserImage(user_from)
        msg = addMessageToChannel(channel=room, user_from=user_from, user_to=user_to, image=user_image, time=time, msg=message['data'])         

        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_room',
            {'data': message['data'], 'room': room, 'user_from': msg.user_from, 'user_to': msg.user_to, 'user_image': msg.user_from_img, 'time': msg.time, 'count': session['receive_count'], 'id': msg.id },
            room=room, user= user_from)

        # broadcasto to clients to push at user_to
        # IT'S not good, it's not secure but works for this project
        # with more time I'd like to learn hwo to push only for this user socket only
        if (room_type == 'PRIVATE'):
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my_join_user',
                {'data': 'Msg for you!','room': room, 'user_to': user_to, 'user_from': user_from, 'user_image': user_image, 'count': session['receive_count'] },
                broadcast=True)

    # # event for PRIVATE rooms
    # def on_my_room_event_user(self, message):
        
    #     time = datetime.datetime.now()
    #     # message['data'] = msg
    #     room = message['room']
    #     user_from = message['user_from']
    #     user_to = message['user_to']
        
    #     print("user:"+ user_from)
        
    #     user_image = getUserImage(user_from)
    #     msg = addMessageToChannel(channel=room, user_from=user_from, user_to=user_to, image=user_image, time=time, msg=message['data'])         

    #     session['receive_count'] = session.get('receive_count', 0) + 1
        
    #     emit('my_room',
    #         {'data': message['data'], 'user_from': msg.user_from, 'user_to': msg.user_to, 'user_image': msg.user_from_img, 'time': msg.time, 'count': session['receive_count'], 'id': msg.id },
    #         room=message['room'], user= user_from)

             
    def on_disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()

        username= session['username']
        # leaveRoomByUser(username)
        

    def on_my_ping(self):
        emit('my_pong')

    def on_connect(self):
        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(background_thread)
        emit('my_response', {'data': 'Connected', 'count': 0})

    def on_disconnect(self):
        print('Client disconnected', request.sid)

socketio.on_namespace(MyNamespace('/chat'))

if __name__ == '__main__':
    app.secret_key = "secret key"
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
    socketio.run(app)
