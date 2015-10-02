# Server to implement simplified Diffie-Hellman protocol and demonstrate socket
# programming in the process.
# Author: Dayton Allen

import socket
import random

def computePublicKey(g, p, s):
    """Computes a node's public key"""
    return (g**s)%p

def computeSecretKey(g, p):
	"""Computes this node's secret key"""
	secretKey = random.randint(int(g), int(p))
	return secretKey

def sendPublicKey(k):
	"""Sends node's public key"""
	status = "130 PubKey " + str(k)
	return status


HOST = 'localhost'       # Symbolic name meaning all available interfaces
PORT = 6111         # Arbitrary non-privileged port
STRHello = "100 Hello"
STRGenerator = "110 Generator"
STRGeneratorResp = "111 Generator Rcvd"
STRPrime = "120 Prime"
STRPrimeResp = "121 Prime Rcvd"
STRPubKey = "130 PubKey"
generator = 5
prime = 23

# Carry out necessary socket set up
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', PORT))
server.listen(1)
serverconnection, serveraddress = server.accept()
print('Server of Dayton J Allen')
print('Connected by', serveraddress)

while True:
    # Receive Hello message
    msg = serverconnection.recv(4096)
    print('Received from client', msg)
	# Handle case of invalid message.
    if not msg:
        break
	# Handle case of valid Hello message
    serverconnection.send(STRHello.encode())
	# Handle case of valid generator message
    generatorresponse = serverconnection.recv(4096)
    print('Received from client', generatorresponse)
    serverconnection.send(STRGeneratorResp.encode())
	# Handle case of valid prime message
    primeresponse = serverconnection.recv(4096)
    print('Received from client', primeresponse)
    serverconnection.send(STRPrimeResp.encode())
	# Handle case of valid public key message
    skey = computeSecretKey(generator, prime)
    publickey = computePublicKey(generator, prime, skey)

    ckey = serverconnection.recv(4096)
    print('Received from client', ckey)
    clientkey = str(ckey)[-3:-1]
    print('Generator:', generator)
    print('Prime:', prime)
    print('Public Key', publickey)
    print("Client's Public Key", clientkey)
    print('Private Key:', skey)

    serverconnection.send(sendPublicKey(publickey).encode())
# Close connection.
serverconnection.close()
