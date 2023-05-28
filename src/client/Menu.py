#Menus
#Here, inheritance enables menus to have different functionality whilst maintaining the same interface
#These are to use as part of the game class using pygame
from Widget import *
import time#Used for blinking cursor

class Menu():
    def __init__(self, width, height, font, textSize, textColour):#Here, protected variables are used rather than private variables, so that they can be accessed by the subclasses


        #Link to the Game the menu will be used with
        #self._Game = Game#Used to send the Game commands to draw to the screen with pyGame
        self._Display = "MenuDisplay"#Used to query a dictionary from the game when drawing to the screen

        #Select the middle of the screen
        self._MiddleWidth = width // 2#self._Game.get_setting("Width") // 2
        self._MiddleHeight = height // 2#self._Game.get_setting("Height") // 2

        #Load the cursor text and dimensions
        self._CursorText = '*'#This will be displayed next to the most closely matching menu option if the mouse is being moved
        self._CursorSize = 15
        self._CursorOffset = -100#Makes the cursor appear to the left of the menu options
        self._TextSize = textSize#Size of the menu options
        self._TextOffset = 20#Space between menu options
        self._Font = font#Name of the font used to draw text
        self._Colour = textColour#Colour of the text to be drawn


        #Define a map to keep track of the correct cursor position
        self._SelectedState = 0
        self._MenuItems = ["State"]#Create the menu items that will be displayed as part of the menu
        self._MenuPositions = [[self._MiddleWidth, self._MiddleHeight + 10 + self._TextOffset]]
        #[ [x,y] ]
        self._Widgets = {}#A list of widget objects that handle all rect positions within the class


    def display_menu(self, keyboardState, mousePosition, mouseState, returnKeys):
        """Blits the menu to the correct display before the connected Game displays it"""

        returnText = []
        returnWidgets = []


        returnSettings = []#Used only in menus that include widgets
        returnValues = []
        

        #Menu drawing
        for x in range(len(self._MenuItems)):
            #self._Game.draw_text(self._MenuItems[x],self._TextSize,self._MenuPositions[x][0],self._MenuPositions[x][1],"White")
            returnText.append([self._MenuItems[x],str(self._MenuPositions[x][0]),str(self._MenuPositions[x][1]),self._Colour,self._Font,self._Display])
            #Some of the inputs have been casted to strings in order to be compatible with other programming languages, where arrays must only consist of a single type

        
        for key in self._Widgets:
            returnWidget = []
            for rect in self._Widgets[key].draw():
                returnWidget.append(rect)

            returnWidgets.append(returnWidget)

                
            #returnWidgets.append(rect for rect in self._Widgets[key].draw())

            
        #Draw the cursor in the correct position
        #print(self._MenuPositions[self._SelectedState])
        #self._Game.draw_text(self._CursorText, self._CursorSize, self._MenuPositions[self._SelectedState][0] + self._CursorOffset, self._MenuPositions[self._SelectedState][1],"White")

        #Check if the cursor should be drawn
        if (time.time() % 1 > 0.5) and len(self._MenuPositions)>0:
            returnText.append([self._CursorText,str(self._MenuPositions[self._SelectedState][0] + self._CursorOffset),str(self._MenuPositions[self._SelectedState][1]),self._Colour,self._Font,self._Display])



        return returnText, returnWidgets, returnSettings, returnValues, "Menu", False#For a default menu, the game should never be started and the menu should never be changed



        

