"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
import sys

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def send_to(self, peer):
        print("here")
        input("Which file do you want?")
        file_name = "roman.txt"
#        try:
        file = open(file_name, 'rb')
        while True:
            file_data = file.read(1024)
            if not file_data:
                break
            msg = json.dumps({"action":"transfer", "target":peer, "data":file_data})
            mysend(self.s, msg) 
        file.close()
        response = json.loads(myrecv(self.s))
        if response["status"] == "self":
            self.out_msg += "Cannot transfer file to yourself\n"
        elif response["status"] == "busy":
            self.out_msg += "User is chatting, cannot transfer files\n" 
        elif response["status"] == "none":
            self.out_msg += "User is not online, try agains later\n"
        else:
            self.out_msg += "Transfer complete successfully\n"
#        except:
#            self.out_msg += "An error occurred when opening the file\n"
                
    
    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})  
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
        
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in
                
                elif my_msg[0] == 'f':
                    peer = my_msg[1:].strip()
                    self.peer = peer
                    self.state = S_TRANSFER
                    self.out_msg += "Which file do you want to send?"

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'
                    
                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"]
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' or my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    if (len(poem) > 0):
                        for i in poem:
                            self.out_msg += i + '\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                try:
                    peer_msg = json.loads(peer_msg)
                except Exception as err :
                    self.out_msg += " json.loads failed " + str(err)
                    return self.out_msg
            
                if peer_msg["action"] == "connect":

                    # ----------your code here------#
                    peer = peer_msg["from"]
                    self.peer = peer
                    self.out_msg += "You are connected with " + self.peer
                    self.state = S_CHATTING
                    # ----------end of your code----#
                    
#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in
                # ----------your code here------#
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "exchange":
                    self.out_msg += peer_msg["message"]
                elif peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " is in)"
                elif peer_msg["action"] == "disconnect":
                    self.disconnect()
                    self.state = S_LOGGEDIN
                # ----------end of your code----#
                
            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
        elif self.state == S_TRANSFER:
            file_name = my_msg
            try:
                file = open(file_name, 'rb')
                while True:
                    file_data = file.read(1024)
                    if not file_data:
                        break
                    msg = json.dumps({"action": "transfer", "target": self.peer, "data": file_data})
                    mysend(self.s, msg)
            except:
                self.out_msg += "An error occurred when transferring the file"
            self.state = S_LOGGEDIN
                
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
