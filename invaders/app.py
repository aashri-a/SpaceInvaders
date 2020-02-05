"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

# Aashri Aggarwal (aia56) and Abby Sachar (ahs265)
# December 10th, 2019
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py


class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is only None if _state is STATE_ACTIVE.
    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    #Attribute _lastkeys: the number of keys pressed last frames
    #Invariant: _lastkeys is an int >= 0
    #
    #Attribute _background: the background color of the game
    #Invariant: _background is a GRectangle object.
    #
    #Attribute _level: the level the player is on
    #Invariant: _level is an int >= 0
    #
    #Attribute _round: the counter that displays what level the player is on
    #Invariant: _round is a GLabel object
    #
    #Attribute _instructions: Instructions to display
    #Invariant: _instructions  is a list of GLabel objects or empty list
    #
    #Attribute: _totalscore: the total score of the player
    #Invariant: _totalscore: int >= 0
    #
    #Attribute: _scoreDisplay: Displays the totalscore of the player
    #Invariant: _scoreDisplay is a GLabel object
    #


    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        self._state = STATE_INACTIVE
        self._wave = None
        self._lastkeys = 0
        start_mes = "Press 'S' to Play"
        center_x = GAME_WIDTH/2
        center_y = GAME_HEIGHT/2
        self._text = GLabel(text = start_mes, font_size = 80, x = center_x, y = center_y,
        bold = True, font_name = 'Arcade', fillcolor = 'black', linecolor = 'white')
        self._level = 1
        self._round = self._displayRound()
        self._instructions = None
        self._totalscore = 0
        self._scoreDisplay = self._displayScore()

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        STATE_LEVEL: The first wave has ended, and the player moves onto the next
        wave. The lives are not reset, and the speed of the aliens increases by 50%.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) in [int, float]
        if self._state == STATE_INACTIVE:
            self._stateInactive(dt)
        if self._state == STATE_NEWWAVE:
            self._stateNewWave(dt)
        if self._state == STATE_ACTIVE:
            self._stateActive(dt)
        if self._state == STATE_PAUSED:
            self._statePaused()
            if self.input.is_key_down('s'):
                self._state = STATE_CONTINUE
        if self._state == STATE_CONTINUE:
            self._stateContinue(dt)
        if self._state == STATE_COMPLETE:
            self._stateComplete()
        if self._state == STATE_LEVEL:
            self._stateLevel(dt)
        if self._state == STATE_INSTRUCTIONS:
            self._stateInstructions(dt)

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        self._background.draw(self.view)
        if self._state != STATE_INACTIVE and self._state != STATE_INSTRUCTIONS:
            self._wave.draw(self.view)
        if not self._text == None: #STATE_INACTIVE
            self._text.draw(self.view)
        if self._state != STATE_INSTRUCTIONS:
            self._round.draw(self.view)
            self._scoreDisplay.draw(self.view)
        if self._state == STATE_INACTIVE:
            self._callInstructions().draw(self.view)
        if self._state == STATE_INSTRUCTIONS:
            for thing in range(len(self._instructions)):
                self._instructions[thing].draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def _callInstructions(self):
        """
        Returns Glabel that tells user how to access the instructions.
        """
        mes = 'Press "i" to view game instructions.'
        x = GAME_WIDTH/2
        y = GAME_HEIGHT/2 - 50
        return GLabel(text = mes, font_size = 30, x = x, y = y,
        bold = True, font_name = 'Arcade',linecolor = 'white', fillcolor = 'black')


    def _displayRound(self):
        """
        Displays the round number in the upper right corner.
        """
        mes = 'Level: ' + str(self._level)
        x = GAME_WIDTH - 100 - ALIEN_H_SEP
        y = GAME_HEIGHT - ALIEN_V_SEP - 25
        return GLabel(text = mes, font_size = 40, x = x, y = y,
        bold = True, font_name = 'Arcade',linecolor = 'white', fillcolor = 'black')

    def _displayScore(self):
        """
        Displays the total score in the upper right corner

        Parameter totalscore: the total score of the player
        Precondition: int >= 0
        """
        mes = 'Score: ' + str(self._totalscore)
        x = GAME_WIDTH/2
        y = GAME_HEIGHT - ALIEN_V_SEP - 25
        return GLabel(text = mes, font_size = 40, x = x, y = y,
        bold = True, font_name = 'Arcade',linecolor = 'white', fillcolor = 'black')

    def _determineState(self):
        """
        Determines the current state and assigns it to self._state.

        The method checks if the key s is pressed for the first time, and if it is,
        changes the self._state to STATE_NEWWAVE.
        """
        if self.input.is_key_down('s'):
            self._state = STATE_NEWWAVE
        if self.input.is_key_down('i'):
            self._state = STATE_INSTRUCTIONS

    def _stateInstructions(self, dt):
        """
        Performs the actions done in STATE_INSTRUCTIONS

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._text = None
        self._round = None
        mes1 = "1. Use the right and left arrow keys to move the ship \n"
        mes2 = "2. Use the up arrow key to fire a bolt at the aliens \n"
        mes3 = "3. Kill all aliens to progress to next level \n"
        mes4 = "4. You have 3 lives \n"
        mes_exit = "Press 'S' to begin"
        mes = mes1 + mes2 + mes3 + mes4
        center_x = GAME_WIDTH/2
        center_y = GAME_HEIGHT/2 + 75
        obj1 = GLabel(text = mes, font_size = 30, x = center_x, y = center_y,
         bold = True, font_name = 'Arcade', linecolor = 'white', fillcolor = 'black')
        obj2 = GLabel(text = mes_exit, font_size = 35, x = center_x, y = GAME_HEIGHT/2,
         bold = True, font_name = 'Arcade', linecolor = 'white', fillcolor = 'black')
        self._instructions = [obj1, obj2]
        if self.input.is_key_down('s'):
            self._state = STATE_NEWWAVE
            self._wave = Wave(SHIP_LIVES, ALIEN_SPEED, ALIEN_ROWS, self._totalscore)
            self._round = self._displayRound()

    def _stateContinue(self, dt):
        """
        Performs the actions done in STATE_CONTINUE

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._wave.shipAlive()
        self._text = None
        self._state = STATE_ACTIVE

    def _stateNewWave(self, dt):
        """
        Performs the actions done in STATE_NEWWAVE

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._text = None
        self._wave = Wave(SHIP_LIVES, ALIEN_SPEED, ALIEN_ROWS, 0)
        self._state = STATE_ACTIVE
        self._level = 1
        self._round = self._displayRound()
        self._scoreDisplay = self._displayScore()

    def _stateInactive(self, dt):
        """
        Performs the actions done in STATE_INACTIVE

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._backgroundcolor()
        self._determineState()

    def _stateLevel(self, dt):
        """
        Performs the actions done in STATE_LEVEL

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._text = None
        old_lives = self._wave.getLives()
        old_speed = self._wave.getSpeed()
        new_speed = old_speed*0.97
        old_rows = self._wave.getAlienRows()
        new_alienrows = min(old_rows + 1, 10)
        self._wave = Wave(old_lives, new_speed, new_alienrows, self._totalscore)
        self._state = STATE_ACTIVE
        self._level = self._level + 1
        self._round = self._displayRound()
        self._scoreDisplay = self._displayScore()

    def _statePaused(self):
        """
        Changes self._state = STATE_PAUSED and informs how many lives are left
        """
        self._state = STATE_PAUSED
        #if self._wave.getLives() != 0:
        mes = ('Uh oh. You now have ' + str(self._wave.getLives()) +
        ' lives left. \n Press "s" to resume.')
        center_x = GAME_WIDTH/2
        center_y = GAME_HEIGHT/2
        self._text = GLabel(text = mes, font_size = 35, x = center_x, y = center_y,
        bold = True, font_name = 'Arcade', linecolor = 'white', fillcolor = 'black')

    def _stateComplete(self):
        """
        Helper method for when state._self = STATE_COMPLETE.
        """
        if self._wave.getWin() == True:
            #self._state = STATE_INACTIVE
            mes = 'Congrats! you won!!! \n Press "spacebar" to continue to next level'
            center_x = GAME_WIDTH/2
            center_y = GAME_HEIGHT/2
            self._text = GLabel(text = mes, font_size = 35, x = center_x, y = center_y,
            bold = True, font_name = 'Arcade',linecolor = 'white', fillcolor = 'black')
            if self.input.is_key_down('spacebar'):
                self._state = STATE_LEVEL
        else:
            mes = 'Uh oh. You lost :( \n Press "s" to play again.'
            center_x = GAME_WIDTH/2
            center_y = GAME_HEIGHT/2
            self._text = GLabel(text = mes, font_size = 35, x = center_x, y = center_y,
            bold = True, font_name = 'Arcade', linecolor = 'white', fillcolor = 'black')
            self._determineState()

    def _stateActive(self, dt):
        """
        Helper method for when state._self = STATE_ACTIVE.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._wave.updateShip(dt, self.input)
        self._wave.alienDead(dt)
        if self._wave.getEnd() == True:
            self._state = STATE_COMPLETE
        self._wave.updateAlienMovement(dt)
        if self._wave.getEnd() == True:
            self._state = STATE_COMPLETE
        self._wave.updateBolts(dt, self.input)
        self._wave.updatePowerUp(dt)
        self._wave.shipDead(dt)
        score = self._wave.getScore()
        self._totalscore = score
        self._scoreDisplay = self._displayScore()
        if self._wave.getShip() == None:
            if self._wave.getLives() != 0:
                self._state = STATE_PAUSED
            else:
                self._state = STATE_COMPLETE

    def _backgroundcolor(self):
        """
        Changes the backgroundcolor for the game.
        """
        self._background = GRectangle(x = GAME_WIDTH/2, y=GAME_HEIGHT/2,
        width = GAME_WIDTH, height = GAME_HEIGHT, fillcolor = 'black')
