"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Aashri Aggarwal (aia56) and Abby Sachar (ahs265)
# December 10th, 2019
"""
from consts import *
from game2d import *
import random
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    pass

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip_x(self):
        """
        Returns the horizontal coordinate of the ship object
        """
        return self.x

    def __init__(self, x, y, width = SHIP_WIDTH, height = SHIP_HEIGHT):
        """
        Initializes the ship dimensions.

        Parameter x: The horizontal coordinate of the object center
        Precondition: Value must be an int or float

        Parameter y: The vertical coordinate of the object center
        Precondition: Value must be an int or float

        Parameter source: The image file of the object created
        Precondition: Must be a png file

        Parameter width: The horizontal length of the object
        Precondition: Value must be an int or float and must be >= 0

        Parameter height: The vertical length of the object
        Precondition: Value must be an int or float and must be >= 0
        """
        assert type(x) in [int, float]
        assert type(y) in [int, float]
        assert type(width) == int or type(width) == float
        assert width >= 0
        assert type(height) == int or type(height) == float
        assert height >= 0

        super().__init__(x=x, y=y,width = width, height = height, source = 'Ship.png')

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collideswShip(self, bolt):
        """
        Returns True if the alien bolt collides with the ship.

        This method returns False if bolt was not fired by an alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        #Check if bolt was fired by player
        if bolt.getVelocity() > 0:
            return False
        if self.contains(bolt.leftTopCorner()) == True:
            return True
        elif self.contains(bolt.rightTopCorner()) == True:
            return True
        elif self.contains(bolt.leftBottomCorner()) == True:
            return True
        elif self.contains(bolt.rightBottomCorner()) == True:
            return True
        else:
            return False

    def collideswShip2(self, pup):
        """
        Returns True if the alien bolt collides with the ship.

        This method returns False if bolt was not fired by an alien.

        Parameter pup: The powerup to check
        Precondition: pup is of class PowerUp
        """
        #Check if bolt was fired by player
        if self.contains(pup.leftTopCorner()) == True:
            return True
        elif self.contains(pup.rightTopCorner()) == True:
            return True
        elif self.contains(pup.leftBottomCorner()) == True:
            return True
        elif self.contains(pup.rightBottomCorner()) == True:
            return True
        else:
            return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    #Attribute: _points: number of points an alien is worth
    #Invariant: _points is an int >= 0
    pass

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAlien_x(self):
        """
        Returns the x coordinate of the alien object.
        """
        return self.x

    def getAlien_y(self):
        """
        Returns the y coordinate of the alien object.
        """
        return self.y

    def getAlienpoints(self):
        """
        Returns the number of points the alien is worth.
        """
        return self._points

    def setAlien_x(self, value):
        """
        Sets x coordinate of the alien object to value.

        Parameter value: the new x coordinate for the alien object
        Precondition: must be an int or float
        """
        assert type(value) in [int, float]
        self.x = value

    def setAlien_y(self, value):
        """
        Sets y coordinate of the alien object to value.

        Parameter value: the new y coordinate for the alien object
        Precondition: must be an int or float
        """
        assert type(value) in [int, float]
        self.y = value

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, source, width = ALIEN_WIDTH, height = ALIEN_HEIGHT):
        """
        Initializes the alien dimensions.

        Parameter x: The horizontal coordinate of the object center
        Precondition: Value must be an int or float

        Parameter y: The vertical coordinate of the object center
        Precondition: Value must be an int or float

        Parameter source: The image file of the object created
        Precondition: Must be a png file

        Parameter width: The horizontal length of the object
        Precondition: Value must be an int or float and must be >= 0

        Parameter height: The vertical length of the object
        Precondition: Value must be an int or float and must be >= 0
        """
        assert type(x) in [int, float]
        assert type(y) in [int, float]
        assert source in ALIEN_IMAGES
        assert type(width) == int or type(width) == float
        assert width >= 0
        assert type(height) == int or type(height) == float
        assert height >= 0

        super().__init__(x=x, y=y,width = width, height = height, source = source)
        if source == ALIEN_IMAGES[0]:
            self._points = 10
        elif source == ALIEN_IMAGES[1]:
            self._points = 20
        elif source == ALIEN_IMAGES[2]:
            self._points = 30

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collideswAlien(self, bolt):
        """
        Returns True if the player bolt collides with this Alien.

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        #Check if bolt was fired by player
        if bolt.getVelocity() < 0:
            return False
        if self.contains(bolt.leftTopCorner()) == True:
            return True
        elif self.contains(bolt.rightTopCorner()) == True:
            return True
        elif self.contains(bolt.leftBottomCorner()) == True:
            return True
        elif self.contains(bolt.rightBottomCorner()) == True:
            return True
        else:
            return False

     # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float
    #

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """
        Return _velocity of the bolt object.
        """
        return self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, velocity, x, y):
        """
        Initializes the bolt dimensions
        """
        super().__init__(x = x, y = y, width = BOLT_WIDTH, height  = BOLT_HEIGHT,
        fillcolor = 'red', linecolor = 'red')
        self._velocity = velocity

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Changes the velocity for a bolt fired by the player
        """
        self._velocity = BOLT_SPEED

    def isAlienBolt(self):
        """
        Changes the velocity for a bolt fired by the alien
        """
        self._velocity = -BOLT_SPEED

    def leftTopCorner(self):
        """
        Returns the top left corner of the bolt object as a tuble.
        """
        x = self.x - 1/2*self.width
        y = self.y + 1/2*self.height
        return (x,y)

    def rightTopCorner(self):
        """
        Returns the top right corner of the bolt object as a tuble.
        """
        x = self.x + 1/2*self.width
        y = self.y + 1/2*self.height
        return (x,y)

    def leftBottomCorner(self):
        """
        Returns the bottom left corner of the bolt object as a tuble.
        """
        x = self.x - 1/2*self.width
        y = self.y - 1/2*self.height
        return (x,y)

    def rightBottomCorner(self):
        """
        Returns the bottom left corner of the bolt object as a tuble.
        """
        x = self.x + 1/2*self.width
        y = self.y - 1/2*self.height
        return (x,y)

    # IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class Heart(GImage):
    """
    A class representing a heart (life).
    """
    def __init__(self, x, y):
        """
        Initializes the heart object.

        Parameter x: The horizontal coordinate of the object center
        Precondition: Value must be an int or float

        Parameter y: The vertical coordinate of the object center
        Precondition: Value must be an int or float
        """
        width = HEART_WIDTH
        height = HEART_HEIGHT
        source = 'heart.png'
        super().__init__(x=x, y=y,width = width, height = height, source = source)

