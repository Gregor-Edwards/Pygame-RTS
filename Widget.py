#Widgets
#Used within the menu class, which in turn interacts with the game class to display things using pygame
#Re-purposed from pygame-widgets


class Widget():
    def __init__(self, x, y, width, height, display):
        """ Base for all widgets

        :param x: X-coordinate of top left
        :type x: int
        :param y: Y-coordinate of top left
        :type y: int
        :param width: Width of button
        :type width: int
        :param height: Height of button
        :type height: int
        """

        self._X = x
        self._Y = y
        self._Width = width
        self._Height = height
        self._Display = display

        self._Hidden = False
        self._Disabled = False


    
    def listen(self, events):#Different widgets should return different values, which are to be handled outside the widget class
        pass

    
    def draw(self):#Returns the rects required to draw the widget to a display. This is also handled outside the widget class
        return []

    def contains(self, x, y):
        if x in range(self._X, self._X + self._Width) and y in range(self._Y,self._Y + self._Height):
            return True
        else:
            return False


    #Getters and Setters
    #-------------------------------------------
    def get_hidden(self):
        return self._Hidden

    def set_hidden(self, state):
        self._Hidden = state

    def get_disabled(self):
        return self._Disabled

    def set_disabled(self, state):
        self._Disabled = state

    def get_pos(self):
        return self._X, self._Y

    def set_position(self, x, y):#Enables the widget to be moved after being created, allowing for more interactive possibilities
        self._X = x
        self._Y = y

    def get_dimensions(self):
        return self._Width, self._Height

    def set_dimensions(self, width, height):
        self._Width = width
        self._Height = height
    #-------------------------------------------