class MainMenu(Menu):
    def __init__(self, width, height, font, textSize, textColour):
        
        #Initialise the shared attributes and methods of the menu class
        Menu.__init__(self, width, height, font, textSize, textColour)
        #self._SelectedState = 0

        #Define a map to keep track of the correct cursor position
        self._MenuItems = ["Start","Options","Credits"]#Create the menu items that will be displayed as part of the menu
        self._MenuPositions = [[self._MiddleWidth, self._MiddleHeight + 10 + self._TextOffset],
                               [self._MiddleWidth, self._MiddleHeight + 10 + 2*self._TextOffset],
                               [self._MiddleWidth, self._MiddleHeight + 10 + 3*self._TextOffset]]




    def display_menu(self, keyboardState, mousePosition, mouseState, returnKeys):
        """Blits the menu to the correct display before the connected Game displays it"""

        #Menu logic
        currentMenu, gameStart = self.check_input(keyboardState, mousePosition, mouseState)#This uses the key states from the attached Game rather than implementing pyGame

        #Menu drawing
        returnText, returnWidgets, returnSettings, returnValues = Menu.display_menu(self, keyboardState, mousePosition, mouseState, returnKeys)[0:4]#Includes position 0, 1, 2 and 3
        #This also returns a third and fourth value to be consistent with the return values of the sub menus
        #However, these are ignored in favour of the ones calculated locally
        returnText.append(["Main Menu",str(self._MiddleWidth), str(self._MiddleHeight - 20), self._Colour, self._Font, self._Display])
        #self._Game.draw_text("Main Menu", 20, self._MiddleWidth, self._MiddleHeight - 20,"White", self._Display)
        

        #Return whether the game has started
        return returnText, returnWidgets, [], [], currentMenu, gameStart



    def check_input(self, keyboardState, mousePosition, mouseState):
        """keyboardState: ["MoveLeft","MoveRight","MoveUp","MoveDown","Enter","Backspace"]"""       

        currentMenu = "MainMenu"
        
        #MoveUp
        if keyboardState[2]:
            self._SelectedState = (self._SelectedState-1)%len(self._MenuItems)
            print("NEW STATE: ", self._SelectedState)

        #MoveDown
        if keyboardState[3]:
            self._SelectedState = (self._SelectedState+1)%len(self._MenuItems)
            print("NEW STATE: ", self._SelectedState)

        #Enter
        if keyboardState[4]:#If the key mapped to enter is pressed

            #Start
            if self._SelectedState == 0:
                print("START PLAYING THE GAME!!!")
                #"MainMenu", False
                return "Ready", False#True #Example to be removed after options have been set up!!!
                
            else:#1 = Options, 2 = Credits
                currentMenu = self._MenuItems[self._SelectedState]
                #self._Game.set_current_menu(self._MenuItems[self._SelectedState])

        #Backspace/Escape
        #N/A

        

        return currentMenu, False#Only return true when the game should start playing


