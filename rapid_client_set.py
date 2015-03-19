#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
import sys
import time

class WeakClient(object):

  def connect(self, host, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host, port))

  def send_recv(self, data):

    size = 16 + len(data)
    seqid = 0
    message_type = 0
    message_version = 0
    message_cmdid = 0
    message_extra = 0

    str = struct.pack("!IIBBHI", size, seqid, message_type, message_version, message_cmdid, message_extra)
    str += data

    self.sock.send(str)

    res = self.sock.recv(16)
    header = struct.unpack("!IIBBHI", res)

    if (0 == (header[0] - 16)):
      return ""
    res = self.sock.recv(header[0] - 16)
    return res

if __name__ == '__main__':
  client = WeakClient()
  client.connect("192.168.0.169", 19890)

  target_url = sys.argv[1]
  testdata = 'set\t' + target_url

  # while 1:
  print client.send_recv(testdata)
  # time.sleep(1)
