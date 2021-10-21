#!/usr/bin/python

import socket
import sys
from config import *

sockChan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockChan.connect((SERVER, PORT))

def SendIRC (msg):
  sockChan.send(bytes(f'{str(msg)} \r\n', 'UTF-8'))
  
SendIRC(f'USER {BotIdent} * * :{BotRealname}')
SendIRC(f'NICK {BotNick}')
connected = True

while connected:
  line = sockChan.recv(2040).decode('UTF-8')
  if line != "":
    lline = line.split()
    if 'PING' in lline[0]:
      SendIRC(f'PONG {lline[1]}')
    if '433' in lline[0]:
      SendIRC(f'NICK {BotAlt}')
    if '001' in lline[0]:
      SendIRC(f'JOIN {Home}')