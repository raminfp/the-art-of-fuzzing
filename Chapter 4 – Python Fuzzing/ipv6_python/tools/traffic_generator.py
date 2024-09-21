#!/usr/bin/python

# Copyright (c) 2016-2021
# United States Government as represented by Joseph Ishac <jishac@nasa.gov>
# No copyright is claimed in the United States under Title 17, U.S.Code. All Other Rights Reserved.

# This program will generate IPv6 UDP or TCP traffic of a certain size to a set
# destination and allow control of the IPv6 Traffic Class and Rate at which the
# data is sent.

import sys, signal, socket
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
  sys.exit(2)

def cleanup():
  global sock
  if sock is not None:
    sock.close()

def any_int(string):
  try: value = int(string,0)
  except:
    raise ArgumentTypeError("{}: Invalid Decimal or Hex, Hex must start with (0x)".format(string))
  return value

def any_str(string):
  try:
    # Python 2.x
    return string.decode('string-escape')
  except AttributeError:
    # Python 3
    return(bytes(string.encode('utf-8').decode('unicode_escape'),'utf-8'))

if __name__ == '__main__':
  # Administrative Stuff
  signal.signal(signal.SIGINT, sigint_handler)
  # Settings
  _MAX_MTU = 0x7fff
  # Globals that will require "cleanup"
  sock = None
  # Parse Arguments
  parser = ArgumentParser(description="This program will generate IPv6 UDP or TCP traffic of a certain size to a set destination and allow control of the IPv6 Traffic Class and Rate at which the data is sent.  IPv4 data can also be generated with the -4 option.")
  parser_protocol = parser.add_mutually_exclusive_group()
  parser_rate = parser.add_mutually_exclusive_group()
  parser_limit = parser.add_mutually_exclusive_group()
  parser.add_argument('-V', '--version', action='version', version='%(prog)s version 1.23, Joseph Ishac (jishac@nasa.gov)')
  parser.add_argument("-D", "--debug", action="store_true", dest="debug", default=False, help="Extra debugging information")
  parser.add_argument("-v", "--verbose", action="count", dest="verbose", default=1, help="Increase verboseness of messages")
  parser.add_argument("-q", "--quiet", action="store_const", dest="verbose", const=0, help="Disable any extra dialog")
  parser_protocol.add_argument("-u", "--udp", action="store_true", dest="udp", default=True, help="Communicate over UDP (Default)")
  parser_protocol.add_argument("-t", "--tcp", action="store_false", dest="udp", help="Communicate over TCP instead of UDP")
  parser.add_argument("-4", "--ipv4", action="store_true", dest="ipv4", default=False, help="Send IPv4 traffic instead of IPv6")
  parser.add_argument("-T", "--timestamp", action="store_true", dest="timestamp", default=False, help="Embed a timestamp in each message")
  parser.add_argument("-b", "--blind", action="store_true", dest="blind", default=False, 
                    help="Send 'Blindly'.  For UDP, ignore ICMP port unreachable messages. Caution! This may cause unwanted return traffic.")
  parser.add_argument("-c", "--count",
                    action="store", type=int, dest="count", default=None,
                    help="Stop after sending COUNT packets.", metavar="COUNT")
  parser_rate.add_argument("-f", "--frequency",
                    action="store", type=float, dest="hz", default=None,
                    help="Send packets at HZ frequency. Default: 1.0 Hz", metavar="HZ")
  parser.add_argument("-F", "--flowlabel",
                    action="store", type=any_int, dest="flowlabel", default=None,
                    help="Allocate and set the 20 bit flow label. If value is zero, kernel allocates random flow label.", metavar="LABEL")
  parser_rate.add_argument("-i", "--interval",
                    action="store", type=float, dest="interval", default=None,
                    help="Wait INTERVAL seconds between sending each packet. Fractional values are allowed. Default: 1.0 sec", metavar="INTERVAL")
