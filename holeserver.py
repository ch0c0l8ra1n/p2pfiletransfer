from socket import *
import re
import time


class Server:
  def __init__(self, ip = "0.0.0.0" , port = 9814 ):
    self.IP = ip
    self.PORT = port

    # This is a table that will contain 
    # [ip,port,nickname,timeofconnection] list of connections
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
        nickName= msg[5:15]
        self.addUser(ip,port,nickName)
      elif re.match(r"QUERY .*",msg):
        qIP = msg[6:]
        self.query(qIP,ip,port)
      elif re.match(r"QUERYNICK .*",msg):
        nick = msg[10:]
        self.queryNick(nick,ip,port)
      if re.match(r"KEEPALIVE .*",msg)
        self.keepalive(ip,port,nick)
  
  def addUser(self,ip,port,nick):
    # Test if username Exists
    if any( list ( filter (lambda x: x==nick , self.userList) ) ):
      self.sendMsg("NICKNAME_EXISTS {}".format(nick),ip,port)

    currTime = time.time()  
    for i , temp in enumerate(self.userList):
      uIP , pP , nN , _ = temp
      if uIP == ip and port != pP:
        self.userList[i][2] = nick
        self.query(ip,ip,port)
        return True
    pair = [ip,port,nick,time.time()]
    self.userList.append(pair)
    self.query(ip,ip,port)
    return True

  def query(self, qIP, ip, port):
    for i , temp in enumerate(self.userList):
      uIP , uPort , nN , _ = temp
      if uIP == qIP :
        self.sendMsg ( "FOUND {} @ {} : {}".format(nN , uIP , uPort) , ip , port )
        return True
    self.sendMsg ( "!FOUND {}".format(qIP) , ip , port )
    return False

  def queryNick (self, qN , ip , port):
    for i , temp in enumerate(self.userList):
      uIP , uPort , nN , _ = temp
      if nN == qN :
        self.sendMsg( "FOUNDNICK {} @ {} : {}".format(nN, uIP, uPort) , ip ,port)
        return True
    self.sendMsg ( "!FOUNDNICK {}".format(qN) , ip , port )

  def keepAlive(self, ip ,port , nick):
    for i , temp in enumerate(self.userList):
      uIP , uPort , nN , _ = temp
      if uIP == ip and nN == nick:
        self.userList[i][3] = time.time()


  def sendMsg (self ,  msg , ip ,port ):
    self.sock.sendto( msg.encode() , (ip,port) )
    return True
        
    
    

if __name__ == "__main__":
  main()
