#from TerminalScreen import TEXT_COLORS, BACKGROUND_COLORS

class GameManager:
    
    def __init__(self):
        #self.gambX = 15
        #self.gambY = 20
        #self.gambV = "P"
        pass
        
    def onUpdate(self,input):
        #if input.isJustPressed("w"):
        #    self.gambY -= 1
        #if input.isJustPressed("a"):
        #    self.gambX -= 1
        #if input.isJustPressed("s"):
        #    self.gambY += 1
        #if input.isJustPressed("d"):
        #    self.gambX += 1
        return True
        
    def onRender(self,screen):
        #screen.setTextColor(screen.defaultTextColor)
        #screen.setBackgroundColor(screen.defaultBackgroundColor)
        #screen.setFill(" ")
        #screen.fillRect(0,0,screen.width,screen.height)
        #screen.setTextColor(TEXT_COLORS.BLUE)
        #screen.setBackgroundColor(BACKGROUND_COLORS.WHITE)
        #screen.setFill("F")
        #screen.fillRect(0,0,10,10)
        #screen.setStroke("S \033[1D")
        #screen.setTextColor(TEXT_COLORS.WHITE)
        #screen.setBackgroundColor(BACKGROUND_COLORS.BLUE)
        #screen.strokeRect(15,15,15,10)
        #screen.setStroke(self.gambV)
        #screen.strokePoint(self.gambX,self.gambY)
        pass
        
    def onClosing(self):
        pass
        
    def beforeStart(self,screen,input):
        #screen.defaultBackgroundColor = BACKGROUND_COLORS.BLACK
        pass
        
    def onStarting(self,screen,input):
        pass
        
    def onMeasuring(self,ups,fps):
        pass
