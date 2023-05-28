#Classes module for Compter Science project
#Purpose: To hold all of the classes that will be run in the game
#Created 01/08/2020 by Greg
#----------------------------------------------------------

import pygame
import os
import re
from Functions import *
import socket
import pickle
#import random
#import time
import threading
#import math


#----------------------------------------------------------
class Thread(object):

    def __init__(self, Target,Parameters):

        thread = threading.Thread(target=self.Run, args=(Target,Parameters,), daemon=True)#The comma after Parameters is required otherwise it will return a type error!!!
        thread.start()

    def Run(self,Target,Parameters):
        print(Target)
        Target(Parameters)
#----------------------------------------------------------



#----------------------------------------------------------
class Object():

    def __init__(OBJECT, ID, Location, Team, Target, Level, Records, Mode, Index):#Object List: [Location]
        #Complete List Of Atttributes: [Location,[Size_X,Size_Y],[Mode/control],Rect,State,Animations,Level,Stats,Team,UnitID]#OUT OF DATE FIX!!!
        #------------------------------------------
        #Sometimes error: Must re-create the game database because something goes wrong?
        #print(Records[4][ID])
        Stats= [int(x) for x in Records[4][ID][4].split(',')]
        print(Stats, "STATS!!!")

        OBJECT.__Attributes= {#The data that must be sent to each client each frame in order to output the correct image of the game!
            #"Name": Records[4][ID][1],
            "Location": Location,#Center of the object [x,y]
            "Direction": 0,#Multiple of 45 #Used to display the unit's direction
            "Size": [int(x) for x in Records[4][ID][2].split(',')],# [x,y]
            "Mode": Mode,#Integer Changes how the unit behaves. Start in mode 2 to move to the target location
            "Target": Target,# Target location that the sprite will move to when in mode 2
            "Path": [],#Path to target location
            "Threads": 0,#Keeps track of the number of threads a unit is currently running
            "State": 0,# Integer 0: Idle, 1: Moving, 2: Attacking
            "Animations": [[int(y) for y in x.split(',')] for x in Records[4][ID][3].split('.')],#[[List of numbers],[...],...] This corresponds to the image number to be blitted to the sprite layer in the IMAGES list #List of animations: 0: Idle, 1: Moving, 2: Attacking, 3: Damaged, 4: Dead
            "Level": Level,#Integer Stats scale by StatX * (Level+Level-1)
            "Stats": {#Stats contains a dictionary of the different stats #Precondition - All stats are integers
                "Health": Stats[0],#Max health
                "Attack": Stats[1],
                "Cooldown": Stats[2],#Used to control how quickly a unit can attack #The maximum time left until the unit attacks again #Measured in frames
                "Defence": Stats[3],
                "Speed": Stats[4],
                "Range": Stats[5],
                "Multi-target": Stats[6],
                "Exp": Stats[7]
                },
            "Current_Health": Stats[0],#Equal to Health stat
            "Current_Exp": 0,
            "Team": Team,# x
            "Frame": 0,#Frame and Current_Frame are used to calculate which frame of animation should be playing!
            "Current_Frame": 0,
            #"Class": Attributes[9],# x #Unit/Building etc.
            "ID": ID,#This will determine the type of attack the object will have
            "Index": Index,#This is used to keep track of where in the all_Sprites group the unit is, which is also used to determine if it has been selected
            "In_Range": [],#This will be used to determine which object will be attacked
            "Attacked": False,#Used to change the behaviour of the unit when it's health is altered by another unit #True when it's health has been lowered!
            "Attacking": [], #E.G.[[[],(0,0,0)]] # [[Location],(Colour)], ...] #List of locations used to draw lines to the sprite layer. Colours are the colour of the line that will be drawn #These are considered to be shots from the sprite
            "Cooldown_Timer": Stats[2],#The remaining time (in frames) until the unit can attack again. #Also used to delay the deletion of the unit!#FIX!!! (MAYBE!!!)
            "Functions": [int(x) for x in Records[4][ID][5].split(',')],#A list of the actions a unit can take.
            "Invalid_Tiles": [int(x) for x in Records[4][ID][6].split(',')]#A list of all tiles that the unit can't travel on!
            }
        #print(OBJECT.__Attributes)
        print("MADE OBJECT!!!")

        if OBJECT!= Object:#If UnitID is not the ID for an Object. This prevents a crash when creating an object
            print("NOT AN OBJECT!!!")
            return OBJECT.__Attributes
        #------------------------------------------

    def Set_Attributes(OBJECT,Keys,Values):
        Attacked=False
        for x in range(len(Keys)):
            #print(OBJECT.__Attributes[Keys[x]],Values[x])
            
            if Keys[x]=="Health":#Check if the unit has been defeated
                print(Values[x], "HEEEEEEEEEAAAAAAAAAAAALLLLLLLLLTTTTTHHHHHHHH!!!")
                if Values[x]==0:
                    OBJECT.__Attributes["State"]=4#Dead #After the cooldown timer expires, the sprite will be deleted!
                elif Values[x]<OBJECT.__Attributes["Current_Health"]:
                    Attacked=True

                OBJECT.__Attributes[Keys[x]]=Values[x]

            #Maybe improve to prevent abuse of this action?
            elif Keys[x]=="State":#Check if the unit has begun to attack and prevent the unit from changing state when it has been defeated
                if OBJECT.__Attributes["State"]!=4:
                    if Values[x]==2:#Attacking
                        OBJECT.__Attributes["Cooldown_Timer"]=0
                    elif Values[x]==3:
                        OBJECT.__Previous_State=OBJECT.__Attributes["State"]

                    OBJECT.__Attributes[Keys[x]]=Values[x]
                    #print(OBJECT.__Attributes["Cooldown_Timer"], "COOLDOWN!!!")
                        
            else:#Any other change that doesn't need validation
                OBJECT.__Attributes[Keys[x]]=Values[x]
        return Attacked

                                                        #Size of object!
    def Position_Validation(OBJECT,Top_Left,Bottom_Right,Size,Location):
        
        #Position validation (Makes sure the object isn't out of bounds!)
        #------------------------------------------
        Test=[[1,0],[1,0]]#reset speed to 0 if [0,x] #x indicates the side in which the object is out of bounds (-1=right/bottom side and 1=left/top side)!
        #print(Top_Left,Bottom_Right)
        Fix=[0,0]#Used to stop the camera from getting stuck at the edge of the screen by adding a constant value to 'fix' the problem of rounding for integers!

        if Bottom_Right[0]>(SIZE[0]):#X_Co-ordinate
            #print("BOTTOM RIGHT 0!!!",Bottom_Right)
            Location[0]=(SIZE[0])-int(Size[0]/2)#Center of object
            Test[0]=[0,-1]
            Fix[0]=-0.25
            #Attributes[1]=[0,0]#reset speed to 0
        elif Top_Left[0]<0:
            #print("TOP LEFT 0!!!")
            Location[0]=0+int(Size[0]/2)+1
            Test[0]=[0,1]
            Fix[0]=-0.5

        if Bottom_Right[1]>(SIZE[1]):#Y_Co-ordinate
            #print("BOTTOM RIGHT 1!!!")
            Location[1]=(SIZE[1])-int(Size[1]/2)
            Test[1]=[0,-1]
            Fix[1]=-0.25
        elif Top_Left[1]<0:
            #print("TOP LEFT 1!!!", Top_Left)
            Location[1]=0+int(Size[1]/2)
            Test[1]=[0,1]
            Fix[1]=0.5
        #------------------------------------------
        return Location,Test,Fix

#----------------------------------------------------------


