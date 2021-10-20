#!/usr/bin/python3
#
#

import sys
import time
import socket
import string
from config import *

DebugMode = True

sockChan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockChan.connect_ex((BotServer, BotPort))


def sendIRC(msg):
    sockChan.sendall(bytes(f'{str(msg)} \r\n', 'UTF-8')) # Send data to IRC server.
    if DebugMode:
        print(f'Sending to Server: {msg}')


sendIRC(f'USER {BotIdent} * * :{BotRealName}') #Command: USER Parameters: <user> <mode> <unused> <realname>
sendIRC('NICK ' + BotNick)
if BotPassword:
    sendIRC('PRIVMSG NICKSERV :IDENTIFY ' + BotPassword)

connected = True

def main():
    while connected:

        line = sockChan.recv(2040).decode('utf-8')

        if DebugMode:
            print(line)
    
        lline = line.split()

        if 'PING' in lline[0]:
            sendIRC("PONG " + lline[1] )
        if '001' in lline[1]:
            sockChan.send("JOIN " + BotChannel )
        if '433' in lline[1]:
            sendIRC('NICK ' + BotAlt )

        if 'PRIVMSG' in lline[1]:
            if '!quit' in lline[3]:                
                sendIRC('QUIT' + QuitMessage )
                sys.exit()
            if '!join' in lline[3]:
                sendIRC('JOIN ' + lline[4] )
            if '!part' in lline[3]:
                sendIRC('PART ' + lline[4] )


main()
