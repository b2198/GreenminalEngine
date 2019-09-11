from pynput.mouse import Button, Controller
import cursor
import math

class FONT_MODES:
    RESET = 0
    BRIGHT = 1
    DIM = 2
    UNDERSCORE = 4
    BLINK = 5
    REVERSE = 7
    HIDDEN = 8

class TEXT_COLORS:
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    
class BACKGROUND_COLORS:
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47

class TerminalScreen:

    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.buffer1 = []
        self.buffer2 = []
        self.strokeValue = 0
        self.fillValue = 0
        self.fontMode = FONT_MODES.RESET
        self.textColor = TEXT_COLORS.WHITE
        self.backgroundColor = BACKGROUND_COLORS.GREEN
        self.changeTracker = []
        self.currentBuffer = self.buffer1
        self.waitingBuffer = self.buffer2
        self.initializeBuffers()


    def initializeBuffers(self):
        for i in range(0,self.height):
            self.buffer1.append([])
            self.buffer2.append([])
            self.changeTracker.append([])
            for j in range(0,self.width):
                self.buffer1[i].append(0)
                self.buffer2[i].append(0)
                self.changeTracker[i].append(1)
        
    def setStroke(self,value):
        self.strokeValue = value
        
    def setFill(self,value):
        self.fillValue = value
                
    def strokePoint(self,x,y):
        if x < self.width and x >= 0 and y < self.height and y >= 0:
            self.waitingBuffer[y][x] = self.strokeValue
            self.changeTracker[y][x] = self.waitingBuffer[y][x] != self.currentBuffer[y][x]
            
    def strokeLine(self,x1,y1,x2,y2):
    
        #determine the deltas
        deltax = x2 - x1
        deltay = y2 - y1
        
        #if the line covers only 1 point
        if deltax == 0 and deltay == 0:
            #if the point is inside the screen
            if x1 < self.width and x1 >= 0 and y1 < self.height and y1 >= 0:
                #mark the point for update
                self.waitingBuffer[y1][x1] = self.strokeValue
                self.changeTracker[y1][x1] = self.waitingBuffer[y1][x1] != self.currentBuffer[y1][x1]
            return
        
        #if the change in x is greater or equal to the change in y
        if abs(deltax) >= abs(deltay):
            #if the horizontal coordinates were inserted from right to left
            if x1 > x2:
                #switch x's and y's
                temp = x1
                x1 = x2
                x2 = temp
                temp = y1
                y1 = y2
                y2 = temp
                
                #recalculate deltas
                deltax = x2 - x1
                deltay = y2 - y1
            #error between drawing and line
            error = 0
            #error increment after each draw
            deltaerr = abs( deltay / deltax )
            y = y1
            #for each x value in the line interval
            for x in range(x1,x2+1):
            
                #if line won't enter the screen anymore
                if(
                    x >= self.width or
                    (deltay > 0 and y >= self.height) or
                    (deltay < 0 and y < 0) or
                    (deltay == 0 and (y >= self.height or y < 0) )
                ):
                    break
            
                #if line is currently in the screen
                if x >= 0 and y >= 0 and y < self.height:
                    #mark the point (x,y) for update
                    self.waitingBuffer[y][x] = self.strokeValue
                    self.changeTracker[y][x] = self.waitingBuffer[y][x] != self.currentBuffer[y][x]
                
                #increment error
                error += deltaerr
                
                #if error is big enough to have the y changed
                if error >= 0.5:
                    #change the y by 1, if the vertical change is positive, -1 if negative, or 0 if 0
                    y += 1 if deltay > 0 else ( 0 if deltay == 0 else -1 )
                    #decrement error
                    error -= 1
        else:
            #if the vertical coordinates were inserted from bottom to top
            if y1 > y2:
                #switch x's and y's
                temp = x1
                x1 = x2
                x2 = temp
                temp = y1
                y1 = y2
                y2 = temp
                
                #recalculate deltas
                deltax = x2 - x1
                deltay = y2 - y1
            #error between drawing and line
            error = 0
            #error increment after each draw
            deltaerr = abs( deltax / deltay )
            x = x1
            #for each y value in the line interval
            for y in range(y1,y2+1):
            
                #if line won't enter the screen anymore
                if(
                    y >= self.height or
                    (deltax > 0 and x >= self.width) or
                    (deltax < 0 and x < 0) or
                    (deltax == 0 and (x >= self.width or x < 0) )
                ):
                    break
            
                #if line is currently in the screen
                if y >= 0 and x >= 0 and x < self.width:
                    #mark the point (x,y) for update
                    self.waitingBuffer[y][x] = self.strokeValue
                    self.changeTracker[y][x] = self.waitingBuffer[y][x] != self.currentBuffer[y][x]
                
                #increment error
                error += deltaerr
                
                #if error is big enough to have the x changed
                if error >= 0.5:
                    #change the x by 1, if the horizontal change is positive, -1 if negative, or 0 if 0
                    x += 1 if deltax > 0 else ( 0 if deltax == 0 else -1 )
                    #decrement error
                    error -= 1
        
    def strokeRect(self,x,y,w,h):
        if x >= self.width or x+w-1 < 0:
            return
        if y >= self.height or y+h-1 < 0:
            return
        for i in range(y,y+h):
            if i >= self.height:
                break
            if i < 0:
                continue
            if i == y or i == y+h-1:
                for j in range(x,x+w):
                    if j >= self.width:
                        break
                    if j < 0:
                        continue
                    self.waitingBuffer[i][j] = self.strokeValue
                    self.changeTracker[i][j] = self.waitingBuffer[i][j] != self.currentBuffer[i][j]
            else:
                self.waitingBuffer[i][x] = self.strokeValue
                self.changeTracker[i][x] = self.waitingBuffer[i][x] != self.currentBuffer[i][x]
                if x+w-1 < self.width:
                    self.waitingBuffer[i][x+w-1] = self.strokeValue
                    self.changeTracker[i][x+w-1] = self.waitingBuffer[i][x+w-1] != self.currentBuffer[i][x+w-1]
                
    def fillRect(self,x,y,w,h):
        if x >= self.width or x+w-1 < 0:
            return
        if y >= self.height or y+h-1 < 0:
            return
        for i in range(y,y+h):
            if i >= self.height:
                break
            if i < 0:
                continue
            for j in range(x,x+w):
                if j >= self.width:
                    break
                if j < 0:
                    continue
                self.waitingBuffer[i][j] = self.fillValue
                self.changeTracker[i][j] = self.waitingBuffer[i][j] != self.currentBuffer[i][j]
                
    #def _dotDrawCircleEightSymetry(self,cx,cy,x,y,odd = True):
    #    cxxp = math.floor(cx)+math.floor(x)
    #    cxyp = math.floor(cx)+math.floor(y)
    #    cxxm = math.floor(cx)-math.floor(x)
    #    cxym = math.floor(cx)-math.floor(y)
    #    cyxm = math.floor(cy)-math.floor(x)
    #    cyym = math.floor(cy)-math.floor(y)
    #    cyxp = math.floor(cy)+math.floor(x)
    #    cyyp = math.floor(cy)+math.floor(y)
    #    self.strokePoint(cxxp,cyyp)#q1.1
    #    self.strokePoint(cxxp,cyym)#q4.2
    #    self.strokePoint(cxxm,cyyp)#q2.2
    #    self.strokePoint(cxxm,cyym)#q3.1
    #    #self.strokePoint(cxyp,cyxp)#q1.2
    #    #self.strokePoint(cxyp,cyxm)#q4.1
    #    #self.strokePoint(cxym,cyxp)#q2.1
    #    #self.strokePoint(cxym,cyxm)#q3.2
    #    if x != y:
    #        self.strokePoint(cxyp,cyxp)#q1.2
    #        self.strokePoint(cxyp,cyxm)#q4.1
    #        self.strokePoint(cxym,cyxp)#q2.1
    #        self.strokePoint(cxym,cyxm)#q3.2
    #    #if not odd:
    #    #    self.strokePoint(cxxp,cyym-1)#q4.2
    #    #    self.strokePoint(cxxm+1,cyyp)#q2.2
    #    #    self.strokePoint(cxxm-1,cyym-1)#q3.1
    #    #    if x != y:
    #    #        self.strokePoint(cxyp,cyxm-1)#q4.1
    #    #        self.strokePoint(cxym+1,cyxp)#q2.1
    #    #        self.strokePoint(cxym-1,cyxm-1)#q3.2
    #
    #def _circleDrawBresenham(self,cx,cy,r,odd = True, stroke = True):
    #    #print("parameters received: cx:[%.1f] cy:[%.1f] r:[%.1f] odd:[%d] stroke:[%d]" % (cx,cy,r,odd,stroke), end = "")
    #    x = 0#0 if odd else 0.5#x = 0
    #    y = r#y = 0.5
    #    decision = 3 - 2 * r#decision = 2
    #    if stroke:
    #        self._dotDrawCircleEightSymetry(cx,cy,x,y,odd)#11,10,0,0.5,True
    #    else:
    #        pass#self._lineDrawCircleEightSymetry(cx,cy,x,y)
    #    while y >= x#y > x+0.5:#0.5 >= 0
    #        x += 1#x = 1
    #        #decision = (x-cx + y-cy) - r * r
    #        if decision <= 0:#True
    #            y -= 1#y = -0.5
    #            decision += 4 * ( x - y ) + 10#decision = 10
    #        else:
    #            decision += 4 * x + 6#decision = 9
    #        if stroke:
    #            self._dotDrawCircleEightSymetry(cx,cy,x,y,odd)#11,10,1,-0.5
    #        else:
    #            pass#self._lineDrawCircleEightSymetry(cx,cy,x,y)
    #                
    #def _circleDrawEvenRadius(self,cx,cy,r,stroke = True):
    #    x = 1
    #    y = r
    #    d = r
    #    while y >= x:
    #        if stroke:
    #            self._dotDrawCircleEightSymetry(cx,cy,x,y)
    #        else:
    #            pass#self._lineDrawCircleEightSymetry(cx,cy,x,y)
    #        
    #        if d > x:
    #            d -= x
    #            x += 1
    #        elif d <= r + 1 - y:
    #            d += y - 1
    #            y -= 1
    #        else:
    #            d += y - x - 1
    #            x += 1
    #            y -= 1
    #        
    #
    #def strokeCircle(self,x,y,d):
    #    if d % 2 == 0:
    #        self._circleDrawBresenham(x+(d-1)/2,y+(d-1)/2,d/2,False)
    #    else:
    #        self._circleDrawBresenham(x+(d-1)/2,y+(d-1)/2,d/2,True)
    
    def _dotDrawCircleEightSymetry(self,cx,cy,x,y):
        self.strokePoint(cx + x, cy + y)
        self.strokePoint(cx + x, cy - y)
        self.strokePoint(cx - x, cy + y)
        self.strokePoint(cx - x, cy - y)
        self.strokePoint(cx + y, cy + x)
        self.strokePoint(cx + y, cy - x)
        self.strokePoint(cx - y, cy + x)
        self.strokePoint(cx - y, cy - x)
        
    def strokeCircle(self,cx,cy,r):
        x = 0
        y = r
        decision = 3 - 2 * r
        self._dotDrawCircleEightSymetry(cx,cy,x,y)
        while y >= x:
            x += 1
            if decision > 0:
                y -= 1
                decision += 4 * ( x - y ) + 10
            else:
                decision += 4 * x + 6
            self._dotDrawCircleEightSymetry(cx,cy,x,y)
        
    def _lineDrawCircleEightSymetry(self,cx,cy,x,y):
        self.strokeLine(cx, cy, cx + x, cy + y)
        self.strokeLine(cx, cy, cx + x, cy - y)
        self.strokeLine(cx, cy, cx - x, cy + y)
        self.strokeLine(cx, cy, cx - x, cy - y)
        self.strokeLine(cx, cy, cx + y, cy + x)
        self.strokeLine(cx, cy, cx + y, cy - x)
        self.strokeLine(cx, cy, cx - y, cy + x)
        self.strokeLine(cx, cy, cx - y, cy - x)
        
    def fillCircle(self,cx,cy,r):
        x = 0
        y = r
        decision = 3 - 2 * r
        temp = self.strokeValue
        self.setStroke(self.fillValue)
        self._lineDrawCircleEightSymetry(cx,cy,x,y)
        while y >= x:
            x += 1
            if decision > 0:
                y -= 1
                decision += 4 * ( x - y ) + 10
            else:
                decision += 4 * x + 6
            self._lineDrawCircleEightSymetry(cx,cy,x,y)
        self.setStroke(temp)
        
        
    def clear(self):
        for i in range(0,self.height):
                print("\033[2K",end="")
                print("\033[F",end="")
    
    def print(self,initial = False):
        temp = self.currentBuffer
        self.currentBuffer = self.waitingBuffer
        self.waitingBuffer = temp
        
        nextChar = " " if initial else "\033[1C"
        nextLineChar = "\n" if initial else "\033[1B"
        
        #print("\0337",end="")#save cursor pos and attributes
        
        print(
            "\033[%d;%d;%dm" % 
            (
                self.fontMode,
                self.textColor,
                self.backgroundColor
            ),
            end=""
        )#changes graphics options
        
        #print("\033[?25 l",end="")
        cursor.hide()
        
        if not initial:
            print("\033[%dA" % (self.height-1),end="")#goes back to top
        
        #printString = ""
        for i in range(0,self.height):
            #rowString = ""
            for j in range(0,self.width):
                changed = False
                if self.changeTracker[i][j] == 1 or initial:
                    print(self.currentBuffer[i][j],end="")
                    self.changeTracker[i][j] = 0
                    changed = True
                if j < self.width-1:
                    if changed:
                        print(nextChar,end="")#moves cursor right 1 time
                    else:
                        print(nextChar + nextChar, end="")#moves cursor right 2 times
                elif i < self.height-1:
                    if changed:
                        print(nextLineChar,end="")#moves cursor down 1 time
                    else:
                        print(nextChar + nextLineChar,end="")#moves cursor right 1 time and down 1 time
                #rowString += str(self.currentBuffer[i][j])
                #rowString += " "
            #print()
            #print("\033[1B",end="")#moves cursor down
            #print("\r",end="")#moves cursor to the start of the line
            print("\033[%dD" % (self.width * 2 - 1),end="")#moves cursor to the start of the line
            #print(rowString)
            #printString += rowString + "\n"
            
        #print("\033[?25 h",end="")
        cursor.show()
        #print(printString,end="\n\033[1A")
        
        print("\033[0m",end="")#restore colors and font modes
        #print("\0338",end="")#restore cursor pos and attributes
        #if initial:
            #print("\n",end="")
        #print("\033[%dB" % (self.height),end="")#moves cursor to the line right below the screen
        

