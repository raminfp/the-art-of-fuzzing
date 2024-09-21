import socket
import ipv6
import atheris_no_libfuzzer as atheris
import sys

def TestOnInput(data):
	#if data:
		try:
			host = b"::1" + data
			port = 3300
			resolve = socket.getaddrinfo(host, port, socket.AF_INET6, socket.SOCK_DGRAM)
			(family, socktype, proto, _, sockaddr) = resolve[0]
			sock = socket.socket(family, socktype, proto)
			sockaddr = ipv6.get_flow_label(sock,*sockaddr)
			#print("Flow Label:",hex(sockaddr[2]))
			sock.sendto(data,sockaddr)
			return
		except RuntimeError:
			pass

atheris.Setup(sys.argv, TestOnInput)
atheris.Fuzz()




