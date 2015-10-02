# Client to implement simplified Diffie-Hellman protocol and demonstrate socket
# programming in the process.
# Author: Dayton Allen

import socket
import math
import random

def IsValidGenerator(g, p):
    """Validation of generator and prime"""
    x = set()
    for i in range(1,p): #to iterate on the powers of the generator modulo p
    	x.add((g**i)%p)
    #print ", ".join(str(e) for e in x)
    if (len(x) == (p-1)) and (g < p):
    	return True
    else:
        return False

def serverHello():
    """Sends server hello message"""
    status = "100 Hello"
    return status

def sendGenerator(g):
    """Sends server generator"""
    status = "110 Generator " + str(g)
    return status

def sendPrime(p):
    """Sends server generator"""
    status = "120 Prime " + str(p)
    return status

def computeSecretKey(g, p):
	"""Computes this node's secret key"""
	secretKey = random.randint(int(g), int(p))
	return secretKey

def computePublicKey(g, p, s):
    """Computes a node's public key"""
    return (g**s)%p

def sendPublicKey(k):
	"""Sends node's public key"""
	status = "130 PubKey " + str(k)
	return status

# M   = message, an integer
# s   = sender's secret key, an integer
# Pub = receiver's public key, an integer
# p   = prime number, an integer
def encryptMsg(M, s, Pub, p):
	"""Encrypts a message M given parameters above"""
	return M*((Pub**s)% p)

# C   = ciphertext, an integer
# s   = receiver's secret key, an integer
# Pub = sender's public key, an integer
# p   = prime number, an integer
def decryptMsg(C, s, Pub, p):
	"""Encrypts a message M given parameters above"""
	return C/((Pub**s)% p)


def main():
    """Driver function for the project"""
    serverHost = 'localhost'        # The remote host
    serverPort = 6111            # The same port as used by the server
    while (True):
    	prime = int(input('Enter a valid prime between 7 and 101: '))
    	generator = int(input('Enter a positive integer less than the prime just entered: '))
    	if (IsValidGenerator(int(generator), int(prime))):
            # Create socket
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect socket
            client.connect((serverHost, serverPort))
            msg = serverHello()
            # Send msg to server
            client.send(serverHello().encode())
            # Receive server's response to Hello message
            response = client.recv(4096)
            # Handle case of invalid response to Hello message
            if not response:
                print("Invalid response received from server")
            else:
        	    # Handle case of valid response to Hello message
                print("Server Response:", str(response))
        	# Send generator to server.
            client.send(sendGenerator(generator).encode())
        	# Handle case of invalid response to generator message

        	# Handle valid response to generator message
            response = client.recv(4096)
            print("Server Response:", str(response))

        	# Send prime to server.
            client.send(sendPrime(prime).encode())
        	# Handle case of invalid response to prime message

            # Handle valid response to prime message
            response = client.recv(4096)
            print("Server Response:", str(response))
        	# Compute secret key
            secretkey = computeSecretKey(generator, prime)
        	# Compute public key
            publickey = computePublicKey(generator, prime, secretkey)
        	# Send public key to server
            client.send(str(sendPublicKey(publickey)).encode())
        	# Handle invalid response to public key message

        	# Handle valid response to public key message.
            skey = client.recv(4096)
            serverkey = str(skey)[-3:-1]
        	# Print keys to standard output
            print('Generator:', generator)
            print('Prime:', prime)
            print('Public Key', publickey)
            print("Server's Public Key", serverkey)
            print('Private Key:', secretkey)
        	# Close connection
            client.close()
if __name__ == "__main__":
    main()
#TODO: Document code. Server displays accepted client messages. Rest of shitz on paper
