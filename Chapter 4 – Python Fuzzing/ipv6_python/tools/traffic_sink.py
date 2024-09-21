#!/usr/bin/python

# Copyright (c) 2016-2021
# United States Government as represented by Joseph Ishac <jishac@nasa.gov>
# No copyright is claimed in the United States under Title 17, U.S.Code. All Other Rights Reserved.

# This program will listen for IPv6 UDP and TCP traffic on a specified port and
# log reception time and the IPv6 Traffic Class.

from __future__ import print_function

import sys, signal, socket, select
import struct
import math
import logging
from time import sleep, time
from argparse import ArgumentParser, ArgumentTypeError, SUPPRESS

def sigint_handler(signal, stackframe):
  # Handler for Ctrl-C (SIGINT)
  print("")
  logging.debug('Caught Interrupt, Exiting!')
  cleanup()
  sys.exit(0)

def cleanup():
  global open_socks
  for sock in open_socks:
    sock.close()

def any_int(string):
  try: value = int(string,0)
  except:
    raise ArgumentTypeError("{}: Invalid Decimal or Hex, Hex must start with (0x)".format(string))
  return value

def any_str(string):
  return string.decode('string-escape') 

def establish_server(host, port, stype, sfamily=socket.AF_INET6):
  sock = None
  try:
    # sfamily defaults of socket.AF_INET6, for IPv6
    for resolve in socket.getaddrinfo(host, port, sfamily, stype):
      family, socktype, proto, canonname, sockaddr = resolve
      try:
        sock = socket.socket(family, socktype, proto)
        if (family == socket.AF_INET6):
          # Setup to get TCLASS Info (IPv6 ONLY)
          sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_RECVTCLASS, 1)
      except socket.error as msg:
        sock = None
        logging.error('Socket Creation Error: {}'.format(msg))
        continue
      try:
        sock.bind((host, port))
        if (socktype == socket.SOCK_STREAM):
          sock.listen(5)
      except socket.error as msg:
        logging.critical('Socket Binding Error: {}'.format(msg))
        sock.close()
        sock = None
        continue
      break
  except socket.error as msg:
    logging.error('Name or address resolution failed: {}'.format(msg))
  if sock is None:
    logging.critical('Fatal Error: Could not open a socket for {} on port {}'.format(options.host, options.port))
    sys.exit(1)
  return sock

def process_msg(msg, tnow, print_data=False):
  p = 0
  msg_len = len(msg)
  while (p < msg_len):
    if ((msg_len - p) < 5):
      return msg[p:]
    (msg_seq, msg_tclass, msg_mf) = struct.unpack("!HBH",msg[p:p+5])
    msg_size = msg_mf & 0x7fff
    if (msg_seq == 0):
      # Cannot have a zero seq# something went wrong, dump the msg
      print("{0:f} !SEQ {2} Rx {1}".format(tnow,msg.encode("hex"),msg_len))
      return None
    if (msg_size == 0):
      # Cannot have a zero size something went wrong, dump the msg
      print("{0:f} !LEN {2} Rx {1}".format(tnow,msg.encode("hex"),msg_len))
      return None
    if ((msg_len - p) < msg_size):
      return msg[p:]
    print("{0:f} {3} {2} Rx {1}".format(tnow,msg_seq,msg_size,hex(msg_tclass)),end='')
    p += 5
    msg_size -= 5
    if (msg_mf & 0x8000):
      (msg_ts,) = struct.unpack("!d",msg[p:p+8])
      p += 8
      msg_size -= 8
      print(" {:f} {:f}".format(msg_ts,(tnow-msg_ts)),end='')
    msg_data = msg[p:p+msg_size]
    p += msg_size
    if (print_data):
      print(" {}".format(msg_data.encode("hex")))
    else:
      print("")
  return None

