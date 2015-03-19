#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
import sys
import time

class WeakClient(object):

  def __init__(self, set_data, get_data):
    self.set_data = set_data
    self.get_data = get_data

  def connect(self, host, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host, port))

  def send_recv(self):

    set_size = 16 + len(self.set_data)
    get_size = 16 + len(self.get_data)
    seqid = 0
    message_type = 0
    message_version = 0
    message_cmdid = 0
    message_extra = 0

    set_str = struct.pack("!IIBBHI", set_size, seqid, message_type, message_version, message_cmdid, message_extra)
    set_str += self.set_data

    get_str = struct.pack("!IIBBHI", get_size, seqid, message_type, message_version, message_cmdid, message_extra)
    get_str += self.get_data

    while 1:
      self.sock.send(set_str)

      res = self.sock.recv(16)
      header = struct.unpack("!IIBBHI", res)

      if (0 == (header[0] - 16)):
        break

      res = self.sock.recv(header[0] - 16)
      print res

      self.sock.send(get_str)

      res = self.sock.recv(16)
      header = struct.unpack("!IIBBHI", res)

      if (0 == (header[0] - 16)):
        break

      res = self.sock.recv(header[0] - 16)
      print res

      time.sleep(1)

    print 'end'

if __name__ == '__main__':
  client1 = WeakClient('set\thttp://www.zamplus.com', 'get\tn9SNLc')
  client2 = WeakClient('set\thttp://www.163.com', 'get\n5vtHh4')
  client3 = WeakClient('set\thttp://www.baidu.com', 'get\tnaPp90')
  client1.connect("192.168.0.169", 19890)

  client1.send_recv()
