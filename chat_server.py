"""
Created on Tue Jul 22 00:47:05 2014

@author: alina, zzhang
"""

import time
import struct
import socket
import select
import sys
import string
import indexer
import json
import base64
import pickle as pkl
from chat_utils import *
import chat_group as grp


class Server:
    def __init__(self):
        self.new_clients = []  # list of new sockets of which the user id is not known
        self.logged_name2sock = {}  # dictionary mapping username to socket
        self.logged_sock2name = {}  # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        self.client_password = {}
        self.state = S_LOGGEDIN
        # start server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        # initialize past chat indices
        self.indices = {}
        # sonnet
        self.sonnet = indexer.PIndex("AllSonnets.txt")

    def new_client(self, sock):
        # add to all sockets and to new clients
        print('new client...')
        sock.setblocking(2)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def loginPage(self, sock):
        # read the msg that should have login code plus username
        try:
            msg = json.loads(myrecv(sock))
            if len(msg) > 0:
                if msg["action"] == "create":
                    name = msg["name"]
                    password = msg["password"]       
                    if name not in self.client_password.keys():
                        file = open(file_name, 'a')
                        file.write(name + ":" + password + "\n")
                        # move socket from new clients list to logged clients
                        self.new_clients.remove(sock)
                        # add into the name to sock mapping
                        self.logged_name2sock[name] = sock
                        self.logged_sock2name[sock] = name
                        # load chat history of that user
                        if name not in self.indices.keys():
                            try:
                                self.indices[name] = pkl.load(
                                    open(name + '.idx', 'rb'))
                            except IOError:  # chat index does not exist, then create one
                                self.indices[name] = indexer.Index(name)
                        print(name + ' logged in')
                        self.client_password[name] = password
                        self.group.join(name)
                        mysend(sock, json.dumps(
                            {"action": "login", "status": "ok"}))
                    else:  # a client under this name has already logged in
                        mysend(sock, json.dumps(
                            {"action": "login", "status": "duplicate"}))
                        print(name + ' duplicate login attempt')
                    
                elif msg["action"] == "login":
                    name = msg["name"]
                    password = msg["password"]
                    if name in self.client_password.keys():
                        if self.client_password[name] == password:
                            # move socket from new clients list to logged clients
                            self.new_clients.remove(sock)
                            # add into the name to sock mapping
                            self.logged_name2sock[name] = sock
                            self.logged_sock2name[sock] = name
                            print(name + ' logged in')
                            self.group.join(name)
                            if name not in self.indices.keys():
                                try:
                                    self.indices[name] = pkl.load(
                                        open(name + '.idx', 'rb'))
                                except IOError:  # chat index does not exist, then create one
                                    self.indices[name] = indexer.Index(name)
                            mysend(sock, json.dumps(
                                {"action": "login", "status": "ok"}))
                        else:
                            mysend(sock, json.dumps({"action": "login", "status": "password"}))
                    else:
                        mysend(sock, json.dumps({"action": "login", "status": "username"}))
                else:
                    print('wrong code received')
            else:  # client died unexpectedly
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)

    def logout(self, sock):
        # remove sock from all lists
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + '.idx', 'wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

