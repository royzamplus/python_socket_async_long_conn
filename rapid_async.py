#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
import sys
import time
import select
import random

seqid = 0
message_type = 0
message_version = 0
message_cmdid = 0
message_extra = 0

# init socket object
def connect():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect(("192.168.0.169", 19890))
  sock.setblocking(0)
  return sock

# pack message to be sent
def prepare_msg(msg):
  size = 16 + len(msg)
  packed_msg = struct.pack("!IIBBHI", size, seqid, message_type, message_version, message_cmdid, message_extra)
  packed_msg += msg
  return packed_msg


if __name__ == '__main__':

  set_str_list = [ prepare_msg('set\thttp://www.zamplus.com'),
                   prepare_msg('get\tn9SNLc'),
                   prepare_msg('set\thttp://www.baidu.com'),
                   prepare_msg('set\t12170'),
                  ]
  # get_str = )

  sockets = [connect(), connect(), connect()]
  sock_2_task = dict([(s, i + 1) for i, s in enumerate(sockets)])

  while sockets:
    rlist, slist, _ = select.select(sockets, sockets, [])
    # send message asynchrosously
    for sock in slist:

      set_str_index = random.randint(0, 2)

      sock.send(set_str_list[set_str_index])
      print sock_2_task[sock], 'send message:', set_str_list[set_str_index]
      time.sleep(1)

    # receive message asynchrosously
    for sock in rlist:
      res = sock.recv(16)
      header = struct.unpack("!IIBBHI", res)

      if (0 == (header[0] - 16)):
        continue

      res = sock.recv(header[0] - 16)
      print sock_2_task[sock], 'receive message:', res
      time.sleep(1)