class Slider(Widget):
    def __init__(self, x, y, width, height, display, **kwargs):
        """kwargs: enables customisation of the slider

                    min: minimum value of the slider
                    max: maximum value of the slider
                    step: values the slider increments by
                    value: initial value of the slider
                    colour: colour of the slider bar
                    handleColour: colour of the slider handle
                    boarderThickness: thickness of the boarder
                    boarderColour: colour of the boarder
                    curved: decides whether the slider will have curved edges
                    vertical: decides whether the slider is vertical or horizontal
                    handleRadius: determines the size of the slider handle"""


        #Setup rects around the widget
        Widget.__init__(self, x, y, width, height, display)


        #Setup numerical attributes
        self.__Min = kwargs.get('min', 0)#Here, if the 'min' argument isn't found, then the default value will be 0 instead
        self.__Max = kwargs.get('max', 100)
        self.__Step = kwargs.get('step', 1)
        self.__Value = kwargs.get('value', self.__Min)

        #Setup graphical attributes
        self.__Colour = kwargs.get('colour', (200, 200, 200))
        self.__HandleColour = kwargs.get('handleColour', (50, 50, 50))

        self.__BorderThickness = kwargs.get('borderThickness', 3)
        self.__BorderColour = kwargs.get('borderColour', (0, 0, 0))

        self.__Curved = kwargs.get('curved', True)
        self.__Vertical = kwargs.get('vertical', False)

        if self.__Curved:
            if self.__Vertical:
                self.__Radius = self._Width // 2
            else:
                self.__Radius = self._Height // 2

        if self.__Vertical:
            self.__HandleRadius = kwargs.get('handleRadius', int(self._Width / 1.3))
        else:
            self.__HandleRadius = kwargs.get('handleRadius', int(self._Height / 1.3))


        #Setup logical attributes
        self.__Selected = False

    #Method for collision detection
    #-------------------------------------------
    def contains(self, x, y):
        """Checks if position (x,y) is within the radius of the slider handle"""
        #Here, self._X and self._Y are the coordinates of the top left of the slider bar
        
        #Find the position of the slider handle
        if self.__Vertical:
            handleX = self._X + self._Width // 2
            handleY = int(self._Y + (self.__Max - self.__Value) / (self.__Max - self.__Min) * self._Height)
        else:
            handleX = int(self._X + (self.__Value - self.__Min) / (self.__Max - self.__Min) * self._Width)#Position of the slider handle from left to right
            handleY = self._Y + self._Height // 2#Middle of the slider bar from top to bottom

        #Check if the mouse position is within the radius of the slider handle
        #E.G. x^2 +y^2 = r^2 for a right angled triangle, in which r is the radius of the circle
        if (handleX - x) ** 2 + (handleY - y) ** 2 <= self.__HandleRadius ** 2:
            return True

        return False
    #-------------------------------------------


    def listen(self, keyboardState, mousePosition, mouseState):
        """mouseState: (leftClick,middleClick,rightClick)"""

        if (not self._Hidden) and (not self._Disabled):
            x, y = mousePosition

            #Check selection status
            if self.contains(x, y) and (mouseState[0] == True):
                self.__Selected = True

            if mouseState[0] == False:#FINISH by checking how the keyboard state constants are transmitted after checking the menu events
                self.__Selected = False

            #Move the slider handle and update the value
            if self.__Selected:
                if self.__Vertical:
                    self.__Value = self.__Max - self.round((y - self._Y) / self._Height * self.__Max)
                    self.__Value = max(min(self.__Value, self.__Max), self.__Min)#Ensures the value stays within the correct bounds and makes sure the handle isn't places beyond the edge of the slider bar
                else:
                    self.__Value = self.round((x - self._X) / self._Width * self.__Max + self.__Min)
                    self.__Value = max(min(self.__Value, self.__Max), self.__Min)
                    #print(self.__Value)

        return self.__Value


    def round(self, value):
        """Ensures both the value and handle remain in valid states when the step size varies"""
        return self.__Step * round(value / self.__Step)
    

    def draw(self):
        """Builds the rect required to draw the widget using positions relative to the top left position of the widget"""
        
        returnRects = []
        
        if not self._Hidden:
            returnRects.append(["Rect", str(self._X), str(self._Y), str(self._Width), str(self._Height), str(self.__Colour[0])+","+str(self.__Colour[1])+","+str(self.__Colour[2]), self._Display])
            #pygame.draw.rect(self.win, self.colour, (self._x, self._y, self._width, self._height))

            if self.__Vertical:
                if self.__Curved:
                    #Circles drawn at the end of the slider bar
                    returnRects.append(["Circle", str(self._X + self._Width // 2), str(self._Y), str(self.__Radius), str(self.__Colour[0])+","+str(self.__Colour[1])+","+str(self.__Colour[2]), self._Display])
                    returnRects.append(["Circle", str(self._X + self._Width // 2), str(self._y + self._Height), str(self.__Radius), str(self.__Colour[0])+","+str(self.__Colour[1])+","+str(self.__Colour[2]), self._Display])

                    #pygame.draw.circle(self.win, self.colour, (self._x + self._width // 2, self._y), self.radius)
                    #pygame.draw.circle(self.win, self.colour, (self._x + self._width // 2, self._y + self._height),self.radius)

                #Draw the slider handle
                returnRects.append(["FilledCircle", str(self._X + self._Width // 2), str(self._Y + int((self.__Max - self.__Value) / (self.__Max - self.__Min) * self._Height)), str(self.__HandleRadius), str(self.__HandleColour[0])+","+str(self.__HandleColour[1])+","+str(self.__HandleColour[2]), self._Display])
                returnRects.append(["AntialiasedCircle", str(self._X + self._Width // 2), str(self._Y + (self.__Max - self.__Value) / (self.__Max - self.__Min) * self._Height), str(self.__HandleRadius), self.__HandleColour, self._Display])

                #handleCircle = (self._x + self._width // 2, int(self._y + (self.max - self.value) / (self.max - self.min) * self._height))

            else:
                if self.__Curved:

                    #Circles drawn at the end of the slider bar
                    returnRects.append(["Circle", str(self._X), str(self._Y + self._Height // 2), str(self.__Radius), str(self.__Colour[0])+","+str(self.__Colour[1])+","+str(self.__Colour[2]), self._Display])
                    returnRects.append(["Circle", str(self._X + self._Width), str(self._Y + self._Height // 2), str(self.__Radius), str(self.__Colour[0])+","+str(self.__Colour[1])+","+str(self.__Colour[2]), self._Display])

                    #pygame.draw.circle(self.win, self.colour, (self._x, self._y + self._height // 2), self.radius)
                    #pygame.draw.circle(self.win, self.colour, (self._x + self._width, self._y + self._height // 2),self.radius)

                #Draw the slider handle
                returnRects.append(["FilledCircle", str(self._X + int((self.__Value - self.__Min) / (self.__Max - self.__Min) * self._Width)), str(self._Y + self._Height // 2), str(self.__HandleRadius), str(self.__HandleColour[0])+","+str(self.__HandleColour[1])+","+str(self.__HandleColour[2]), self._Display])
                returnRects.append(["AntialiasedCircle", str(self._X + (self.__Value - self.__Min) / (self.__Max - self.__Min) * self._Width), str(self._Y + self._Height // 2), str(self.__HandleRadius), self.__HandleColour, self._Display])

                #handleCircle = (int(self._x + (self.value - self.min) / (self.max - self.min) * self._width),self._y + self._height // 2)
 
            #gfxdraw.filled_circle(self.win, *circle, self.handleRadius, self.handleColour)
            #gfxdraw.aacircle(self.win, *circle, self.handleRadius, self.handleColour)


            #Return the value of the slider to enable interactive changes elsewhere
            print("DRAWING SLIDER!!!")
            return returnRects


    #Getters and Setters
    #-------------------------------------------
    def getValue(self):
        return self.__Value

    def setValue(self, value):
        self.__Value = value
    #-------------------------------------------





class Button(Widget):
    def __init__(self, x, y, width, height, display, text, **kwargs):
        """kwargs: enables customisation of the 

                    inactiveColour: colour when the button is inactive, not pressed and the mouse isn't hovering over it
                    hoverColour: colour when the mouse hovers over the button
                    pressedColour: colour when the button has been activated and pressed
                    colour: the actual colour of the button. This will be overridden with the correct colour given the current state of the button
                    shadowDistance: size of the shadow behind the button
                    shadowColour: colour of the shadow
                    onClick: function to execute when the button has been pressed
                    onRelease: function to execute when the button has been released
                    onClickParams: parameters required to execute the oclick function
                    onReleaseParams: parameters required to execute the onRelease function

                    textColour: colour of the text held in the button
                    fontSize: size of the text held in the button
                    text: text held in the button
                    font: font of the text held in the button
                    textHAlign: horizontal text allignment
                    textVAlign: vertical text allignment
                    margin

                    image
                    imageHAlign
                    imageVAlign

                    borderThickness: thickness of the border on the button
                    inactiveBorderColour: colour of the border when the button is inactive, not pressed and the mouse isn't hovering over it
                    hoverBorderColour: colour of the border when the mouse hovers over the button
                    radius"""


        Widget.__init__(self, x, y, width, height, display)

        #Colour
        self.__InactiveColour = kwargs.get('inactiveColour', (150, 150, 150))
        self.__HoverColour = kwargs.get('hoverColour', (125, 125, 125))
        self.__PressedColour = kwargs.get('pressedColour', (100, 100, 100))
        self.__Colour = kwargs.get('colour', self.__InactiveColour)  # Allows colour to override inactiveColour
        self.__ShadowDistance = kwargs.get('shadowDistance', 0)
        self.__ShadowColour = kwargs.get('shadowColour', (210, 210, 180))

        #Function
        #self.__onClick = kwargs.get('onClick', lambda *args: None)
        #self.__onRelease = kwargs.get('onRelease', lambda *args: None)
        #self.__onClickParams = kwargs.get('onClickParams', ())
        #self.__onReleaseParams = kwargs.get('onReleaseParams', ())
        self.__Clicked = False#Used to determine when the button has just been clicked without just hovering over the button or holding down left click

        #Text
        self.__TextColour = kwargs.get('textColour', "White")
        self.__FontSize = kwargs.get('fontSize', 20)
        self.__Font = kwargs.get('font', "sans-serif")
        self.__Text = text
        self.__TextHAlign = kwargs.get('textHAlign', 'centre')
        self.__TextVAlign = kwargs.get('textVAlign', 'centre')
        self.__Margin = kwargs.get('margin', 20)

        #Image
        #self.__Image = kwargs.get('image', None)
        #self.__ImageHAlign = kwargs.get('imageHAlign', 'centre')
        #self.__ImageVAlign = kwargs.get('imageVAlign', 'centre')


        #Text allignment
        #self.__textRect = ["Rect", str(self._X), str(self._Y), str(self._Width), str(self._Height), str(self.__Colour[0])+","+str(self.__Colour[1])+","+str(self.__Colour[2]), self._Display]

        #self.alignTextRect()

        # Image
        #self.__image = kwargs.get('image', None)
        #self.__imageHAlign = kwargs.get('imageHAlign', 'centre')
        #self.__imageVAlign = kwargs.get('imageVAlign', 'centre')

        #if self.__image:
        #    self.__imageRect = self.image.get_rect()
        #    self.alignImageRect()

        # Border
        self.__BorderThickness = kwargs.get('borderThickness', 0)
        self.__InactiveBorderColour = kwargs.get('inactiveBorderColour', (0, 0, 0))
        self.__HoverBorderColour = kwargs.get('hoverBorderColour', (80, 80, 80))
        self.__PressedBorderColour = kwargs.get('pressedBorderColour', (100, 100, 100))
        self.__BorderColour = kwargs.get('borderColour', self.__InactiveBorderColour)
        self.__InactiveBorderColour = self.__BorderColour
        self.__Radius = kwargs.get('radius', 0)

    #def alignImageRect(self):
    #    self.imageRect.center = (self._x + self._width // 2, self._y + self._height // 2)

        #if self.imageHAlign == 'left':
        #    self.imageRect.left = self._x + self.margin
        #elif self.imageHAlign == 'right':
        #    self.imageRect.right = self._x + self._width - self.margin

        #if self.imageVAlign == 'top':
        #    self.imageRect.top = self._y + self.margin
        #elif self.imageVAlign == 'bottom':
        #    self.imageRect.bottom = self._y + self._height - self.margin

    #def alignTextRect(self):
    #    self.textRect.center = (self._x + self._width // 2, self._y + self._height // 2)

        #if self.textHAlign == 'left':
        #    self.textRect.left = self._x + self.margin
        #elif self.textHAlign == 'right':
        #    self.textRect.right = self._x + self._width - self.margin

        #if self.textVAlign == 'top':
        #    self.textRect.top = self._y + self.margin
        #elif self.textVAlign == 'bottom':
        #    self.textRect.bottom = self._y + self._height - self.margin

    def listen(self, keyboardState, mousePosition, mouseState):

        if (not self._Hidden) and (not self._Disabled):
            x, y = mousePosition

            if self.contains(x, y):

                #Check for clicked button
                if (mouseState[0] == False) and self.__Clicked:
                    self.__Clicked = False
                    #self.onRelease(*self.onReleaseParams)
                    print(self.__Text)
                    return True

                #Check for pressed button
                elif mouseState[0] == True:
                    self.__Clicked = True
                    #self.onClick(*self.onClickParams)
                    self.__Colour = self.__PressedColour
                    self.__BorderColour = self.__PressedBorderColour

                #Check for mouse hovering over the button
                else:
                    self.__Colour = self.__HoverColour
                    self.__BorderColour = self.__HoverBorderColour

            #Check for mouse dragging over the button without clicking it, regardless of whether or not it was being pressed
            else:
                self.__Clicked = False
                self.__Colour = self.__InactiveColour
                self.__BorderColour = self.__InactiveBorderColour

        #In any scenario where the button isn't clicked, return False
        return False

    def draw(self):
        """Build the rects required to draw the widget"""


        returnRects = []
        
        if not self._Hidden:

            #Border rects
            returnRects.append(["Rect", str(self._X + self.__Radius), str(self._Y), str(self._Width - 2*self.__Radius), str(self._Height), str(self.__BorderColour[0])+","+str(self.__BorderColour[1])+","+str(self.__BorderColour[2]), self._Display])
            returnRects.append(["Rect", str(self._X), str(self._Y + self.__Radius), str(self._Width), str(self._Height - 2*self.__Radius), str(self.__BorderColour[0])+","+str(self.__BorderColour[1])+","+str(self.__BorderColour[2]), self._Display])


            #Border circles
            returnRects.append(["Circle", str(self._X + self.__Radius), str(self._Y + self.__Radius), str(self.__Radius), str(self.__BorderColour[0])+","+str(self.__BorderColour[1])+","+str(self.__BorderColour[2]), self._Display])
            returnRects.append(["Circle", str(self._X + self.__Radius), str(self._Y + self._Height - self.__Radius), str(self.__Radius), str(self.__BorderColour[0])+","+str(self.__BorderColour[1])+","+str(self.__BorderColour[2]), self._Display])
            returnRects.append(["Circle", str(self._X + self._Width - self.__Radius), str(self._Y + self.__Radius), str(self.__Radius), str(self.__BorderColour[0])+","+str(self.__BorderColour[1])+","+str(self.__BorderColour[2]), self._Display])
            returnRects.append(["Circle", str(self._X + self._Width - self.__Radius), str(self._Y + self._Height - self.__Radius), str(self.__Radius), str(self.__BorderColour[0])+","+str(self.__BorderColour[1])+","+str(self.__BorderColour[2]), self._Display])

            #BackgroundRects
            returnRects.append(["Rect", str(self._X + self.__BorderThickness + self.__Radius), str(self._Y + self.__BorderThickness), str(self._Width - 2*(self.__BorderThickness + self.__Radius)), str(self._Height - 2*self.__BorderThickness), str(self.__Colour[0])+","+str(self.__Colour[1])+","+str(self.__Colour[2]), self._Display])
            returnRects.append(["Rect", str(self._X + self.__BorderThickness), str(self._Y + self.__BorderThickness + self.__Radius), str(self._Width - 2*self.__BorderThickness), str(self._Height - 2*(self.__BorderThickness + self.__Radius)), str(self.__Colour[0])+","+str(self.__Colour[1])+","+str(self.__Colour[2]), self._Display])

            #Background circles
            returnRects.append(["Circle", str(self._X + self.__Radius + self.__BorderThickness), str(self._Y + self.__Radius + self.__BorderThickness), str(self.__Radius), str(self.__Colour[0])+","+str(self.__Colour[1])+","+str(self.__Colour[2]), self._Display])
            returnRects.append(["Circle", str(self._X + self.__Radius), str(self._Y + self._Height - self.__Radius - self.__BorderThickness), str(self.__Radius), str(self.__Colour[0])+","+str(self.__Colour[1])+","+str(self.__Colour[2]), self._Display])
            returnRects.append(["Circle", str(self._X + self._Width - self.__Radius - self.__BorderThickness), str(self._Y + self.__Radius + self.__BorderThickness), str(self.__Radius), str(self.__Colour[0])+","+str(self.__Colour[1])+","+str(self.__Colour[2]), self._Display])
            returnRects.append(["Circle", str(self._X + self._Width - self.__Radius - self.__BorderThickness), str(self._Y + self._Height - self.__Radius - self.__BorderThickness), str(self.__Radius), str(self.__Colour[0])+","+str(self.__Colour[1])+","+str(self.__Colour[2]), self._Display])

            #Text
            returnRects.append(["Text", self.__Text, str(self._X + (self._Width // 2)), str(self._Y + (self._Height // 2)), self.__TextColour, self.__Font, self._Display])
            
            #if self.image:
            #    self.imageRect = self.image.get_rect()
            #    self.alignImageRect()
            #    self.win.blit(self.image, self.imageRect)

            #self.textRect = self.text.get_rect()
            #self.alignTextRect()
            #self.win.blit(self.text, self.textRect)

            return returnRects

    def get_text(self):
        return self.__Text

    def get_font(self):
        return self.__Font


    #def setImage(self, image):
    #    self.image = image
    #    self.imageRect = self.image.get_rect()
    #    self.alignImageRect()

    #def setOnClick(self, onClick, params=()):
    #    self.onClick = onClick
    #    self.onClickParams = params

    #def setOnRelease(self, onRelease, params=()):
    #    self.onRelease = onRelease
    #    self.onReleaseParams = params

    #def setInactiveColour(self, colour):
    #    self.inactiveColour = colour

    #def setPressedColour(self, colour):
    #    self.pressedColour = colour

    #def setHoverColour(self, colour):
    #    self.hoverColour = colour

    #def get(self, attr):
    #    parent = super().get(attr)
    #    if parent is not None:
    #        return parent

    #    if attr == 'colour':
    #        return self.colour

    #def set(self, attr, value):
    #    super().set(attr, value)

    #    if attr == 'colour':
    #        self.inactiveColour = value