#----------------------------------------------------------
class Camera(Object,pygame.sprite.Sprite):

    def __init__(self,Attributes):
        
        #Complete List Of Atttributes: [Location,[Speed_X,Speed_Y],[Size_X,Size_Y],[Mode/control],Rect,State,Animations,Level,Stats,Team]
        #List for Camera: [[Location_X,Location_Y],[Speed_X,Speed_Y],Accel]
        #------------------------------------------
        self.__Attributes= {
            "Location": Attributes[0],#Top left of the camera
            "Speed": Attributes[1], #[x,y]
            "Acceleration": Attributes[2], #int
            "Team": Attributes[3],
            "Selected_List": [[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,0]], [],0,0],#[[[name,pointer],...],[Free space],start,current length] #circular Linked list #SHOULD start with the location of the selected units or at [0,0]
            "Selected": 0,
            "Start_Pos": [0,0],#Used to track and draw the selection box when right click is held down!
            "End_Pos": [0,0]#Used to track and draw the selection box when right click is held down!
            }

        #Image of the whole camera overlay
        #------------------------------------------
        #MINI_MAP_SIZE=4 # Setting #The smaller the number (int) the bigger the size!

        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((Settings["WIDTH"],Settings["HEIGHT"]))

        self.image.convert_alpha()
        self.image.set_colorkey((0,0,0))
        self.image.set_alpha(150)
        
        #Minimap         #MINI_MAP_SIZE=4 # Setting #The smaller the number (int) the bigger the size!
        #------------------------------------------
        #Boarder for map!
        self.image.fill((50,50,50,50),(self.__Attributes["Location"][0]+(Settings["WIDTH"]-(int(1/Settings["MINI_MAP_SIZE"])*Settings["WIDTH"]))-1,self.__Attributes["Location"][1],Settings["WIDTH"]//Settings["MINI_MAP_SIZE"],Settings["HEIGHT"]//Settings["MINI_MAP_SIZE"]))
        #------------------------------------------

        #Info bar   #INFO_BAR_SIZE=4
        #------------------------------------------
        self.image.fill((255,255,255,255), (0,(Settings["HEIGHT"]-int(1/Settings["INFO_BAR_SIZE"]*Settings["HEIGHT"])),Settings["WIDTH"],Settings["HEIGHT"]))
        #------------------------------------------

        #Actions menu
        #------------------------------------------
        self.image.fill((255,255,255,255), (0,0,Settings["WIDTH"]//4,Settings["HEIGHT"]//4))
        #------------------------------------------

        #Range circle
        #------------------------------------------
        #Done in the update!
        #------------------------------------------

        #Selection box
        #------------------------------------------
        #Done in the update!
        #------------------------------------------
        
        #Rect/Camera Rect
        #------------------------------------------
        self.rect=pygame.Rect(self.__Attributes["Location"][0],self.__Attributes["Location"][1],Settings["WIDTH"],Settings["HEIGHT"])#self.image.get_rect()
        #self.rect.topleft=self.__Attributes[0]
        #self.rect.center=[self.__Attributes[0][0]+WIDTH//2,self.__Attributes[0][1]+HEIGHT//2]

        #self.__Camera_Rect=pygame.Rect(self.__Attributes[0],self.__Attributes[1],WIDTH//Scale,HEIGHT//Scale)
        #------------------------------------------
        #print(self.__Attributes)
        print("MADE CAMERA!!!")


    def Get_Attributes(self):

        #------------------------------------------
        return self.__Attributes
        #------------------------------------------
        
    def update(self,Data,SUBSCREEN,Selected_Lists,IMAGES,Attributes,Records_Data):
        #Data: [Key_State,Mouse_Pos (NOT adjusted), Mouse_Pos (adjusted),Mouse_State,Previous_Mouse_Pos (adjusted),Previous_Mouse_State]
        #Adjustment to the Mouse_Pos etc in order to be relative to the game environment. [(Mouse_Pos[0]//Settings["SCALE"])+Camera_Attributes["Location"][0],(Mouse_Pos[1]//Settings["SCALE"])+Camera_Attributes["Location"][1]]
        #How to unadjust the Mouse_Pos #[(self.__Attributes["Start_Pos"][0]-self.__Attributes["Location"][0])*Settings["SCALE"],(self.__Attributes["Start_Pos"][1]-self.__Attributes["Location"][1])*Settings["SCALE"]]
        #Attributes contains: [ID,Location[0]//256,Location[0]%256,Location[1]//256,Location[1]%256,Direction,State,Level,Current_Health,Current_Exp,Current_Frame, [Null]] for each unit
        #print(Attributes, "ATTRIBUTES!!!")
        #print(Selected_Lists, "CAMERA LISTS!!!")

        #Adjusted_Mouse_Pos=[(Data[1][0]//Settings["SCALE"])+Camera_Attributes["Location"][0],(Data[1][1]//Settings["SCALE"])+Camera_Attributes["Location"][1]]
        #print(Sprite_Attributes, "ATTRIBUTES!!!")
        self.image.fill((0,0,0))#Refresh the overlay
        
        #Draw selection box
        #------------------------------------------
        #Calculate rect relative to the game environment based on moue input
        if Data[3][2]==1:#Mouse_State[Right click]
            if Data[5][2]==0:#Previous_Mouse_State[Right click]
                self.__Attributes["Start_Pos"]= Data[2]
            self.__Attributes["End_Pos"]= Data[2]#The End_Pos is always updated, since the calculations of which units are to be selected will be done by the server once the right click is no lnger held down!
            #print(self.__Attributes["Start_Pos"],self.__Attributes["End_Pos"], "POSITIONS!!!")
            
            #Validate position of rect to be drawn (Make sure it is inside the camera image)
            #This is done to prevent the camera image from enlarging, which will slow down the game!!!
            #This will use the unadjusted version of the mouse position
            #The End_Pos will always be on-screen, so no validation is needed for this point

            Start_Of_Rect=[int((self.__Attributes["Start_Pos"][0]-self.__Attributes["Location"][0])*Settings["SCALE"]),int((self.__Attributes["Start_Pos"][1]-self.__Attributes["Location"][1])*Settings["SCALE"])]
            #print(Start_Of_Rect)
            #print(abc)

            if Start_Of_Rect[0]<0:#Left side of the screen
                Start_Of_Rect[0]=0#This is adjusted outside of the game environment (Start and End Pos use the game environment's dimensions, but the camera image uses the normal screen dimensions)
            elif Start_Of_Rect[0]>Settings["WIDTH"]:#Right side of the screen
                Start_Of_Rect[0]=Settings["WIDTH"]

            if Start_Of_Rect[1]<0:#Top of the screen
                Start_Of_Rect[1]=0
            elif Start_Of_Rect[1]>Settings["HEIGHT"]:#Bottom of the screen
                Start_Of_Rect[1]=Settings["HEIGHT"]

            #Draw rect
            #The processing for the selection box will be done in the server!
            #print(self.__Attributes["Start_Pos"],self.__Attributes["End_Pos"],Top_Left, "ATTTTTTTTTTR!!!")
            #print(min(Top_Left[0],self.__Attributes["End_Pos"][0]),min(Top_Left[1],self.__Attributes["End_Pos"][1]),abs(Top_Left[0]-self.__Attributes["End_Pos"][0]),abs(Top_Left[1]-self.__Attributes["End_Pos"][1]), "RECT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            self.image.fill((150,150,150,255),(min(Start_Of_Rect[0],Data[1][0]),min(Start_Of_Rect[1],Data[1][1]),abs(Start_Of_Rect[0]-Data[1][0]),abs(Start_Of_Rect[1]-Data[1][1])))
                                                                    #Current_Mouse_Pos
        #------------------------------------------

        #Check for Lock_On and Movement of the camera
        #------------------------------------------
        Return=self.Lock_On(Data[0],Selected_Lists[self.__Attributes["Team"]],Attributes)
        print(Return)
        
        if Return==False:#Do all of the things required when true inside this function!

            #Move
            #------------------------------------------
            self.Move(Data[1])#Mouse_Pos
            #------------------------------------------
            
        else:

            #Draw range circle
            #------------------------------------------
            #FIX!!! #Change to red when an enemy unit is in range!
            #Gray if no enemy is within range, and red if there is at least one in range
            print(self.__Attributes["Selected"], "Selected unit!!!")
            Location=[(Attributes[Selected_Lists[self.__Attributes["Team"]][self.__Attributes["Selected"]]][1]*256)+Attributes[Selected_Lists[self.__Attributes["Team"]][self.__Attributes["Selected"]]][2],(Attributes[Selected_Lists[self.__Attributes["Team"]][self.__Attributes["Selected"]]][3]*256)+Attributes[Selected_Lists[self.__Attributes["Team"]][self.__Attributes["Selected"]]][4]]

            Change=[0,0]
            #Change the location of the range circle on the screen when the unit is near the edge of the map!
            #print(Location)
            if (Location[0]*Settings["SCALE"])<Settings["WIDTH"]//2:#x-axis
                #print("Left side!!!")
                Change[0]=(Settings["WIDTH"]//2)-(Location[0]*Settings["SCALE"])

            elif ((SIZE[0]-(Location[0]))*Settings["SCALE"])<Settings["WIDTH"]//2:
                #print("right side!!!")
                Change[0]=(Settings["WIDTH"]//2)-((SIZE[0]-(Location[0]))*Settings["SCALE"])

            if (Location[1]*Settings["SCALE"])<Settings["HEIGHT"]//2:#y-axis
                #print("top!!!")
                Change[1]=(Settings["HEIGHT"]//2)-(Location[1]*Settings["SCALE"])

            elif ((SIZE[1]-(Location[1]))*Settings["SCALE"])<Settings["HEIGHT"]//2:
                #print("Bottom!!!")
                Change[1]=(Settings["HEIGHT"]//2)-((SIZE[1]-(Location[1]))*Settings["SCALE"])

            #print(Change, "CHANGE!!!")                                                                                                                                    #Radius of the circle #Range of selected unit:             #ID of the selected_Unit                                           #Value of range in Records_Data (each section is contained in 2 lists at the moment, therefore more indexes are needed!!!
            pygame.draw.circle(self.image,(50,50,50,255),[(Settings["WIDTH"]//2)+14-Change[0],(Settings["HEIGHT"]//2)+14-Change[1]],   int(Records_Data[Attributes[Selected_Lists[self.__Attributes["Team"]][self.__Attributes["Selected"]]][0]][3][0][5]),0)
            #------------------------------------------

            #Update Info bar #Max size of 8 units
            #------------------------------------------
            self.image.fill((200,200,200,255), (0,(Settings["HEIGHT"]-int(1/Settings["INFO_BAR_SIZE"]*Settings["HEIGHT"])),Settings["WIDTH"],Settings["HEIGHT"]))
            print(len(Selected_Lists[self.__Attributes["Team"]]), "LENGTH!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            for x in range(len(Selected_Lists[self.__Attributes["Team"]])):

                #Highlight the currently selected unit
                if x ==self.__Attributes["Selected"]:
                    #Change the colour depending on the team of the unit

                    #FIX - Keep track of the different team colours for multi-player, then use this colour to determine this colour
                    #print(Attributes, "ATTRIBUTES!!!")#Doesn't yet contain the team
                    #print(abc)

                    #Colour=Colours[   Attributes[Selected_Lists[self.__Attributes["Team"]][x]]   ["Team"]

                    self.image.fill((50,50,50,255),( int((Settings["WIDTH"]*((x%4)/5))), int(Settings["HEIGHT"]-((1/Settings["INFO_BAR_SIZE"])*Settings["HEIGHT"])+((x//4)*int(((1/Settings["INFO_BAR_SIZE"])*Settings["HEIGHT"])//2))), int((Settings["WIDTH"]*(1/5))), int(((1/Settings["INFO_BAR_SIZE"])*Settings["HEIGHT"])//2)))
                    ###
                    
                print("LOOP:", x)
                #Attributes contains: [ID,Location[0]//256,Location[0]%256,Location[1]//256,Location[1]%256,Direction,State,Level,Current_Health,Current_Exp,Current_Frame, [Null]] for each unit
                #Image of the sprite                                    #ID of Selected unit                                    #State of selected unit                                         #Current frame of selected unit
                Image=pygame.transform.scale(IMAGES[int(Records_Data[Attributes[Selected_Lists[self.__Attributes["Team"]][x]][0]][2][Attributes[Selected_Lists[self.__Attributes["Team"]][x]][7]][Attributes[Selected_Lists[self.__Attributes["Team"]][x]][11]])], (Settings["WIDTH"]//20, int(Settings["HEIGHT"]*(0.25/Settings["INFO_BAR_SIZE"])) ))
                Top_Left=[int((Settings["WIDTH"]*((x%4)/5))+Settings["WIDTH"]//10),int(Settings["HEIGHT"]-((1/Settings["INFO_BAR_SIZE"])*Settings["HEIGHT"])+((x//4)*int(((1/Settings["INFO_BAR_SIZE"])*Settings["HEIGHT"])//2))+int(Settings["HEIGHT"]*((1/Settings["INFO_BAR_SIZE"])))//16)]
                Bottom_Right=[Top_Left[0]+Settings["WIDTH"]//20,Top_Left[1]+int(Settings["HEIGHT"]*(0.25/Settings["INFO_BAR_SIZE"]))]
                #print(Top_Left,Bottom_Right)
                self.image.blit(Image, (Top_Left[0],Top_Left[1]))

                #Hp bar of the sprite
                Split_Health=int((Attributes[Selected_Lists[self.__Attributes["Team"]][x]][9]/int(Records_Data[Attributes[Selected_Lists[self.__Attributes["Team"]][x]][0]][3][0][0])))#*((Settings["WIDTH"]//20)-1))#Split between drawing in different colours                                                                                                         #Current health / #Health stat of the selected unit *Width of the bar ([ID][Stats][particular stat])                
                self.image.fill((50,50,50,50), (Top_Left[0]-1,Bottom_Right[1]+5, (Settings["WIDTH"]//20)+1,5) )
                self.image.fill((0,255,0,255), (Top_Left[0],Bottom_Right[1]+6,Split_Health*((Settings["WIDTH"]//20)-1),3))
                self.image.fill((255,0,0,255), (Top_Left[0]+Split_Health*((Settings["WIDTH"]//20)-1),Bottom_Right[1]+6,int((1-Split_Health)*((Settings["WIDTH"]//20)-1)),3))

                #Exp bar of the sprite
                Split_Exp=int((Attributes[Selected_Lists[self.__Attributes["Team"]][x]][10]/int(Records_Data[Attributes[Selected_Lists[self.__Attributes["Team"]][x]][0]][3][0][7])))#*((Settings["WIDTH"]//20)-1))#Split between drawing in different colours                                                                                                         #Current health / #Health stat of the selected unit *Width of the bar ([ID][Stats][particular stat])

                self.image.fill((50,50,50,50), (Top_Left[0]-1,Bottom_Right[1]+11, (Settings["WIDTH"]//20)+1,5) )
                self.image.fill((0,0,255,255), (Top_Left[0],Bottom_Right[1]+12,Split_Exp*((Settings["WIDTH"]//20)-1),3))
                self.image.fill((255,0,0,255), (Top_Left[0]+Split_Exp*((Settings["WIDTH"]//20)-1),Bottom_Right[1]+12,int((1-Split_Exp)*((Settings["WIDTH"]//20)-1)),3))

            #Display the locked_on sprite's stats #FINISH!!!
            #------------------------------------------
            #Unit's stats circle
            self.image.fill((150,150,150,255), (int(Settings["WIDTH"]*4/5), (Settings["HEIGHT"]-int(1/Settings["INFO_BAR_SIZE"]*Settings["HEIGHT"])),int(Settings["WIDTH"]*1/5),int(1/Settings["INFO_BAR_SIZE"]*Settings["HEIGHT"])))
            pygame.draw.circle(self.image,(50,50,50,255),(int(Settings["WIDTH"]*9/10),(Settings["HEIGHT"]-int((1/2)*(1/Settings["INFO_BAR_SIZE"]*Settings["HEIGHT"])))),60)

            #------------------------------------------
            
            #------------------------------------------

            #Update Actions menu
            #------------------------------------------
            self.image.fill((255,255,255,50), (0,0,Settings["WIDTH"]//4,Settings["HEIGHT"]//4))
            #------------------------------------------


        #------------------------------------------

        #Update Minimap        #MINI_MAP_SIZE=4 #INFO_BAR_SIZE=4 # Settings
        #------------------------------------------
        #Determining what to display as the minimap and where
        RECT=pygame.Rect((Settings["WIDTH"]-int((1/Settings["MINI_MAP_SIZE"])*Settings["WIDTH"])),0,Settings["WIDTH"]//Settings["MINI_MAP_SIZE"],Settings["HEIGHT"]//Settings["MINI_MAP_SIZE"])
        IMAGE=pygame.transform.scale(SUBSCREEN,(Settings["WIDTH"]//Settings["MINI_MAP_SIZE"],Settings["HEIGHT"]//Settings["MINI_MAP_SIZE"]))
        
        #Boarder of the minimap
        self.image.fill((50,50,50),((Settings["WIDTH"]-int((1/Settings["MINI_MAP_SIZE"])*Settings["WIDTH"])),0,Settings["WIDTH"]//Settings["MINI_MAP_SIZE"],Settings["HEIGHT"]//Settings["MINI_MAP_SIZE"]))
        #The minimap
        self.image.blit(IMAGE,RECT)#,special_flags=pygame.BLEND_RGBA_ADD)#((Settings["WIDTH"]-(int(1/Settings["MINI_MAP_SIZE"])*Settings["WIDTH"])),0))#RECT)
        self.rect=pygame.Rect(0,0,Settings["WIDTH"],Settings["HEIGHT"])
        #------------------------------------------

        #Position validation 
        #------------------------------------------
        #Makes sure the camera isn't out of bounds!
        Return=Object.Position_Validation(self,self.__Attributes["Location"],[self.__Attributes["Location"][0]+(Settings["WIDTH"]/Settings["SCALE"]),self.__Attributes["Location"][1]+(Settings["HEIGHT"]/Settings["SCALE"])],[Settings["WIDTH"]//Settings["SCALE"],Settings["HEIGHT"]//Settings["SCALE"]],[self.__Attributes["Location"][0]+(Settings["WIDTH"]/(2*Settings["SCALE"])),self.__Attributes["Location"][1]+(Settings["HEIGHT"]/(2*Settings["SCALE"]))])
        #print(Return)
        self.__Attributes["Speed"]=[self.__Attributes["Speed"][0]*Return[1][0][0],self.__Attributes["Speed"][1]*Return[1][1][0]]
        self.__Attributes["Location"]=[Return[0][0]-(Settings["WIDTH"]/(2*Settings["SCALE"]))+Return[2][0],Return[0][1]-(Settings["HEIGHT"]/(2*Settings["SCALE"]))+Return[2][1]]
        #print("POSITION!!!", self.__Attributes["Location"],[self.__Attributes["Location"][0]+(Settings["WIDTH"]/Settings["SCALE"]),self.__Attributes["Location"][1]+(Settings["HEIGHT"]/Settings["SCALE"])])
        #print("SPEED!!!", self.__Attributes[1])
        #------------------------------------------


    def Move(self,Mouse_Pos):#Use Object.Get_Attributes(self) to obtain the attributes for the camera!

        Deceleration=1/Settings["SCALE"]#Setting #Make sure both the Accel and Decel are even numbers to prevent jittering of the camera!

        #gradual decceleration until the camera stops moving
        #------------------------------------------
        if self.__Attributes["Speed"][0]>0:#SpeedX
            self.__Attributes["Speed"][0]-=Deceleration
            if self.__Attributes["Speed"][0]<0:
                self.__Attributes["Speed"][0]=0
        elif self.__Attributes["Speed"][0]<0:
            self.__Attributes["Speed"][0]+=Deceleration
            if self.__Attributes["Speed"][0]>0:
                self.__Attributes["Speed"][0]=0
            
        if self.__Attributes["Speed"][1]>0:#SpeedY
            self.__Attributes["Speed"][1]-=Deceleration
            if self.__Attributes["Speed"][1]<0:
                self.__Attributes["Speed"][1]=0
        elif self.__Attributes["Speed"][1]<0:
            self.__Attributes["Speed"][1]+=Deceleration
            if self.__Attributes["Speed"][1]>0:
                self.__Attributes["Speed"][1]=0
        #------------------------------------------
     
        #Acceleration depending on mouse position
        #------------------------------------------
        if Mouse_Pos[0]>(Settings["WIDTH"]-50):#Move left (scroll camera right)
            self.__Attributes["Speed"][0]+=self.__Attributes["Acceleration"]#self.Camera_Speedx-=Camera_Accel
            #print("MOVE RIGHT!!!")            
        elif Mouse_Pos[0]<50:#Move right (scroll camera left)
            self.__Attributes["Speed"][0]-=self.__Attributes["Acceleration"]#Camera_Speedx+=Camera_Accel
            #print("MOVE LEFT!!!")
        if Mouse_Pos[1]<50:#Move downwards (scroll camera downwards)
            self.__Attributes["Speed"][1]-=self.__Attributes["Acceleration"]#Camera_Speedy-=Camera_Accel
            #print("MOVE UP!!!")
        elif Mouse_Pos[1]>(Settings["HEIGHT"]-50):#Move upwards (scroll camera upwards)
            self.__Attributes["Speed"][1]+=self.__Attributes["Acceleration"]#Camera_Speedy+=Camera_Accel
            #print("MOVE DOWN!!!")
        #------------------------------------------


        #Speed validation
        #------------------------------------------
        if self.__Attributes["Speed"][0]>Settings["MAX_CAMERA_SPEED"]:
            self.__Attributes["Speed"][0]=Settings["MAX_CAMERA_SPEED"]
        elif self.__Attributes["Speed"][0]<-Settings["MAX_CAMERA_SPEED"]:
            self.__Attributes["Speed"][0]=-Settings["MAX_CAMERA_SPEED"]
            
        if self.__Attributes["Speed"][1]>Settings["MAX_CAMERA_SPEED"]:
            self.__Attributes["Speed"][1]=Settings["MAX_CAMERA_SPEED"]
        elif self.__Attributes["Speed"][1]<-Settings["MAX_CAMERA_SPEED"]:
            self.__Attributes["Speed"][1]=-Settings["MAX_CAMERA_SPEED"]
        #------------------------------------------
            
        #Move camera
        #------------------------------------------
        self.__Attributes["Location"][0]+=self.__Attributes["Speed"][0]#//Scale#
        self.__Attributes["Location"][1]+=self.__Attributes["Speed"][1]#//Scale#

        #print(self.__Attributes[0],"LOCATION")
        #print(self.__Attributes[1], "SPEED")
        #------------------------------------------

    def Lock_On(self,Key_State,Selected_List,Attributes):
        #Attributes contains: [ID,Location[0]//256,Location[0]%256,Location[1]//256,Location[1]%256,Direction,State,Level,Current_Health,Current_Exp,Current_Frame, [Null]] for each unit

        #If any units are selected, then the unit in the position of the "Selected" attribute will be locked onto!
        #If shift is held down, then no unit will be locked onto. This will be done so that the player can select a far away distance for the selected units to travel to!

        Locked_On=False

        #print(Selected_List, "SELECTED TEST!!!")
        if len(Selected_List)>0:
            self.__Attributes["Selected"]==self.__Attributes["Selected"]%len(Selected_List)

            #Tab controls!!!
            if Key_State[pygame.K_TAB]==1:
                print("PRESSING TAB KEY!!! NOW PRESS 1-8!!!")
                for x in range(8):#Selects the highest key that is pressed down in the event of multiple keys being pressed simultaneously
                    #print(x)
                    if Key_State[pygame.K_1+x]==1 and (x+1)<=len(Selected_List):#keys 1 through 0 inclusive on the keyboard [1,2,3,4,5,6,7,8,9,0]
                        self.__Attributes["Selected"]=x
                    #else:
                    #    print("INVALID UNIT SELECTION!!!")
                        
            if Key_State[pygame.K_LSHIFT]==0 and Key_State[pygame.K_RSHIFT]==0:#Only lock on if shift isn't held down

                #print(Attributes, "ATTRIBUTES!!!")
                Location=[(Attributes[Selected_List[self.__Attributes["Selected"]]][1]*256)+Attributes[Selected_List[self.__Attributes["Selected"]]][2],(Attributes[Selected_List[self.__Attributes["Selected"]]][3]*256)+Attributes[Selected_List[self.__Attributes["Selected"]]][4]]
            
                self.__Attributes["Location"]=[Location[0]-Settings["WIDTH"]/(2*Settings["SCALE"]),Location[1]-Settings["HEIGHT"]/(2*Settings["SCALE"])]#Location=Sprite's location adjusted so that it lies in the center of the screen!
                self.__Attributes["Speed"]=[0,0]#Reset speed
                #self.__Attributes["Acceleration"]=0
                print("LOCKED ON!!!")
                Locked_On=True

        return Locked_On

    def Display_Info(self,SPRITE):
        print("HI")

#----------------------------------------------------------


#----------------------------------------------------------
class Sprite(Object,pygame.sprite.Sprite):

    def __init__(SPRITE,  ID, Location, Team, Target, Level, Records, Mode, Index):

        #Complete List Of Atttributes: [Location,[Size_X,Size_Y],[Mode/control],Rect,State,Animations,Level,Stats,Team]
        #---------------------------------------
        SPRITE.__Attributes=Object.__init__(SPRITE,  ID, Location, Team, Target, Level, Records, Mode, Index)
        #print(SPRITE.__Attributes)
        pygame.sprite.Sprite.__init__(SPRITE)
        #---------------------------------------

        #Image
        #---------------------------------------
        SPRITE.rect=pygame.Rect(SPRITE.__Attributes["Location"][0]-(SPRITE.__Attributes["Size"][0]//2),SPRITE.__Attributes["Location"][1]-(SPRITE.__Attributes["Size"][1]//2),SPRITE.__Attributes["Size"][0],SPRITE.__Attributes["Size"][1])
        SPRITE.rect.center=(SPRITE.__Attributes["Location"][0],SPRITE.__Attributes["Location"][1])

        #For testing purposes!!!
        #---------------------------------------
        #self.image=pygame.Surface((self.__Attributes[1][0],self.__Attributes[1][1]))
        #self.image.fill((0,255,0))
        #self.origional_image=self.image
        #self.rect=self.image.get_rect()
        #self.rect.center=self.__Attributes[0]


        #print(SPRITE.__Attributes["Animations"])
        #self.image=pygame.transform.scale(self.image,(self.__Attributes[1][0],self.__Attributes[1][1]))#change size of image
        #SPRITE.image.set_colorkey(000,0)#make this colour (black) transparent using RGB values
        #SPRITE.origional_image=SPRITE.image#Used for rotation

        #---------------------------------------
        print("MADE SPRITE!!!")

        if SPRITE!=Sprite:
            print("NOT A SPRITE!!!")
            return SPRITE.__Attributes

    def Get_Attributes(self):

        #------------------------------------------
        return self.__Attributes
        #------------------------------------------

    def Set_Attributes(self,Attributes,Values):
        
        #------------------------------------------
        self.__Attributes=Object.Set_Attributes(self,self.__Attributes,Attributes,Values)
        #------------------------------------------




    def update(SPRITE):
        #Updates the frame of animation the sprite will display
        #Makes sure the sprite is in-bounds

        #Image
        #---------------------------------------
        SPRITE.__Attributes["Frame"]=(SPRITE.__Attributes["Frame"]+1)%Settings["FPS"]#use interpolation here!!!
        SPRITE.__Attributes["Current_Frame"]=round((SPRITE.__Attributes["Frame"]/Settings["FPS"])*(len(SPRITE.__Attributes["Animations"][SPRITE.__Attributes["State"]])-1)) #the -1 is because list indexing starts at 0 rather than 1!!!        
        #---------------------------------------

        #Position validation (Makes sure the sprite isn't out of bounds or on an invalid tile!)
        #------------------------------------------ #Top left of the sprite
        Return=Object.Position_Validation(SPRITE,[SPRITE.__Attributes["Location"][0]-(SPRITE.__Attributes["Size"][0]/2),SPRITE.__Attributes["Location"][1]-(SPRITE.__Attributes["Size"][1]/2)],[SPRITE.__Attributes["Location"][0]+(SPRITE.__Attributes["Size"][0]/2),SPRITE.__Attributes["Location"][1]+(SPRITE.__Attributes["Size"][1]/2)],SPRITE.__Attributes["Size"],SPRITE.__Attributes["Location"])
        SPRITE.__Attributes["Location"]=Return[0] #Location adjusted for the sides of the screen        
        SPRITE.rect.center=(SPRITE.__Attributes["Location"][0],SPRITE.__Attributes["Location"][1])
        #print(Return)
        #------------------------------------------

#----------------------------------------------------------


#----------------------------------------------------------
class Unit(Sprite):
        #self.Add_Sprite(Unit([[300,300],[5,5],[1,1],[0,0],0,[[0,0,0,0,1,1,1,1],[0,1,2,3,4,5,6,7]],1,[1,0,0,0,0,0,0,0],0,2,0,1]),0)
                                                               #list of animations (image numbers)
                                                               #Animations: 0. Idle, 1. Moving, 2. Attacking, 3. Getting hit(flash of white), 4. Building
    def __init__(self, ID, Location, Team, Target, Level, Records, Mode, Index):

        #Complete List Of Atttributes: [Location,[Size_X,Size_Y],[Mode/control],Rect,State,Animations,Level,Stats,Team]
        #---------------------------------------
        self.__Attributes=Sprite.__init__(self, ID, Location, Team, Target, Level, Records, Mode, Index)
        print("UNIT ATTRIBUTES", self.__Attributes)
        #self.image=pygame.transform.scale(self.image,(self.__Attributes["Size"][0],self.__Attributes["Size"][1]))#change size of image

        #Attributes that shouldn't be altered by the player!
        self.__Speed=[0,0]#Not the Unit's speed stat! Used to calculate the movement of the unit based on the speed stat (Which is the first value in self.__Attributes[8])!

        self.__Previous_Location=[0,0]
        self.__Reset=0#Reset from damaged animation
        self.__Previous_State=0#State to return to after any damage has been taken

        #if Attributes[9]!=2:#If the type is not a unit (E.G. using the Unit init function through inheritance)
        #    return self.__Attributes

        #print(self.__Attributes)
        #print(self.rect)
        #---------------------------------------
        
    def Get_Attributes(self):

        #------------------------------------------
        return self.__Attributes
        #------------------------------------------

    def Set_Attributes(self,Keys,Values):
        
        #------------------------------------------
        #print(Keys,Values)
        #print(self.__Attributes)
        Attacked=Object.Set_Attributes(self,Keys,Values)
        self.__Attributes["Attacked"]=Attacked#Check to see if the unit has been attacked or not. This acts as a flag that will be reset in the Check_Attack method!
        #------------------------------------------
        #print(self.__Attributes)

    def update(self,Data,Selected_Lists, Map_Data):
        #A sprite will update based on its team's input
        #The data is the data from each client
        #Data: [Key_State, Mouse_Pos relative to the game environment, Mouse_State] for each client!
        #print(Data)

        #---------------------------------------
        #Keystate=pygame.key.get_pressed()#This will be done in the game loop!
        Return=self.Check_Mode(Data,Selected_Lists)

        if type(Data[self.__Attributes["Team"]])!=int and self.__Attributes["State"]!=4:#If the sprite's team is not responding to the server, then an integer will be sent instead of the player's input. This means that the sprite doesn't need to check it's movement this frame!
            self.Check_Movement(Data[self.__Attributes["Team"]],Map_Data)

            self.Check_Attack(Data[self.__Attributes["Team"]][0])


        self.Check_Stats()#Includes health and exp!

        Sprite.update(self)#Includes updating the frames of animation along with the position validation

        #print("TILE NUMBER!!!", Map_Data[0][self.__Attributes["Location"][1]//20][self.__Attributes["Location"][0]//20])
        #[0], since the tiles will only change when animation is implemented, in which the additional tiles will have the same properties as those present on frame 0!
        #REMEMBER the tiles in Map_Data are all held as strings NOT integers!!!
        if Map_Data[0][self.__Attributes["Location"][1]//20][self.__Attributes["Location"][0]//20] in self.__Attributes["Invalid_Tiles"]:#FIX to include all invalid tiles for a particular sprite!!!
            self.Move_Back()
            print("Should have moved back!!!")

        #---------------------------------------


    def Check_Mode(self,Data,Selected_Lists):#Checks the mode of the sprite, along with resetting the damaged animation!        #These are updated when the right click is held down!
        #Data[x]: [Key_State, Mouse_Pos adjusted for the camera position, Mouse_State, Previous_Mouse_Pos, Previous_Mouse_State,Start_Pos,End_Pos] for team x
        #Selected_Lists should be passed by reference!!!

        #print(Data, "DATA!!!")
        print(Selected_Lists, "SELECTED LISTS!!!")
        
        #Change the animations of the sprites
        #------------------------------------------
        if self.__Attributes["State"]==3:#Damaged
            self.__Reset+=1#Used to reset the animation to its previous state after 1 frame, making the sprite flash white
            #print(self.__Reset, "RESET")

        elif self.__Attributes["State"]==4:#Defeated
            self.__Attributes["Cooldown_Timer"]-=1#Used to delete the unit
            #print("COOLDOWN!!!", self.__Attributes["Cooldown_Timer"])

        if self.__Reset>1:#If the unit was damaged the previous frame
            self.__Attributes["State"]=self.__Previous_State
            self.__Reset=0
            #print(self.__Attributes["State"], "STATE!!!")
            #self.__Attributes["State"]=0
        #------------------------------------------
        
        #Change the modes of the sprites
        #------------------------------------------
        for x in range(len(Data)):#x is the team number!
 
            if type(Data[x])==int:#This must be done, since each input is processed, rather than just the input from the sprite's team!
                #print("INVALID DATA FROM TEAM", x)
                pass

            else:
                #Used to calculate whether a mouse press is inside the sprite
                Left=self.__Attributes["Location"][0]-(self.__Attributes["Size"][0]//2)
                Top=self.__Attributes["Location"][1]-(self.__Attributes["Size"][1]//2)

                #Left click
                #------------------------------------------
                    #Mouse_State[0]
                if Data[x][2][0]==1:#If left mouse butten is pressed down
                    
                    #Left click + Shift
                    #------------------------------------------
                    #Regardless of the mode, if selected and this is received by its team's camera, then the unit will change to mode 2
                        #Key_State[pygame.K_LSHIFT] etc.
                    if  (Data[x][0][pygame.K_LSHIFT] or Data[x][0][pygame.K_RSHIFT])==True:
                        print("LEFT CLICK + SHIFT!!!")
                        print(Selected_Lists, "SELECTED LISTS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        if self.__Attributes["Index"] in Selected_Lists[x]:
                            print("YEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEES!!!")
                            print(bool(self.__Attributes["Team"]==x and self in Selected_Lists[x]))

                        if (self.__Attributes["Team"]==x and self in Selected_Lists[x]):
                            #If selected by its team's camera:
                            print("IT WORKS!!!")
                            
                            #Change to mode 2
                            self.__Attributes["Mode"]=2
                            #print(Data[x], "DATA", x)
                            self.__Attributes["Target"]=Data[x][1]#Mouse position adjusted for camera position
                            print("TARGET", self.__Attributes["Target"], "LOCATION", self.__Attributes["Location"])
                            self.__Attributes["Path"]=[]#This will allow the unit to immediately change its target without ending up in the wrong location
                            print("CHANGE TO MODE 2!!!!")
                    #------------------------------------------
                        #CRASHES HERE!!!
                    #Just left click
                    #------------------------------------------
                    #This depends on the mode of the unit
                    
                    else:
                        print("LEFT CLICKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK!!!", self.__Attributes["Mode"])
                        #If in mode 0 or 2
                        #------------------------------------------
                        #If inside the unit, change mode to mode 1 if on the same team
                        #Then, regardless of the team, deselect all of that team's units and select this unit by itself
                        print(Selected_Lists, "SELECTED LISTS")
                        print(self.__Attributes["Mode"], "MODE!!!")
                        print("TESTING:", Data[x][1], Left, Left+self.__Attributes["Size"][0])


                        #Check if the click is inside the unit
                            #Mouse_Pos[0]                                                             #Mouse_Pos[1]
                        if ((Data[x][1][0]*256)+Data[x][1][1]) in range(Left,(Left+self.__Attributes["Size"][0])) and ((Data[x][1][2]*256)+Data[x][1][3]) in range(Top,(Top+self.__Attributes["Size"][1])):
                            print("Team:", x, "pressed the left mouse button at", Data[x][1])
                            #print("TOP LEFT", Left,Top)
                        
                            if self.__Attributes["Mode"]!=1:


                                #Change modes if the same team as the camera
                                if self.__Attributes["Team"]==x:
                                    self.__Attributes["Mode"]=1
                                    #reset movement if in mode 2
                                    self.__Attributes["Target"]=[-1,-1]
                                    self.__Attributes["Path"]=[]

                                #Remove all other selected units # Done in the server!!!


                                #Select the unit
                                #try:
                                Selected_Lists[x].append(self.__Attributes["Index"])
                                print("ADDED UNIT TO SELECTED LISTS!!!", Selected_Lists)
                                #except len(Selected_Lists[x])>8:#Return an error message if the length of the selected list is too long!
                                    #print("Selected_List", x, "is full!!!")
                                
                        #------------------------------------------

                        #If in mode 1
                        #------------------------------------------
                        #If outside the unit, change mode to mode 0 if on the same team
                        #Then, regardless of the team, deselect this unit
                        elif self.__Attributes["Mode"]==1:
                            print("MOOOOOOOOOOOOOOOOOODE 1!!!", Data[x][1], Left, Left+self.__Attributes["Size"][0], Top, Top+self.__Attributes["Size"][1])
                            
                            #Change modes if the same team as the camera
                            if self.__Attributes["Team"]==x:
                                self.__Attributes["Mode"]=0

                            #De-select the unit
                            print(self.__Attributes["Mode"])
                            try:
                                Selected_Lists[x].remove(self.__Attributes["Index"])
                            except ValueError:#Return an error message if the length of the selected list is too long!
                                print("Selected_List", x, "doesn't contain this sprite!!!")
                        #------------------------------------------
                #------------------------------------------

                #Right click
                #------------------------------------------#Finish11!!!
                #If shift is held down, the camera will not lock onto any units!!!

                #A rect box will be created by the client's camera whilst they hold down right click.
                #Once they have released right click. The unit will check if its location is inside the boundaries between the start and end position

                #If inside the rect, select the unit if the selected list is not full!
                #This will be done on the client side except for when there is both a start and end position is present

                #If right mouse butten has been held down and the sprite is in range of the rect created, then select it regardless of the mode or team
                        #Start of hold                                                      End of hold
                Hold=[(Data[x][5][0]*256)+Data[x][5][1],(Data[x][5][2]*256)+Data[x][5][3],(Data[x][6][0]*256)+Data[x][6][1],(Data[x][6][2]*256)+Data[x][6][3]]#Locations of the selection box created when holding right click
                
                    #Mouse_State[1]      #Previous_Mouse_State[1]                                       #Start of hold[0],End of hold[0]                                                                    #Start of hold[1],End of hold[1]
                if (Data[x][2][2]==0 and Data[x][4][2]==1) and self.__Attributes["Location"][0] in range(int(min(Hold[0],Hold[2])), int(max(Hold[0],Hold[2]))) and self.__Attributes["Location"][1] in range(int(min(Hold[1],Hold[3])),int(max(Hold[1],Hold[3]))):
                    if len(Selected_Lists[x])<8:#If not full
                        Selected_Lists[x].append(self.__Attributes["Index"])
                        print("ADDED UNIT!!!")
                #------------------------------------------
        #------------------------------------------
                        
    def Check_Movement(self,Data,Map_Data):
        #Data: [Key_State, Mouse_Pos, Mouse_State, Camera_Pos] for each client!
        #print(Data)

        #print(self.rect.center)
        self.__Previous_Location=self.rect.center
                
        #Mode 0
        #---------------------------------------
        #Do nothing
        #---------------------------------------

        #Mode 1
        #---------------------------------------
        #Move depending on the keyboard input
        if self.__Attributes["Mode"]==1:#mode

            #Movement speed
            #---------------------------------------
                                #Stats[Speed]                       Key_State[pygame.K_RIGHT] etc.
            self.__Speed[0]=self.__Attributes["Stats"]["Speed"]*((Data[0][pygame.K_RIGHT] or Data[0][pygame.K_d])-(Data[0][pygame.K_LEFT] or Data[0][pygame.K_a]))
                            #Upwards movement-downwards movement
            self.__Speed[1]=self.__Attributes["Stats"]["Speed"]*((Data[0][pygame.K_DOWN] or Data[0][pygame.K_s])-(Data[0][pygame.K_UP] or Data[0][pygame.K_w]))
            ##---------------------------------------

            #Direction
            #---------------------------------------
            Direction_x=90*((Data[0][pygame.K_RIGHT] or Data[0][pygame.K_d])-(Data[0][pygame.K_LEFT] or Data[0][pygame.K_a]))
            Direction_y=45*((Data[0][pygame.K_DOWN] or Data[0][pygame.K_s])-(Data[0][pygame.K_UP] or Data[0][pygame.K_w]))

            if Direction_x==90:
                self.__Attributes["Direction"]=Direction_x+Direction_y
                
            elif Direction_x==-90:
                self.__Attributes["Direction"]=Direction_x-Direction_y
                
            elif Direction_y!=0:#This should allow the sprite to face the same direction that it will travel in when no keys are pressed!
                                    #downwards direction check
                self.__Attributes["Direction"]=0-180*(Data[0][pygame.K_DOWN] or Data[0][pygame.K_s])

            #print(self.__Attributes["Direction"])
            #---------------------------------------
        #---------------------------------------

        #Mode 2
        #---------------------------------------
        elif self.__Attributes["Mode"]==2:
            #print("THREADS:", self.__Attributes["Threads"])

            #Decide what to do
            #------------------------------------------
            if self.__Attributes["Location"]==self.__Attributes["Target"]:
                #Change to mode 0
                self.__Attributes["Mode"]=0
                #Reset threads attribute
                self.__Attributes["Threads"]=0
                #Reset the path attribute
                self.__Attributes["Path"]=[]

            elif len(self.__Attributes["Path"])==0:#If no threads or path and the current location isn't equal to the target location, then create a thread
                if self.__Attributes["Threads"]==0:
                    #Create a shortest path
                    self.__Attributes["Threads"]+=1
                    print("SHORTEST PATH!!!")
                    Shortest_Path_Algorithm=Thread(self.Shortest_Path,Map_Data)
                    #Shortest_Path_Algorithm.start()#Automatically changes the path attribute of the unit, then resets the threads attribute
                    print(self.__Attributes["Path"], "Path in the main thread!!!")
                    print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")

            else:#Move depending on the path created
                print("PATH WHEN MOVING!!!", self.__Attributes["Path"])
                self.__Attributes["Location"]=[self.__Attributes["Location"][0]+self.__Attributes["Path"][0][0],self.__Attributes["Location"][1]+self.__Attributes["Path"][0][1]]
                del self.__Attributes["Path"][0]#remove index 0!!!
                print(self.__Attributes["Path"], "PATH NOW!!!")
            #------------------------------------------
                
        #---------------------------------------
        
        #---------------------------------------

        
        #calculate movement (All modes)
        #---------------------------------------
        self.__Attributes["Location"]=[self.__Attributes["Location"][0]+self.__Speed[0],self.__Attributes["Location"][1]+self.__Speed[1]]
        #self.rect.center=self.__Attributes[0]#Thhis will be done when calling the sprite update function!
        #---------------------------------------

        #move the rect (All modes)
        #---------------------------------------               
        #The rect itself doesn't change!
        self.rect.center=self.__Attributes["Location"][0],self.__Attributes["Location"][1]
        #---------------------------------------

    def Move_Back(self):#Return to previous location
        #print(self.__Previous_Location,self.__Attributes["Location"])
        self.rect.center=self.__Previous_Location
        self.__Attributes["Location"]=[self.rect.center[0],self.rect.center[1]]
        #print(self.rect.center,"UPDATED!")
        
    def Check_Attack(self,Key_State):
        #Key_State of the unit's team used in mode 1
        #A check for any collisions will occur in the main game loop

        #print(self.__Attributes["In_Range"])
        #print(Key_State[pygame.K_SPACE], "SPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACE!!!")
        if len(self.__Attributes["In_Range"])>0:
            
            #Mode 0
            #---------------------------------------
            #If attacked, automatically attack back via cpu(switch to mode 2)
            #Team checking will occur here
            if self.__Attributes["Mode"]==0:
                self.__Attributes["Mode"]=2
                self.__Attributes["Target"]=self.__Attributes["Location"]#Make sure the unit doesn't move until the unit has checked its target in mode 2!
            #---------------------------------------
            #Mode 1
            #---------------------------------------
            #If space bar pressed, do attack animation and check the 1/4 circle radius for any other sprite from another team. If any collisions occur, set that unit's health to a lower ammount dependent on the attack stat etc
            #The range circle will appear red#THIS WILL BE DONE BY THE CAMERA!!!
            elif self.__Attributes["Mode"]==1:
                if Key_State[pygame.K_SPACE]==1:# or (self.__Attributes["Mode"][0]==1 and self.__Attributes["Action"]=="Attack")):#NOT#Test for the right team will be done in the collision detection!

                    #Change to attack animation
                    #---------------------------------------
                    if self.__Attributes["State"] not in [2,3]:#If not already attacking, being damaged or dead
                        self.__Attributes["Cooldown_Timer"]=0

                        self.__Attributes["State"]=2#Attacking
                    #print(self.__Attributes["Cooldown_Timer"])
                    #---------------------------------------
                    
                    #Function depends on the unitID of the unit!!!
                    #---------------------------------------
                    if self.__Attributes["ID"] in range(0,5) and self.__Attributes["Cooldown_Timer"]==0:#Attack the closest enemy

                        #for x in range(len(self.__Attributes["Multi-target"])):
                        x=0
                        y=0
                        while (y!=self.__Attributes["Stats"]["Multi-target"] and x<len(self.__Attributes["In_Range"])):
                            Attributes=self.__Attributes["In_Range"][x][1].Get_Attributes()
                            if Attributes["Team"]!=self.__Attributes["Team"] and Attributes["Current_Health"]>0:
                                Attributes["Current_Health"]-=(self.__Attributes["Stats"]["Attack"]-Attributes["Stats"]["Defence"])
                                if Attributes["Current_Health"]<0:
                                    Attributes["Current_Health"]=0
                                self.__Attributes["In_Range"][x][1].Set_Attributes(["Stats","State"],[Attributes["Stats"],3])

                                #if Attributes["Stats"]["Health"]>0:#If the sprite isn't already defeated
                                self.__Attributes["Attacking"].append([Attributes["Location"],(0,0,254)])#Allows a line to be drawn from the center of the sprite to this sprite's location
                                print(Attributes["Stats"])
                                print(self.__Attributes["Attacking"], "ATTACKING!!! ATTRIBUTE TEST!!!")
                                y+=1
                            x+=1

                    elif self.__Attributes["ID"] in range(6,10):#Heal the closest ally
                        x=0
                        y=0
                        while (y!=self.__Attributes["Stats"]["Multi-target"] and x<len(self.__Attributes["In_Range"])):
                            Attributes=self.__Attributes["In_Range"][x][1].Get_Attributes()
                            if Attributes["Team"]==self.__Attributes["Team"] and Attributes["Current_Health"]>0:
                                Attributes["Current_Health"]-=(self.__Attributes["Stats"]["Attack"]-Attributes["Stats"]["Defence"])
                                self.__Attributes["In_Range"][x][1].Set_Attributes(["Stats"],[Attributes["Stats"]])
                                self.__Attributes["Attacking"].append([Attributes["Location"],(0,254,0)])
                                y+=1
                            x+=1

                    else:#TEST!!!
                        self.__Attributes["Attacking"]=[]#Prevents lines from being drawn whilst not attacking!
                        #pass#Any more extra functions go here!
                    #---------------------------------------
                    
                    
                    #Reset the cooldown timer if =0
                    if self.__Attributes["Cooldown_Timer"]==0:
                        self.__Attributes["Cooldown_Timer"]=self.__Attributes["Stats"]["Cooldown"]
                        #self.__Attributes["State"]=0#idle #

                    #Delete the unit if it has no health remaining
                    #Done when setting the attributes!!!

                else:
                    self.__Attributes["Attacking"]=[]
                    if self.__Attributes["Cooldown_Timer"]==0:#reset state when not attacking!
                        self.__Attributes["State"]=0
            
            #Check modes if not attacking
            #---------------------------------------
            #If damaged, the state will be forcefully changed to 3 (damaged)

            #if self.__Attributes["Cooldown_Timer"]<0:
                #if self.__Attributes["Stats"]["Health"]<=0:#This will be done in Check_Stats
                #    self.__Attributes["State"]=4
                #else:#ALSO MOVEMENT TO CHANGE TO MODE 1 #FIX!!!
                #self.__Attributes["State"]=0
             #   print("PASS")
            #---------------------------------------
            
##            #Decrement the cooldown timer
##            self.__Attributes["Cooldown_Timer"]-=1
            #---------------------------------------
                
            #Mode 2
            #---------------------------------------
            #If sprite from another team is in range, attack and set the health to a lower ammount
            #SHOULD attack the closest object in range that is on another team!!!
            #In_Range should be an ordered list!!!
            #When the cooldown timer reaches 0, the attack animation should be played, and the attack drawn to the screen!

        elif self.__Attributes["Cooldown_Timer"]==0:#reset state when not attacking!
            self.__Attributes["State"]=0
            self.__Attributes["Attacking"]=[]

        #Decrement the cooldown timer
        self.__Attributes["Cooldown_Timer"]=abs(self.__Attributes["Cooldown_Timer"]-1)
        #print(self.__Attributes["Cooldown_Timer"], "COOLDOWN!!!")

        
    def Check_Stats(self):#FINISH!!!
        
        #Check to see if the unit has levelled up!
        #---------------------------------------
        if self.__Attributes["Stats"]["Exp"]==50*(10^self.__Attributes["Level"]):
            #for x in range(len(self.__Attributes["Stats"])):
            #    self.__Attributes["Stats"][x]+=self.__Attributes["Stats"][x]
            pass
        #---------------------------------------

        #Check to see if the unit has no health left!
        #---------------------------------------
        if self.__Attributes["Current_Health"]<=0:#This will be dealt with in the server!
            self.__Attributes["State"]=4#Defeated
            print("DEFEATED!!!")
        #---------------------------------------

    def Functions(self, Function):
        print("HI")

    def Direct_Path(self,Position,Target):#Movement within the same tile or directly between tiles
        Path=[]
        POSITION=[int(Position[0]),int(Position[1])]
        TARGET=[int(Target[0]),int(Target[1])]#Create a copy of the variables (make them be passed by value)
                                        #x                      #y
        print("DIRECT_PATH!!!", abs(POSITION[0]-TARGET[0]), abs(POSITION[1]-TARGET[1]))
        while POSITION[0]!=TARGET[0] or POSITION[1]!=TARGET[1]:
            #print(-self.__Attributes["Stats"]["Speed"],self.__Attributes["Stats"]["Speed"])

            if POSITION[0]-TARGET[0] in range(-self.__Attributes["Stats"]["Speed"],self.__Attributes["Stats"]["Speed"]+1) and POSITION[1]-TARGET[1] in range(-self.__Attributes["Stats"]["Speed"],self.__Attributes["Stats"]["Speed"]+1):
                Path.append([-(POSITION[0]-TARGET[0]),-(POSITION[1]-TARGET[1])])#Difference between the two locations. This should then end the while loop!
                POSITION=TARGET
                print("TELEPORT!!!")
    
            else:
                Path.append([0,0])
                print(POSITION,TARGET,self.__Attributes["Stats"]["Speed"])
                if POSITION[0]-TARGET[0]>self.__Attributes["Stats"]["Speed"]:
                    Path[len(Path)-1][0]=-self.__Attributes["Stats"]["Speed"]#Left
                    POSITION[0]-=self.__Attributes["Stats"]["Speed"]
                    print("LEFT!!!")
                
                elif POSITION[0]-TARGET[0]<-self.__Attributes["Stats"]["Speed"]:
                    Path[len(Path)-1][0]=self.__Attributes["Stats"]["Speed"]#Right
                    POSITION[0]+=self.__Attributes["Stats"]["Speed"]
                    print("RIGHT!!!")


                if POSITION[1]-TARGET[1]>self.__Attributes["Stats"]["Speed"]:
                    Path[len(Path)-1][1]=-self.__Attributes["Stats"]["Speed"]#Up
                    POSITION[1]-=self.__Attributes["Stats"]["Speed"]
                    print("UP!!!")

                elif POSITION[1]-TARGET[1]<-self.__Attributes["Stats"]["Speed"]:
                    Path[len(Path)-1][1]=self.__Attributes["Stats"]["Speed"]#Down
                    POSITION[1]+=self.__Attributes["Stats"]["Speed"]
                    print("DOWN!!!")

                if Path[len(Path)-1]==[0,0]:#Testing only!!!
                    print("NO DIRECTION!!!")

            print(POSITION, TARGET, Path, self.__Attributes["Location"], "LOCATION IN ALGORITHM!!!")

        print(Path)
        
        return Path

    def Shortest_Path(self,Map_Data):#Requires a valid tile to be selected at the moment!!!

        #print("TARGET LOCATION!!!", self.__Attributes["Target"])

        #Decide which pathing mode to use
        
        #If the target is on the same tile as the current location (Direct_Path)
        #---------------------------------------
        #(Uses 8 directions)
        if self.__Attributes["Target"][0]//20==self.__Attributes["Location"][0]//20 and self.__Attributes["Target"][1]//20==self.__Attributes["Location"][1]//20:
            print("LOCATION NOW!!! (part 1)", self.__Attributes["Location"])
            Path=self.Direct_Path(self.__Attributes["Location"],[int(self.__Attributes["Target"][0]),int(self.__Attributes["Target"][1])])
            self.__Attributes["Path"]=Path
            print("LOCATION NOW!!!", self.__Attributes["Location"])
            #return Path
        #---------------------------------------

        #If the target is on a different tile (A* Algorithm)
        #---------------------------------------
        #(Uses 4 directions)
        else:
            Invalid=[]#A list of all the invalid tiles to avoid during the algorithm
            Path=[]#Calculate path to the center of the tile done below

            #Generate a graph of valid tile locations for the unit
            #---------------------------------------
            print(self.__Attributes["Location"], "LOCATION!!!!!!!!!!!!!!!!!!!!!! in [x,y]")
            print(self.__Attributes["Target"], "TARGET!!!!!!!!!!!!!!!!!!!!!!!!!!! in [x,y]")
            Graph=[[],[],[],[],[],[],[],[],[],[],[]]#Specifically for a 11x11 grid!
            #Distances=[]#List of heuristics for each tile
            Target_Tile=[0,0]
            for y in range(11):#11 for a 11x11 grid, since 5+1+5 = 11
                for x in range(11):
                    Location_y=20*((self.__Attributes["Location"][1]//20)-5+y)
                    Location_x=20*((self.__Attributes["Location"][0]//20)-5+x)
                    print([Location_x,Location_y], "in [x,y]")
                    
                    #Check for invalid tiles or out of bounds locations and don't add them to the graph
                    if Location_y<0 or Location_y>20*len(Map_Data[0]) or Location_x<0 or Location_x>20*len(Map_Data[0][0]):
                        print("OUT OF BOUNDS!!!", [y,x])
                        Graph[y].append([[-1,-1],-1,-1,-1])
                        Invalid.append([y,x])
                    elif (Map_Data[0][Location_y//20][Location_x//20] in self.__Attributes["Invalid_Tiles"]):#FIX MAYBE? for x,y and y,x?
                        print("INVALID TILE!!!", [y,x], "MAP TILES!!!")
                        Graph[y].append([[-1,-1],-1,-1,-1])
                        Invalid.append([y,x])
                    else:
                        Graph[y].append([[Location_x,Location_y],(20*(abs(5-x)+abs(5-y))),abs(self.__Attributes["Target"][0]-Location_x)+abs(self.__Attributes["Target"][1]-Location_y),-1])#Location of each tile in the graph that the unit can travel to

            print("Graph:", Graph)#Each list is made up of: [[Locationx,Locationy],Distance from start_tile,Heuristic(Distance from target location),Previous_Tile]

            print("Invalid:", Invalid)#A list of all the invalid tiles that will be scipped in the A* algorithm
            #---------------------------------------


            #Calculate the target tile
            #---------------------------------------
            #Minimum distance to the target
            Value=min(([Graph[y][x][2] for y in range(len(Graph)) for x in range(len(Graph[y])) if (Graph[y][x][2]>-1)]))
            print("VALUE!!!", Value)

            #Index of the minimum distance to the target. This is also the index of the target tile!
            Target_Tile=[[y,x] for y in range(len(Graph)) for x in range(len(Graph[y])) if Graph[y][x][2]==Value]
            print("Target tile:", Target_Tile)
            #---------------------------------------
            

            #A* Algorithm
            #---------------------------------------
            Visited=[]#A list of all visited nodes during the algorithm. This will be used to determine the final path of the unit!
            Current_Tile=[5,5]#Also the starting tile!
            Start_Tile=[5,5]
            print("Visited:", Visited)

            #Target_Tile[0], since the tile is held in its own list!
            while Current_Tile!=Target_Tile[0]: #while Target_Tile not in Visited:
                print("CURRENT TILE!!!", Current_Tile, Graph[Current_Tile[1]][Current_Tile[0]])
                print("TARGET TILE!!!", Target_Tile)
                print("INVALID", Invalid)
                
                #For each connected tile in the graph
                Distances=[]#Used to calculate the next node to visit
                for x in [1,3,5,7]:#FINISH!!!
                    print("CURRENT_TILE",Current_Tile)
                    print("TESTING TILE:", [Current_Tile[0]+((x//3)%3)-1,Current_Tile[1]+(x%3)-1])

                                            #y axis                         #x axis
                    #print("Tile", x, Graph[Current_Tile[1]+((x//3)%3)-1][Current_Tile[0]+(x%3)-1])
                    if [Current_Tile[0]+((x//3)%3)-1,Current_Tile[1]+(x%3)-1] not in Invalid and [Current_Tile[0]+((x//3)%3)-1,Current_Tile[1]+(x%3)-1] not in Visited and (Current_Tile[0]+((x//3)%3)-1 in range(0,11)) and (Current_Tile[1]+(x%3)-1 in range(0,11)):
                        #Path from start. Not needed, since every node on the graph is the same distance away!
                        #This will instead simply be the path that the nodes are visited!
                        print("TESTING!!!", abs(Graph[Current_Tile[0]][Current_Tile[1]][0][0]), Current_Tile[0]+((x//3)%3)-1, Current_Tile[1]+(x%3)-1)
                        print("MORE!!!", Graph[Current_Tile[0]+((x//3)%3)-1][Current_Tile[1]+(x%3)-1])
                        
                        Distance_From_Start=(abs(Graph[Current_Tile[0]][Current_Tile[1]][0][0]-Graph[Current_Tile[0]+((x//3)%3)-1][Current_Tile[1]+(x%3)-1][0][0])+abs(Graph[Current_Tile[0]][Current_Tile[1]][0][1]-Graph[Current_Tile[0]+((x//3)%3)-1][Current_Tile[1]+(x%3)-1][0][1]))

                        #Distance_From_Start=Graph[Current_Tile[1]+((x//3)%3)-1][Current_Tile[0]+(x%3)-1][2]
                        print("Distance_From_Start:", Distance_From_Start)

                        Heuristic=Graph[Current_Tile[0]+((x//3)%3)-1][Current_Tile[1]+(x%3)-1][2]
                        print("Heuristic:", Heuristic)

                        Total_Distance=Distance_From_Start+Heuristic
                        print("Total distance:", Total_Distance)
                        Distances.append(Total_Distance)

                    else:
                        if [Current_Tile[0]+((x//3)%3)-1,Current_Tile[1]+(x%3)-1] not in Invalid:
                            print("NOT IN INVALID!!!")
                        if [Current_Tile[0]+((x//3)%3)-1,Current_Tile[1]+(x%3)-1] not in Visited:
                            print("NOT IN VISITED!!!") 
                        print("INVALID TILE!!!", [Current_Tile[0]+((x//3)%3)-1,Current_Tile[1]+(x%3)-1])
                        Distances.append(-1)


                print(Distances, "DISTANCES")
                #print(Distances.index(min(Distances)))
                print(min([i for i in Distances if i>-1]))
                x=(2*Distances.index(min([i for i in Distances if i>-1])))+1#x is one of the values used in the for loop above (2n +1 to have a value 1,3,5 or 7)
                                    #y axis                 #x axis
                print(x, "X", [Current_Tile[0]+((x//3)%3)-1,Current_Tile[1]+(x%3)-1])
                Visited.append(Current_Tile)
                Current_Tile=[Current_Tile[0]+((x//3)%3)-1,Current_Tile[1]+(x%3)-1]
                print(Visited, "VISITED")

            Visited.append(Target_Tile[0])
            print("FINAL VISITED PATH:", Visited)
            #---------------------------------------


            #Calculate the path that the unit will take, then return it
            #---------------------------------------
            if Target_Tile[0]==[5,5]:#If there is a difference between manhatton distance and direct shortest distance
                print(self.__Attributes["Location"],self.__Attributes["Target"])
                Return=self.Direct_Path(self.__Attributes["Location"],self.__Attributes["Target"])# in [x,y] #Travel straight to the target
                print(Return, "RETURN!!!")
                
                for y in range(len(Return)):
                    Path.append(Return[y])

            else:
                Path=self.Direct_Path(self.__Attributes["Location"],[(20*(self.__Attributes["Location"][0]//20))+10,(20*(self.__Attributes["Location"][1]//20))+10])
                print("Path to the center of the current tile:", Path)
                
                for x in range(len(Visited)-1):
                            #x axis             #y axis             # xaxis         #y axis
                    print([20*Visited[x][1],20*Visited[x][0]],[20*Visited[x+1][1],20*Visited[x+1][0]], "[x axis, y axis]")
                    Return=self.Direct_Path([20*Visited[x][1],20*Visited[x][0]],[20*Visited[x+1][1],20*Visited[x+1][0]])
                    print(Return, "RETURN!!!")
                    for y in range(len(Return)):
                        Path.append(Return[y])

            print("FINAL PATH!!!", Path)
            #print(self.__Attributes["Path"])
            self.__Attributes["Path"]=Path
            #print(self.__Attributes["Path"])
            
            #print(self.__Attributes["Threads"])
        self.__Attributes["Threads"]-=1
        print(self.__Attributes["Threads"], "THREADS NOW!!!")
            #print(BREAK)
            #return Path
            #print(abc)#REMOVE!!!
            #---------------------------------------
            
            #---------------------------------------        

        #---------------------------------------


#----------------------------------------------------------    


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

        print(Records)
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
        self.Menus(0,(0,0),[0],[0],0)
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
