#Game
#Here, the game handles all pygame specific information instead of offloading this to other classes

#Imports
#---------------------------------------
import pygame
import pygame.gfxdraw
from Menu import *
from Client import *
from Server import *
#---------------------------------------

class Game():

    def __init__(self):
        """The game uses the client in order to enable communication with servers on the local network.
           This is the client side processing of the game logic so that the game can be displayed by each client device"""

        #Load settings
        self.__Settings = {
            "Players": 1,#Settings that must remain the same each time the game loads, and are game dependant
            "Online": False,
            "Hosting": True,
        }
        self.load_settings("Settings.txt")

        #Define keys, which should already be a part of pygame
        #self.__UP_KEY, self.__DOWN_KEY, self.__START_KEY, self.__BACK_KEY = False, False, False, False#Keys to be checked within the Game Loop

        #Load controls
        self.__Keymap = {#This is the default key binding if no file is available
            "Enter" : pygame.K_RETURN,
            "Escape" : pygame.K_ESCAPE,
            "Backspace" : pygame.K_BACKSPACE,
            "MoveUp" : pygame.K_UP,
            "MoveDown" : pygame.K_DOWN,
            "MoveLeft" : pygame.K_LEFT,
            "MoveRight" : pygame.K_RIGHT
            }#Used to store different key bindings that the user chooses
        #self.load_controls("Controls.txt")

        
        #Initialise client
        self.__Client = Client()



        #Initialise pygame
        pygame.init()#initialises pygame
        pygame.mixer.init()#initialises sound
        self.__Window = pygame.display.set_mode(((self.__Settings["Width"],self.__Settings["Height"])))#Window the game is held in
        pygame.display.set_caption("Game_Name")#Caption at the top of the window

        self.__Fonts = {
            "8-Bit": pygame.font.Font("8-BIT WONDER.TTF",20),
            "sans-serif": pygame.font.SysFont("sans-serif", 40),
            "default": pygame.font.get_default_font()#Used if no other font is available
            }

        #Load displays
        self.__Displays = {
            "MenuDisplay" : pygame.Surface((self.__Settings["Width"],self.__Settings["Height"])),
            "GameBackgroundLayer" : pygame.Surface((self.__Settings["Width"],self.__Settings["Height"])),
            "GameSpriteLayer" : pygame.Surface((self.__Settings["Width"],self.__Settings["Height"])),
            "GameUILayer" : pygame.Surface((self.__Settings["Width"],self.__Settings["Height"]))
            }

        #Game specifics
        #self.__GameScreen = ... #Load the different screens that the game will be played on
        self.__Data = []#Used to store the data to send to the server
        self.__running, self.__playing = True, False#Variables to check the status of the game loops


        #Define colours
        self.__Colours = {
            "Black" : (0,0,0),
            "White" : (255,255,255)
            }

        #Load menus
        self.__Menus = {
            "MainMenu" : MainMenu(self.__Settings["Width"], self.__Settings["Height"], "8-Bit", 20, "White"),
            "Options" : OptionsMenu(self.__Settings["Width"], self.__Settings["Height"], "8-Bit", 20, "White"),
            "Volume" : VolumeMenu(self.__Settings["Width"], self.__Settings["Height"], "8-Bit", 20, "White"),
            "Controls" : ControlsMenu(self.__Settings["Width"], self.__Settings["Height"], "8-Bit", 20, "White", self.__Keymap.keys(), [pygame.key.name(self.__Keymap[key]) for key in self.__Keymap]),
            "Credits" : CreditsMenu(self.__Settings["Width"], self.__Settings["Height"], "8-Bit", 20, "White"),
            "Ready" : ReadyMenu(self.__Settings["Width"], self.__Settings["Height"], "8-Bit", 20, "White")
            }
        
        for key in self.__Keymap:
            self.__Menus.update({key:KeyMenu(self.__Settings["Width"], self.__Settings["Height"], "8-Bit", 20, "White", key, pygame.key.name(self.__Keymap[key]))})
        
        self.__CurrentMenu = self.__Menus["MainMenu"]


        #Load options
        self.__Options = {
            "Single/Multiplayer" : "Single",
            "No. of Players" : "1"
            }
            


    #Initialisation functions
    #-------------------------------------------
    def load_settings(self,file):

        settings = open(file,'r')
        text = settings.readline()
        while text != "END":

            values = text.split(',')#Splits into comma separated values
            #print(values)
            #print(int(values[1]))
            self.__Settings[values[0]] =  int(values[1])

            text = settings.readline()

        print("Settings loaded successfully!")
        settings.close()


    def load_controls(self,file):
        """Reads a certain number of lines in the Controls file, assuming that the mapping of each key matches the game files listing of keys"""

        controls = open(file,'r')
        for key in self.__Controls:
            text = controls.readline()
            if text != "END":
                self.__Controls[key] =  text.split(',')[1]

        print("Controls loaded successfully!")
        controls.close()
    #-------------------------------------------


    #Getters and Setters
    #-------------------------------------------
    def get_setting(self,setting):
        try:
            print("Setting", setting, "found with value: ", self.__Settings[setting])
            return self.__Settings[setting]
        except:
            print("Unable to return setting", setting, "! Returning nothing...")
            return

    def set_setting(self,setting,value):
        try:
            self.__Settings[setting] = value
            #print("Setting changed successfully!")
        except:
            print("Unable to change setting ", setting, "to value", value)

    def set_keymap(self,setting,value):
        try:
            self.__Keymap[setting] = pygame.key.key_code(value)
            print("Keymap", setting, "has been updated to", value, "with key code", pygame.key.key_code(value))
        except:
            print("Unable to change the keymap of ", setting, "to value", value)
                

    def get_current_menu(self):
        print("Current menu: ", self.__CurrentMenu)
        return self.__CurrentMenu

    def set_current_menu(self,menu):
        print("Setting menu to: ", menu)
        self.__CurrentMenu = self.__Menus[menu]

    #-------------------------------------------


    def running_loop(self):

        #Initialize the running loop
        returnKeys = []
        keyboardState, mousePosition, mouseState, returnKeys = self.check_menu_events((0,0),(False,False,False), returnKeys)#Here, the mouse_Position must be remembered to avoid inconsistencies with the actual position of the mouse

        while self.__running:#The game_loop function may be called from here, creating an inner loop


            #Build the menus, updating the current menu if necessary
            returnText, returnWidgets, returnSettings, returnValues, currentMenu, self.__playing = self.__CurrentMenu.display_menu(keyboardState, mousePosition, mouseState, returnKeys)
            self.__CurrentMenu = self.__Menus[currentMenu]

            #Display the menus
            for text, xPos, yPos, colour, font, display in returnText:
                self.draw_text(text, int(xPos), int(yPos), colour, font, display)#(text[0], int(text[1]), int(text[2]), int(text[3]), text[4], text[5])
                #self.draw_text(self._MenuItems[x],self._TextSize,self._MenuPositions[x][0],self._MenuPositions[x][1],"White", self.__Display)

            for widget in returnWidgets:
                self.draw_widget(widget)
                #widgetRects = [ [rectType, display, kwargs**]

            for x in range(len(returnSettings)):#Should be strings representing the setting to be changed
                setting = returnSettings[x].split(' ')
                #E.G. "Settings Volume", "50"
                #E.G. "Keymap Enter", "Return"

                #Check for changes to a dictionary
                if setting[0] == "Settings":
                    self.set_setting(setting[1],returnValues[x])
                elif setting[0] == "Keymap":
                    self.set_keymap(setting[1],returnValues[x])

            self.blit_displays([self.__Displays["MenuDisplay"]])



            #Re-check the keyboard state ready for the next iteration of the loop
            returnKeys = []
            keyboardState, mousePosition, mouseState, retunKeys = self.check_menu_events(mousePosition,mouseState,returnKeys)#Here, the mouse_Position must be remembered to avoid inconsistencies with the actual position of the mouse
            #print(keyboardState, mousePosition, mouseState, returnKeys)

            #Check if the game should begin
            if self.__playing == True:#Make sure to check the game settings through the menus

                if self.get_setting("Hosting") == True:
                    #Setup the server
                    print("Setting up host server...")
                    if self.get_setting("Online") == "True":#Online game
                        hostServer = Server(5000, self.get_setting("Players"), True)
                    else:#Offline game
                        hostServer = Server(5000, self.get_setting("Players"), False)
                    
                    #Start the server in a separate thread
                    serverThread = threading.Thread(target=hostServer.start,args=([]), daemon=True)
                    serverThread.start()
                    #hostServer.start()
                    
                    #Setup client to connect to the correct ip and port number
                    self.__Client.set_host("localhost")#hostServer.get_ip())
                    self.__Client.set_port(5000)#hostServer.get_port())

                    #Connect the client to the selected server
                    print("Connecting to server...")
                    print(hostServer)
                    self.__Client.connect()
                
                    print("Waiting for other players...")
                    self.intro_loop()

                    #Play the game
                    print("Entering game loop now...")
                    self.game_loop()

                    #Ensure the server closes after the game has ended
                    serverThread.join()
                
                else:#Find the IP address of a running server
                    #FINISH!!!
                    print("NOT HOSTING!!!")
                    self.__Client.set_host("localhost")
                    self.__Client.set_port(5000)

                #If hosting a server, close the server
                #This is done automatically within the server

                #Reset game settings
                self.set_setting("Players",1)
                self.set_setting("Online",False)
                self.set_setting("Hosting",True)

                #Reset client
                self.__Client.set_host("localhost")
                self.__Client.set_port(5000)

                #Exit to the main menu upon completion of the game
                self.set_current_menu("MainMenu")
            
                

        #Clean environment
        pygame.quit()#Closes the pygame window
        del self#Delete the object ready for the application to close
        #exit()#Closes the python program

    def intro_loop(self):

        #Introduction to the level story if in single player, depending on the map/level
        #load the map
        #display the scrolling text intro
        #after the text has been scrolled, present the ready menu

        #Ready up sequence with all clients

        #Check whether the ready button has been pressed
        #If the button has been pressed, then trigger the server to start the game countdoen if all players are ready
        pass


    def game_loop(self):

        while self.__playing:
            #Check player input
            self.check_game_events()#FINISH!!!

            #Game logic will be performed by the server
            input="Hello World!"

            #Send input to the server, then receive the sprites, game statistics, player info etc. from the server
            self.__Client.send(input)

            #Build the layers, using the data returned from the server

            #Background
            #for tile in self.__MapTiles:



            #Display the layers
            self.blit_displays([self.__Displays["GameBackgroundLayer"], self.__Displays["GameSpriteLayer"], self.__Displays["GameUILayer"]])
            #Build the background layer

            #Build the sprite layer

            #Build the UI layer



    #Methods to obtain keyboard and mouse input
    #-------------------------------------------
    def check_text_events(self, textBox):
        """Used for text entry during the execution of the program"""
        pass