#  parser.add_argument("-I", "--interface",
#                    action="store", type=str, dest="iface", default=None,
#                    help="Set the interface (Not Yet Implemented)", metavar="IFACE")
  parser.add_argument("-A", "--adjust",
                    action="append", type=int, dest="adjust", default=None, nargs='+',
                    help="Adjust the size of a transmission in the given slot(s). Multiple adjustments can be made. Format (Size [Slot1 .. SlotN])", metavar="N")
  parser.add_argument("-l", "--preload",
                    action="store", type=int, dest="preload", default=0,
                    help="Send PRELOAD packets immediately when starting", metavar="PRELOAD")
  parser.add_argument("-o", "--offset",
                    action="store", type=float, dest="offset", default=None,
                    help="Offset transmissions by some fixed delay in seconds (can be fractional). Offset is from the start of nearest second. Thus, an offset of zero can be used to start transmissions on a second boundary.", metavar="SEC")
  parser.add_argument("-p", "--pattern",
                    action="store", type=any_str, dest="pattern", default='',
                    help="You may specify a PATTERN of bytes to fill out the packet. The pattern will be repeated.", metavar="PATTERN")
  parser.add_argument("-P", "--period",
                    action="store", type=float, dest="period", default=None,
                    help="The basis of time for transmissions in seconds. \
                    Thus, an interval of 2 and period of 6 would equate to 3 transmissions over 6 seconds. Default: 1.0 sec", metavar="SEC")
  parser.add_argument("-Q", "--qos", "--dscp",
                    action="store", type=str, dest="tclass", default=None,
                    help="Set the DiffServ *Experimental* Code Point in the packets.\
                    Thus, values from 0-15 will produce a traffic class field of 0x0c to 0xfc (to comply with ECN). \
                    Alternatively, specify an explicit traffic class field (including ECN bits) by entering values larger than 0xf.\
                    Common code point names (ie: CS1, AF11) can also be used.\
                    TOS can be entered in decimal or hex (hex prefixed with 0x).", metavar="TOS")
  parser.add_argument("-s", "--size",
                    action="store", type=int, dest="size", default=56,
                    help="Specifies the number of data bytes to be sent per packet. Default: %(default)s", metavar="BYTES")
  parser_limit.add_argument("-S", "--skip",
                    action="store", type=int, nargs='+', dest="skip", default=None,
                    help="Skip the Nth transmission in every period. Multiple values can be specified. \
                    For example, '-S 1 3' will skip the first and third transmission.", metavar="N")
  parser_limit.add_argument("-O", "--only",
                    action="store", type=int, nargs='+', dest="only", default=None,
                    help="Send only the Nth transmission in every period. Multiple values can be specified. \
                    For example, '-O 1 3' will only send the first and third transmission.", metavar="N")
  parser.add_argument("host",
                    action="store", type=str, default=None,
                    help="The destination IPv6 host or address.", metavar="host")
  parser.add_argument("port",
                    action="store", type=int, default=None,
                    help="The destination port number.", metavar="port")
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

  # Check the Period
  if (options.period is None):
    options.period = 1.0

  # Coordinate Freq and Interval
  if (options.interval is not None):
    # Interval was set - Adjust the Freq
    options.hz = options.period/options.interval
  elif (options.hz is not None):
    # Frequency was set - Adjust the interval
    options.interval = options.period/options.hz
  elif (options.period != 1.0):
    # Lastly, Perhaps Period was set and interval or Hz left at the default.  This is ambiguous!
    # ie: -P 5 and Hz = 1 and Interval = 1; should it be 5Hz and 1sec or 1Hz and 5sec??
    parser.error("Cannot set the period and not specify the frequency or interval!!")
  else:
    # Everything is at their defaults
    options.hz = 1.0
    options.interval = 1.0

  # Establish the Prefix Size
  # SEQ#, TCLASS, Length (MSB bit is TStamp flag), TS
  if (options.timestamp):
    prefix = bytearray(struct.pack('!HBHd',0,0,0,0.0))
  else:
    prefix = bytearray(struct.pack('!HBH',0,0,0))
  prefix_len = len(prefix)

  # Flow Label Stuff
  if (options.flowlabel is not None):
    try:
      import ipv6
    except ImportError as e:
      logging.critical("Flow Label Extensions not found!! Check your paths!")
      options.flowlabel=None
  
  # Additional Options Checking
  if ((options.count is not None) and (options.count <= 0)):
    parser.error("Bad number of packets to transmit.")
  if ((options.preload < 0) or (options.preload > 0xff)):
    parser.error("Bad preload value, should be 0..65536")
  if (options.only is not None):
    options.skip = []
    if (options.hz <= 1):
      parser.error("Insufficient number of transmissions in one period!  Cannot limit transmissions!")
    for s in range(1,int(options.hz)+1):
      if (s not in options.only):
        options.skip.append(s)
  if (options.skip is not None):
    if (options.hz <= 1):
      parser.error("Insufficient number of transmissions in one period!  Cannot skip transmissions!")
    for s in options.skip:
      if (s <= 0):
        parser.error("Skip values must be positive and non-zero")
      if (s > options.hz):
        parser.error("Skip value of {} is outside the number of transmissions in one period: {}".format(s,options.hz))
  # DiffServ Support
  # Table of common names to values
  _dscp_table = {}
  for dscp in range(8):
    _dscp_table["CS{}".format(dscp)]=(dscp<<3)
  for dscp in range(1,4):
    for dscpv in range(1,5):
      _dscp_table["AF{}{}".format(dscpv,dscp)]=(dscpv<<3)+(dscp<<1)
  _dscp_table["EF"]=46
  _dscp_table["BE"]=0
  if (options.tclass is not None):
    if options.tclass in _dscp_table:
      options.tclass = _dscp_table[options.tclass]
      # Shift for ECN bits
      options.tclass <<= 2
    else:
      try:
        options.tclass = any_int(options.tclass)
        if ((options.tclass < 0) or (options.tclass > 255)):
          parser.error("Traffic Class must be a value between 0 (0x00) and 255 (0xff)")
        elif ((options.tclass >= 0) and (options.tclass <= 15)):
          # Set experimental points
          options.tclass = (options.tclass<<4)+0xc
      except ArgumentTypeError:
        parser.error("Invalid DSCP code Point: {}".format(options.tclass))
        options.tclass = None
  if (options.tclass is None):
    options.tclass = 0x00
  if (options.size < prefix_len):
    parser.error("Payload size must be at least {} bytes.".format(prefix_len))
  if (options.size > _MAX_MTU):
    parser.error("Payload sizes exceeding {} bytes are not currently supported".format(_MAX_MTU))
  if (options.offset is not None):
    if (options.offset < 0):
      parser.error("Negative offsets are not supported.")
  if (options.adjust is not None):
    for adj in options.adjust:
      if (len(adj) < 2):
        logging.warn("Nothing to adjust... That's fine.  Ignoring Rule: {}".format(adj))
        options.adjust.remove(adj)
        continue
      if ((adj[0] < prefix_len) or (adj[0] > _MAX_MTU)):
        parser.error("Error in Rule {}: Payload sizes must be at least {} bytes and cannot exceed {} bytes.".format(adj,prefix_len,_MAX_MTU))
      for s in adj[1:]:
        if ((s <= 0) or (s > options.hz)):
          parser.error("Adjustment value of {} in rule {} is outside the number of transmissions in one period: {}".format(s,adj,options.hz))

  # Show all set options for Debugging output
  if (options.debug):
    print("Set Options: {}".format(options))
  
  if (options.hz < 1):
    # So as the features of the program expanded it introduced an issue when options.hz is less than 1
    # Since we don't really output this variable to the user, we are adjusting as a quick fix
    # This should allow something like "-i 5" or "-f 0.2" to be used on the command line without also setting the period
    options.hz = 1
  hz_int = int(options.hz)
  # Set the Payload
  pattern_len = len(options.pattern)
  payload_len = (options.size - prefix_len)
  # Set Globally First
  payload_ref={}
  payload = bytearray()
  if (pattern_len > 0):
    payload.extend(options.pattern*(payload_len//pattern_len))
    payload.extend(options.pattern[0:(payload_len%pattern_len)])
  else:
    payload.extend(b"\x00"*payload_len)
  for s in range(1,hz_int+1):
    payload_ref[s]=payload
  if (options.debug):
    print("PAYLOAD SIZES")
    print("DEFAULT: Prefix: {} bytes; Payload: {} bytes; Total Payload: {}".format(
        prefix_len, payload_len, (prefix_len+payload_len) ))
  # Adjust if needed
  if (options.adjust is not None):
    for adj in options.adjust:
      payload_len = (adj[0] - prefix_len)
      payload = bytearray()
      if (pattern_len > 0):
        payload.extend(options.pattern*(payload_len//pattern_len))
        payload.extend(options.pattern[0:(payload_len%pattern_len)])
      else:
        payload.extend("\x00"*payload_len)
      for s in adj[1:]:
        payload_ref[s]=payload
  if (options.debug):
    print("ALL: Tx#, Size, Payload")
    for k in payload_ref:
      print("{}, {}, {}".format(k,len(payload_ref[k]),repr(payload_ref[k])))

  if ((options.host is None) or (options.port is None)):
    # This shouldn't be possible with argparse
    parser.error("You must specify a host and port.")

  if (options.udp):
    stype = socket.SOCK_DGRAM
  else:
    stype = socket.SOCK_STREAM

  if (options.ipv4):
    sfamily = socket.AF_INET
  else:
    sfamily = socket.AF_INET6

  sock = None
  try:
    for resolve in socket.getaddrinfo(options.host, options.port, sfamily, stype):
      family, socktype, proto, canonname, sockaddr = resolve
      logging.info('Attempting to transmit to {} port {}'.format(*sockaddr))
      try:
        sock = socket.socket(family, socktype, proto)
      except socket.error as msg:
        sock = None
        logging.error('Socket Creation Error: {}'.format(msg))
        continue
      # For "Blind" UDP, we are done
      if ((options.udp) and (options.blind)):
        break
      try:
        sock.bind(('', 0))
      except socket.error as msg:
        logging.critical('Socket Binding Error: {}'.format(msg))
        sock.close()
        sock = None
        continue
      tries = 5
      while (tries > 0):
        try:
          sock.connect(sockaddr)
          tries = 0
        except socket.error as msg:
          logging.warning('Cannot connect to remote host: {}'.format(msg))
          logging.warning('Retrying in 20 seconds')
          sleep(20)
          tries -= 1
          if tries == 0:
            logging.error('Connection Failed (Max Attempts Reached): {}'.format(msg))
            sock.close()
            sock = None
            continue
      break
  except socket.error as msg:
    logging.error('Name or address resolution failed: {}'.format(msg))
  if sock is None:
    logging.critical('Fatal Error: Could not open a socket for {} on port {}'.format(options.host, options.port))
    sys.exit(1)
  if (options.udp):
    logging.info('UDP: Ready to Transmit.')
  else:
    logging.info('TCP: Connection Established.')

  # Socket Options - Set TCP_NODELAY to disable Nagle
  if (not options.udp):
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

  # IPv6 configs only
  if (not options.ipv4):
    # Setup to get TCLASS Info
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_RECVTCLASS, 1)
    # Set the TCLASS
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_TCLASS, options.tclass)

    # Set the flow label if requested
    if (options.flowlabel is not None):
      if (options.flowlabel == 0):
        sockaddr = ipv6.get_flow_label(sock,*sockaddr)
        logging.info("Using flow label {} ({}) assigned by the kernel".format(sockaddr[2],hex(sockaddr[2])))
      else:
        logging.critical('Setting the flowlabel explicitly is currently unsupported.  Sorry!  Use "0" to have the kernel assign a value.')
        cleanup()
        sys.exit(1)
  else:
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, options.tclass)
  
  # Precalculate the fixed part of the Header
  prefix_flags = 0
  if (options.timestamp):
    prefix_flags += 0x8000
  if (options.adjust is not None):
    prefix = bytearray(struct.pack('!B',options.tclass))
  else:
    prefix = bytearray(struct.pack('!BH',options.tclass,options.size+prefix_flags))

  tnow = time()
  # If offset is set, sleep to that point
  if (options.offset is not None):
    tnext = (math.ceil(tnow)+options.offset)
    sleep(tnext-tnow)
  else:
    tnext = tnow
  tx_count = 0
  skip_count = 0
  while True:
    tnow = time()
    tx_count += 1
    cycle_count = (((tx_count-1)%hz_int)+1)
    sequence_number = (((tx_count-1)%0xffff)+1)
    # Check for discrepancy against previous tnext and set a new tnext
    # tfudge will be positive if we slept too long, negative if we woke up too early
    tfudge = tnow-tnext
    tnext = round(tnow+options.interval-tfudge,6)
    if (options.debug):
      print("Time Wake: {:f}, Fudge: {:f}, Next Tx: {:f}".format(tnow, tfudge, tnext))
    tx_bytes = bytearray()
    # Pack the Sequence Number and Fixed Prefix
    tx_bytes.extend(struct.pack('!H',sequence_number))
    tx_bytes.extend(prefix)
    # Pack the Size if it is variable
    if (options.adjust is not None):
      tx_bytes.extend(struct.pack('!H',len(payload_ref[cycle_count])+prefix_len+prefix_flags))
    # Pack the Timestamp if enabled
    tnow = time()
    if (options.timestamp):
      tx_bytes.extend(struct.pack('!d',tnow))
    # Pack the remaining payload
    tx_bytes.extend(payload_ref[cycle_count])
    # See if we should skip this transmission
    if (options.skip is not None) and (cycle_count in options.skip):
      skip_count += 1
      if (options.debug):
        print("{:f}: Skip packet #{}".format(tnow, sequence_number))
    else:
      try:
        sock.sendto(tx_bytes,sockaddr)
      except socket.error as msg:
        logging.critical('Socket Transmission Error: {}'.format(msg))
        break
      if (options.debug):
        print("{:f}: Sent packet #{}".format(tnow, sequence_number))
      if (options.verbose != 0):
        # Normal Output, unless -q is used
        print("{0:f} {3} {2} Tx {1}".format(tnow,sequence_number,len(tx_bytes),hex(options.tclass)))
    # Check to see if we've reached our count
    if ((options.count is not None) and (tx_count >= options.count)):
      break
    # Update the Time
    tnow = time()
    # Go immediately to the next transmission if we are preloading
    # OR if we are somehow already past tnext!
    if ( (tnow > tnext) or (tx_count <= options.preload) ):
      # Adjust tnext
      tnext = tnow
      continue
    # Sleep till our next transmission
    if (options.debug):
      print("Time After Tx: {:f}, Sleeping for: {:f}".format(tnow, (tnext-tnow)))
    sleep(tnext - tnow)

  sock.close()
  sys.exit(0)
