import datetime
from datetime import date
from flask_socketio import SocketIO, Namespace, emit, send, join_room, leave_room, close_room, rooms, disconnect
from model import *
from flask import request, redirect, make_response
from flask_session import Session
from flask import Flask, session, render_template,jsonify, url_for, flash
from socketio import Namespace as _Namespace
from threading import Lock

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



# @socketio.on('message')
# def handleMessage(msg):
    
#     print(f"Message: {msg}")
#     message = Message(datetime.datetime.today().replace(microsecond=0), session['nickname'], msg)
    
#     print (message.getMessage)
#     msg = f"{datetime.datetime.today().replace(microsecond=0)}  {session['nickname']}: {msg}"
#     for item in list_channel:
#         if (item.name == session['channel']):
#             item.add_message(msg)
#             print(item.print_info())

    
#     send(msg, room = session['channel'], broadcast = True)




# @socketio.on("submit vote")
# def vote(data):
#     selection = data["selection"]
#     votes[selection] += 1
#     emit("vote totals", votes, broadcast=True)



@app.route('/login', methods= ['GET', 'POST'] )
def login():
        print("login ")
        existUser = False

        if request.method == 'GET':
            print("login get")
            return render_template('login.htm', messages=list_messages, channels = list_channel)
        else:
            if request.method == 'POST':
                print("login post")
                nickname = request.form['form-nickname']
                # channel = request.form['form-channel']
                
                if (validateUser(nickname)):                
                    user = User(nickname)
                    for item in list_user:
                        if (item.name == nickname):
                            item.active = True
                            existUser = True
                            print("users in chat:"+list_user)
                    if (existUser == False):
                        list_user.add(user)        
                else:
                    return render_template('login.htm', errorAlert="Nickname already loged",   nickname= nickname, channels = list_channel)
 
 
                session.permanent = True
                session['dateLogin'] = datetime.datetime.today().replace(microsecond=0)
                session['nickname'] = nickname
                # session['channel'] = channel

                session['today'] = datetime.datetime.today().replace(microsecond=0)
                
                now = datetime.datetime.today().replace(microsecond=0)

                # return redirect(url_for('room', channel=channel))
                # return redirect(url_for('channel'))
                return redirect(url_for('home'))


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

def addChannelToUser(channel, nickname):
    print(f"--Add channel {channel} to user {nickname} --")

    user=User(nickname)

    if (len(list_user)>0):
        for item in list_user:
            if (item.name == nickname):
                if (item.channels.count(channel)==0):
                    item.add_channel(channel)
                print(item.name, item.channels)
    else:
        print(f"Error....Add user {nickname}")
        user = User(nickname)
        if (user.channels.count(channel)==0):
            user.add_channel(channel)
        list_user.add(user)

    # TODO: may be must to save json
    session['users'] = list_user


def addUserToChannel(channel, nickname):
    print(f"--Add user {nickname} to channel {channel}--")

    user=nickname #User(nickname)

    if (len(list_channel)>0):
        for item in list_channel:
            if (item.name == channel):
                print(f"Add user {user} to channel {channel}")
                if (item.users.count(user)==0):
                    item.add_user(user)
                item.print_info()
    else:
        print(f"Add channel {channel}")
        channel = Channel(channel, 'Public', user)
        print(f"Add user {user} to channel {channel}")
        if (channel.users.count(user)==0):
            channel.add_user(user)
        list_channel.add(channel)

    # TODO: may be must to save json
    session['channels'] = list_channel


def addMessageToChannel(channel, user, time, msg):
    print(f"--add msg {msg} to channel {channel}--")

    msg = Message(user, getDay(time), msg)
    list_messages.append(repr(msg))

    for item in list_channel:
        if (item.name == channel):
            item.add_message(msg)
            print(item.print_info())


def validateUserBychannel(nickname, channel):
    print(f"--Validate {nickname} in {channel}--")
    user=User(nickname)

    if (len(list_channel)>0):
        for item in list_channel:
            if (item.name == channel):
                if (len(item.users)>0):
                    item.print_info()
                    for item2 in item.users:
                        if (item2.name == nickname):
                            print("not valid")
                            return False
    
    print("valid")
    return True

