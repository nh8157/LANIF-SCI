# ICS Final Project by Sheldon & Ding

## **Video Demonstration**
[Project Demonstration](https://youtu.be/ZE5z39jZEQo)

## **Features**
- Log-in system
- File transfer system
- **5** interesting single-player games coded in Pygame
- **1** online game coded in Pygame
- Presentation written in **HTML & CSS**

## **Log-in System**
The server has a text file to save the usernames and passwords of all users in the format of "username": "password". After the server is booted, it would read all usernames and passwords and save them in a dictionary. Users would be asked whether they are new or old client as soon as they are connected to the server. If the user is a new client, he or she need to create an account by putting in username and password, which would be transferred to the server and saved in the text file mentioned above. If the user has logged in before, he or she needs to type in their username and password. If the username and password exists in the dictionary mapping username to passwords, the user would be in the system; otherwise they need to try again. 

## **File Transfer System**
File transfer system uses the server as a relay, which receives binary data dent from the sender before sending it to the target. 
To send a file, the user need to input **f _peer_**
The _peer_ specifies the target it is sending to. If the receiver is available, the user would be prompted to input the name of the file needs to be sent. The file needs to be in the same folder as the code is in. In the meantime, the receiver would receive a message, saying **_peer_ is transferring a file to you**. The file would be transferred after the sender puts in an existing file. 

## **Single-player Games**
The games include Snake(single), Snake(multi-player), Flappy Bird, 2048. The first two are original games designed by Ding. 

## **Online Game**
The real-time game involves two red blocks moving in a rectangle space. It is amazing for it runs on a different server as the chat system does, and two players can move constantly on the screen. Their movement can be seen from each other's screen. 

## **Bugs Pending to be Fixed**
- The server would stuck and die in its while loop receiving binary data, which would lead to receiving incomplete binary data, and result in damaged file. On the receiving side, however, most of the files transferred are openable. 
- The online could not be added more functions to. As real-time display of information requires massive data transfer, the serve would die easily when more data needs to be sent. 

## **Acknowledgements**
Great thanks to Joyce, Peter Huang, Tom Zhu, Wen and Dragon Liao, who have helped us out with numerous obstacles we encountered throughout the process. 