# ==============================================================================
# main command switchboard
# ==============================================================================
    def handle_msg(self, from_sock):
        # read msg code
        if self.state == S_LOGGEDIN:
            msg = myrecv(from_sock)
            if len(msg) > 0:
                # ==============================================================================
                # handle connect request this is implemented for you
                # ==============================================================================
                msg = json.loads(msg)
                if msg["action"] == "connect":
                    to_name = msg["target"]
                    print(from_sock)
                    from_name = self.logged_sock2name[from_sock]
                    print(from_name)
                    if to_name == from_name:
                        msg = json.dumps({"action": "connect", "status": "self"})
                    # connect to the peer
                    elif self.group.is_member(to_name):
                        to_sock = self.logged_name2sock[to_name]
                        self.group.connect(from_name, to_name)
                        the_guys = self.group.list_me(from_name)
                        msg = json.dumps(
                            {"action": "connect", "status": "success"})
                        for g in the_guys[1:]:
                            to_sock = self.logged_name2sock[g]
                            mysend(to_sock, json.dumps(
                                {"action": "connect", "status": "request", "from": from_name}))
                    else:
                        msg = json.dumps(
                            {"action": "connect", "status": "no-user"})
                    mysend(from_sock, msg)
                
    # ==============================================================================
    # file transfer between users
    # ==============================================================================                
                    
                elif msg["action"] == "transfer":
                    from_name = self.logged_sock2name[from_sock]
                    to_name = msg['target']
                    if to_name == from_name:
                        msg = json.dumps({"action": "transfer", "status": "self"})
                    elif to_name in self.group.members:
                        if to_name not in self.group.chat_grps.values():
                            to_sock = self.logged_name2sock[to_name]
                            mysend(to_sock, json.dumps({"action": "transfer", "from": from_name}))
                            self.state = S_TRANSFER
                            msg = json.dumps({"action": "transfer", "status": "available"})
                        else:
                            msg = json.dumps({"action": "transfer", "status": "busy"})
                    elif to_name not in self.group.members:
                        msg = json.dumps({"action": "transfer", "status": "none"})
                    mysend(from_sock, msg)
                    
                        
    # ==============================================================================
    # handle messeage exchange: IMPLEMENT THIS
    # ==============================================================================
                elif msg["action"] == "exchange":
                    from_name = self.logged_sock2name[from_sock]
                    """
                    Finding the list of people to send to and index message
                    """
                    # IMPLEMENTATION
                    # ---- start your code ---- #
                    message = '[' + from_name + ']' + msg["message"]
                    # ---- end of your code --- #
    
                    the_guys = self.group.list_me(from_name)[1:]
                    words = msg["message"].split()
                    for wd in words:
                        if wd not in self.indices:
                            self.indices[wd] = [str(time.strftime("%H:%M:%S")) + message]
                        else:
                            self.indices[wd].append(str(time.strftime("%H:%M:%S")) + message)
                    for g in the_guys:
                        to_sock = self.logged_name2sock[g]
                                            
                        # g.add_msg_and_index(time.strftime("%J:%M:%S") + " " + message)
                        
    #                    # IMPLEMENTATION
    #                    # ---- start your code ---- #
    #                    self.indices[from_name].append(g.add_msg_and_index(message))
    #                    for i in g.index.keys():
    #                        self.indices[i] += g.index[i]
                        mysend(to_sock, json.dumps({"action": "exchange", "from": from_name, "message": message}))
    
                        # ---- end of your code --- #
    
    # ==============================================================================
    # the "from" guy has had enough (talking to "to")!
    # ==============================================================================
                elif msg["action"] == "disconnect":
                    from_name = self.logged_sock2name[from_sock]
                    the_guys = self.group.list_me(from_name)
                    self.group.disconnect(from_name)
                    the_guys.remove(from_name)
                    if len(the_guys) == 1:  # only one left
                        g = the_guys.pop()
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps(
                            {"action": "disconnect", "message": "everyone left, you are alone"}))
    # ==============================================================================
    #                 listing available peers: IMPLEMENT THIS
    # ==============================================================================
                elif msg["action"] == "list":
    
                    # IMPLEMENTATION
                    # ---- start your code ---- #
                    msg = self.group.list_all(self.logged_sock2name[from_sock])
                    # ---- end of your code --- #
                    mysend(from_sock, json.dumps(
                        {"action": "list", "results": msg}))
    # ==============================================================================
    #             retrieve a sonnet : IMPLEMENT THIS
    # ==============================================================================
                elif msg["action"] == "poem":
    
                    # IMPLEMENTATION
                    # ---- start your code ---- #
                    num = msg["target"]
                    poem = self.sonnet.get_poem(int(num))
                    print('here:\n', poem)
                    # ---- end of your code --- #
    
                    mysend(from_sock, json.dumps(
                        {"action": "poem", "results": poem}))
    # ==============================================================================
    #                 time
    # ==============================================================================
                elif msg["action"] == "time":
                    ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                    mysend(from_sock, json.dumps(
                        {"action": "time", "results": ctime}))
    # ==============================================================================
    #                 search: : IMPLEMENT THIS
    # ==============================================================================
                elif msg["action"] == "search":
    
                    # IMPLEMENTATION
                    # ---- start your code ---- #
                    try:
                        result = str(self.indices[msg["target"]])
                    except:
                        result = ''
                    #print('server side search: ' + search_rslt)
    
                    # ---- end of your code --- #
                    mysend(from_sock, json.dumps(
                        {"action": "search", "results": result}))
                
    
    # ==============================================================================
    #                 the "from" guy really, really has had enough
    # ==============================================================================
    
            else:
                # client died unexpectedly
                self.logout(from_sock)
        else:
            msg = myrecv(from_sock)
            if len(msg) > 0:
                msg = json.loads(msg)
                # identify the peer the file is transferring to
                to_name = msg["target"]
                to_sock = self.logged_name2sock[to_name]
                mysend(to_sock, json.dumps({"action": "transfer", "filename": msg["filename"]}))
#                file = open('asdfasdf.docx', 'wb')
                while True:
                    file_data = myrecvF(from_sock)
                    print("yes")
                    mysendF(to_sock, file_data)
                    if not file_data:
                        break
                print("sent")
                self.state = S_LOGGEDIN

                    
        
# ==============================================================================
# main loop, loops *forever*
# ==============================================================================
    def run(self):
        print('starting server...')
        file = open(file_name, 'r')
        file_data = file.readlines()
        for i in range(len(file_data)):
            info = file_data[i].split(":")
            self.client_password[info[0]] = info[1][:-1].strip()
        print(self.client_password)
        file.close()
        while(1):
            read, write, error = select.select(self.all_sockets, [], [])
            print('checking logged clients..')
            for logc in list(self.logged_name2sock.values()):
                if logc in read:
                    self.handle_msg(logc)
            print('checking new clients..')
            for newc in self.new_clients[:]:
                if newc in read:
                    self.loginPage(newc)
            print('checking for new connections..')
            if self.server in read:
                # new client request
                sock, address = self.server.accept()
                self.new_client(sock)

def convert_string_to_bytes(string):
    bytes = b''
    for i in string:
        bytes += struct.pack("B", ord(i))
    return bytes

def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