def getMessagesByChannel(channel):
    
    if (len(list_channel)>0):
        for item in list_channel:
            if (item.name == channel):
                return item.messages
    
    return None


def getUsersByChannel(channel):
    
    if (len(list_channel)>0):
        for item in list_channel:
            if (item.name == channel):
                return item.users
    
    return None

def getChannelsByUser(nickname):
    if (len(list_user)>0):
        for item in list_user:
            if (item.name == nickname):
                return item.channels
    
    return None

# @app.route('/channel/<string:channel>', methods= ['GET', 'POST'] )
# def room(channel):
@app.route('/channel', methods= ['GET', 'POST'] )
def channel():

    nickname = session['nickname']
    try:
        channel = request.form['join_room']
        session['channel'] = channel

    except:
        try:
            channel = request.form['create_room']
            session['channel'] = channel

        except:
            pass


    # users = getUsersByChannel(channel)
    # messages = getMessagesByChannel(channel)

   

    if ('nickname' not in session):
        return redirect(url_for('login'))
    else:
        if ('channel' not in session):
            return render_template('index.htm', nickname=nickname, channel="General", channels=list_channel)
        else:
            return render_template('index.htm', nickname=nickname,   channels=list_channel, messages=getMessagesByChannel(session['channel']))


@app.route('/logout', methods=['GET'])
def logout():
    
    # delete the session variables
    if ('nickname' in session):
        nickname= session['nickname']
        del session ['nickname'] 

    # try:
    #     lista_users.remove(user)
    # except:
    #     print("error to remove user from list")

        try:
            if (len(list_user)>0):
                for item in list_user:
                    if (item.name == nickname):
                        item.actve = False
     

        except:
            print("error to remove user from channel")

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
def chat():

    nickname = session['nickname']
    # try:
    #     channel = request.form['join_room']
    #     session['channel'] = channel

    # except:
    #     try:
    #         channel = request.form['create_room']
    #         session['channel'] = channel

    #     except:
    #         pass


    # users = getUsersByChannel(channel)
    # messages = getMessagesByChannel(channel)

   

    if ('nickname' not in session):
        return redirect(url_for('login'))
    else:
        # if ('channel' not in session):
        #     return render_template('index.htm', nickname=nickname, channel="General", channels=list_channel)
        # else:
        #     return render_template('index.htm', nickname=nickname,   channels=list_channel, messages=getMessagesByChannel(session['channel']))
        return render_template('chat.htm',  nickname=session['nickname'],  list_channel=list_channel)


@app.route('/')
def home():

    print(f"N° Channels: {len(list_channel)}")
    if (len(list_channel) == 0):
        channel = Channel(name="Room1", type="Public", owner="Admin")
        channel.print_info()
        list_channel.add(channel)
        channel = Channel("Room2", "Private", "Admin")
        list_channel.add(channel)
        channel = Channel("Room3", "Private", "Admin")
        list_channel.add(channel)

    print(f"N° Channels: {len(list_channel)}")
    print(list_channel)


    if ('nickname' not in session):
        return redirect(url_for('login'))
    else:
        # return render_template('index.htm', nickname=session['nickname'], channels=list_channel, messages=list_messages)
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
    
        msg = f"{datetime.datetime.today().replace(microsecond=0)}  {session['nickname']}: {message['data']}"
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
             {'data': nickname + ' has entered the room ' + room + ' , '.join(rooms()),
              'room': room, 'messages': channel_msg_list,'count': session['receive_count']})
        
 
    def on_leave(self, message):
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
        
        # msg = f"{datetime.datetime.today().replace(microsecond=0)}: {message['data']}"
        
        # time = getDay(datetime.datetime.today())
        time = datetime.datetime.now()
        # message['data'] = msg
        room = message['room']
        user = message['user']
        print("user:"+ user)
        addMessageToChannel(room, user, time, message['data'])
        # 

        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_room',
            {'data': message['data'], 'user': user, 'time': getDay(time), 'count': session['receive_count']},
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
