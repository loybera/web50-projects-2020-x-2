import random
import datetime
import json

from datetime import date

picture = {1 : 'dog', 2 : 'cat', 3 : 'cheeta', 4 : 'eagle', 5 : 'guanaco', 6 : 'horse', 7 : 'wolf', 8 : 'parrot', 9 : 'mapache', 10: 'monkey', 11: 'rabbit', 12: 'squee', 13: 'tiger', 14: 'tucan', 15: 'turtle'}

class Channel:

    def __init__(self, channel, name,  owner, channel_type):

        # # Keep track of id number.
        self.id = channel.lower()


        # Keep track of passengers.
        self.users = []
        self.messages = []

        self.name = name
        self.channel_type = channel_type
        self.owner = owner
        self.image = picture[random.randrange(1,8)]


    def print_info(self):
        print("-----begin-----")
        print(f"Channel id: {self.id}  name: {self.name} channel_type: {self.channel_type} Owner: {self.owner}")
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

    def __init__(self, id, name ):
        # Keep track of id number.
        self.id = id
        self.name = name.lower()
        self.active = True
        self.image = picture[random.randrange(9,15)]
        self.channels = []

    def add_channel(self, c):
        self.channels.append(c)

    def __repr__(self):
        return (f"User #{self.id} Name: {self.name} Active: {self.active}")

class ChannelUser:


    def __init__(self, id, name, image, channel_type, user_to, user_from):

        # # Keep track of id number.
        self.id = id
        self.name = name.lower()
        self.image = image
        self.channel_type = channel_type
        self.user_to = user_to
        self.user_from = user_from

class Message:

    counter = 1

    def __init__(self, channel, user_from, user_to, time, post, user_from_img):
        # Keep track of id number.
        self.id = Message.counter
        self.channel = channel.lower()
        self.user_from = user_from.lower()
        self.user_from_img = user_from_img
        self.user_to = user_to.lower()
        self.time = time
        self.post = post
        Message.counter += 1
        
    def __repr__(self):

        return (f"Message #{self.id} channel: {self.channel} from {self.user_from} to: {self.user_to} in {self.time} post: {self.post} image:{self.user_from_img}")
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
 
    
    




