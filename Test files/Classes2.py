import pygame
import os
import re
from Functions import *
import socket
import threading


#----------------------------------------------------------
class Game():

    def __init__(self,Player,Settings,Records):
        
        #Initialise pygame
        #---------------------------------------
        pygame.init()#initialises pygame
        pygame.mixer.init()#initialises sound
        #---------------------------------------

        #Set the settings
        #---------------------------------------
        self.__Font = pygame.font.SysFont('arial',22)
        self.__Menu_Text=[ [["Start",1],["Quit",-3]] , [["Play game",2],["Achievements",9],["Settings",10],["Go back",0]] , [["Controls",3],["Tutorials",4],["Single player",6],["Multiplayer",7],["Go back",1]] , [["Controls: 1. 2. 3. etc. left click to return...",2]] , [["Tutorial 1.",2],["Tutorial 2.",2],["Tutorial 3. ...",2],["Go back",2]] , [["Faction x",6],["Go back",2]] , [["Level 1",-3],["Change faction",5],["Go back",2]], [["Host game",-3],["Join game",-3],["Change faction",5], ["Go back",2]] , [["THIS IS A TEST MENU!!!",0]] , [["THIS IS A PLACEHOLDER MENU!!!",0]] , [["THIS IS A PLACEHOLDER MENU!!!",0]] ]
        
        Return=Set_Settings(Settings)
        self.__Settings=Return[2]
        #print(self.__Settings, "SETTINGS!!!")
        self.__SCREEN=Return[0]
        self.__CAMERA_VIEW=Return[1]#pygame.surface.Surface((Settings["WIDTH"]//Settings["SCALE"],Settings["HEIGHT"]//Settings["SCALE"]))
        #Used to speed up drawing to screen!
        #---------------------------------------

        #Load normal menus
        #---------------------------------------
        self.__Menus=[0,1,2,3,4,5,6,7,8]
        for x in range(len(self.__Menus)):
            self.__Menus[x]=pygame.surface.Surface((Settings["WIDTH"],Settings["HEIGHT"])).convert_alpha()
            self.__Menus[x].fill((0,0,0,0))#Completely transparent
            
            #Place the options either in the center of the screen or at either side of the screen!
            if len(self.__Menu_Text[x])<=4:
                for y in range(len(self.__Menu_Text[x])):
                    Text = self.__Font.render(self.__Menu_Text[x][y][0],True, (255,255,255))
                    self.__Menus[x].fill((50,50,50,150),pygame.Rect(int((Settings["WIDTH"]*3/8)),int((Settings["HEIGHT"]*(((2*y)+1)/8)))-int(Settings["HEIGHT"]/16),int(Settings["WIDTH"]/4),int(Settings["HEIGHT"]/8)))
                    self.__Menus[x].blit(Text,(int((Settings["WIDTH"]*3/8)),int((Settings["HEIGHT"]*(((2*y)+1)/8)))))#Write menu text!!!
            
            elif len(self.__Menu_Text[x])in range(5,9):#between 4 and 8 options
                for y in range(len(self.__Menu_Text[x])):
                    Text = self.__Font.render(self.__Menu_Text[x][y][0],True, (255,255,255))
                    if y <4:#includes 0!
                        self.__Menus[x].fill((50,50,50,150),pygame.Rect(int((Settings["WIDTH"]*1/8)),int((Settings["HEIGHT"]*(((2*y)+1)/8)))-int(Settings["HEIGHT"]/16),int(Settings["WIDTH"]/4),int(Settings["HEIGHT"]/8)))
                        self.__Menus[x].blit(Text,(int((Settings["WIDTH"]*1/8)),int((Settings["HEIGHT"]*(((2*y)+1)/8)))))#Write menu text!!!

                    else:
                        self.__Menus[x].fill((50,50,50,150),pygame.Rect(int((Settings["WIDTH"]*5/8)),int((Settings["HEIGHT"]*(((2*(y-4))+1)/8)))-int(Settings["HEIGHT"]/16),int(Settings["WIDTH"]/4),int(Settings["HEIGHT"]/8)))
                        self.__Menus[x].blit(Text,(int((Settings["WIDTH"]*5/8)),int((Settings["HEIGHT"]*(((2*(y-4))+1)/8)))))#Write menu text!!!

            else:
                print("Not allowed that many options!!!")
        #---------------------------------------

        #Load Achievements Menu
        #---------------------------------------
        self.__Menus.append(pygame.surface.Surface((Settings["WIDTH"],Settings["HEIGHT"])).convert_alpha())
        self.__Menus[len(self.__Menus)-1].fill((235,195,0,255))#Used to check if all achievements have been unlocked!

        for x in range(len(Records[0])):#Load all achievements (MAX 11!!!)
            Text=self.__Font.render(Records[0][x][1],True, (255,255,255))#Achievement name
            #Regular expressions! These will be used to check the progress, since string slicing wouldn't work with both 1/100 AND 10/100!!!
            Match=re.match(r"^([0-9]*)/([0-9]*)$",Records[0][x][2])#Should return 2 groups in the structure: Current progress/Required progress

            if Match.groups()[0]==Match.groups()[1]:#Green background on the achievement!
                self.__Menus[len(self.__Menus)-1].fill((0,255,0,255),pygame.Rect(int((Settings["WIDTH"]*(2*(x%3)+1)/6))-int(Settings["WIDTH"]/12),int((Settings["HEIGHT"]*(2*(x//3)+1)/8))-int(Settings["HEIGHT"]/16),int(Settings["WIDTH"]/6),int(Settings["HEIGHT"]/8)))
                
            else:#Grey background on achievement and transparent background for the menu
                self.__Menus[len(self.__Menus)-1].fill((192,192,192,255))#If any achievements haven't been collected yet

                self.__Menus[len(self.__Menus)-1].fill((100,100,100,255),pygame.Rect(int((Settings["WIDTH"]*(2*(x%3)+1)/6))-int(Settings["WIDTH"]/12),int((Settings["HEIGHT"]*(2*(x//3)+1)/8)),int(Settings["WIDTH"]/6),int(Settings["HEIGHT"]/8)))

            #Display text
            self.__Menus[len(self.__Menus)-1].blit(Text,(int((Settings["WIDTH"]*(2*(x%3)+1)/6))-int(Settings["WIDTH"]/12),int((Settings["HEIGHT"]*(2*(x//3)+1)/8))))

            #for y in range(2,4):#2-3#REMOVE
            Text=self.__Font.render(Records[0][x][2],True, (255,255,255))#The rest of the info in the SQL table
            self.__Menus[len(self.__Menus)-1].blit(Text,(int((Settings["WIDTH"]*(2*(x%3)+1)/6))-int(Settings["WIDTH"]/12),int((Settings["HEIGHT"]*(2*(x//3)+1)/8))+(10*y)))
         
        #---------------------------------------

        #Load Settings Menu
        #---------------------------------------
        #for x in range(2):#FIX!!!
        self.__Menus.append(pygame.surface.Surface((Settings["WIDTH"],Settings["HEIGHT"])).convert_alpha())
        self.__Menus[len(self.__Menus)-1].fill((0,0,255,255))

        for x in range(len(Records[2])):#Settings
            self.__Menus[len(self.__Menus)-1].fill((100,100,100,255),pygame.Rect(int((Settings["WIDTH"]*(2*(x%3)+1)/6))-int(Settings["WIDTH"]/12),int((Settings["HEIGHT"]*(2*(x//3)+1)/8)),int(Settings["WIDTH"]/6),int(Settings["HEIGHT"]/8)))

            Text=self.__Font.render(Records[2][x][1],True, (255,255,255))#The setting name
            self.__Menus[len(self.__Menus)-1].blit(Text,(int((Settings["WIDTH"]*(2*(x%3)+1)/6))-int(Settings["WIDTH"]/12),int((Settings["HEIGHT"]*(2*(x//3)+1)/8))))

        #---------------------------------------

        for x in range(1,3):#1-2 #Both menus require a "go back" button
            Text=self.__Font.render("Go back",True, (255,255,255))#Go back button
            self.__Menus[len(self.__Menus)-x].fill((100,100,100,255),pygame.Rect(int(Settings["WIDTH"]*(5/6))-int(Settings["WIDTH"]/12),int(Settings["HEIGHT"]*(7/8))-int(Settings["HEIGHT"]/16),int(Settings["WIDTH"]/6),int(Settings["HEIGHT"]/8)))
            self.__Menus[len(self.__Menus)-x].blit(Text,(int(Settings["WIDTH"]*(5/6))-int(Settings["WIDTH"]/12),int(Settings["HEIGHT"]*(7/8))-int(Settings["HEIGHT"]/16)))

        #print(Records)
        #---------------------------------------





        #Setup the Sub-screen and layers#This should be done when loading the map!!!
        #---------------------------------------
        self.__SUBSCREEN=pygame.surface.Surface((SIZE[0],SIZE[1]))#The size will depend on the map!
        
        #self.__FOG_LAYER=pygame.surface.Surface((SIZE[0],SIZE[1]))#This if done for each camera
        #self.__FOG_LAYER.set_colorkey((0,0,0))
        
        self.__SPRITE_LAYER=pygame.surface.Surface((SIZE[0],SIZE[1]))
        self.__SPRITE_LAYER.set_colorkey((0,0,0))
        
        #---------------------------------------

        #Initialise the map with animations!
        #---------------------------------------
        #8 surfaces (1 per frame)
        self.__Surfaces=[pygame.surface.Surface((SIZE[0],SIZE[1]))]
        #self.__Surfaces=[pygame.surface.Surface((SIZE[0],SIZE[1])),pygame.surface.Surface((SIZE[0],SIZE[1])),pygame.surface.Surface((SIZE[0],SIZE[1])),pygame.surface.Surface((SIZE[0],SIZE[1])),pygame.surface.Surface((SIZE[0],SIZE[1])),pygame.surface.Surface((SIZE[0],SIZE[1])),pygame.surface.Surface((SIZE[0],SIZE[1])),pygame.surface.Surface((SIZE[0],SIZE[1]))]
        #---------------------------------------
                              
        pygame.display.set_caption("Game_Name")#name at the top of the window
        self.__CLOCK=pygame.time.Clock()#clock#This will be done on the server
        #---------------------------------------
        
        #Testing stuff
        #---------------------------------------
        
        #Load the animations used in the game
        #---------------------------------------
        self.__IMAGES=[]
        #for x in range(len(Records[5])):
        for y in range(6):
            #First \ in \\ is an escape character
            Str="\\"#FIX for different operating systems!!!
            #print(Str)
            Path="img"+Str+str(y)+".jpg"#Use a standard image type!!!
            Path=str(Path)
            #print(Path)
            self.__IMAGES.append(pygame.transform.scale(pygame.image.load(os.path.join(Path)).convert_alpha(),[5,5]))#.convert_alpha())
        #print(IMAGES, "IMAGES")
        #--------------------------------------------

        #Tiles used for the maps
        #---------------------------------------
        self.__TILES=[]
        for y in range(254):#Precondition - Assuming only 254 max tiles so that the information of the tile number can be converted to bytes (0,253) #not (0,255) because the values 254 and 255 are used to signify the end of a row or frame!!!
            Str="\\"#FIX for different operating systems!!!
            Str2=""
            if y<100:
                Str2="0"
                if y<10:
                    Str2="00"
            Str2=Str2+str(y)
            Path="tiles"+Str+"tile"+Str2+".png"
            Path=str(Path)
            #print(Path)
            self.__TILES.append(pygame.transform.scale(pygame.image.load(os.path.join(Path)).convert_alpha(),[20,20]))#.convert_alpha())
        #print(self.__TILES, "TILES")
        #--------------------------------------------




        self.__Sprites=[pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group()]#List of [pygame.sprite.Group(),...] for each player that joins!
        self.__All_Sprites=pygame.sprite.Group()
        
        #List for Camera: [[Location_X,Location_Y],[Speed_X,Speed_Y],Accel]
        #self.Add_Camera(Camera([[0,0],[0,0],.2]))This will be done when the game is run!
        #Stats -->                                                                          #Stats [Speed,Range,Attack,Defence,Health,Exp,...]
        #Complete List: [Location,[Size_X,Size_Y],[Mode/control],Rect,State,Animations,Level,Stats,Team,UnitID,Visible]
                                                    #Mode: 2=Selected, 1=Display Info (and Selected), 0=None #Used by the camera!
                                                    #Control:2=CPU player 1=Player, 0=CPU(Automatic/default)
        #---------------------------------------

        #Automatically load the menus
        #---------------------------------------
        print("Starting menus!!!")
        #self.Menus(0,(0,0),[0],[0],0) #Doing this would eventually cause a recursion error!
        #---------------------------------------

    def Check(self):
        #---------------------------------------
        #print("CHECKING STUFF!!!")
        for event in pygame.event.get():
            
            #check for closing window
            if event.type==pygame.QUIT:
                return False
        
        #---------------------------------------


    def Add_Sprite(self,Sprite):
        #print(Sprite)
        #print(self.__Sprites[Team])
        #self.__Sprites[Team].add(Sprite)
        self.__All_Sprites.add(Sprite)

    def Menus(self, Menu,Mouse_Pos,Mouse_State,Previous_Mouse_State,Frame):#Prevent the menus from immediately changing if the mouse is not lifted
        Choice=""
        Menu=0
        while Choice!="Quit" and self.Check()!=False:
            #print("Menu = ", Menu, "Mouse_State = ", Mouse_State[0], "Previous mouse state = ", Previous_Mouse_State[0], "Mouse_Pos = ", Mouse_Pos)
            #print(Mouse_Pos[0], Mouse_Pos[1])

            self.__SCREEN.fill((RED))#Place start screen here!!! E.G. blit self.__Menus[9]
            self.__SCREEN.blit(pygame.transform.scale(self.__Menus[Menu],(Settings["WIDTH"],Settings["HEIGHT"])),(0,0))#Menu options

            #Achievements menu
            #---------------------------------------
            if Menu==9:
                print(Choice, "CHOICE!!!")
                if (Choice!="Go Back" and Choice!="Achievements"):#display the detailed achievement
                    self.__SCREEN.fill((50,50,50,50))
                    self.__SCREEN.fill((100,100,100,255),pygame.Rect(int(Settings["WIDTH"]/4),int(Settings["HEIGHT"]/3),Settings["WIDTH"]//2,Settings["HEIGHT"]//3))

                    for x in range(3):
                        print(Records[0][0][x+1])
                        Text=self.__Font.render(Records[0][Choice][x+1],True, (255,255,255))
                        self.__SCREEN.blit(Text,(int(Settings["WIDTH"]/4)+10,int(Settings["HEIGHT"]/3)+(50*x)+(50*(x//2))))

                    #progress bar
                    self.__SCREEN.fill((50,50,50,50),pygame.Rect(int(Settings["WIDTH"]/4)+10,int(Settings["HEIGHT"]/3)+100,Settings["WIDTH"]//3,Settings["HEIGHT"]//16))
                    Progression=Records[0][0][2].split("/")#used to make the progress bar
                    #print(Progression)
                    Division=int(Progression[0])//int(Progression[1])
                    #print(Division)
                    self.__SCREEN.fill((0,255,0,50),pygame.Rect(int(Settings["WIDTH"]/4)+11,int(Settings["HEIGHT"]/3)+101,(Division*((Settings["WIDTH"]//3)-1))-1,(Settings["HEIGHT"]//16)-2))
                    self.__SCREEN.fill((255,0,0,50),pygame.Rect(int(Settings["WIDTH"]/4)+11+(Division*((Settings["WIDTH"]//4)-1)),int(Settings["HEIGHT"]/3)+101,((1-Division)*((Settings["WIDTH"]//3)-1))-1,(Settings["HEIGHT"]//16)-2))
                      

                    if (Mouse_State[0]==1 and Previous_Mouse_State[0]==0) and not ((Mouse_Pos[0] in range(int(Settings["WIDTH"]/4),int(Settings["WIDTH"]*3/4)) and Mouse_Pos[1] in range(int(Settings["HEIGHT"]/3),int(Settings["HEIGHT"]*2/3)))):
                        Choice="Achievements"#Return to Achievement Menu!
                        

                elif Mouse_State[0]==1 and Previous_Mouse_State[0]==0:#Get choice from player
                    for x in range(len(Records[0])):
                        if Mouse_Pos[0] in range(int((Settings["WIDTH"]*(2*(x%3)+1)/6))-int(Settings["WIDTH"]/12),int((Settings["WIDTH"]*(2*(x%3)+1)/6))+int(Settings["WIDTH"]/12)) and Mouse_Pos[1] in range(int((Settings["HEIGHT"]*(2*(x//3)+1)/8)),int((Settings["HEIGHT"]*(2*(x//3)+1)/8))+int(Settings["HEIGHT"]/8)):
                            Choice=x
                            print(Choice, "CHOICE!!!")
                    if Mouse_Pos[0] in range(int((Settings["WIDTH"]*(2*(11%3)+1)/6))-int(Settings["WIDTH"]/12),int((Settings["WIDTH"]*(2*(11%3)+1)/6))+int(Settings["WIDTH"]/12)) and Mouse_Pos[1] in range(int((Settings["HEIGHT"]*(2*(11//3)+1)/8))-int(Settings["HEIGHT"]/16),int((Settings["HEIGHT"]*(2*(11//3)+1)/8))+int(Settings["HEIGHT"]/16)):
                        Menu=1

                    #print("HI")
            #---------------------------------------
                    
            #Settings menu
            #---------------------------------------
            elif Menu==10:
                print(Choice, "CHOICE!!!")
                if (Choice!="Go Back" and Choice!="Settings"):#display the detailed achievement
                    self.__SCREEN.fill((50,50,50,50))
                    self.__SCREEN.fill((100,100,100,255),pygame.Rect(int(Settings["WIDTH"]/4),int(Settings["HEIGHT"]/3),Settings["WIDTH"]//2,Settings["HEIGHT"]//3))

                    for x in range(3):
                        Text=self.__Font.render(Records[2][Choice][x+1],True, (255,255,255))
                        self.__SCREEN.blit(Text,(int(Settings["WIDTH"]/4)+10,int(Settings["HEIGHT"]/3)+(50*x)+(50*(x//2))))

                    #slider bar
                    self.__SCREEN.fill((50,50,50,50),pygame.Rect(int(Settings["WIDTH"]/4)+10,int(Settings["HEIGHT"]/3)+100,(Settings["WIDTH"]//3)+20,Settings["HEIGHT"]//16))
                    self.__SCREEN.fill((100,100,100,50),pygame.Rect(int(Settings["WIDTH"]/4)+11,int(Settings["HEIGHT"]/3)+101,(Settings["WIDTH"]//3)+18,(Settings["HEIGHT"]//16)-2))#+20 to width to fit the bar itself without clipping

                    Division=int(Records[2][Choice][2])/100#%of maximum value. The absolute value will be implemented as a multiplication of this %
                    self.__SCREEN.fill((150,150,150,50),pygame.Rect(int(Settings["WIDTH"]/4)+11+int(Division*((Settings["WIDTH"]//3)-2)),int(Settings["HEIGHT"]/3)+101,20,(Settings["HEIGHT"]//16)-2))

                    if (Mouse_State[0]==1):
                        #print(Previous_Mouse_Pos,Previous_Mouse_State[0],int(WIDTH/4)+11+int(Division*((WIDTH//4)-1)))

                        
                        if Previous_Mouse_State[0]==0 and not ((Mouse_Pos[0] in range(int(Settings["WIDTH"]/4),int(Settings["WIDTH"]*3/4)) and Mouse_Pos[1] in range(int(Settings["HEIGHT"]/3),int(Settings["HEIGHT"]*2/3)))):
                            Choice="Settings"#Return to Settings Menu!

                        #Alter the chosen setting
                        elif ( (Previous_Mouse_Pos[0] in range(int(Settings["WIDTH"]/4)+11),int(Settings["WIDTH"]/4)+11+((Settings["WIDTH"]//4)+19) and (Previous_Mouse_Pos[1] in range(int(Settings["HEIGHT"]/3)+101,int(Settings["HEIGHT"]/3)+101+(Settings["HEIGHT"]//16)-2)))):
                            #print(Mouse_Pos[0]-(int(WIDTH/4)+11)/((WIDTH//3)+8))
                            #print(int(100*(Mouse_Pos[0]-(int(WIDTH/4)+11))//((WIDTH//3)+8)))


                            Records[2][Choice][2]=str(int(100*(Mouse_Pos[0]-(int(Settings["WIDTH"]/4)+11))//((Settings["WIDTH"]//3)+8)))
                            if int(Records[2][Choice][2])<0:
                                Records[2][Choice][2]="0"
                            elif int(Records[2][Choice][2])>100:
                                Records[2][Choice][2]="100"

                      

                elif Mouse_State[0]==1 and Previous_Mouse_State[0]==0:#Get choice from player
                    for x in range(len(Records[2])):
                        if Mouse_Pos[0] in range(int((Settings["WIDTH"]*(2*(x%3)+1)/6))-int(Settings["WIDTH"]/12),int((Settings["WIDTH"]*(2*(x%3)+1)/6))+int(Settings["WIDTH"]/12)) and Mouse_Pos[1] in range(int((Settings["HEIGHT"]*(2*(x//3)+1)/8)),int((Settings["HEIGHT"]*(2*(x//3)+1)/8))+int(Settings["HEIGHT"]/8)):
                            Choice=x
                            print(Choice, "CHOICE!!!")
                    if Mouse_Pos[0] in range(int((Settings["WIDTH"]*(2*(11%3)+1)/6))-int(Settings["WIDTH"]/12),int((Settings["WIDTH"]*(2*(11%3)+1)/6))+int(Settings["WIDTH"]/12)) and Mouse_Pos[1] in range(int((Settings["HEIGHT"]*(2*(11//3)+1)/8))-int(Settings["HEIGHT"]/16),int((Settings["HEIGHT"]*(2*(11//3)+1)/8))+int(Settings["HEIGHT"]/16)):
                        Menu=1
                        Return=Set_Settings(self.__Settings)#Change the settings upon leaving the menu!
                        self.__CAMERA_VIEW=Return[1]
                        self.__Settings=Return[2]
            #---------------------------------------
                    
            #Normal menus
            #---------------------------------------
            elif Mouse_State[0]==1 and Previous_Mouse_State[0]==0:#Left click which has not been held
                print("LEFT CLICK!!!")
                
                #Get choice from player
                #------------------------------------------
                print(self.__Menu_Text[Menu])
                print(self.__Menu_Text)
                print("NOW IN MENU:", Menu)
                if Menu=="Achievements!":
                    print("HI")
                    
                elif len(self.__Menu_Text[Menu])<=4:
                    for x in range(len(self.__Menu_Text[Menu])):#Make reusable to improve ability to debug and maintain!

                        if Mouse_Pos[0] in range(int((Settings["WIDTH"]*3/8)),int((Settings["WIDTH"]*3/8)+(Settings["WIDTH"]/4))) and Mouse_Pos[1] in range(int((Settings["HEIGHT"]*(((2*x)+1)/8))-(Settings["HEIGHT"]/16)),int((Settings["HEIGHT"]*(((2*x)+1)/8))+(Settings["HEIGHT"]/16))):
                            Choice=self.__Menu_Text[Menu][x][0]
                            Menu=self.__Menu_Text[Menu][x][1]
                            
                elif len(self.__Menu_Text[Menu]) in range(5,9):
                    for x in range(len(self.__Menu_Text[Menu])):

                        if x<4:#includes 0!
                            if Mouse_Pos[0] in range(int((Settings["WIDTH"]*1/8)),int((Settings["WIDTH"]*1/8)+(Settings["WIDTH"]/4))) and Mouse_Pos[1] in range(int((Settings["HEIGHT"]*(((2*x)+1)/8))-(Settings["HEIGHT"]/16)),int((Settings["HEIGHT"]*(((2*x)+1)/8))+(Settings["HEIGHT"]/16))):
                                Choice=self.__Menu_Text[Menu][x][0]
                                Menu=self.__Menu_Text[Menu][x][1]
                        else:
                            if Mouse_Pos[0] in range(int((Settings["WIDTH"]*5/8)),int((Settings["WIDTH"]*5/8)+(Settings["WIDTH"]/4))) and Mouse_Pos[1] in range(int((Settings["HEIGHT"]*(((2*(x-4))+1)/8))-(Settings["HEIGHT"]/16)),int((Settings["HEIGHT"]*(((2*(x-4))+1)/8))+(Settings["HEIGHT"]/16))):
                                Choice=self.__Menu_Text[Menu][x][0]
                                Menu=self.__Menu_Text[Menu][x][1]

                print("Changing to menu:", Menu)
                #------------------------------------------

                #Start a particular game based upon the user's choices
                #------------------------------------------
                print(Choice)
                if len(Choice)>6:
                    print(Choice[:5], "CHOICE!!!")
                    if Choice[:5] == "Level":
                        print("YAY")
                        Level=int(Choice[6:])
                        self.Run(Level, 1,-1,True)#Parameters: (Level, No_Of_Players,Map)                        
                #------------------------------------------
            
            #---------------------------------------
                        
            pygame.display.flip()
            
            Previous_Mouse_State=Mouse_State
            Previous_Mouse_Pos=Mouse_Pos
            Mouse_Pos=pygame.mouse.get_pos()
            Mouse_State=pygame.mouse.get_pressed()

        #Update the database of settings/Achievements etc. then close the program
        Update_Database(Records,TABLE_COLUMNS)
        self.Quit()#This will happen if the choice is to quit or if the window is closed!

    def Server(self,Map,Level,Players,Records):#This will be run as a thread
        
        #Create the server and bind the host address and port together
        #------------------------------------------
        Host = 'localhost'#socket.gethostname()
        Port = 5000  #The port must be above 1024

        Server = socket.socket()
        Server.bind((Host, Port))
        #------------------------------------------

        #Load Map and data to initialise the client
        #------------------------------------------
        
        #Map_Data
        #Used to calculate invalid tiles in the server, and to draw the tiles in the client. This allows the users to change the tiles if necessary to their own tilesets, as long as there are <=256 tiles
        Map_Data=[[[int(x) for x in y.split(',')] for y in F.split('.')] for F in Records[1][Map][3].split('F')]# in [y,x] #[Data for each frame:[Data for each column:[Data for each row[...,List],List],List],List]

        Map_Data_Bytes=bytearray()
        for F in range(len(Map_Data)):#All frames
            for y in range(len(Map_Data[F])):#All rows
                #print(bytes(Map_Data[F][y]))
                Map_Data_Bytes+=bytearray(Map_Data[F][y])
                #for x in range(len(Map_Data[F][y])):#All values
                #    Bytes.append(Map_Data[F][y][x])
                Map_Data_Bytes.append(254)#Used to determine when a row etc. has ended

            Map_Data_Bytes.append(255)#New frame
        #print(Bytes, len(Bytes))

        #Records_Data
        #The data required to blit the correct images to the screen
        String=""
        for ID in range(len(Records[4])):#Each unit
            for y in range(1,len(Records[4][ID])):
                String+=Records[4][ID][y]+"F"
                #String.append("F")
            String+="I"#Precondition - None of the units begin with the letter I of F
        #print(String, "STRING!!!")
        Records_Data_Bytes=String.encode('utf-8')
        #print(Records_Data.decode('utf-8'))
        #print(Records_Data_Bytes, "RECORDS_DATA!!!", len(Records_Data_Bytes))

        SERVER_FRAME_RATE=60 #Change depending on the speed of the final product
        #------------------------------------------
        
        #Listen out for clients and connect to them. This requires the Client to be run for each client that will be connecting!
        #------------------------------------------
        Server.listen(Players)#Number of connections that can occur simultaniously (4)
        #X=0
        Teams=[]
        #Camera_Positions=[]

        while len(Teams)!=Players:#4:# or X!=3600:#4 connections or One minute wait
            conn, address = Server.accept()
            Teams.append([conn])
            print("Connection from: " + str(address))
            print(Teams,(len(Teams)-1))#team number
            
            #Send the team number and map to each client
            Team_Lengths_And_Frame_Rate=bytearray((len(Teams)-1,SERVER_FRAME_RATE,len(Records_Data_Bytes)//256,len(Records_Data_Bytes)%256,len(Map_Data_Bytes)//256,len(Map_Data_Bytes)%256))#6 bytes
            #Precondition - There are <256 teams in total in the future and the length of the data is <65535 bytes ((255*256)+255)

            Teams[len(Teams)-1][0].send(Team_Lengths_And_Frame_Rate)
            Teams[len(Teams)-1][0].send(Records_Data_Bytes)
            Teams[len(Teams)-1][0].recv(1)#This is done to prevent the corruption of data
            Teams[len(Teams)-1][0].send(Map_Data_Bytes)#Map_Data
        #------------------------------------------

        #Testing (Load the level)
        #------------------------------------------
        #self.Add_Sprite(Unit([[300,300],[5,5],[1,1],[0,0],0,ANIMATIONS[0],1,[1,0,0,0,0,0,0,0],0,2]))
                #Attributes: Location, Size, Mode, Target, State, Animations, Level, Stats, Team, Class, ID

        #for x in range(5):
        self.Add_Sprite(Unit(0, [20,40], 0, [0,0], 1, Records, 0,len(self.__All_Sprites)))#Not +1 since indexing starts at 0
        self.Add_Sprite(Unit(0, [20,60], 1, [0,0], 1, Records, 0,len(self.__All_Sprites)))

        #self.Add_Sprite(Unit([[20,20],[5,5],[0],[0,0],0,[[0,0,0,0,1,1,1,1],[0,1,2,3,4,5,6,7],[2,2,2,2,3,3,3,3],[4,4,4,4,4,4,4,4],[5,5,5,5,5,5,5,5]],1,[100,25,30,5,1,200,2,100,0],0,2,0,1]),0)
                                                            #list of animations (image numbers) #List of stats: Health, Attack, Cooldown(Frames), Defense, Speed, Range, Multi-target, Exp, ...
        
        ##self.Add_Sprite(Unit([[50,50],[5,5],[0,[0,0,0,0]],[0,0],0,[[0,0,0,0,1,1,1,1],[0,1,2,3,4,5,6,7],[2,2,2,2,3,3,3,3],[4,4,4,4,4,4,4,4],[5,5,5,5,5,5,5,5]],1,[100,25,60,5,1,200,2,100,0],1,2,0,1]),1)

        Selected_Lists=[[],[],[],[]]#One for each client

        #------------------------------------------

        #Game loop. This will be done for each client!
        #------------------------------------------
        Clock=pygame.time.Clock()
        Current_Frame=0#used to keep track of which frame of animation the map should display once multiple frames of animation have been implemented.
        while True:
            Clock.tick(Settings["FPS"])#60
            Current_Frame=(Current_Frame+1)%Settings["FPS"]
            print(Current_Frame, "CURRENT_FRAME!!!")
            
            
            #Interact with each client currently connected
            #-------------------------------------------
            Client_Data=[0,1,2,3]#placeholder value
            for x in range(len(Teams)):
                
                #Receive data (1024 bytes)
                #-------------------------------------------
                #conn.recv(1024)
                Client_Data[x]=[]
                Transmitted_Data = list(Teams[x][0].recv(351))
                #Teams[0][x].send(bytearray(Current_Frame))#Precondition - Maximum framerate of 255 FPS!!!
                if not Transmitted_Data:#if data is not received break
                    print("NO DATA FROM CONNECTION", x,"!!!")
                    #conn.close()#Close the connection
                else:
                    #print(Transmitted_Data, "DATA FROM CLIENT:", x)#PART 2!!!

                    #Convert the client data into a format that can be understood by the server
                    temp=0#Used to determine the start point of each piece of data transmitted by the client
                    Transmitted_Data.append(255)#Used to ensure the end section of the data is correctly transferred
                    for y in range(len(Transmitted_Data)):
                        if Transmitted_Data[y]==255:
                            #print(Transmitted_Data[temp:y], "TESTING!!!", len(Transmitted_Data), y)
                            Client_Data[x].append( Transmitted_Data[temp:y])
                            temp=y+1
                    #Client_Data[x].append(Transmitted_Data[temp:len(Transmitted_Data)-1
                    #print(Client_Data[x], "CLIENT_DATA!!! [Key_State], [Mous_Pos]...")
                #-------------------------------------------

                    #Update Selected_Lists
                    #-------------------------------------------
                    #Empty the list if a left click or right click
                    #print(Client_Data[x][0][pygame.K_LSHIFT], "TEST!!!!!")
                    if (Client_Data[x][2][0]==1 and Client_Data[x][0][pygame.K_LSHIFT]==0 and Client_Data[x][0][pygame.K_RSHIFT]==0) or (Client_Data[x][2][2]==0 and Client_Data[x][4][2]==1):
                        Selected_Lists[x]=[]
                        #Other logic should be done by the individual units etc.
                    #-------------------------------------------
            
            #Process data
            #-------------------------------------------

            #Update sprites
            #---------------------------------------
            #Data = [Key_State, Mouse_Pos, Mouse_State, Previous_Mouse_Pos, Previous_Mouse_State]#The camera will be updated on the client side!
            #Data[x]: [Key_State, Mouse_Pos relative to the game environment, Mouse_State, Previous_Mouse_Pos, Previous_Mouse_State,Start_Pos,End_Pos] for team x
            #print(Data)
            #print(Client_Data, "CLIENT_DATA!!!")
            self.__All_Sprites.update(Client_Data,Selected_Lists,Map_Data)#Data from each client: Key_State,Mouse_Pos,Mouse_State,Top_Left
            #---------------------------------------

            #Update cameras #This will be done by the client!
            #---------------------------------------
            #---------------------------------------

            #Update the map
            #---------------------------------------
            #Current_Frame=round((X/Settings["FPS"])*(len(self.__Surfaces)-1))#-1 since indexing starts at 0!
            #This controls which frame of animation the map will be displaying
            #---------------------------------------
            
            #-------------------------------------------
                
            #-------------------------------------------

            #Collision detection
            #-------------------------------------------
            #Checks for any collisions.
            #If any occur, the first sprite to notice will move to its previous location
            #Any sprites in range of the current sprite will be appended to a list and sent to the sprite

            Defeated=[]
            for x in range(len(self.__All_Sprites.sprites())):#Each sprite checks against each other sprite currently instantiated#
                Attributes_0=self.__All_Sprites.sprites()[x].Get_Attributes()
                
                if Attributes_0["State"]==4 and Attributes_0["Cooldown_Timer"]==0:
                    #print(Attributes_0["Cooldown_Timer"])
                    #print("REMOVE", x)
                    Defeated.append(x)

                else:
                    
                    In_Range=[]
                    for y in range(len(self.__All_Sprites.sprites())):
                        if y==x:#Doesn't check itself
                            continue
                        else:
                            #Check the sprite is in range
                            #Attributes_0=self.__All_Sprites.sprites()[x].Get_Attributes()
                            Attributes_1=self.__All_Sprites.sprites()[y].Get_Attributes()
                            #print((Attributes_1["Location"][0]-Attributes_0["Location"][0])**2+(Attributes_1["Location"][1]-Attributes_0["Location"][1])**2, (Attributes_1["Stats"]["Range"]/10)**2)
                            if (Attributes_1["Location"][0]-Attributes_0["Location"][0])**2+(Attributes_1["Location"][1]-Attributes_0["Location"][1])**2<=(Attributes_1["Stats"]["Range"]/10)**2:
                                print("IN RANGE!!!!!!!!!!!!!!!!")
                                In_Range.append([y,self.__All_Sprites.sprites()[y]])
                                
                                #Move the sprite back to it's previous location
                                if len(pygame.sprite.spritecollide(self.__All_Sprites.sprites()[x],self.__All_Sprites.sprites(), dokill=False))>1:
                                    print("COLLLLLLLLLLLLISIONNNNNNNNNNNNNNNNNNN!!!!!!!!!!!!!!!!")
                                    self.__All_Sprites.sprites()[x].Move_Back()
                        
                    self.__All_Sprites.sprites()[x].Set_Attributes(["In_Range"],[In_Range])
            #-------------------------------------------
            
            #Remove defeated sprites from the game
            #-------------------------------------------
            for x in range(len(Defeated)):

                Defeated_Sprite=self.__All_Sprites.sprites()[Defeated[x]]
                
                print(Selected_Lists, "Lists of selected units!!!")
                print(defeated[x].Get_Attributes(), "DEFEATED ATTRIBUTES!!!")
                print(abcd)#Check the index and update the index of the remaining units in the self.__All_Sprites() group!!!
                for y in range(len(Selected_Lists)):#Remove from selected lists
                    try:
                        Selected_Lists[y].remove(Defeated_Sprite)
                    except ValueError:#Not in the list
                        print("Unit not in selected list:", y)
                        
                self.__All_Sprites.remove(Defeated_Sprite)

                del Defeated_Sprite
                print("DELEEEEEEEEEEEEEEEEEEEEEEEETED!!!")
            #-------------------------------------------

            #Set up the data to return to each client
            #-------------------------------------------
            #Selected Lists
            Selected_Bytes=bytearray()
            for x in range(4):#0,1,2,3 # Adds the selected lists
                Selected_Bytes+=bytearray(Selected_Lists[x])#This is because this bytearray will add the attributes to the end!!!
                Selected_Bytes.append(255)
            #print(Selected_Bytes, "SELECTED_LISTS_BYTES!!!")
            
            #Sprite Attributes                
            Attributes_Bytes=bytearray()
            for x in range(len(self.__All_Sprites.sprites())): # Adds the attributes of each unit
                Attributes=self.__All_Sprites.sprites()[x].Get_Attributes()
                #print(Attributes, "Attributes TEST!!!")
                #print((Attributes["ID"],Attributes["Location"][0]//256,Attributes["Location"][0]%256,Attributes["Location"][1]//256,Attributes["Location"][1]%256,Attributes["Direction"],Attributes["State"],Attributes["Level"],Attributes["Current_Health"],Attributes["Current_Exp"],Attributes["Current_Frame"]))

                Attributes_Bytes+=bytearray((Attributes["ID"],Attributes["Location"][0]//256,Attributes["Location"][0]%256,Attributes["Location"][1]//256,Attributes["Location"][1]%256,(Attributes["Direction"]+360)//256,(Attributes["Direction"]+360)%256,Attributes["State"],Attributes["Level"],Attributes["Current_Health"],Attributes["Current_Exp"],Attributes["Current_Frame"],len(Attributes["Attacking"])))

                #print(Attributes["Attacking"], "ATTACKING!!!")
                #print(len(Attributes["Attacking"]), "ATTACKING!!!!")#Precondition - Length of attacking attribute must be less than 255

                if len(Attributes["Attacking"])>0:
                    #print( [[Value[0][0]//256,Value[0][0]%256,Value[0][1]//256,Value[0][1]%256, Value[1][0],Value[1][1],Value[1][2]] for Value in Attributes["Attacking"]])
                    Values=[[Value[0][0]//256,Value[0][0]%256,Value[0][1]//256,Value[0][1]%256, Value[1][0],Value[1][1],Value[1][2]] for Value in Attributes["Attacking"]]
                    for x in range(len(Values)):
                        Attributes_Bytes+=bytearray(Values[x])#A fixed number of values, therefore only the length of the attacking attribute is required!
                        #[[Value[0][0]//256,Value[0][0]%256,Value[0][1]//256,Value[0][1]%256, Value[1][0],Value[1][1],Value[1][2]] for Value in Attributes["Attacking"]])#[[],(0,0,0)]] as mentioned before in the object class
                    print(Attributes_Bytes, "TEST BYTES!!!")
                #Precondition - The attacking colour must contain values less than 255!!!
                Attributes_Bytes+=bytearray([255])
                
            #print(Attributes_Bytes, "ATTRIBUTE_BYTES!!!", list(Attributes_Bytes), len(Attributes_Bytes))


            #Selected lists will contain a maximum of 8*4 = 32 items, therefore only a single byte is needed here
            Lengths=bytearray((len(Selected_Bytes),len(Attributes_Bytes)//256,len(Attributes_Bytes)%256,Current_Frame))#Precondition - Less than 65536 bytes will be sent from here by the server each frame
            #print(Lengths, "LENGTHS!!!", list(Lengths), len(Lengths))
            #-------------------------------------------
                    
            #Send data to each client
            #-------------------------------------------

            
            for x in range(len(Teams)):#This will send all of the attributes to all of the players when all of the inputs have been processed!
                #The 0 is because the connection is held in a list
                #print(Lengths, "SERVER LENGTHS!!!")
                Teams[x][0].send(Lengths)
                Teams[x][0].send(Selected_Bytes)
                Teams[x][0].recv(1)
                Teams[x][0].send(Attributes_Bytes)
            #------------------------------------------

        #conn.close()#FIX RESET THE GAME WHEN EXITING!!!
        #------------------------------------------
        
    def Run(self, Level, No_Players, Map, Host):

        #Connect to the correct server
        #---------------------------------------
        if No_Players == 1 or Host==True:#Host of the game
            print("RUN THE SERVER!!!")#Run the server as a thread
            SERVER = threading.Thread(target=self.Server,args=(Map,Level,No_Players, Records), daemon=True)
            SERVER.start()#Starts the thread

            print("RUN THE CLIENT!!!")
            self.Client('localhost',5000)
            
        else:#Use a code to join another game
            Code='localhost'
            Host=Code#socket.gethostname() #localhost is used since both the client and server are being tested on the same computer
            Port=5000

            self.Client(Host,Port)

        #---------------------------------------


    def Client(self,Host,Port):
        
        #Create the client and connect to the server via the host and port
        #------------------------------------------
        #Host='localhost'#socket.gethostname() #localhost is used since both the client and server are being tested on the same computer
        #Port=5000

        Client=socket.socket()
        Client.connect((Host,Port))
        #------------------------------------------

        #Get team and Map_Data from the server and format them
        #------------------------------------------
        #Team number, Server_Frame_Rate and size of Map_Data and Records_Data
        Team_Lengths_And_Frame_Rate = list(Client.recv(6))#Team and size of Map_Data to be transmitted
        #Precondition - Assuming the team number + length of the data is held in 3 bytes!!!
        #print(Team_Lengths_And_Frame_Rate)
        #print("Recieved team number:", Team_Lengths_And_Frame_Rate[0])
        #print("Lengths:", (Team_Lengths_And_Frame_Rate[2]*256)+Team_Lengths_And_Frame_Rate[3], (Team_Lengths_And_Frame_Rate[4]*256)+Team_Lengths_And_Frame_Rate[5])

        Server_Frame_Rate=Team_Lengths_And_Frame_Rate[1]
        Records_Data_Bytes = Client.recv((Team_Lengths_And_Frame_Rate[2]*256)+Team_Lengths_And_Frame_Rate[3]).decode('utf-8')#This converts the encoded length values obtained back into the origional value, then receives data = to that amount. This is done because I am using a bytearray which can only accept values between 0 and 255. This is acceptable because in my design I wished to limit the amount of processing power. This is achieved here by limiting the amount of data that will be transmitted each frame.
        Client.send(bytearray(1))
        Map_Data = Client.recv((Team_Lengths_And_Frame_Rate[4]*256)+Team_Lengths_And_Frame_Rate[5])
        
        #Map_Data=list(Data)#Converts a bytearray back into a list of ints
        #print(Records_Data.decode('utf-8'))#Converts an encoded string back into a regular string

        #print("Received records data:", Records_Data_Bytes)
        #print("Received map data:", Map_Data)
        #Should recieve: Map_Data and Records[4] to ensure a global variable is not needed!!!

        Records_Data=[[[[value for value in a.split(",")] for a in b.split(".")] for b in c.split("F")] for c in Records_Data_Bytes.split("I")]#Splits the records data into the separate components. Does the opposite os the server to decode the data
        print(Records_Data, "RECORDS!!!!!!!!!!!")
        #------------------------------------------

        #Blit the tiles to the screen #Should be done by the client only!!!
        #------------------------------------------
        #print(Map_Data)
        y=0
        x=0
        F=0
        for Value in range(len(Map_Data)):
            if Map_Data[Value]==254:#Signifies a new row
                x=0
                y+=1
            elif Map_Data[Value]==255:#Signifies a new frame
                x=0
                y=0
                self.__Surfaces.append(pygame.surface.Surface((SIZE[0],SIZE[1])))
                F+=1
            else:
                #print(x,y,F,Value,Map_Data[Value], "TESTING!!!")
                self.__Surfaces[F].blit(self.__TILES[Map_Data[Value]],(20*x,20*y))
                x+=1
        #print(len(self.__Surfaces), "LENGTH CHECK!!!")
##        Map_Size=[len(Data[1][0]),len(Data[1][0][0])]# in [y,x] assuming row 0 is the longest and a square map
        #------------------------------------------

        #Load the camera
        #------------------------------------------
        Camera1=Camera([[0,0],[0,0],0.2,Team_Lengths_And_Frame_Rate[0]])
        #------------------------------------------
        
        
        #Game loop #Display the screen each frame
        #---------------------------------------
        X=0#TEST FOR FRAMERATE!!!
        Previous_Mouse_Pos=[0,0]#These are re-calculated at the end of each frame!
        Previous_Mouse_State=(0,0,0)

        #Get camera attributes required to blit the correct things to the screen
        Camera_Attributes=Camera1.Get_Attributes()

        RUNNING=True#set to false if the game ends
        while RUNNING==True:
            
            self.__CLOCK.tick(self.__Settings["FPS"])#lag will occur if too much is updated too slowly!!!
            #Received from the server to synchronise all of the clients below

            #Process input and send data to the server
            #-------------------------------------------
            #print("CHECKING EVENTS!!!")
            if self.Check()==False:#Checks for events from the pygame window (E.G. if the window is closed!)
                RUNNING=False

            Key_State=pygame.key.get_pressed()
            Mouse_Pos=pygame.mouse.get_pos()
            Mouse_State=pygame.mouse.get_pressed()

            #Build the bytearray to be transmitted
            #-------------------------------------------
            #Key_State
            Client_Data=bytearray(Key_State)#323 bytes
            Client_Data.append(255)#1 byte
            
            #Mouse_Pos (Adjusted for game environment)
            Append=bytearray((((Mouse_Pos[0]//Settings["SCALE"])+int(Camera_Attributes["Location"][0]))//256,((Mouse_Pos[0]//Settings["SCALE"])+int(Camera_Attributes["Location"][0]))%256,((Mouse_Pos[1]//Settings["SCALE"])+int(Camera_Attributes["Location"][1]))//256,((Mouse_Pos[1]//Settings["SCALE"])+int(Camera_Attributes["Location"][1]))%256))
            #4 bytes
            #Precondition - Game Environment size (Map_Size) must be in the range([0,0] and [65279,65279]), since 255 is used to signify the next piece of data to be sent, therefore (254*256)+255
            Client_Data+=Append
            Client_Data.append(255)
            #1 byte
            
            #Mouse_State
            Append=bytearray(Mouse_State)#3 bytes
            Client_Data+=Append
            Client_Data.append(255)#1 byte
            
            #Previous_Mouse_Pos (Adjusted for game environment)
            Append=bytearray((((Previous_Mouse_Pos[0]//Settings["SCALE"])+int(Camera_Attributes["Location"][0]))//256,((Previous_Mouse_Pos[0]//Settings["SCALE"])+int(Camera_Attributes["Location"][0]))%256,((Previous_Mouse_Pos[1]//Settings["SCALE"])+int(Camera_Attributes["Location"][1]))//256,((Previous_Mouse_Pos[1]//Settings["SCALE"])+int(Camera_Attributes["Location"][1]))%256))
            #4 bytes
            Client_Data+=Append
            Client_Data.append(255)#1 byte
            
            #Previous_Mouse_State
            Append=bytearray(Previous_Mouse_State)#3 bytes
            Client_Data+=Append
            Client_Data.append(255)#1 byte
            
            #Selection_Box start and end positions
            #Start_Pos
            #print(Camera_Attributes["Start_Pos"],Camera_Attributes["Start_Pos"], "CAMERA_POSITIONS!!!")
            Camera_Ints=[int(Camera_Attributes["Start_Pos"][0]),int(Camera_Attributes["Start_Pos"][1]),int(Camera_Attributes["End_Pos"][0]),int(Camera_Attributes["End_Pos"][1])]
            #print(Camera_Ints, "CAMERA INTS!!!")
            Append=bytearray((Camera_Ints[0]//256,Camera_Ints[0]%256,Camera_Ints[1]//256,Camera_Ints[1]%256,255,Camera_Ints[2]//256,Camera_Ints[2]%256,Camera_Ints[3]//256,Camera_Ints[3]%256))#PART 1!!!
            #9 bytes
            Client_Data+=Append
            #Don't need an extra 255 because this is the end of the data being sent!

            #print(Client_Data, "CLIENT_DATA!!!", len(Client_Data))#351 bytes in total
            Client.send(Client_Data)
            #-------------------------------------------
            
            #-------------------------------------------

            #Receive the Data from the server and convert into the correct format
            #-------------------------------------------
            Lengths=Client.recv(4)
            #print(Lengths, "CLIENT LENGTHS", list(Lengths))
            #print(Lengths[0],(Lengths[1]*256)+Lengths[2], "SIZE OF TRANSMISSIONS")

            Current_Frame=round((Lengths[3]/self.__Settings["FPS"])*(len(self.__Surfaces)-1))#Waits for the server to respond to ensure there is no mix up in the data or race conditions!!! #-1 since indexing starts at 0!
            Selected_Lists_Ints=list(Client.recv(Lengths[0]))
            Client.send(bytearray(1))
            Attributes_Ints = list(Client.recv((Lengths[1]*256)+Lengths[2]))#all of the attributes of every sprite
            #print('Data from server:', Selected_Lists_Ints, "Part 1!!!", Attributes_Ints, "Part 2!!!")

            Selected_Lists=[]
            temp=0
            for x in range(len(Selected_Lists_Ints)):#Converts the list of integers from the server into a list of lists that can be indexed, therefore able to be used in the rest of the code
                if Selected_Lists_Ints[x]==255:
                    Selected_Lists.append(Selected_Lists_Ints[temp:x])
                    temp=x+1
            #print(Selected_Lists, "Formatted selected lists!!!")

            Attributes=[]
            temp=0
            for x in range(len(Attributes_Ints)):#Same as above, except for the Attributes (The reverse of what is happening in the server)
                if Attributes_Ints[x]==255:
                    Attributes.append(Attributes_Ints[temp:x])
                    temp=x+1
            #print(Attributes, "Formatted attributes!!!")

            for x in range(len(Attributes)):#For each attribute, uses the fixed position 12 from the formatted attributesthat that contains the length of the attacking attribute and converts this into the attacking attribute using the remaining data that is variable in size behind it!
                Attributes[x]=Attributes[x][0:12]+[Attributes[x][13:len(Attributes[x])]]#Format the "Attacking" attribute into the correct format
                #print(Attributes[x], len(Attributes[x][len(Attributes[x])-1]), "TESTING ATTRIBUTES!!!!!!!!")

            #[Location_X//256,Location_X%256,Location_Y//256,Location_Y%256,Colour_R,Colour_G,Colour_B,...(Repeated for each unit attacked)]
            print(Attributes, "Attacking attribute formatting!!!")

            #Selected_Lists contains: index of unit in Attributes #FIX to ensure this is the case!!!
            #Attributes contains: [ID,Location[0]//256,Location[0]%256,Location[1]//256,Location[1]%256,Direction,State,Level,Current_Health,Current_Exp,Current_Frame] for each unit
            #-------------------------------------------
            
            #Update camera
            #-------------------------------------------
            #Sprites are updated on the server!
            Camera1.update([Key_State,Mouse_Pos,[(Mouse_Pos[0]//Settings["SCALE"])+Camera_Attributes["Location"][0],(Mouse_Pos[1]//Settings["SCALE"])+Camera_Attributes["Location"][1]],Mouse_State,[(Previous_Mouse_Pos[0]//Settings["SCALE"])+Camera_Attributes["Location"][0],(Previous_Mouse_Pos[1]//Settings["SCALE"])+Camera_Attributes["Location"][1]],Previous_Mouse_State],self.__SUBSCREEN,Selected_Lists,self.__IMAGES, Attributes,Records_Data)#First part used to lock on to a particular sprite!
            #-------------------------------------------

            
            #Render/Output
            #-------------------------------------------
            #Get camera attributes required to blit the correct things to the screen
            Camera_Attributes=Camera1.Get_Attributes()

            #Draw the sprites to the SPRITE_LAYER
            #---------------------------------------
            #Attributes contains: [ID,Location[0]//256,Location[0]%256,Location[1]//256,Location[1]%256,Direction,State,Level,Current_Health,Current_Exp,Current_Frame,Attacking] for each unit
            #Records contains: [Name,Size,Animations,Stats,Invalid,Functions,Null]
            for x in range(len(Attributes)):#The sprite attributes
                                                                                #[Animations from a certain ID][State][Current_Frame]                          #Direction                                   #Location[x]                                  Size[x]//2                              #Location[y]                                           #Size[y]//2
                self.__SPRITE_LAYER.blit(pygame.transform.rotate(self.__IMAGES[int(Records_Data[Attributes[x][0]][2][Attributes[x][7]][Attributes[x][11]])],-((Attributes[x][5]*256)+Attributes[x][6]-360)),( ((Attributes[x][1]*256)+Attributes[x][2])-int(Records_Data[Attributes[x][0]][1][0][0])//2, ((Attributes[x][3]*256)+Attributes[x][4])-int(Records_Data[Attributes[x][0]][1][0][1])//2))#blit the sprites themselves!
                #print(Attributes, "ATTR TEST!!!")
                #Precondition - The lines drawn must have RGB values <255 to avoid creating extra values in the attributes list which will result in a crash!!!
                #print(Attributes[x])
                #print(Attributes[x][12], "PART TEST!!!")


                for y in range(len(Attributes[x][12])//7):#All the values in the "Attacking" attribute (7 values per attacked sprite: #[Location_X//256,Location_X%256,Location_Y//256,Location_Y%256,Colour_R,Colour_G,Colour_B,...(Repeated for each unit attacked)] )
                                                                #Colour_R           #Colour_G                   #Colour_B                               Unit_Location_X              Unit_Location_Y                            #Attacking_Location_X                                       #Attacking_Location_Y                                      #Thickness of line drawn
                    print(Attributes[x][12], "ATTRIBUTE 12!!!")
                    #print((Attributes[x][12][(7*y)+4],Attributes[x][12][(7*y)+5],Attributes[x][12][(7*y)+6]))
                    pygame.draw.line(self.__SPRITE_LAYER,(Attributes[x][12][(7*y)+4],Attributes[x][12][(7*y)+5],Attributes[x][12][(7*y)+6]),((Attributes[x][1]*256)+Attributes[x][2],(Attributes[x][3]*256)+Attributes[x][4]),((Attributes[x][12][(7*y)]*256)+Attributes[x][12][(7*y)+1], (Attributes[x][12][(7*y)+2]*256)+Attributes[x][12][(7*y)+3]),2)#Any shots taken during the frame
            #---------------------------------------

            #Blit the layers onto the SUBSCREEN
            #---------------------------------------#Current_Frame
            self.__SUBSCREEN.blits(((self.__Surfaces[Current_Frame],(0,0)),(self.__SPRITE_LAYER,(0,0))))#,(self.__FOG_LAYER,(0,0))))
            #---------------------------------------

            #Blit the SUBSCREEN to the SCREEN
            #---------------------------------------            #Top_Left
            self.__CAMERA_VIEW.blit(self.__SUBSCREEN,[0,0],(int(Camera_Attributes["Location"][0]),int(Camera_Attributes["Location"][1]),self.__Settings["WIDTH"]//self.__Settings["SCALE"],self.__Settings["HEIGHT"]//self.__Settings["SCALE"]))

            self.__SCREEN.blit(pygame.transform.scale(self.__CAMERA_VIEW,(self.__Settings["WIDTH"],self.__Settings["HEIGHT"])),[0,0])#self.__SUBSCREEN,(-Top_Left[0],-Top_Left[1],WIDTH,HEIGHT))#self.__CAMERA_VIEW,[0,0])#SCALED_CAMERA_VIEW,[0,0])
            self.__SCREEN.blit(Camera1.image,[0,0])#Draw the Player's Camera to the (Player's) Screen
            #---------------------------------------

            #Re-fresh the sprite layer
            #---------------------------------------
            for x in range(len(Attributes)):#All of the currently active units. #The sprites' images #Data[2]
                                                                #Top_Left[0]                                                                            #Top_Left[1]                                                                                #Width                                      #Height
                self.__SPRITE_LAYER.fill((0,0,0),pygame.Rect(((Attributes[x][1]*256)+Attributes[x][2])-int(Records_Data[Attributes[x][0]][1][0][0])//2,((Attributes[x][3]*256)+Attributes[x][4])-int(Records_Data[Attributes[x][0]][1][0][1])//2,2*int(Records_Data[Attributes[x][0]][1][0][0]),2*int(Records_Data[Attributes[x][0]][1][0][1])))

                for y in range(len(Attributes[x][12])//7):#The shots fired during the frame
                    pygame.draw.line(self.__SPRITE_LAYER,(0,0,0),((Attributes[x][1]*256)+Attributes[x][2],(Attributes[x][3]*256)+Attributes[x][4]),((Attributes[x][12][(7*y)]*256)+Attributes[x][12][(7*y)+1], (Attributes[x][12][(7*y)+2]*256)+Attributes[x][12][(7*y)+3]),2)
            #---------------------------------------

            #-------------------------------------------
            pygame.display.flip()#double buffering #flips the display #MUST BE DONE AFTER DRAWING EVERYTHING!!!

            Previous_Mouse_Pos=Mouse_Pos
            Previous_Mouse_State=Mouse_State
        #---------------------------------------
        

    def Quit(self):

        pygame.quit()
#----------------------------------------------------------
print("Classes module")


#Main Program
#Purpose: To run the game
#Created 01/08/2020 by Greg
#----------------------------------------------------------

Records=Create_Database()
#print(Records)

pygame.display.set_mode((0,0),pygame.FULLSCREEN)
SCREEN_INFO=pygame.display.Info()

Settings= {#Set up settings and constants depending on the user's preferences (Default values if they haven't selected yet)
    "SCALE": int(Records[2][0][2]),#Scales all of the images used to help improve the frame-rate. A higher scale decreases the size of the images, therefore reducing the amount of memory and processing power required to output
    "WIDTH": int((int(Records[2][1][2])/100)*SCREEN_INFO.current_w),#800 #Width of the screen
    "HEIGHT": int((int(Records[2][2][2])/100)*SCREEN_INFO.current_h),#600 #Height of the screen
    "FPS": int(Records[2][3][2]),#Frame-rate of the client
    "MINI_MAP_SIZE": int(Records[2][4][2]),
    "INFO_BAR_SIZE": int(Records[2][5][2]),
    "MAX_CAMERA_SPEED": int(Records[2][6][2])
    }

def Set_Settings(Settings):
    Settings["SCALE"]=int(Records[2][0][2])

    #print(SCREEN_INFO.current_w)
    Settings["WIDTH"]=int((int(Records[2][1][2])/100)*SCREEN_INFO.current_w)
    Settings["HEIGHT"]=int((int(Records[2][2][2])/100)*SCREEN_INFO.current_h)

    #print(Settings["WIDTH"], "WIDTH", Settings["HEIGHT"], "Height")
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"
    SCREEN=pygame.display.set_mode((Settings["WIDTH"],Settings["HEIGHT"]))

    Settings["FPS"] =int(Records[2][3][2])
    Settings["MINI_MAP_SIZE"]=int(Records[2][4][2])
    Settings["INFO_BAR_SIZE"]=int(Records[2][5][2])
    Settings["MAX_CAMERA_SPEED"]=int(Records[2][6][2])

    Camera_View=pygame.surface.Surface((Settings["WIDTH"]//Settings["SCALE"],Settings["HEIGHT"]//Settings["SCALE"]))

    #print(Settings)
    return SCREEN,Camera_View,Settings

SIZE=[1000,1000]#Temporary This will be chosen when the map is selected!
#--------------------------------------------















#Constants
#--------------------------------------------
#The map size will be decided when the map is selected!
TABLE_COLUMNS=[["Achievement","AchievementID","AchievementName", "Progress", "AchievementDescription"],["Map","MapID","MapName","MapSize"],["Setting","SettingID","SettingName","SettingValue","SettingDescription"],["Building","BuildingID","BuildingName","BuildingStats","BuildingFaction"],["Unit","UnitID","UnitName", "UnitAnimations", "UnitStats", "InvalidTiles", "UnitFunctions"],["Animation","AnimationID","AnimationName","UnitID","BuildingID"]]#Used when updating the database!

#colours
#---------------------------------------
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
#---------------------------------------

#--------------------------------------------

Game1=Game(0,Settings,Records)#Starts the game!

#----------------------------------------------------------
