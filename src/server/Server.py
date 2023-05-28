#Server

#Imports
#---------------------------------------
import socket
import threading
#---------------------------------------

class Server():


    def __init__(self,Port,MaxConnections,Online):
        """Pre-condition: The Port number must be above 1024"""

        #Socket specifics
        self.__Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#AF_INET family uses Ipv4 addresses (rather than Ipv6 etc.) which is the address assigned to the current device by the router
        if Online:
            self.__IP = socket.gethostbyname(socket.gethostname())#Gets the IP address of the current device
        else:
            self.__IP = "localhost"
        
        #This allows connections across the local network
        #If this is required to run across the internet instead, then the IP should be eplaced by the public IP adress of the device running the server

        self.__PORT = Port#The port must be above 1024
        self.__MAXCONNECTIONS = MaxConnections
        
        #The following must be the same between both the server and the client
        self.__HEADER = 64#This will be the length of the header message (in bytes) that each client will send to the server to determine the length of the message to be transmitted
        self.__FORMAT = 'utf-8'#This is the format by which 5each message from the client will be decoded
        self.__DISCONNECT_MESSAGE = "!DISCONNECT"#If this message is received by the server during the handling of a client, then the client will be cleanly disconnected from the server
        #All of the server specifics are constants once selected

        #Game specifics
        self.__Teams = []#Used to store the connections and addresses of each client
        self.__Threads = []#Used to handle each clients thread on the server side
        self.__Data = []#Used to store the data received by each client in order to correctly update the game state




        
        self.__Server.bind((self.__IP, self.__PORT))#'' can be replaced with the client IP address
        print("The server is initialised with IP " + self.__IP + " and port " + str(self.__PORT))
    


    def get_ip(self):
        return self.__IP
    
    def get_port(self):
        return self.__PORT




    def handle_client(self,conn,address):
        print("Now handling client with conn:", conn, "and address:", address)

        #Game loop
        connected = True
        while connected:
            #Receive data from the client
            #ADD A TIMEOUT HERE!!!
            length = conn.recv(self.__HEADER).decode(self.__FORMAT)#This will wait until the client has sent the number of bytes specified
            if length:#Ensures that the message is valid.
                #In addition, the first message received will be blank, since a blank message is sent when the client connects to the server
                length = int(length)
                data = conn.recv(length).decode(self.__FORMAT)
                print("Data from client:", conn, ": ", data)
                if data == self.__DISCONNECT_MESSAGE:
                    connected = False
                else:
                    #Handle the data received
                    pass

        #Disconnect the client from the server
        conn.close()


    def start(self):
        
        #Listen and accept connections from clients
        self.__Server.listen(self.__MAXCONNECTIONS)
        print("Server is listening on IP: ", self.__IP)
        while len(self.__Teams)<self.__MAXCONNECTIONS:#This enables a certain number of connections to occur, and waits until this number of connections occurs before running the threads
            #If you need to run an indefinite number of clients, replace the above with while True: and run the threads within the while loop
            conn, address = self.__Server.accept()
            self.__Teams.append([conn,address])
            print("Connection from: " + str(address))
            print(len(self.__Teams), self.__MAXCONNECTIONS)
            

        #Handle each client in a separate thread to avoid waiting on a slow client
        for x in range(len(self.__Teams)):
            thread = threading.Thread(target=self.handle_client, args=(self.__Teams[x][0],self.__Teams[x][1]))#(conn,address)
            self.__Threads.append(thread)
            thread.start()

        #Close the server after all clients have been handled
        for x in range(len(self.__Threads)):
            self.__Threads[x].join()

        #EXTRA CODE TO CLOSE THE SERVER!!!

        print("Closing server...")
        self.__Server.close()
        del self#Remove the server object that has been created
        


#TESTING!!!

#server1 = Server(5000,2)
#server1.start()








##    def Host_Game(self):
##        #self.Get_Host()
##        
##        self.__Server.listen(self.__MaxConnections)#Listen and accept connections from clients
##        print("The server has been started with IP" + self.__IP + "and port" + str(self.__Port))
##        print("The server is now listening for a connection")
##        
##        while len(self.__Teams)<self.__MaxConnections:
##            conn, address = self.__Server.accept()
##            print(len(self.__Teams))
##            self.__Teams.append(conn)
##            print("NEW LENGTH OF TEAMS: " + str(len(self.__Teams)))
##            print("Connection from: " + str(address))
##
##
##        #Send_Map_Data(options[3])#Send the correct map data to all connections in self.__Teams
##
##        #Play Game
##        running = True
##        while running:
##            
##
##        print("Closing all connections...")
##        for conn in self.__Teams:
##            print(conn)
##            #print(address)
##            conn.close
##
##        self.__Teams = []
##
##        print("Closing server...")
##        self.__Server.close()
