from TerminalScreen import TerminalScreen
from GameLoopController import GameLoopController
from GameManager import GameManager
from InputManager import InputManager
from time import perf_counter, sleep
from pynput.keyboard import Key
import math
from logging import debug, info, warning, error, critical
import os

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
        self.onWindows = os.name == "nt"
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
            #info("exit key press detected on update, initializing closing procedures")
        if not self.gameManager.onUpdate(self.input):
            self.active = False
            #info("manager requested close, initializing closing procedures")
        
    def render(self):
        self.gameManager.onRender(self.screen)
        self.screen.print()
        
    def onClosing(self):
        self.gameManager.onClosing()
        print("\033[1A\n",end="")#just to flush anything that hasn't been flushed yet

    def enableOnWindowsConsole(self):
        from WindowsFix import enable_vt_mode
        self.restoreConsole = enable_vt_mode()
        
    def restoreWindowsConsole(self):
        from WindowsFix import set_conout_mode
        set_conout_mode(self.restoreConsole)
            
    def run(self):
        #info("Initializing run")
        
        if self.onWindows:
            self.enableOnWindowsConsole()
        
        self.gameManager.beforeStart(self.screen,self.input)
        self.screen.initializeBuffers()
        self.screen.print(True)
        self.loopController.start()
        self.input.start()
        self.gameManager.onStarting(self.screen,self.input)
        #info("run initialized, starting loop\n")
        while(self.active):
            #debug("\t[%d]: starting iteration" % (perf_counter()))
            if self.loopController.isTimeForUpdate():
                #debug("\t[%d]: starting update" % (perf_counter()))
                self.input.update()
                #debug("\t[%d]: input updated" % (perf_counter()))
                self.update()
                #debug("\t[%d]: update done" % (perf_counter()))
                self.loopController.registerUpdate()
                #debug("\t[%d]: update registered" % (perf_counter()))
            elif self.loopController.isTimeForRender():
                #debug("\t[%d]: starting render" % (perf_counter()))
                self.render()
                #debug("\t[%d]: render done" % (perf_counter()))
                if self.printMeasures and self.loopController.isTimeForMeasure():
                    print("\r%03d ups, %03d fps  " % (self.loopController.getUps(),self.loopController.getFps()),end="")
                self.loopController.registerRender()
                #debug("\t[%d]: render registered" % (perf_counter()))
            if self.loopController.isTimeForMeasure():
                #debug("\t[%d]: starting measures" % (perf_counter()))
                self.loopController.measure()
                #debug("\t[%d]: printing measures: %03d ups, %03d fps" % (perf_counter(),self.loopController.getUps(),self.loopController.getFps()))
                self.gameManager.onMeasuring(self.loopController.getUps(),self.loopController.getFps())
                #debug("\t[%d]: measures sent to manager" % (perf_counter()))
            #debug("\t[%d]: finishing iteration\n" % (perf_counter()))
            sleep(0)
        self.onClosing()
        #debug("\t[%d]: closing sent to manager" % (perf_counter()))
        
        if self.onWindows:
            self.restoreWindowsConsole()
            
        #info("\trun finished.\n\n")
    