class Spark(GEllipse):
    """
    A class to represent particles created in shell explosions.
    """
    # HIDDEN ATTRIBUTES
    # Attribute _vx: velocity in x direction
    # Invariant: _vx is a float
    #
    # Attribute _vy: velocity in y direction
    # Invariant: _vy is a float

    def __init__(self, x, y, color=WHITE_COLOR):
        """
        Initializes a particle at (x,y) with random velocity and given color.

        Parameter x: the starting x-coordinate
        Precondition: x is a number (int or float)

        Parameter y: the starting y-coordinate
        Precondition: y is a number (int or float)

        Parameter color: the spark color
        Precondition: color is a valid color object or name (e.g. a string)
        """
        super().__init__(x=x, y=y,
                         width=PARTICLE_DIAMETER, height=PARTICLE_DIAMETER,
                         fillcolor=color)
        self._vy = random.uniform(-MAX_INIT_VEL,MAX_INIT_VEL)
        self._vx = math.sqrt(MAX_INIT_VEL**2 - self._vy**2) * math.sin(random.uniform(0,2*math.pi))

    def move(self):
        """
        Moves the spark by the current velocity
        """
        self.x += self._vx
        self.y += self._vy
        self._vy += GRAVITY

class PowerUp(GImage):
    """
    A class representing different power ups.

    The class will have different power ups including: ExtraLife
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    def __init__(self, x):
        """
        Initializes a game object powerup.
        """
        source = 'heart.png'
        y = GAME_WIDTH - 100
        width = PUP_WIDTH
        height = PUP_HIEGHT
        super().__init__(x = x, y = y, width = width, height = height, source = source)

    def leftTopCorner(self):
        """
        Returns the top left corner of the bolt object as a tuble.
        """
        x = self.x - 1/2*self.width
        y = self.y + 1/2*self.height
        return (x,y)

    def rightTopCorner(self):
        """
        Returns the top right corner of the bolt object as a tuble.
        """
        x = self.x + 1/2*self.width
        y = self.y + 1/2*self.height
        return (x,y)

    def leftBottomCorner(self):
        """
        Returns the bottom left corner of the bolt object as a tuble.
        """
        x = self.x - 1/2*self.width
        y = self.y - 1/2*self.height
        return (x,y)

    def rightBottomCorner(self):
        """
        Returns the bottom left corner of the bolt object as a tuble.
        """
        x = self.x + 1/2*self.width
        y = self.y - 1/2*self.height
        return (x,y)
