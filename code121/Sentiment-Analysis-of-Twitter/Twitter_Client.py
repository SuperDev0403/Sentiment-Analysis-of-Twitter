import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json

consumer_key = '4sg2noNLt5n7mIr3gTcgXPBRj '
consumer_secret = 'bff05fe6oS9FS2szGkBwe04eUvR6w0vzGJdXQephNpbHLc39x0'
access_token = '347203012-M9U6TIiEbfTt0ArJj7YzDVeFC5P1LfGRQY1CdNC2'
access_secret = '5FZVDoFUQDX6R1qRb7P7GYZ3D1YdXQwzz9oxTeumWZbTl '

class TweetsListener(StreamListener):

  def __init__(self, csocket):
      self.client_socket = csocket

  def on_data(self, data):
      try:
          msg = json.loads( data )
          print( msg['text'])
          self.client_socket.send( msg['text'])

          return True
      except BaseException as e:
          print("Error on_data: %s" % str(e))
      return True

  def on_error(self, status):
      print(status)
      return True

def sendData(c_socket):
  auth_info = OAuthHandler(consumer_key, consumer_secret)
  auth_info.set_access_token(access_token, access_secret)

  twitter_stream_receive = Stream(auth_info, TweetsListener(c_socket))
  twitter_stream_receive.filter(track=['UseAnyWordHere'])

if __name__ == "__main__":
  ss = socket.socket()         # Create a socket object

  hostaddress  = socket.gethostbyname(socket.gethostname())
  port_setting = 5001                 # Reserve a port for your service.
  ss.bind((hostaddress, port_setting))        # Bind to the port

  print("Listening on port: %s" % str(port_setting))

  ss.listen(5)                 # Now wait for client connection.
  c, addr = ss.accept()        # Establish connection with client.

  print( "Received request from: " + str( addr ) )

  sendData( c )

