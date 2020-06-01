import datetime
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


def validateUser(nickname):
    print(f"Validate {nickname}")

    if (len(list_user)>0):
        for item in list_user:
            if (item.name == nickname):
                if (item.active == True):
                    print("Nickname already connected")
                    return False
            
    print("Nickname valid")
    return True

# add channel number to channel list of user connected
def addChannelToUser(channel, nickname):

    print(f"--Add channel {channel} to user {nickname} --")

    newChannel = ChannelUser(channel, getChannelLabel(channel), getChannelImage(channel))
    print(newChannel)
    userInChannel = False

    if (len(list_user)>0):
        for item in list_user:
            if (item.name == nickname):
                # validate if channel exists in user list's
                for chn in item.channels:
                    if (chn.id == channel):
                        userInChannel = True

                if (userInChannel == False):
                    item.add_channel(newChannel)
                # user and channels
                print(item.name, item.channels)
    else:
        print(f"Error....Add user {nickname}")
        addUser(nickname)



    # TODO: may be must to save json
    session['users'] = list_user

def addUser(nickname):
    createUser=True
    usr = User(nickname)
    for item in list_user:
        if (item.name == nickname):
            createUser = False
            item.active = True

    if (createUser):
        list_user.add(usr)
        print(repr(usr))

def addChannel(channel, name, owner, public):
    createChannel  = True
    chn = Channel(channel, name, owner, public)
    for item in list_channel:
        if (item.id == channel):
            createChannel = False

    if (createChannel):
        list_channel.add(chn)
        chn.print_info()


def removeChannelFromUser(channel, nickname):
    print(f"--Remove channel  {channel} from user {nickname} --")

    # remove user from channel list
    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel):
                if (item.users.count(nickname)>0):
                    item.users.remove(nickname)
                    print(f"Remove user  {nickname} from channel list {channel}" )
                    pass
                item.print_info()

    else:
        print("Error, removing user from channel list")

    # remove channel from user list
    if (len(list_user)>0):
        for item in list_user:
            if (item.name == nickname):
                # validate if channel exists in user list's
                for chn in item.channels:
                    if (chn.id == channel):
                        item.channels.remove(chn)
                        print(f"Remove channel {channel} from user list {nickname}" )

 
                print(item.name, item.channels)
    else:
        print(f"Error....removing channel from user {nickname}")
        addUser(nickname)

    #update sessions variables
    session['channels'] = list_channel
    session['users'] = list_user



def addUserToChannel(channel, nickname):
    print(f"--Add user {nickname} to channel {channel}--")

    # add user to list_user of channel element
    user=nickname

    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel):
                print(f"Add user {user} to channel {channel}")
                if (item.users.count(user)==0):
                    item.add_user(user)
                    pass
                item.print_info()
    else:
        print("Error, channel list doesnt exists")

    session['channels'] = list_channel

def addMessageToChannel(channel, user, image, time, msg):
    print(f"--add msg {msg} to channel {channel}--")

    msg = Message(user_from= user, user_to= channel, time= getDay(time), post= msg, user_from_img= image)
    # backup users messages
    list_messages.append(repr(msg))

    # Don't keep the broadcast messages at channel
    if (user.upper() !='ADMIN'):
        for item in list_channel:
            if (item.id == channel):
                if (len(item.messages)>9):
                    print("remove first message")
                    # remove first message to put the new message (max 100 per channel)
                    item.messages.pop(0)
                # put new message in channel 
                item.add_message(msg)
                print(item.print_info())

    return msg

def validateUserBychannel(nickname, channel):
    print(f"--Validate {nickname} in {channel}--")

    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel):
                if (len(item.users)>0):
                    item.print_info()
                    for item2 in item.users:
                        if (item2.name == nickname):
                            print("not valid")
                            return False
    
    print("valid")
    return True

def getChannelLabel(channel):
    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel):
                return item.name
    return None

def getChannelImage(channel):
    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel):
                return item.image
    
    return 'user-profile'

def getMessagesByChannel(channel):
    
    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel):
                return item.messages
    
    return None


def getUsersByChannel(channel):
    
    if (len(list_channel)>0):
        for item in list_channel:
            if (item.id == channel):
                return item.users
    
    return None

def getChannelsByUser(nickname):
    listResult = []
    if (len(list_user)>0):
        for item in list_user:
            if (item.name == nickname):
                print(f"load channels {item.channels} for user {nickname}")
                if (len(item.channels)>0):
                    for chn in item.channels:
                        listResult.append(chn)
    
    return listResult

