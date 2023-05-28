#Main


#The client program handles the pygame and display attributes, wheras the server performs the game logic
#In order to display to the screen, the data must be passed from the server to the client



#Imports
#---------------------------------------
#import pygame
import threading
import socket
from Server import *
from Client import *
from Functions import *
#---------------------------------------

#Constants
#---------------------------------------
#The map size will be decided when the map is selected!
TABLE_COLUMNS=[["Achievement","AchievementID","AchievementName", "Progress", "AchievementDescription"],["Map","MapID","MapName","MapSize"],["Setting","SettingID","SettingName","SettingValue","SettingDescription"],["Building","BuildingID","BuildingName","BuildingStats","BuildingFaction"],["Unit","UnitID","UnitName", "UnitAnimations", "UnitStats", "InvalidTiles", "UnitFunctions"],["Animation","AnimationID","AnimationName","UnitID","BuildingID"]]#Used when updating the database!
#---------------------------------------


#colours
#---------------------------------------
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
#---------------------------------------


#Initialisation
#---------------------------------------
Records=Create_Database()

#pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#SCREEN_INFO=pygame.display.Info()

Settings= {#Set up settings and constants depending on the user's preferences (Default values if they haven't selected yet)
    "SCALE": int(Records[2][0][2]),#Scales all of the images used to help improve the frame-rate. A higher scale decreases the size of the images, therefore reducing the amount of memory and processing power required to output
    "WIDTH": int((int(Records[2][1][2])/100)*SCREEN_INFO.current_w),#800 #Width of the screen
    "HEIGHT": int((int(Records[2][2][2])/100)*SCREEN_INFO.current_h),#600 #Height of the screen
    "FPS": int(Records[2][3][2]),#Frame-rate of the client
    "MINI_MAP_SIZE": int(Records[2][4][2]),
    "INFO_BAR_SIZE": int(Records[2][5][2]),
    "MAX_CAMERA_SPEED": int(Records[2][6][2])
    }
#print("Initialising...")
#serverName = Server()
                    #Creates a server so that both multiplayer and single player games can be started
                    #This will be run as and when needed

clientName = Client()
                    #Creates a client so that both multiplayer and single player games can be started
                    #Loads the game window in the correct format so that everything can be displayed correctly
                    #Loads the menus so that settings can be changed and games can be started
                    #This will also load the records, so that progress towards achievements can be made whilst playing games
                    #Clients should connect to the correct server when attempting to join a game

#print("Initialisation complete")
#---------------------------------------


#Outer game loop
#---------------------------------------
#Options to be determined by the client
options={
    "Play/Quit": "Play",
    "Host/Join": "Host",
    "Host_IP": "",
    "Port": 5000,
    "No_Players": 1,
    "Map": 1,







    #Used to determine what the user selects in the menus
                    #Using integers to prevent multiple type usage
                    #[0] : Play/Quit
                    #[1] : Host/Join
                    #[2] : No. of players
                    #[3] : Map


#serverThread = threading.Thread(target=serverName.Host,args=([options]), daemon=True)

while options["Play/Quit"]="Play":

    print("Launching menus...")
    #options=clientName.Menus()
                    #displays the menus and returns the option that the user has selected
    print(options, "Options returned by the client")

    if options[0] == 1:#Play game
        
        if options[1] == 1:#Host a game
            serverThread = threading.Thread(target=serverName.Host_Game,args=([options]), daemon=True)
            serverThread.start()
            Host = serverName.Get_Host()
            Port = 5000
            #print("Connecting to server with host: " + Host + " on port: " + str(Port))

            Client = socket.socket()
            Client2 = socket.socket()
            
            #print(Client, "This is a test")
            Client.connect((Host,Port))#Localhost
            Client2.connect((Host,Port))#Localhost
            
            
            print("Waiting for server to close...")
            serverThread.join()
            print("Server closed. Returning to menus...")

        else:#Join a game
            clientName.Join(otherServer)
#---------------------------------------


