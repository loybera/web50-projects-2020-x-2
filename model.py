import datetime
import json

from datetime import date

class Channel:

    counter = 1

    def __init__(self, name, type, owner):

        # # Keep track of id number.
        # self.id = Channel.counter
        # Channel.counter += 1

        # Keep track of passengers.
        self.users = []
        self.messages = []

        # Details about flight.
        self.name = name
        self.type = type
        self.owner = owner
        # self.socket = socket


    def print_info(self):
        print("-----inicio-----")
        print(f"Channel name: {self.name}")
        print(f"Channel type: {self.type}")
        print(f"Channel owner: {self.owner}")

        print()
        print(f"Users in channel: {len(self.users)}")
        for user in self.users:
            print(user)

        print(f"Messages in channel: {len(self.messages)}")
        for msg in self.messages:
            print(repr(msg))

        print("-----fin-----")

    def delay(self, amount):
        self.duration += amount

    def add_user(self, u):
        self.users.append(u)

    def remove_user(self, u):
        self.users.remove(u)

    def add_message(self, m):
        self.messages.append(m.toJSON())

    def remove_message(self, m):
        self.messages.remove(m)


class User:


    def __init__(self, name):
        self.name = name
        self.active = True

        self.channels = []

    def add_channel(self, c):
        self.channels.append(c)

    def __repr__(self):
        return "user: " +self.name + ' active:' + str(self.active)


class Message:

    def __init__(self, user, time, post):
        self.time = time
        self.user = user
        self.post = post
        # self.timeFtd = timeFtd

        
    def __repr__(self):

        return (f"Message from {self.user} in {self.time} with {self.post}")
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
 
    
    




