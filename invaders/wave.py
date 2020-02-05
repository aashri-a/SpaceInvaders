"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Aashri Aggarwal (aia56) and Abby Sachar (ahs265)
# December 10th, 2019
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    #Attribute _direction: the direction that the aliens are moving
    #Invariant: _direction is a string that is either "left" or "right"
    #
    #Attribute _fire: the number of steps until an alien fires
    #Invariant: _fire is an int between 1 and BOLT_RATE
    #
    #Attribute _aliensteps: the number of steps alien has taken since firing a bolt
    #Invariant: _aliensteps: is an int between 0 and BOLT_RATE
    #
    #Attribute _end: when the wave is finished or the user has lost
    #Invariant: _end is True when the wave is over and False when the wave is not finished
    #
    #Attribute _win: determines if the outcome is a win or a loss
    #Invariant: _win is True when the player has won or False when the aliens have won
    #
    #Attribute: _speed: the speed of the alien movement
    #Invariant: the number of seconds (0 < float <= 1) between alien steps
    #
    #Attribute: _alienrows: the number of rows of aliens
    #Invariant: _alienrows is an int between ALIEN_ROWS and 10
    #
    #Attribute: _score: the player score
    #Invariant: _score is a int >= 0
    #
    #Attribute: _release: the number of steps alien until a PowerUp is released
    #Invariant: _release is an int between 0 and BOLT_RATE


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        Returns the value of self._ship
        """
        return self._ship

    def getLives(self):
        """
        Returns the value of self._lives
        """
        return self._lives

    def getSpeed(self):
        """
        Returns the value of self._speed
        """
        return self._speed

    def getScore(self):
        """
        Returns the value of self._score
        """
        return self._score

    def getAlienRows(self):
        """
        Returns the value of self._alienrows
        """
        return self._alienrows

    def getEnd(self):
        """
        Returns the value of self._end.
        """
        return self._end

    def getWin(self):
        """
        Returns the value of self._win.
        """
        return self._win

    def __init__(self, lives, speed, alienrows, score):
        """
        Initializing the wave.

        Parameter lives: the number of lives the player has remaining
        Precondition: lives is an int between 0 and SHIP_LIVES

        Parameter speed: the speed the aliens move across the screen
        Precondition: speed is a float between 0 and ALIEN_SPEED
        """
        self._alienrows = alienrows
        self._aliens = self._createList()
        self._ship = Ship(GAME_WIDTH/2, SHIP_BOTTOM)
        line = [0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE]
        self._dline = GPath(points = line, linewidth = 3, linecolor = 'white')
        self._time = 0
        self._direction = 'right'
        self._bolts = []
        self._fire = random.randint(1,BOLT_RATE)
        self._aliensteps = 0
        self._lives = lives
        self._end = False
        self._win = False
        self._heart = self._drawLives()
        self._speed = speed
        self._sparks = []
        self._score = score
        self._time2 = 0
        self._release = random.randint(5, PUP_RATE)
        self._powerup = []

    def updatePowerUp(self, dt):
        """
        """
        self._time2 = self._time2+ dt
        if self._release <= self._time2:
            x = random.randint(0, GAME_WIDTH)
            self._powerup.append(PowerUp(x))
            self._release = random.randint(5, PUP_RATE)
            self._time2 = 0

        for i in range(len(self._powerup)):
            self._powerup[i].y = self._powerup[i].y + PUP_SPEED
        j = 0
        while j < len(self._powerup):
            if self._ship.collideswShip2(self._powerup[j]) == True:
                del self._powerup[j]
                self._lives = min(self._lives + 1, 5)
                self._heart = self._drawLives()
                j = len(self._powerup)
            else:
                j += 1
        #delete powerup
        i = 0
        while i < len(self._powerup):
            if self._powerup[i].y > GAME_WIDTH or self._powerup[i].y < 0:
                del self._powerup[i]
            else:
                i += 1


    def shipAlive(self):
        """
        Changes the self._ship from None to a ship object and resets bolts
        """
        self._ship = Ship(GAME_WIDTH/2, SHIP_BOTTOM)
        self._bolts = []

    def updateShip(self, dt, input):
        """
        Animates the self._ship and makes it move left and right.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Attribute input: the input (inherited from GameApp)
        Precondition: input is an instance of GInput
        """
        da = self._ship.x
        if input.is_key_down('left'):
            da = max(da -SHIP_MOVEMENT, SHIP_WIDTH/2)
        if input.is_key_down('right'):
            da = min(da+SHIP_MOVEMENT,GAME_WIDTH-SHIP_WIDTH/2)
        self._ship.x = da

    def updateAlienMovement(self, dt):
        """
        Animates the aliens and makes it move left, right, and down.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._time = self._time + dt
        if not self._checksifAlien():
            if self._time > self._speed:
                if self._direction == 'right':
                    self._alienMoveRight()
                    self._time = 0
                    self._aliensteps = self._aliensteps + 1
                elif self._direction == 'left':
                    self._alienMoveLeft()
                    self._time = 0
                    self._aliensteps = self._aliensteps + 1

        self._crossDline()
        #move Sparks
        for spark in self._sparks:
            spark.move()
        #Deletes Sparks
        i = 0
        while i < len(self._sparks):
            if self._sparks[i].y < -10:
                del self._sparks[i]
            else:
                i += 1

    def updateBolts(self, dt, input):
        """
        Animates the bolts from both the players and modifies self._bolts for each bolt

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Attribute input: the input (inherited from GameApp)
        Precondition: input is an instance of GInput
        """
        if self._end == False:
            self._updatePlayerBolts(dt, input)
            self._updateAlienBolts(dt)
            for i in range(len(self._bolts)):
                self._bolts[i].y = self._bolts[i].y + self._bolts[i].getVelocity()

            #Delete player bolts once they are off offscreen
            i = 0
            while i < len(self._bolts):
                if self._bolts[i].y > GAME_WIDTH or self._bolts[i].y < 0:
                    del self._bolts[i]
                else:
                    i += 1

    def alienDead(self, dt):
        """
        Sets an alien that is hit by bolt to None and changes self._win if all aliens are None

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        pewSound = Sound('blast2.wav')
        for c in range(len(self._aliens)):
            for r in range(len(self._aliens[c])):
                for i in range(len(self._bolts)):
                    if self._aliens[c][r] != None:
                        if self._aliens[c][r].collideswAlien(self._bolts[i]) == True:
                            pewSound.play()
                            self._explodeAlien(self._aliens[c][r])
                            self._addsScore(self._aliens[c][r])
                            self._aliens[c][r] = None
                            del self._bolts[i]
        self._end = self._checksifAlien()
        if self._checksifAlien() == True:
            self._win = True

    def _addsScore(self, alien):
        """
        Adds to the player score, each time an alien is hit.

        Parameter alien: the alien whose points are being added
        Preondition: alien is an Alien object
        """
        points = alien.getAlienpoints()
        self._score = self._score + points

    def shipDead(self, dt):
        """
        Alters self._lives, self._ship, and self._win when ship is hit by bolt

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        i = 0
        pewSound = Sound('blast2.wav')
        while i < len(self._bolts):
            if self._ship.collideswShip(self._bolts[i]) == True:
                del self._bolts[i]
                self._ship = None
                pewSound.play()
                self._lives = self._lives - 1
                if self._lives == 0:
                    self._win = False
                i = len(self._bolts)
            else:
                i += 1

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the aliens, ship, defense line, and bolts onto the screen
        """
        #Draw the aliens
        for col in range(len(self._aliens)):
            for row in range(len(self._aliens[col])):
                if not (self._aliens[col][row] is None):
                    self._aliens[col][row].draw(view)
        #Draw the ship
        if self._ship != None:
            self._ship.draw(view)
        #Draw the defensive line
        self._dline.draw(view)
        #Draw Bolts
        for things in range(len(self._bolts)):
            self._bolts[things].draw(view)
        #Draw Lives
        for hearts in range(self._lives):
            self._heart[hearts].draw(view)

        #Draw Sparks
        for spark in range(len(self._sparks)):
            self._sparks[spark].draw(view)

        for pup in range(len(self._powerup)):
            self._powerup[pup].draw(view)


    def _drawLives(self):
        """
        Helper to draw the hearts represting each life.
        """
        y = GAME_HEIGHT - ALIEN_V_SEP - 25
        thing = ALIEN_H_SEP + 30
        list = []
        for life in range(self._lives):
            x = 2*thing + 50*(life - 1)
            list.append(Heart(x, y))
        return list

    def _alienMoveRight(self):
        """
        Animates the aliens and makes them move right.
        """
        #Figure out which is the last alien
        good_c = self._findRightAlien()
        good_r = self._bottomAlien(good_c)
        x_last_A = self._aliens[good_r][good_c].getAlien_x()
        check = x_last_A + ALIEN_H_WALK + ALIEN_H_SEP
        if check < GAME_WIDTH - ALIEN_H_SEP:
            for col in range(len(self._aliens)):
                for row in range(len(self._aliens[col])):
                    if not (self._aliens[col][row] is None):
                        new = self._aliens[col][row].getAlien_x() + ALIEN_H_WALK
                        self._aliens[col][row].setAlien_x(new)
        else:
            self._alienMoveDown()
            self._direction = "left"

    def _findLeftAlien(self):
        """
        Returns the column of the left-most column of aliens that is not None
        """
        for i in range(ALIENS_IN_ROW):
            for j in range(self._alienrows):
                if self._aliens[j][i] != None:
                    return i

    def _findRightAlien(self):
        """
        Returns the column of right-most column of aliens that is not None
        """
        for i in range(ALIENS_IN_ROW):
            for j in range(self._alienrows):
                if self._aliens[j][ALIENS_IN_ROW-1-i] != None:
                    return ALIENS_IN_ROW-1-i

    def _alienMoveLeft(self):
        """
        Animates the aliens and makes them move left
        """
        good_c = self._findLeftAlien()
        good_r = self._bottomAlien(good_c)
        x_first_A = self._aliens[good_r][good_c].getAlien_x()

        check = x_first_A - ALIEN_H_WALK - ALIEN_H_SEP
        if check > 0 + ALIEN_H_SEP:
            for col in range(len(self._aliens)):
                for row in range(len(self._aliens[col])):
                    if not (self._aliens[col][row] is None):
                        new = self._aliens[col][row].getAlien_x() - ALIEN_H_WALK
                        self._aliens[col][row].setAlien_x(new)
        else:
            self._alienMoveDown()
            self._direction = "right"

    def _alienMoveDown(self):
        """
        Animates the aliens and makes them move down
        """
        for col in range(len(self._aliens)):
            for row in range(len(self._aliens[col])):
                if not (self._aliens[col][row] is None):
                    new = self._aliens[col][row].getAlien_y() - ALIEN_V_WALK
                    self._aliens[col][row].setAlien_y(new)

        if self._direction == 'right':
            self._direction = 'left'
        if self._direction == 'left':
            self._direction = 'right'
        #Gameover when Alien_y is less than D_Line

    def _updatePlayerBolts(self, dt, input):
        """
        Fires a bolt from the player
        """
        boltFired = False
        pewSound = Sound('pew2.wav')
        old_len = len(self._bolts)
        for i in range(len(self._bolts)):
            if self._bolts[i].getVelocity() > 0:
                boltFired = True
        if boltFired == False:
            if input.is_key_down('up'):
                x = self._ship.getShip_x()
                y = SHIP_HEIGHT/2 + SHIP_BOTTOM + BOLT_HEIGHT/2
                new = Bolt(0,x, y)
                new.isPlayerBolt()
                self._bolts.append(new)
        if len(self._bolts) > old_len:
            pewSound.play()

    def _updateAlienBolts(self, dt):
        """
        Figures out which alien to fire and fires the bolt from that alien
        """
        #Figuring out column of aliens
        pewSound = Sound('pop1.wav')
        thing = False
        while thing == False:
            column = random.randint(0,len(self._aliens[0])-1)
            for aliens in range(len(self._aliens)):
                if self._aliens[aliens][column] != None:
                    thing = True

        if self._aliensteps == self._fire:
            #Fire Bolt
            key_alien_row = self._bottomAlien(column)
            x_pos = self._aliens[key_alien_row][column].getAlien_x()
            y_pos = self._aliens[key_alien_row][column].getAlien_y() - ALIEN_HEIGHT/2
            new = Bolt(0, x_pos, y_pos)
            new.isAlienBolt()
            self._bolts.append(new)
            pewSound.play()
            self._fire = random.randint(1,BOLT_RATE)
            self._aliensteps = 0

    def _bottomAlien(self, column):
        """
        Returns the bottom most alien in column that is not None

        Parameter: column is a column in self._aliens
        Precondition: column is an int between 0 and number of columns
        in self._aliens
        """

        for aliens in range(len(self._aliens)):
            if self._aliens[aliens][column] != None:
                return aliens

    def _crossDline(self):
        """
        Sets self._end to True if bottom alien has crossed dline
        """
        for c in range(len(self._aliens)):
            for r in range(len(self._aliens[c])):
                if self._aliens[c][r] != None:
                    if self._aliens[c][r].getAlien_y() - ALIEN_HEIGHT/2 < DEFENSE_LINE:
                        self._end = True
                        self._win = False

    def _checksifAlien(self):
        """
        Sees if the all of the aliens in self._aliens are None
        """
        for c in range(len(self._aliens)):
            for r in range(len(self._aliens[c])):
                if self._aliens[c][r] != None:
                    return False
        return True

    def _explodeAlien(self, alien):
        """
        Explodes the alien when a bolt hits it.

        Parameter alien: The alien to explode
        Precondition: alien must be of type Alien
        """
        color = introcs.RGB(random.randrange(256),
                            random.randrange(256),
                            random.randrange(256))
        for i in range(PARTICLES_PER_SHELL):
            spark = Spark(alien.getAlien_x(), alien.getAlien_y(), color)
            self._sparks.append(spark)

    def _createList(self):
        """
        Returns a 2d list of Alien objects
        """
        lista = []
        first_x = ALIEN_H_SEP + ALIEN_WIDTH/2
        first_y = GAME_HEIGHT - (ALIEN_CEILING + ALIEN_HEIGHT/2 +
        (self._alienrows-1)*ALIEN_HEIGHT + (self._alienrows-1)*ALIEN_V_SEP)
        for i in range(self._alienrows):
            #this is the number of rows of aliens
            listb = []
            for j in range(ALIENS_IN_ROW):
                #number of aliens in EACH row
                if i%6 == 0 or i%6 == 1:
                    listb.append(Alien(first_x, first_y, ALIEN_IMAGES[0]))
                elif i%6 == 2 or i%6 == 3:
                    listb.append(Alien(first_x, first_y, ALIEN_IMAGES[1]))
                elif i%6 == 4 or i%6 == 5:
                    listb.append(Alien(first_x, first_y, ALIEN_IMAGES[2]))
                first_x = first_x + ALIEN_H_SEP + ALIEN_WIDTH
            lista.append(listb)
            first_y = first_y + ALIEN_V_SEP + ALIEN_HEIGHT
            first_x = ALIEN_H_SEP + ALIEN_WIDTH/2
        return lista