##        #Check if the window has been closed
##        for event in pygame.event.get():
##            #print("EVENT: ", event)
##            if event.type == pygame.QUIT:
##                self.__running, self.__playing = False, False
##                return
##            
##            if event.type == pygame.KEYDOWN:
##                self.showCursor = True
##                self.keyDown = True
##                self.repeatKey = event
##                self.repeatTime = time.time()
##
##                if event.key == pygame.K_BACKSPACE:
##                    if self.cursorPosition != 0:
##                        self.maxLengthReached = False
##                        self.text.pop(self.cursorPosition - 1)
##                        self.onTextChanged(*self.onTextChangedParams)
##
##                    self.cursorPosition = max(self.cursorPosition - 1, 0)
##
##                elif event.key == pygame.K_DELETE:
##                    if not self.cursorPosition >= len(self.text):
##                        self.maxLengthReached = False
##                        self.text.pop(self.cursorPosition)
##                        self.onTextChanged(*self.onTextChangedParams)
##
##                elif event.key == pygame.K_RETURN:
##                    self.onSubmit(*self.onSubmitParams)
##
##                elif event.key == pygame.K_RIGHT:
##                    self.cursorPosition = min(self.cursorPosition + 1, len(self.text))
##
##                elif event.key == pygame.K_LEFT:
##                    self.cursorPosition = max(self.cursorPosition - 1, 0)
##
##                elif event.key == pygame.K_END:
##                    self.cursorPosition = len(self.text)
##
##                elif event.key == pygame.K_ESCAPE:
##                    if not self.escape:
##                        self.selected = False
##                        self.showCursor = False
##                        self.escape = True
##                        self.repeatKey = None
##                        self.keyDown = None
##                        self.firstRepeat = True
##
##                elif not self.maxLengthReached:
##                    if len(event.unicode) > 0:
##                        self.text.insert(self.cursorPosition, event.unicode)
##                        self.cursorPosition += 1
##                        self.onTextChanged(*self.onTextChangedParams)
##
##            elif event.type == pygame.KEYUP:
##                self.repeatKey = None
##                self.keyDown = None
##                self.firstRepeat = True
##                self.escape = False

    
    def check_game_events(self):
        """Used during gameplay,
           since this takes the keys currently pressed down each frame.
           This is part of a separate function to check_menu_events,
           since each function will be checking for different types of input"""
        pass

