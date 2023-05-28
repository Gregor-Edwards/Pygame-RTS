#Client

#Imports
#---------------------------------------
#import pygame
import socket
#---------------------------------------

class Client():


    def __init__(self):
        """Client that should be able to connect and disconnect to differenc connections without requiring any additional setup"""

        #Socket specifics
        self.__Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#AF_INET family uses Ipv4 addresses (rather than Ipv6 etc.) which is the address assigned to the current device by the router
        self.__HOST_IP = "localhost"#Here, the Host is an input IP address which corresponds to the device on the network in which the server is being run
        self.__PORT = 5000#The port must be above 1024


        #The following must be the same between both the server and the client
        self.__HEADER = 64#This will be the length of the header message (in bytes) that each client will send to the server to determine the length of the message to be transmitted
        self.__FORMAT = 'utf-8'#This is the format by which each message from the client will be decoded
        self.__DISCONNECT_MESSAGE = "!DISCONNECT"#If this message is received by the server during the handling of a client, then the client will be cleanly disconnected from the server
        #All of the socket specifics are constants once selected

        
        print("Client initialised!")

        
    #Getters and Setters
    #-------------------------------------------
    def get_host(self):
        return self.__HOST_IP

    def set_host(self,Host):
        print("Setting host to: ", Host)
        self.__HOST_IP = Host

    def get_port(self):
        return self.__PORT

    def set_port(self,Port):
        if Port > 1024:
            print("Setting port to: ", Port)
            self.__PORT = Port
        else:
            print("Invalid port number!")
            return
    #-------------------------------------------


    #Socket handling functions
    #-------------------------------------------
    def connect(self):
        print("Connecting to: " + self.__HOST_IP + " with port: " + str(self.__PORT))
        self.__Client.connect((self.__HOST_IP, self.__PORT))
        print("The client has been initialised and connected to server with IP" + self.__HOST_IP + "on port" + str(self.__PORT))


    def send(self,data):
        #encode the message, then send the length of the message along with the data itself
        message = data.encode(self.__FORMAT)
        length = str(len(message)).encode(self.__FORMAT)
        length += b' ' * (self.__HEADER - len(length))
        self.__Client.send(length)
        self.__Client.send(message)
    
    def receive(self):
        length = self.__Client.recv(self.__HEADER).decode(self.__FORMAT)#This will wait until the client has sent the number of bytes specified
        if length:#Ensures that the message is valid.
            #In addition, the first message received will be blank, since a blank message is sent when the client connects to the server
            length = int(length)
            data = self.__Client.recv(length).decode(self.__FORMAT)
            print("Data from server: ", data)
            if data == self.__DISCONNECT_MESSAGE:
                connected = False
            else:
                #Handle the data received
                print("Handling data from the server...")

    def reset_client(self):#May not be required
        self.__Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #-------------------------------------------  
        