def getUserImage(nickname):

    if (len(list_user)>0):
     for item in list_user:
            if (item.name == nickname):
                print(f"load image {item.image} for user {nickname}")
                return item.image

    return 'user-profile'

                        
def login_required(f):
    @wraps(f)
    def decorated_funtion(*args, **kwargs):
        if 'nickname' not in session:
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
                nickname = request.form['form-nickname']
                nickname = nickname.title()

                if (validateUser(nickname)):                
                    addUser(nickname)
                    # TODO: push user to clients
                else:
                    return render_template('login.htm', errorAlert="Nickname already loged",   nickname= nickname)
 
 
                session.permanent = True
                session['dateLogin'] = datetime.datetime.today().replace(microsecond=0)
                session['nickname'] = nickname
                session['today'] = datetime.datetime.today().replace(microsecond=0)
                
                now = datetime.datetime.today().replace(microsecond=0)

                print(f"login load to list_channeluser: {list_channeluser}    ")
       
                return redirect(url_for('home'))


 

@app.route('/logout', methods=['GET'])
def logout():
    
    # delete the session variables
    if ('nickname' in session):
        nickname= session['nickname']
        del session ['nickname'] 

        print("inactive user " + nickname)
        try:
            if (len(list_user)>0):
                for item in list_user:
                    if (item.name == nickname):
                        item.active = False
                        print(f"logout channel: {item.channels}")
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
        addChannel(channel="things", name="Things", owner="Admin", public=True)
        addChannel(channel="otherthings", name="Other Things", owner="Admin", public=True)
        addChannel(channel="barfriends", name="Bar Friends", owner="Admin", public=True)
        addChannel(channel="soccermondays", name="Soccer Mondays", owner="Admin", public=True)
        addChannel(channel="university", name="University", owner="Admin", public=True)
        addChannel(channel="cs50pythoncourse", name="Cs50 Python course", owner="Admin", public=True)

    print(f"N° Channels: {len(list_channel)}")
    print(list_channel)
    nickname = session['nickname']
    list_channeluser = getChannelsByUser(nickname)
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

    return render_template('chat.htm',  nickname=session['nickname'],  list_usr_channel=list_channeluser, list_channel=list_channel2, list_user=list_user)


@app.route('/')
def home():

   

    if ('nickname' not in session):
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
                      namespace='/project2')

class MyNamespace(Namespace):
    def on_my_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
    
        msg = f"{datetime.datetime.today().replace(microsecond=0)} {session['nickname']}: {message['data']}"
        message['data'] = msg

        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']})

    def on_my_broadcast_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1

        msg = f"{datetime.datetime.today().replace(microsecond=0)}  {session['nickname']}: {message['data']}"
        message['data'] = msg

        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']},
             broadcast=True)

    def on_join(self, message):

        room = message['room']
        session['channel'] = room
        nickname = session['nickname']
        try:
            create_room = message['create_room']
            if (create_room):
                addChannel(room, message['data'], nickname, True)
                # TODO: push channel to clients
        except:
            print("room already existing, just join it")

        print(f"Join Room: {message['room']} User: {session['nickname']}")        
        # add user connected to channel list
        addUserToChannel(room, nickname)
        # add channel to user profile for next login
        addChannelToUser(room, nickname)

        # join user to room  
        join_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        
        # get message list from channel to send html client
        channel_msg_list = getMessagesByChannel(room)
        print (f"list msg channel: {channel_msg_list}")

        emit('my_response',
             {'data': nickname + ' has entered' + ' , '.join(rooms()),
              'room': room, 'messages': channel_msg_list,'count': session['receive_count']})
        
 
    def on_leave(self, message):

        nickname = session['nickname']
        room = message['room']
        removeChannelFromUser(room, nickname)
        
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

    def on_my_room_event(self, message):
        
        time = datetime.datetime.now()
        # message['data'] = msg
        room = message['room']
        user = message['user']
        print("user:"+ user)
        
        msg = addMessageToChannel(room, user, getUserImage(user), time, message['data'])         

        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_room',
            {'data': message['data'], 'user': msg.user_from, 'user_image': msg.user_from_img, 'time': msg.time, 'count': session['receive_count'], 'id': msg.id },
            room=message['room'], user= user)


    def on_disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()

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

socketio.on_namespace(MyNamespace('/project2'))

if __name__ == '__main__':
    app.secret_key = "secret key"
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
    socketio.run(app)