class OptionsMenu(Menu):
    def __init__(self, width, height, font, textSize, textColour):
        
        #Initialise the shared attributes and methods of the menu class
        Menu.__init__(self, width, height, font, textSize, textColour)


        #Define a map to keep track of the correct cursor position
        self._MenuItems = ["Volume","Controls"]#Create the menu items that will be displayed as part of the menu
        self._MenuPositions = [[self._MiddleWidth, self._MiddleHeight + 10 + self._TextOffset],
                               [self._MiddleWidth, self._MiddleHeight + 10 + 2*self._TextOffset]]

        self._Widgets = {
            "Go back" : Button(self._MiddleWidth- (200 // 2), self._MiddleHeight + 20 + 3*self._TextOffset, 200, 25, self._Display, "Go back", font = "8-Bit", radius = 7)
            }
            

    def display_menu(self, keyboardState, mousePosition, mouseState, returnKeys):
        """Blits the menu to the correct display before the connected Game displays it"""

        #Menu logic
        currentMenu, gameStart = self.check_input(keyboardState, mousePosition, mouseState)
        
        #Menu drawing
        returnText, returnWidgets, returnSettings, returnValues = Menu.display_menu(self, keyboardState, mousePosition, mouseState, returnKeys)[0:4]
        returnText.append(["Options",str(self._MiddleWidth), str(self._MiddleHeight - 20), self._Colour, self._Font, self._Display])


        return returnText, returnWidgets, returnSettings, returnValues, currentMenu, gameStart


    def check_input(self, keyboardState, mousePosition, mouseState):
        """keyboardState: ["MoveLeft","MoveRight","MoveUp","MoveDown","Enter","Backspace"]"""       

        currentMenu = "Options"
        
        #MoveUp
        if keyboardState[2]:
            self._SelectedState = (self._SelectedState-1)%len(self._MenuItems)

        #MoveDown
        if keyboardState[3]:
            self._SelectedState = (self._SelectedState+1)%len(self._MenuItems)

        #Enter
        if keyboardState[4]:#If the key mapped to enter is pressed
            currentMenu = self._MenuItems[self._SelectedState]#Handles all possible options

        #Backspace
        elif keyboardState[5] or keyboardState[6]:#If the key mapped to enter or backspace are pressed
            currentMenu = "MainMenu"

        #Go back button
        else:
            #If the go back button is clicked, return to the controls menu
            for key in self._Widgets:
                returnValue = self._Widgets[key].listen(keyboardState,mousePosition,mouseState)
                if returnValue == True:#If the button is pressed
                    if key == "Go back":
                        currentMenu = "MainMenu"


        return currentMenu, False




class VolumeMenu(Menu):
    def __init__(self, width, height, font, textSize, textColour):
        
        #Initialise the shared attributes and methods of the menu class
        Menu.__init__(self, width, height, font, textSize, textColour)


        #Define a map to keep track of the correct cursor position
        #self._MenuItems = []#Create the menu items that will be displayed as part of the menu
        #self._MenuPositions = []

        #Define widgets to interact with the menu
        self._Widgets = {
            "Settings Volume" : Slider(self._MiddleWidth- (200 // 2), self._MiddleHeight - 10 + self._TextOffset, 200, 20, self._Display),
                        #Slider(xPos,yPos,width,height,display,min,max,step,value,colour...)
            "Go back" : Button(self._MiddleWidth- (200 // 2), self._MiddleHeight + 20 + 2*self._TextOffset, 200, 25, self._Display, "Go back", font = "8-Bit", radius = 7)
            }
            

    def display_menu(self, keyboardState, mousePosition, mouseState, returnKeys):
        """Blits the menu to the correct display before the connected Game displays it"""

        #Menu logic
        currentMenu, gameStart = self.check_input(keyboardState, mousePosition, mouseState)

        returnSettings = []
        returnValues = []
        
        #Widget logic
        #for key in self._Widgets:
        #    returnSettings.append(key)
        #    returnValues.append(self._Widgets[key].listen(keyboardState,mousePosition,mouseState))
        
        
        #Menu drawing
        returnText, returnWidgets, returnSettings, returnValues = Menu.display_menu(self, keyboardState, mousePosition, mouseState, returnKeys)[0:4]

        returnText = []
        returnText.append(["Set Volume", str(self._MiddleWidth), str(self._MiddleHeight - 20), self._Colour, self._Font, self._Display])



        return returnText, returnWidgets, returnSettings, returnValues, currentMenu, gameStart


    def check_input(self, keyboardState, mousePosition, mouseState):
        """keyboardState: ["MoveLeft","MoveRight","MoveUp","MoveDown","Enter","Backspace"]"""       

        currentMenu = "Volume"
        
        #MoveUp
        if keyboardState[2]:
            self._SelectedState = (self._SelectedState-1)%len(self._MenuItems)

        #MoveDown
        if keyboardState[3]:
            self._SelectedState = (self._SelectedState+1)%len(self._MenuItems)

        #Backspace
        if keyboardState[5]:#If the key mapped to enter or backspace are pressed
            currentMenu = "Options"

        #Escape
        elif keyboardState[6]:
            currentMenu = "MainMenu"

        #Go back button
        else:
            #If the go back button is clicked, return to the controls menu
            for key in self._Widgets:
                returnValue = self._Widgets[key].listen(keyboardState,mousePosition,mouseState)
                if key == "Go back" and returnValue == True:#If the button is pressed
                    currentMenu = "Options"
                #elif key == "Settings Volume":
                #Handled in the menu super class
                    




        return currentMenu, False


class ControlsMenu(Menu):
    def __init__(self, width, height, font, textSize, textColour, keymap, keyNames):
        """Precondition: The menu items size must match the menu positions size
           Precondition: All items in the keymap section must have their position added separately inside this function"""
        
        #Initialise the shared attributes and methods of the menu class
        Menu.__init__(self, width, height, font, textSize, textColour)
        self._CursorOffset = -105


        #Define a map to keep track of the correct cursor position
        self._MenuItems = []
        self.__KeyNames = keyNames
        
        for key in keymap:
            self._MenuItems.append(key)#Since the text needs to be alligned to the left side of the screem, its more simple to calculate the correct positions manually

        self._MenuPositions = [[(self._MiddleWidth // 2) - 40 , self._MiddleHeight + 10 + self._TextOffset],
                               [(self._MiddleWidth // 2) - 30, self._MiddleHeight + 10 + 2*self._TextOffset],
                               [(self._MiddleWidth // 2), self._MiddleHeight + 10 + 3*self._TextOffset],
                               [(self._MiddleWidth // 2) - 25, self._MiddleHeight + 10 + 4*self._TextOffset],
                               [(self._MiddleWidth // 2), self._MiddleHeight + 10 + 5*self._TextOffset],
                               [(self._MiddleWidth // 2) - 5, self._MiddleHeight + 10 + 6*self._TextOffset],
                               [(self._MiddleWidth // 2), self._MiddleHeight + 10 + 7*self._TextOffset]]


        

        #for x in range(len(keyNames)):
        #    self._MenuItems.append(keyNames[x])
        #    self._MenuPositions.append([((self._MiddleWidth * 3) // 2), self._MiddleHeight + 10 + (x+1)*self._TextOffset])#Since the key names will be alligned centrally, the positions can be calculated automatically
        self._Widgets = {
            "Go back" : Button(self._MiddleWidth- (200 // 2), self._MiddleHeight + 20 + 8*self._TextOffset, 200, 25, self._Display, "Go back", font = "8-Bit", radius = 7)
            }
            
        #self._MenuItems.append("Go Back")
        #self._MenuPositions.append([self._MiddleWidth, self._MiddleHeight + 10 + (len(keyNames)+2)*self._TextOffset])
        
            

    def display_menu(self, keyboardState, mousePosition, mouseState, returnKeys):
        """Blits the menu to the correct display before the connected Game displays it"""

        #Menu logic
        currentMenu, gameStart = self.check_input(keyboardState, mousePosition, mouseState)
        
        
        #Menu drawing
        returnText, returnWidgets, returnSettings, returnValues = Menu.display_menu(self, keyboardState, mousePosition, mouseState, returnKeys)[0:4]
        returnText.append(["Controls", str(self._MiddleWidth), str(self._MiddleHeight - 20), self._Colour, self._Font, self._Display])

        length = len(self.__KeyNames)
        for x in range(length):
            returnText.append([self.__KeyNames[x], str((self._MiddleWidth * 3) // 2), str(self._MiddleHeight + 10 + (x+1)*self._TextOffset), self._Colour, self._Font, self._Display])



        #Change cursor position to match the left allignment of the text
        if time.time() % 1 > 0.5:#Check if the cursor needs to be drawn
            #if self._SelectedState in range(0,(len(self._MenuItems)-1)//2):
                #self._CursorOffset = -105
            if self._SelectedState != len(self._MenuItems)-1:
                returnText[len(returnText)-length-2][1] = (self._MiddleWidth // 2) + self._CursorOffset

            #elif self._SelectedState != len(self._MenuItems)-1:
                #self._CursorOffset = -100
                #returnText[len(returnText)-2][1] = ((self._MiddleWidth*3) // 2) + self._CursorOffset
            #else:#This case is covered by the default menu class

        return returnText, returnWidgets, returnSettings, returnValues, currentMenu, gameStart


    def check_input(self, keyboardState, mousePosition, mouseState):
        """keyboardState: ["MoveLeft","MoveRight","MoveUp","MoveDown","Enter","Backspace","Escape"]"""       

        currentMenu = "Controls"
        
        #MoveUp
        if keyboardState[2]:
            self._SelectedState = (self._SelectedState-1)%len(self._MenuItems)

        #MoveDown
        if keyboardState[3]:
            self._SelectedState = (self._SelectedState+1)%len(self._MenuItems)


        #Enter
        if keyboardState[4]:#If the key mapped to enter is pressed
                currentMenu = self._MenuItems[self._SelectedState]#Handles all possible options

        #Backspace
        elif keyboardState[5]:
            currentMenu = "Options"

        #Escape
        elif keyboardState[6]:
            currentMenu = "MainMenu"

        #Go back button   
        else:
            #If the go back button is clicked, return to the controls menu
            for key in self._Widgets:
                returnValue = self._Widgets[key].listen(keyboardState,mousePosition,mouseState)
                if returnValue == True:#If the button is pressed
                    if key == "Go back":
                        currentMenu = "Options"




        return currentMenu, False


class KeyMenu(Menu):
    def __init__(self, width, height, font, textSize, textColour, action, key):
        """Precondition: The menu items size must match the menu positions size
           Precondition: All items in the keymap section must have their position added separately inside this function"""
        
        #Initialise the shared attributes and methods of the menu class
        Menu.__init__(self, width, height, font, textSize, textColour)
        self._CursorOffset = -105

        self.__Action = action#Name of the action for which a key is mapped to
        self.__Key = key#Name of the key that is currently mapped to the action
        self.__ChangeKey = self.__Key


        #Define a map to keep track of the correct cursor position
        #self._MenuItems = []
        #self._MenuItems.append(key)#This is to be done elsewhere, since the menu name will be this value

        #self._MenuPositions = []
        
        

        #Define widgets to interact with the menu
        String = "Keymap " + self.__Action
        self._Widgets = {
            String : Button(self._MiddleWidth - (200 // 2), self._MiddleHeight + 60 + 4*self._TextOffset, 200, 25, self._Display, "Confirm", font = "8-Bit", radius = 7),
                        #Slider(xPos,yPos,width,height,display,min,max,step,value,colour...)
            "Return" : Button(self._MiddleWidth- (200 // 2), self._MiddleHeight +70 + 4*self._TextOffset + 25, 200, 25, self._Display, "Return", font = "8-Bit", radius = 7)
            }
            

    def display_menu(self, keyboardState, mousePosition, mouseState, returnKeys):
        """Blits the menu to the correct display before the connected Game displays it"""

        #Menu logic
        currentMenu, gameStart, changeKeymap = self.check_input(keyboardState, mousePosition, mouseState, returnKeys)
        
        #Menu drawing
        returnWidgets, returnSettings, returnValues = Menu.display_menu(self, keyboardState, mousePosition, mouseState, returnKeys)[1:4]
        returnText = []
        returnText.append([self.__Action,str(self._MiddleWidth), str(self._MiddleHeight - 20), self._Colour, self._Font, self._Display])
        returnText.append(["Current",str(self._MiddleWidth // 2), str(self._MiddleHeight + 20), self._Colour, self._Font, self._Display])
        returnText.append(["mapping",str(self._MiddleWidth //2), str(self._MiddleHeight + 20 + self._TextOffset), self._Colour, self._Font, self._Display])
        returnText.append([self.__Key,str((self._MiddleWidth * 3) // 2), str(self._MiddleHeight + 30), self._Colour, self._Font, self._Display])

        returnText.append(["New",str(self._MiddleWidth // 2), str(self._MiddleHeight + 20 + 3*self._TextOffset), self._Colour, self._Font, self._Display])
        returnText.append(["mapping",str(self._MiddleWidth // 2), str(self._MiddleHeight + 20 + 4*self._TextOffset), self._Colour, self._Font, self._Display])
        returnText.append([self.__ChangeKey,str((self._MiddleWidth * 3) // 2), str(self._MiddleHeight + 30 + 3*self._TextOffset), self._Colour, self._Font, self._Display])

        #Button pressed logic
        if changeKeymap == True:
            returnSettings.append("Keymap " + self.__Action)
            returnValues.append(self.__Key)


        #Remove the cursor, since the only options are buttons
        #returnText.pop(len(returnText)-2)#Removes the item in the specified position in the list 
        #Change cursor position to match the left allignment of the text
##        if time.time() % 1 > 0.5:#Check if the cursor needs to be drawn
##            if self._SelectedState in range(0,(len(self._MenuItems)-1)//2):
##                #self._CursorOffset = -105
##                returnText[len(returnText)-2][1] = (self._MiddleWidth // 2) + self._CursorOffset
##            elif self._SelectedState != len(self._MenuItems)-1:
##                #self._CursorOffset = -100
##                returnText[len(returnText)-2][1] = ((self._MiddleWidth*3) // 2) + self._CursorOffset
##            #else:#This case is covered by the default menu class

        return returnText, returnWidgets, returnSettings, returnValues, currentMenu, gameStart


    def check_input(self, keyboardState, mousePosition, mouseState, returnKeys):
        """keyboardState: ["MoveLeft","MoveRight","MoveUp","MoveDown","Enter","Backspace"]"""       

        currentMenu = self.__Action
        changeKeymap = False

        #Check if a different key has been entered
        length = len(returnKeys)
        if length > 0:
            self.__ChangeKey = returnKeys[length-1]


        #If the go back button is clicked, return to the controls menu
        for key in self._Widgets:
            returnValue = self._Widgets[key].listen(keyboardState,mousePosition,mouseState)
            if returnValue == True:#If the button is pressed
                if key == "Keymap " + self.__Action:
                    self.__Key = self.__ChangeKey
                    changeKeymap = True
                elif key == "Return":
                    currentMenu = "Controls"


        
        #if self.__Key == "Enter":


        #Enter/Backspace
        #if keyboardState[4] or keyboardState[5]:#If the key mapped to enter or backspace are pressed
        #    currentMenu = "Controls"

        return currentMenu, False, changeKeymap

class CreditsMenu(Menu):
    def __init__(self, width, height, font, textSize, textColour):
        #Initialise the shared attributes and methods of the menu class
        Menu.__init__(self, width, height, font, textSize, textColour)

        
        #Define a map to keep track of the correct cursor position
        #self._MenuItems = ["Go Back"]#Create the menu items that will be displayed as part of the menu
        #self._MenuPositions = [[self._MiddleWidth, self._MiddleHeight + 10 + 5*self._TextOffset]]

        self._Widgets = {
            "Go back" : Button(self._MiddleWidth- (200 // 2), self._MiddleHeight +20 + 5*self._TextOffset, 200, 25, self._Display, "Go back", font = "8-Bit", radius = 7)
            }



        
    def display_menu(self, keyboardState, mousePosition, mouseState, returnKeys):
        """Blits the menu to the correct display before the connected Game displays it"""

        #Menu logic
        currentMenu, gameStart = self.check_input(keyboardState, mousePosition, mouseState)
        
        #Menu drawing
        returnText, returnWidgets, returnSettings, returnValues= Menu.display_menu(self, keyboardState, mousePosition, mouseState, returnKeys)[0:4]
        returnText = []
        returnText.append(["Credits",str(self._MiddleWidth), str(self._MiddleHeight - 20), self._Colour, self._Font, self._Display])
        returnText.append(["Made by me",str(self._MiddleWidth), str(self._MiddleHeight), self._Colour, self._Font, self._Display])

        return returnText, returnWidgets, [], [], currentMenu, gameStart


    def check_input(self, keyboardState, mousePosition, mouseState):
        """keyboardState: ["MoveLeft","MoveRight","MoveUp","MoveDown","Enter","Backspace","Escape"]"""
        #This could be used to show dev pictures etc.

        currentMenu = "Credits"
        
        #MoveUp
        if keyboardState[2]:
            print("SCROLL THE SCREEN UP!!!")

        #MoveDown
        if keyboardState[3]:
            print("SCROLL THE SCREEN DOWN!!!")

        #Enter
        #N/A


        #Backspace/Escape
        if keyboardState[5] or keyboardState[6]:#If the key mapped to enter or backspace are pressed
            currentMenu = "MainMenu"

        #Go back button
        else:
            #If the go back button is clicked, return to the controls menu
            for key in self._Widgets:
                returnValue = self._Widgets[key].listen(keyboardState,mousePosition,mouseState)
                if returnValue == True:#If the button is pressed
                    if key == "Go back":
                        currentMenu = "MainMenu"


        

        return currentMenu, False



class ReadyMenu(Menu):
    def __init__(self, width, height, font, textSize, textColour):
        
        #Initialise the shared attributes and methods of the menu class
        Menu.__init__(self, width, height, font, textSize, textColour)

        self._MenuItems = []#Create the menu items that will be displayed as part of the menu
        self._MenuPositions = []


        self._Widgets = {
            "Ready" : Button(self._MiddleWidth- (200 // 2), self._MiddleHeight + 30 - 1*self._TextOffset, 200, 25, self._Display, "Ready", font = "8-Bit", radius = 7),
            "Go back" : Button(self._MiddleWidth- (200 // 2), self._MiddleHeight + 10 + 2*self._TextOffset, 200, 25, self._Display, "Go back", font = "8-Bit", radius = 7)
            }
            

    def display_menu(self, keyboardState, mousePosition, mouseState, returnKeys):
        """Blits the menu to the correct display before the connected Game displays it"""

        #Menu logic
        currentMenu, gameStart = self.check_input(keyboardState, mousePosition, mouseState)
        
        #Menu drawing
        returnText, returnWidgets, returnSettings, returnValues = Menu.display_menu(self, keyboardState, mousePosition, mouseState, returnKeys)[0:4]
        returnText.append(["Ready Up",str(self._MiddleWidth), str(self._MiddleHeight - 20), self._Colour, self._Font, self._Display])


        return returnText, returnWidgets, returnSettings, returnValues, currentMenu, gameStart


    def check_input(self, keyboardState, mousePosition, mouseState):
        """keyboardState: ["MoveLeft","MoveRight","MoveUp","MoveDown","Enter","Backspace"]"""       

        currentMenu = "Ready"

        #Backspace
        if keyboardState[5] or keyboardState[6]:#If the key mapped to enter or backspace are pressed
            currentMenu = "MainMenu"

        #Go back button
        else:
            #If the go back button is clicked, return to the controls menu
            for key in self._Widgets:
                returnValue = self._Widgets[key].listen(keyboardState,mousePosition,mouseState)
                if returnValue == True:#If the button is pressed
                    if key == "Ready":
                        return "MainMenu", True
                    if key == "Go back":
                        currentMenu = "MainMenu"


        return currentMenu, False
        
