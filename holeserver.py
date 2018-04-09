from socket import *
import re
import time


class Server:
  def __init__(self, ip = "0.0.0.0" , port = 9814 ):
    self.IP = ip
    self.PORT = port

    # This is a table that will contain 
    # (ip,port,nickname,timeofconnection) tuples of connections
    self.userList = []
    
    # create socket and bind it to a port
    self.sock = socket( AF_INET, SOCK_DGRAM )
    self.sock.bind( ( self.IP , self.PORT ) )
    
    self.realPort = self.sock.getsockname()[1]
    if self.realPort != self.PORT:
      print ( "Unable to bind to {} , bound to {} instead".format(self.PORT , self.realPort) )
    else:
      print ("Bound to {}".format(self.PORT)) 
  def serve(self):
    while True:
      print(self.userList)
      msgE , _ , _ , ipport  = self.sock.recvmsg(1024)
      ip , port = ipport
      msg = msgE.decode()
      if re.match("JOIN .*",msg):
        nickName= msg[6:16]
        self.addUser(ip,port,nickName)
      elif re.match(r"QUERY .*s",msg):
        qIP = msg[6:]
        self.query(qIP,ip,port)
  
  def addUser(self,ip,port,nick):
    # Test if username Exists
    if reduce (lambda x,y : x and y , list ( filter (lambda x: x==nick , self.userList) ) ):
      self.sendMsg("NICKNAME_EXISTS {}".format(nick),ip,port)

    currTime = time.time()  
    for i , uIP , _ , nN , _ in enumerate(self.userList):
      if uIP == ip:
        self.userList[i][1] = port
        self.userList[i][2] = nick
        self.query(ip,ip,port)
        return True
    pair = (ip,port,nick,time.time())
    self.userList.append(pair)
    self.query(ip,ip,port)
    return True

  def query(self, qIP, ip, port):
    for i , uIP , uPort , nN , _ in enumerate(self.userList):
      if uIP == qIP :
        self.sendMsg ( "FOUND {} @ {} : {}".format(nN , uIP , uPort) , ip , port )
        return True
    self.sendMsg ( "!FOUND {}".format(qIP) , ip , port )
    return False

  def sendMsg (self ,  msg , ip ,port ):
    self.sock.sendto( msg.encode() , (ip,port) )
    return True
        
    
    

if __name__ == "__main__":
  main()
