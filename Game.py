from TerminalScreen import TerminalScreen
from GameLoopController import GameLoopController
from GameManager import GameManager
import time
from WindowsFix import enable_vt_mode, set_conout_mode
from InputManager import InputManager
from pynput.keyboard import Key
import math

class Game:

    def __init__(
        self, width = 36,
        height = 27,
        expectedUps = 60,
        expectedFps = 60,
        maxFrameSkip = 5,
        expectedMps = 1,
        exitKey = Key.esc.name,
        gameManager = GameManager(),
        printMeasures = True
    ):
        self.restoreConsole = enable_vt_mode()
        self.screen = TerminalScreen(width,height)
        self.loopController = GameLoopController(expectedUps,expectedFps,maxFrameSkip,expectedMps)
        self.gameManager = gameManager
        self.active = True
        self.exitKey = exitKey
        self.input = InputManager()
        self.printMeasures = printMeasures
    
    #def windowsFix(self):
    #    if platform.system().lower() == 'windows':
    #        from ctypes import windll, c_int, byref
    #        stdout_handle = windll.kernel32.GetStdHandle(c_int(-11))
    #        mode = c_int(0)
    #        windll.kernel32.GetConsoleMode(c_int(stdout_handle), byref(mode))
    #        mode = c_int(mode.value | 4)
    #        windll.kernel32.SetConsoleMode(c_int(stdout_handle), mode)

    def update(self):
        if self.exitKey is not None and self.input.isJustPressed(self.exitKey):
            self.active = False
        if not self.gameManager.onUpdate(self.input):
            self.active = False
        
    def render(self):
        self.gameManager.onRender(self.screen)
        self.screen.print()
        
    def onClosing(self):
        self.gameManager.onClosing()
        set_conout_mode(self.restoreConsole)

    def run(self):
        self.screen.print(True)
        print()
        self.loopController.start()
        self.input.start()
        self.gameManager.onStarting(self.screen,self.input)
        while(self.active):
            if self.loopController.isTimeForUpdate():
                self.input.update()
                self.update()
                self.loopController.registerUpdate()
            elif self.loopController.isTimeForRender():
                self.render()
                if self.printMeasures:
                    print("\033[1B\r%d ups, %d fps   \033[1A" % (self.loopController.getUps(),self.loopController.getFps()),end="")
                self.loopController.registerRender()
            if self.loopController.isTimeForMeasure():
                self.loopController.measure()
                self.gameManager.onMeasuring(self.loopController.getUps(),self.loopController.getFps())
        self.onClosing()
    