if __name__ == '__main__':
  # Administrative Stuff
  signal.signal(signal.SIGINT, sigint_handler)
  # Settings
  _MAX_MTU = 0x7fff
  # Globals that will require "cleanup"
  open_socks = []
  # Parse Arguments
  parser = ArgumentParser(description="This program will listen for IPv6 UDP and TCP traffic on a specified port and log reception time and the IPv6 Traffic Class.")
  parser_protocol = parser.add_mutually_exclusive_group()
  parser.add_argument('-V', '--version', action='version', version='%(prog)s version 1.23, Joseph Ishac (jishac@nasa.gov)')
  parser.add_argument("-D", "--debug", action="store_true", dest="debug", default=False, help="Extra debugging information")
  parser.add_argument("-v", "--verbose", action="count", dest="verbose", default=1, help="Increase verboseness of messages")
  parser.add_argument("-q", "--quiet", action="store_const", dest="verbose", const=0, help="Disable any extra dialog")
  parser_protocol.add_argument("-u", "--udp", action="store_false", dest="tcp", default=True, help="Listen on UDP Only")
  parser_protocol.add_argument("-t", "--tcp", action="store_false", dest="udp", default=True, help="Listen on TCP Only")
  parser.add_argument("-4", "--ipv4", action="store_true", dest="ipv4", default=False, help="Receive IPv4 traffic instead of IPv6")
  parser.add_argument("-p", "--payload", action="store_true", dest="payload", default=False, help="Log the payload sent")
  parser.add_argument("-s", "--size",
                    action="store", type=int, dest="size", default=9200,
                    help="Specifies the capture length in bytes. Default: %(default)s", metavar="BYTES")
  parser.add_argument("host",
                    action="store", type=str, default='::', nargs="?",
                    help="The IPv6 host or address to listen on.", metavar="host")
  parser.add_argument("port",
                    action="store", type=int, default=None,
                    help="The port number to listen on.", metavar="port")
  options = parser.parse_args()
    
  # Establish logging
  # Set log level here in "basicConfig", levels are NOTSET, DEBUG, INFO, WARNING, ERROR and CRITICAL
  logging_format = "%(asctime)s; %(levelname)s; %(funcName)s; %(lineno)d; %(message)s"
  if options.debug:
    logging.basicConfig(level=logging.DEBUG, format=logging_format)
  elif (options.verbose >= 2):
    logging.basicConfig(level=logging.INFO, format=logging_format)
  elif (options.verbose == 1):
    logging.basicConfig(level=logging.ERROR, format=logging_format)
  else:
    logging.basicConfig(level=logging.CRITICAL, format=logging_format)

  # Additional Options Checking
  if (options.size < 1280):
    parser.error("Capture size must be at least {} bytes.".format(prefix_len))
  if (options.size > _MAX_MTU):
    parser.error("Payload sizes exceeding {} bytes are not currently supported".format(_MAX_MTU))

  # Show all set options for Debugging output
  if (options.debug):
    print("Set Options: {}".format(options))
  
  if ((options.host is None) or (options.port is None)):
    # This shouldn't be possible with argparse
    parser.error("You must specify a host and port.")

  if (options.ipv4):
    sfamily=socket.AF_INET
  else:
    sfamily=socket.AF_INET6

  usock = None
  tsock = None
  if (options.udp):
    usock = establish_server(options.host,options.port,socket.SOCK_DGRAM,sfamily)
    open_socks.append(usock)
  if (options.tcp):
    tsock = establish_server(options.host,options.port,socket.SOCK_STREAM,sfamily)
    open_socks.append(tsock)

  tcp_buffers={}

  while True:
    (rsock, wsock, esock) = select.select(open_socks,[],open_socks)
    for sock in rsock:
      if sock is tsock:
        # New TCP connection waiting
        try:
          (new_sock, new_dst) = sock.accept()
          open_socks.append(new_sock)
          tcp_buffers[new_sock] = None
          logging.info("Accepted Connection from {}:{}".format(*new_dst))
        except socket.error as err:
          logging.error("Unexpected Socket Error: {}".format(err))
      elif sock is usock:
        # Got a UDP message
        try:
          msg = sock.recv(options.size)
          tnow = time()
        except socket.error as err:
          logging.error("Unable to read from UDP: {}".format(err))
          continue
        msg_part = process_msg(msg,tnow,options.payload)
        if (msg_part is not None):
          # This shouldn't happen for UDP
          logging.critical("Got a partial message over UDP!")
      else:
        # Got a TCP message
        try:
          msg = sock.recv(options.size)
          tnow = time()
        except socket.error as err:
          logging.error("Remote client terminated unexpectedly: {}".format(err))
          msg = ''
        if (msg == ''):
          # Client disconnected
          logging.info("Remote client at {}:{} has disconnected.".format(*sock.getpeername()))
          open_socks.remove(sock)
          if (tcp_buffers[sock] is not None):
            # Closed with data outstanding!
            logging.error("Discarding Partial Data!")
          del tcp_buffers[sock]
          continue
        if (tcp_buffers[sock] is not None):
          # Have some partial data, join with current
          msg = b"".join((tcp_buffers[sock],msg))
          tcp_buffers[sock] = None
        msg_part = process_msg(msg,tnow,options.payload)
        if (msg_part is not None):
          # Have some data left over, save it for next time
          tcp_buffers[sock] = msg_part


  sys.exit(0)
