#!/usr/bin/python

from config import *

import socket
import sys
import string
import time

BotNick = "CBot"
BotAlt = "CBot-"
BotIdent = "CBot"
BotRealname = "CBot"
SERVER = "irc.irchighway.net"
PORT = 6667


sockChan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockChan.connect((SERVER, PORT))

def SendIRC (msg):
  sockChan.send(bytes(f'{str(msg)} \r\n', 'UTF-8'))
  
SendIRC(f'USER {BotIdent} * * :{BotRealname}')
SendIRC(f'NICK {BotNick}')
connected = True

while connected:
  line = sockChan.recv(2040).decode('UTF-8')
  print(line)
  if line != "":
    lline = line.split()
    if 'PING' in lline[0]:
      SendIRC(f'PONG {lline[1]}')
    if '433' in lline[1]:
      SendIRC(f'NICK {BotAlt}')