##        #Check if the window has been closed
##        for event in pygame.event.get():
##            #print("EVENT: ", event)
##            if event.type == pygame.QUIT:
##                self.__running, self.__playing = False, False
##                return
##
##        #Get the keyboard input
##        keyboardInput = pygame.key.get_pressed()
##        
##        #Return the actions specific to the menus
##        return [keyboardInput[self.__Keymap["MoveUp"]],
##                keyboardInput[self.__Keymap["MoveDown"]],
##                keyboardInput[self.__Keymap["Enter"]],
##                keyboardInput[self.__Keymap["Backspace"]]]

    def check_menu_events(self, mousePosition, mouseState, returnKeys):
        """Used during menus or text input,
           since this gathers each key that has been pressed down on the current frame"""


        #Capture each key that has been pressed down this frame
        keyboardState = [False,False,False,False,False,False,False]
        #keyboardState: ["MoveLeft","MoveRight","MoveUp","MoveDown","Enter","Backspace"]
        #This is used to check for any actions that need to be taken
        #Copies are made, since this information needs to be passed to other classes in different files, in which pygame is not imported

        #returnKeys = ['h', 'i']#This is used to capture any other keys that have been pressed for pur[oses such as changing the key mapping
        
        #mouseState = (False,False,False)
        #mouseState: (LeftClick,MiddleClick,RightClick)

        
        #Check if the window hafs been closed
        for event in pygame.event.get():
            #print("EVENT: ", event)
            if event.type == pygame.QUIT:
                self.__running, self.__playing = False, False
                return keyboardState, mousePosition, mouseState, returnKeys#Ensure the function will always return the same type

            #Mouse Position
            if event.type == pygame.MOUSEMOTION:
                mousePosition = pygame.mouse.get_pos()
                print("The mouse has been moved to position: ", mousePosition)

            #Mouse State
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                mouseState = pygame.mouse.get_pressed()
                print("The mouse state has been changed to: ", mouseState)


            #Keyboard input
            if event.type == pygame.KEYDOWN:
                print("A key has been pressed!")

                #Arrow keys
                if event.key == self.__Keymap["MoveLeft"]:#Here, all the options are if/switch statements without a break so that keys mapped to multiple actions will be registered for all actions they have been mapped to
                    print("Left arrow pressed")
                    keyboardState[0]=True
                    
                if event.key == self.__Keymap["MoveRight"]:
                    print("Right arrow pressed")
                    keyboardState[1]=True
                    
                if event.key == self.__Keymap["MoveUp"]:
                    print("Up arrow pressed")
                    keyboardState[2]=True
                    
                if event.key == self.__Keymap["MoveDown"]:
                    print("Down arrow pressed")
                    keyboardState[3]=True

                #Enter key
                if event.key == self.__Keymap["Enter"]:
                    print("Enter pressed")
                    keyboardState[4]=True

                #Backspace
                if event.key == self.__Keymap["Backspace"]:
                    print("Backspace pressed")
                    keyboardState[5]=True

                #Escape key
                if event.key == self.__Keymap["Escape"]:
                    print("Escape pressed")
                    keyboardState[6]=True

                #Record the name of the key that has been pressed
                #print(pygame.key.name(event.key))
                returnKeys.append(pygame.key.name(event.key))


                #else:#Any unicode characters
                #    x = event.unicode
                #    print("Key ",x ,"has been pressed!")

        return keyboardState, mousePosition, mouseState, returnKeys#returnKeys
    #-------------------------------------------


    def draw_text(self, text, x, y, colour, font, display):#Here, the size of a font can't be changed after it has been created, therefore requiring additional fonts with different sizes
        """Pre-condition: The font is already defined as the game is initialised"""

        #Render the text
        text_surface = self.__Fonts[font].render(text, True, self.__Colours[colour])

        #Find and position the produced rect that contains the text
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)

        #Blit the text to the screen
        self.__Displays[display].blit(text_surface,text_rect)

    def draw_widget(self, rects):
        """Used to draw rects from a widget as part of the widget class"""

        #print(rects)
        for rect in rects:
            #rect: [rectType,xPos,yPos, args specific to rect type]
            #print(rect)
            if rect[0] == "Rect":
                pygame.draw.rect(self.__Displays[rect[6]],tuple(map(int, rect[5].split(','))),(int(rect[1]),int(rect[2]),int(rect[3]),int(rect[4])))
                                #Display,Colour,(xPos,yPos,width,height)

            elif rect[0] == "Text":
                self.draw_text(rect[1], int(rect[2]), int(rect[3]), rect[4], rect[5], rect[6])


            elif rect[0] == "Circle":
                pygame.draw.circle(self.__Displays[rect[5]], tuple(map(int, rect[4].split(','))), (int(rect[1]), int(rect[2])), int(rect[3]))
                                    #Display,Colour,(centreX,centreY),Radius)

            elif rect[0] == "FilledCircle":
                pygame.gfxdraw.filled_circle(self.__Displays[rect[5]], int(rect[1]), int(rect[2]), int(rect[3]), tuple(map(int, rect[4].split(','))))
                                            #Display, x, y, radius, colour 



    def blit_image(self, image, x, y, width, height, display):
        """Blit an image from another class onto a screen"""
        pass



    def blit_displays(self, displays):
        """Blits the current menu to the screen, updates the display, then refreshes the screen ready for the next frame
           Pre-condition: All displays must be the same size to prevent screen tearing when changing displays"""

        #Blit the screen
        for display in displays:
            self.__Window.blit(display, (0,0))#This draws to the screen without updating what is displayed to the user

        #Update the display
        pygame.display.update()

        #Refresh the screen for the next frame
        for display in displays:
            display.fill((0,0,0))
        


#    def display_menus(self):
#        menuCondition = True
#        while menuCondition:
#            #Create the menu
#            menuCondition = self.__CurrentMenu.display_menu()#Returns a boolean
#            #Here, this function also changes the menu depending on the input from the client, menaing this covers all menus the game will display
#
#            #Blit the menu to the screen
#            self.blit_menu()


    def refresh_screen(self):
        self.__Display.fill((0,0,0))
