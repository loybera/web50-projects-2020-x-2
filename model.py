import datetime
import json

from datetime import date

class Channel:

    def __init__(self, channel, name,  owner, public):

        # # Keep track of id number.
        self.id = channel


        # Keep track of passengers.
        self.users = []
        self.messages = []

        self.name = name
        self.public = public
        self.owner = owner
        # self.socket = socket


    def print_info(self):
        print("-----begin-----")
        print(f"Channel id: {self.id}  name: {self.name} public: {self.public} Owner: {self.owner}")
        print(f"Users in channel: {len(self.users)}")
        for user in self.users:
            print(repr(user))

        print(f"Messages in channel: {len(self.messages)}")
        for msg in self.messages:
            print(repr(msg))

        print("--end channel--")
 

    def add_user(self, u):
        self.users.append(u)

    def remove_user(self, u):
        self.users.remove(u)

    def add_message(self, m):
        self.messages.append(m.toJSON())

    def remove_message(self, m):
        self.messages.remove(m)


class User:

    counter = 1

    def __init__(self, name):
        # Keep track of id number.
        self.id = User.counter
        User.counter += 1

        self.name = name
        self.active = True
        self.channels = []

    def add_channel(self, c):
        self.channels.append(c)

    def __repr__(self):
        return (f"User #{self.id} Name: {self.name} Active: {self.active}")

class ChannelUser:


    def __init__(self, id, name):

        # # Keep track of id number.
        self.id = id
        self.name = name

class Message:

    counter = 1

    def __init__(self, user, time, post):
        # Keep track of id number.
        self.id = Message.counter
        Message.counter += 1
        
        self.time = time
        self.user = user
        self.post = post
        # self.timeFtd = timeFtd

        
    def __repr__(self):

        return (f"Message #{self.id} from {self.user} in {self.time} post: {self.post}")
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
 
    
    




