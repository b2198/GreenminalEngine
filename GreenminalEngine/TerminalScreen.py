import cursor
import math
import logging

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
        self.strokeValue = 0
        self.fillValue = 0
        self.defaultFontMode = FONT_MODES.RESET
        self.fontMode = self.defaultFontMode
        self.defaultTextColor = TEXT_COLORS.WHITE
        self.textColor = self.defaultTextColor
        self.defaultBackgroundColor = BACKGROUND_COLORS.GREEN
        self.backgroundColor = self.defaultBackgroundColor
        self.changeTracker = []
        self.initializeBuffers()


    def initializeBuffers(self):
        self.buffer1 = []
        self.buffer2 = []
        for i in range(0,self.height):
            self.buffer1.append([])
            self.buffer2.append([])
            self.changeTracker.append([])
            for j in range(0,self.width):
                self.buffer1[i].append({
                    "value": 0,
                    "fontMode": self.defaultFontMode,
                    "textColor": self.defaultTextColor,
                    "backgroundColor": self.defaultBackgroundColor
                })
                self.buffer2[i].append({
                    "value": 0,
                    "fontMode": self.defaultFontMode,
                    "textColor": self.defaultTextColor,
                    "backgroundColor": self.defaultBackgroundColor
                })
                self.changeTracker[i].append(1)
        self.currentBuffer = self.buffer1
        self.waitingBuffer = self.buffer2
        
    def setStroke(self,value):
        self.strokeValue = str(value)
        
    def setDoubleDigitStroke(self,value):
        self.strokeValue = str(value) + "\033[1D"
        
    def setFill(self,value):
        self.fillValue = str(value)
        
    def setDoubleDigitFill(self,value):
        self.fillValue = str(value) + "\033[1D"
        
    def setTextColor(self,value):
        self.textColor = value
        
    def setBackgroundColor(self,value):
        self.backgroundColor = value
        
    def setFontMode(self, value):
        self.fontMode = value
                
    def strokePoint(self,x,y):
        if x < self.width and x >= 0 and y < self.height and y >= 0:
            self.waitingBuffer[y][x]["value"] = self.strokeValue
            self.waitingBuffer[y][x]["fontMode"] = self.fontMode
            self.waitingBuffer[y][x]["textColor"] = self.textColor
            self.waitingBuffer[y][x]["backgroundColor"] = self.backgroundColor
            self.changeTracker[y][x] = 1 if (
                self.waitingBuffer[y][x]["value"] != self.currentBuffer[y][x]["value"] or
                self.waitingBuffer[y][x]["fontMode"] != self.currentBuffer[y][x]["fontMode"] or
                self.waitingBuffer[y][x]["textColor"] != self.currentBuffer[y][x]["textColor"] or
                self.waitingBuffer[y][x]["backgroundColor"] != self.currentBuffer[y][x]["backgroundColor"]
            ) else 0
            
    def strokeLine(self,x1,y1,x2,y2):
    
        #determine the deltas
        deltax = x2 - x1
        deltay = y2 - y1
        
        #if the line covers only 1 point
        if deltax == 0 and deltay == 0:
            #if the point is inside the screen
            if x1 < self.width and x1 >= 0 and y1 < self.height and y1 >= 0:
                #mark the point for update
                self.waitingBuffer[y1][x1]["value"] = self.strokeValue
                self.waitingBuffer[y][x]["fontMode"] = self.fontMode
                self.waitingBuffer[y1][x1]["textColor"] = self.textColor
                self.waitingBuffer[y1][x1]["backgroundColor"] = self.backgroundColor
                self.changeTracker[y1][x1] = 1 if (
                    self.waitingBuffer[y1][x1]["value"] != self.currentBuffer[y1][x1]["value"] or
                    self.waitingBuffer[y1][x1]["fontMode"] != self.currentBuffer[y1][x1]["fontMode"] or
                    self.waitingBuffer[y1][x1]["textColor"] != self.currentBuffer[y1][x1]["textColor"] or
                    self.waitingBuffer[y1][x1]["backgroundColor"] != self.currentBuffer[y1][x1]["backgroundColor"]
                ) else 0
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
                    self.waitingBuffer[y][x]["value"] = self.strokeValue
                    self.waitingBuffer[y][x]["fontMode"] = self.fontMode
                    self.waitingBuffer[y][x]["textColor"] = self.textColor
                    self.waitingBuffer[y][x]["backgroundColor"] = self.backgroundColor
                    self.changeTracker[y][x] = 1 if (
                        self.waitingBuffer[y][x]["value"] != self.currentBuffer[y][x]["value"] or
                        self.waitingBuffer[y][x]["fontMode"] != self.currentBuffer[y][x]["fontMode"] or
                        self.waitingBuffer[y][x]["textColor"] != self.currentBuffer[y][x]["textColor"] or
                        self.waitingBuffer[y][x]["backgroundColor"] != self.currentBuffer[y][x]["backgroundColor"]
                    ) else 0
                
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
                    self.waitingBuffer[y][x]["value"] = self.strokeValue
                    self.waitingBuffer[y][x]["fontMode"] = self.fontMode
                    self.waitingBuffer[y][x]["textColor"] = self.textColor
                    self.waitingBuffer[y][x]["backgroundColor"] = self.backgroundColor
                    self.changeTracker[y][x] = 1 if (
                        self.waitingBuffer[y][x]["value"] != self.currentBuffer[y][x]["value"] or
                        self.waitingBuffer[y][x]["fontMode"] != self.currentBuffer[y][x]["fontMode"] or
                        self.waitingBuffer[y][x]["textColor"] != self.currentBuffer[y][x]["textColor"] or
                        self.waitingBuffer[y][x]["backgroundColor"] != self.currentBuffer[y][x]["backgroundColor"]
                    ) else 0
                
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
                    self.waitingBuffer[i][j]["value"] = self.strokeValue
                    self.waitingBuffer[i][j]["fontMode"] = self.fontMode
                    self.waitingBuffer[i][j]["textColor"] = self.textColor
                    self.waitingBuffer[i][j]["backgroundColor"] = self.backgroundColor
                    self.changeTracker[i][j] = 1 if (
                        self.waitingBuffer[i][j]["value"] != self.currentBuffer[i][j]["value"] or
                        self.waitingBuffer[i][j]["fontMode"] != self.currentBuffer[i][j]["fontMode"] or
                        self.waitingBuffer[i][j]["textColor"] != self.currentBuffer[i][j]["textColor"] or
                        self.waitingBuffer[i][j]["backgroundColor"] != self.currentBuffer[i][j]["backgroundColor"]
                    ) else 0
            else:
                self.waitingBuffer[i][x]["value"] = self.strokeValue
                self.waitingBuffer[i][x]["fontMode"] = self.fontMode
                self.waitingBuffer[i][x]["textColor"] = self.textColor
                self.waitingBuffer[i][x]["backgroundColor"] = self.backgroundColor
                self.changeTracker[i][x] = 1 if (
                    self.waitingBuffer[i][x]["value"] != self.currentBuffer[i][x]["value"] or
                    self.waitingBuffer[i][x]["fontMode"] != self.currentBuffer[i][x]["fontMode"] or
                    self.waitingBuffer[i][x]["textColor"] != self.currentBuffer[i][x]["textColor"] or
                    self.waitingBuffer[i][x]["backgroundColor"] != self.currentBuffer[i][x]["backgroundColor"]
                ) else 0
                if x+w-1 < self.width:
                    self.waitingBuffer[i][x+w-1]["value"] = self.strokeValue
                    self.waitingBuffer[i][x+w-1]["fontMode"] = self.fontMode
                    self.waitingBuffer[i][x+w-1]["textColor"] = self.textColor
                    self.waitingBuffer[i][x+w-1]["backgroundColor"] = self.backgroundColor
                    self.changeTracker[i][x+w-1] = 1 if (
                        self.waitingBuffer[i][x+w-1]["value"] != self.currentBuffer[i][x+w-1]["value"] or
                        self.waitingBuffer[i][x+w-1]["fontMode"] != self.currentBuffer[i][x+w-1]["fontMode"] or
                        self.waitingBuffer[i][x+w-1]["textColor"] != self.currentBuffer[i][x+w-1]["textColor"] or
                        self.waitingBuffer[i][x+w-1]["backgroundColor"] != self.currentBuffer[i][x+w-1]["backgroundColor"]
                    ) else 0
                
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
                self.waitingBuffer[i][j]["value"] = self.fillValue
                self.waitingBuffer[i][j]["fontMode"] = self.fontMode
                self.waitingBuffer[i][j]["textColor"] = self.textColor
                self.waitingBuffer[i][j]["backgroundColor"] = self.backgroundColor
                self.changeTracker[i][j] = 1 if (
                    self.fillValue != self.currentBuffer[i][j]["value"] or
                    self.fontMode != self.currentBuffer[i][j]["fontMode"] or
                    self.textColor != self.currentBuffer[i][j]["textColor"] or
                    self.backgroundColor != self.currentBuffer[i][j]["backgroundColor"]
                ) else 0
                
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
                
    def _getNextSpaceChar(self, amount = 1):
        if amount > 0:
            return "\033[%dC" % (amount)
        return ""
    
    def print(self,initial = False):
        #timeNow = perf_counter_ns()
        #debug("\t[%d]: starting print of screen, initial? " % (timeNow) + str(initial))
        #debugTime = timeNow
        temp = self.currentBuffer
        self.currentBuffer = self.waitingBuffer
        self.waitingBuffer = temp
        
        #print("\0337",end="")#save cursor pos and attributes
        
        print(
            "\033[%d;%d;%dm" % 
            (
                self.defaultFontMode,
                self.defaultTextColor,
                self.defaultBackgroundColor
            ),
            end=""
        )#changes graphics options
        
        #print("\033[?25 l",end="")
        cursor.hide()
        
        #timeNow = perf_counter_ns()
        #debug("\t[%d]: initializalization done in %.9f seconds" % (timeNow, (timeNow - debugTime) / 1e9) )
        #debugTime = timeNow
        
        lastFontMode = None
        lastTextColor = None
        lastBackgroundColor = None
        
        if initial:
            for i in range(0,self.height):
                #timeNow = perf_counter_ns()
                #debug("\t[%d]: starting row drawing" % (timeNow))
                #rowTime = timeNow
                changeds = []
                endChar = " "
                for j in range(0,self.width):
                    if(
                        self.currentBuffer[i][j]["fontMode"] != lastFontMode or
                        self.currentBuffer[i][j]["textColor"] != lastTextColor or
                        self.currentBuffer[i][j]["backgroundColor"] != lastBackgroundColor
                    ):
                        print(
                            "\033[%d;%d;%dm" %
                            (
                                self.currentBuffer[i][j]["fontMode"],
                                self.currentBuffer[i][j]["textColor"],
                                self.currentBuffer[i][j]["backgroundColor"]
                            ),
                            end=""
                        )
                        lastFontMode = self.currentBuffer[i][j]["fontMode"]
                        lastTextColor = self.currentBuffer[i][j]["textColor"]
                        lastBackgroundColor = self.currentBuffer[i][j]["backgroundColor"]
                    if j == self.width-1:
                        endChar = "\n"
                    print(self.currentBuffer[i][j]["value"],end=endChar)
                    self.changeTracker[i][j] = 0
                #debug("printed a new line at i %d" % (i))
                #print("\\n <- I am a new line",end="")
                
                #timeNow = perf_counter_ns()
                #if timeNow - rowTime > 16*1e6 / 27:
                #    warning("\t[%d]: row [%d] drawn in %.9f seconds" % (timeNow, i, (timeNow - rowTime) / 1e9) )
        else:
            #print("| <- I was the previous cursor pos",end="")
            print("\r\033[%dA" % (self.height),end="")#goes back to top
            #print("| <- I am the starting cursor pos",end="")
            
            changedRows = []
            rowMoveAmt = 0
            finalRowIndex = 0
        
            for i in range(0,self.height):
            
                #timeNow = perf_counter_ns()
                #debug("\t[%d]: starting row drawing" % (timeNow))
                #rowTime = timeNow
                
                rowChanged = False
                changedRows.append(False)
                
                changedCols = []
                colMoveAmt = 0
                finalColIndex = 0
                for j in range(0,self.width):
                    colChanged = False
                    changedCols.append(False)
                    if self.changeTracker[i][j] == 1:
                        #debug("\tchecking (%d, %d), colMoveAmt = %d" % (i,j,colMoveAmt)) 
                        
                        if not rowChanged:
                            if rowMoveAmt > 0:
                                print("\033[%dB" % (rowMoveAmt),end="")#moves cursor down to the line that changed
                            rowMoveAmt = 1
                            finalRowIndex = i
                        
                            rowChanged = True
                            changedRows[i] = True
                        
                        if(
                            self.currentBuffer[i][j]["fontMode"] != lastFontMode or
                            self.currentBuffer[i][j]["textColor"] != lastTextColor or
                            self.currentBuffer[i][j]["backgroundColor"] != lastBackgroundColor
                        ):
                            print(
                                "\033[%d;%d;%dm" %
                                (
                                    self.currentBuffer[i][j]["fontMode"],
                                    self.currentBuffer[i][j]["textColor"],
                                    self.currentBuffer[i][j]["backgroundColor"]
                                ),
                                end=""
                            )
                            lastFontMode = self.currentBuffer[i][j]["fontMode"]
                            lastTextColor = self.currentBuffer[i][j]["textColor"]
                            lastBackgroundColor = self.currentBuffer[i][j]["backgroundColor"]
                        print(self._getNextSpaceChar(colMoveAmt),end="")#moves cursor right to the next changed
                        print(self.currentBuffer[i][j]["value"],end="")
                        #print(" \033[1D",end="")
                        self.changeTracker[i][j] = 0
                        colChanged = True
                        changedCols[j] = True
                        colMoveAmt = 1
                        finalColIndex = 2 * j + 1
                    else:
                        colMoveAmt += 2
                
                if rowChanged:
                    if finalColIndex > 0:
                        print("\033[%dD" % (finalColIndex),end="")#moves cursor to the start of the line
                else:
                    rowMoveAmt += 1
                    
                if i == self.height - 1:
                    print("\033[%dB" % (self.height - finalRowIndex),end="")#moves cursor down to the lline after the end of the screen, if it's not there already
                    
                #print("\r",end="")
                
                #if timeNow - rowTime > 16*1e6 / 27:
                #    warning("\t[%d]: row [%d] drawn in %0.9f seconds" % (timeNow, i, (timeNow - rowTime) / 1e9) )
                #    for j in range(0,self.width):
                #        debug("\t\t[%d]: changedCols[%d] = %d" % (timeNow, j, changedCols[j]))
            
        
        #timeNow = perf_counter_ns()
        #debug("\t[%d]: loop done in %0.9f seconds" % (timeNow, (timeNow - debugTime) / 1e9) )
        #debugTime = timeNow
        #print("\033[?25 h",end="")
        cursor.show()
        #print(printString,end="\n\033[1A")
        
        print("\033[0m",end="")#restore colors and font modes
        #print("\0338",end="")#restore cursor pos and attributes
        #print("check: " + str(check))
        
        #timeNow = perf_counter_ns()
        #debug("\t[%d]: render finish done in %.9f seconds" % (timeNow, (timeNow - debugTime) / 1e9) )
        #debugTime = timeNow
        #if initial:
            #print("\n",end="")
        #print("\033[%dB" % (self.height),end="")#moves cursor to the row right below the screen
        

if __name__ == "__main__":
    from time import perf_counter
    import sys
    from datetime import datetime
    from logging import debug, info, warning, error, critical
    
    if len(sys.argv) > 1:
        logLevel = sys.argv[1].lower()
    else:
        logLevel = "--debug"
    
    if logLevel == "--debug":
        logLevel = logging.DEBUG
    elif logLevel == "--info":
        logLevel = logging.INFO
    elif logLevel == "--warning":
        logLevel = logging.WARNING
    elif logLevel == "--error":
        logLevel = logging.ERROR
    elif logLevel == "--critical":
        logLevel = logging.CRITICAL
    else:
        logLevel = logging.DEBUG
    
    logging.basicConfig(filename = "log.txt", level=logLevel)
    
    timeNow = perf_counter()
    info("Starting tests with TerminalScreen.")
    debug("[datetime = %s][time = %0.9f] Starting time" % (datetime.now(), timeNow))
    totalTime = timeNow
    
    
    iterations = 600
    
    width = 30
    height = 25
    screen = TerminalScreen(width,height)
    
    timeNow = perf_counter()
    debug("[time = %0.9f] starting operations took %0.9f seconds" % (timeNow, timeNow - totalTime))
    
    #========== No color operations =========={
    initPrintTime = timeNow
    noColorTime = timeNow
    
    info("Starting colorless operations.")
    screen.initializeBuffers()
    screen.print(True)
    
    timeNow = perf_counter()
    debug("[time = %0.9f] initial print took %0.9f seconds" % (timeNow, timeNow - initPrintTime))
    
    #===== Full print loop ====={
    timeNow = perf_counter()
    info("Starting full loop check with %d iterations." % (iterations))
    loopTime = timeNow
    
    for i in range(0,iterations):
    
        screen.setFill("F")
        screen.fillRect(0,0,width,height)
    
        screen.setStroke("S")
        screen.strokeRect(0,0,width,height)
        
        screen.setFill("f")
        screen.fillRect(0,0,width//2,height//2)
        
        screen.setStroke("s")
        screen.strokeRect(width//2,height//2,width//2,height//2)
        
        screen.print(False)
    
    
    timeNow = perf_counter()
    avgTime = 1000 * (timeNow - loopTime) / iterations
    debug("[time = %0.9f] full loop took %0.9f seconds (%0.6f ms on average per iteration)" % (
        timeNow,
        timeNow - loopTime,
        avgTime
    ))
    if avgTime > 16.6:
        warning("Render time too high (average %0.6f ms), screen won't be able to maintain 60 fps" % (avgTime))
    info("Done.")
    #}===== end Full print loop =====
        
    
    #===== Large fill loop ====={
    timeNow = perf_counter()
    info("Starting large fill loop test with %d iterations." % (iterations))
    loopTime = timeNow
    
    for i in range(0,iterations):
        
        screen.setFill(" ")
        screen.fillRect(0,0,width,height)
    
    timeNow = perf_counter()
    avgTime = 1000 * (timeNow - loopTime) / iterations
    debug("[time = %0.9f] large fill loop took %0.9f seconds (%0.6f ms on average per iteration)" % (
        timeNow,
        timeNow - loopTime,
        avgTime
    ))
    if avgTime > 16.6:
        warning("Large fill calls time too high (average %0.6f ms), screen won't be able to maintain 60 fps" % (avgTime))
    info("Done.")
    #}===== end Large fill loop =====
        
    
    #===== Large stroke loop ====={
    timeNow = perf_counter()
    info("Starting large stroke loop test with %d iterations." % (iterations))
    loopTime = timeNow
    
    for i in range(0,iterations):
        
        screen.setStroke("D")
        screen.strokeRect(0,0,width,height)
    
    timeNow = perf_counter()
    avgTime = 1000 * (timeNow - loopTime) / iterations
    debug("[time = %0.9f] large stroke loop took %0.9f seconds (%0.6f ms on average per iteration)" % (
        timeNow,
        timeNow - loopTime,
        avgTime
    ))
    if avgTime > 16.6:
        warning("Large stroke calls time too high (average %0.6f ms), screen won't be able to maintain 60 fps" % (avgTime))
    info("Done.")
    #}===== end Large stroke loop =====
        
    #===== Small fill loop ====={
    timeNow = perf_counter()
    info("Starting small fill loop test with %d iterations." % (iterations))
    loopTime = timeNow
    
    for i in range(0,iterations):
        
        screen.setFill("F")
        screen.fillRect(0,0,width//2,height//2)
    
    timeNow = perf_counter()
    avgTime = 1000 * (timeNow - loopTime) / iterations
    debug("[time = %0.9f] small fill loop took %0.9f seconds (%0.6f ms on average per iteration)" % (
        timeNow,
        timeNow - loopTime,
        avgTime
    ))
    if avgTime > 16.6:
        warning("Small fill calls time too high (average %0.6f ms), screen won't be able to maintain 60 fps" % (avgTime))
    info("Done.")
    #}===== end Small fill loop =====
    
    #===== Small stroke loop ====={
    timeNow = perf_counter()
    info("Starting small stroke loop test with %d iterations." % (iterations))
    loopTime = timeNow
    
    for i in range(0,iterations):
        
        screen.setStroke("-")
        screen.strokeRect(width//2,height//2,width//2,height//2)
    
    timeNow = perf_counter()
    avgTime = 1000 * (timeNow - loopTime) / iterations
    debug("[time = %0.9f] small stroke loop took %0.9f seconds (%0.6f ms on average per iteration)" % (
        timeNow,
        timeNow - loopTime,
        avgTime
    ))
    if avgTime > 16.6:
        warning("Small stroke calls time too high (average %0.6f ms), screen won't be able to maintain 60 fps" % (avgTime))
    info("Done.")
    #}===== end Small stroke loop =====
    
    #===== Empty print loop ====={
    timeNow = perf_counter()
    info("Starting empty print loop test with %d iterations." % (iterations))
    loopTime = timeNow
    
    for i in range(0,iterations):
        
        screen.print(False)
    
    timeNow = perf_counter()
    avgTime = 1000 * (timeNow - loopTime) / iterations
    debug("[time = %0.9f] print loop took %0.9f seconds (%0.6f ms on average per iteration)" % (
        timeNow,
        timeNow - loopTime,
        avgTime
    ))
    if avgTime > 16.6:
        warning("Print calls time too high (average %0.6f ms), screen won't be able to maintain 60 fps" % (avgTime))
    info("Done.")
    #}===== End of Empty print loop =====
    info("Finished colorless operations.")
    #}========== End of No color operations ==========
    
    #========== Color operations =========={
    
    timeNow = perf_counter()
    debug("[time = %0.9f] colorless operations took %0.9f seconds" % (timeNow, timeNow - noColorTime))
    colorTime = timeNow
    initPrintTime = timeNow
    
    
    info("Starting colored operations.")
    screen.initializeBuffers()
    screen.print(True)
    
    timeNow = perf_counter()
    debug("[time = %0.9f] initial print took %0.9f seconds" % (timeNow, timeNow - initPrintTime))
    
    #===== Full print loop ====={
    timeNow = perf_counter()
    info("Starting full loop check with %d iterations." % (iterations))
    loopTime = timeNow
    
    for i in range(0,iterations):
    
        screen.setBackgroundColor(BACKGROUND_COLORS.YELLOW)
        screen.setDoubleDigitFill("F ")
        screen.fillRect(0,0,width,height)
    
        screen.setBackgroundColor(BACKGROUND_COLORS.WHITE)
        screen.setTextColor(TEXT_COLORS.GREEN)
        screen.setStroke("S")
        screen.strokeRect(0,0,width,height)
        
        screen.setBackgroundColor(screen.defaultBackgroundColor)
        screen.setTextColor(TEXT_COLORS.BLUE)
        screen.setFill("f")
        screen.fillRect(0,0,width//2,height//2)
        
        screen.setTextColor(screen.defaultTextColor)
        screen.setDoubleDigitStroke("ss")
        screen.strokeRect(width//2,height//2,width//2,height//2)
        
        screen.print(False)
    
    
    timeNow = perf_counter()
    avgTime = 1000 * (timeNow - loopTime) / iterations
    debug("[time = %0.9f] full loop took %0.9f seconds (%0.6f ms on average per iteration)" % (
        timeNow,
        timeNow - loopTime,
        avgTime
    ))
    if avgTime > 16.6:
        warning("Render time too high (average %0.6f ms), screen won't be able to maintain 60 fps" % (avgTime))
    info("Done.")
    #}===== end Full print loop =====
        
    
    #===== Large fill loop ====={
    timeNow = perf_counter()
    info("Starting large fill loop test with %d iterations." % (iterations))
    loopTime = timeNow
    
    for i in range(0,iterations):
        
        screen.setBackgroundColor(BACKGROUND_COLORS.YELLOW)
        screen.setTextColor(TEXT_COLORS.RED)
        screen.setFill(" ")
        screen.fillRect(0,0,width,height)
    
    timeNow = perf_counter()
    avgTime = 1000 * (timeNow - loopTime) / iterations
    debug("[time = %0.9f] large fill loop took %0.9f seconds (%0.6f ms on average per iteration)" % (
        timeNow,
        timeNow - loopTime,
        avgTime
    ))
    if avgTime > 16.6:
        warning("Large fill calls time too high (average %0.6f ms), screen won't be able to maintain 60 fps" % (avgTime))
    info("Done.")
    #}===== end Large fill loop =====
        
    
    #===== Large stroke loop ====={
    timeNow = perf_counter()
    info("Starting large stroke loop test with %d iterations." % (iterations))
    loopTime = timeNow
    
    for i in range(0,iterations):
        
        screen.setBackgroundColor(BACKGROUND_COLORS.YELLOW)
        screen.setTextColor(TEXT_COLORS.RED)
        screen.setStroke("D")
        screen.strokeRect(0,0,width,height)
    
    timeNow = perf_counter()
    avgTime = 1000 * (timeNow - loopTime) / iterations
    debug("[time = %0.9f] large stroke loop took %0.9f seconds (%0.6f ms on average per iteration)" % (
        timeNow,
        timeNow - loopTime,
        avgTime
    ))
    if avgTime > 16.6:
        warning("Large stroke calls time too high (average %0.6f ms), screen won't be able to maintain 60 fps" % (avgTime))
    info("Done.")
    #}===== end Large stroke loop =====
        
    #===== Small fill loop ====={
    timeNow = perf_counter()
    info("Starting small fill loop test with %d iterations." % (iterations))
    loopTime = timeNow
    
    for i in range(0,iterations):
        
        screen.setBackgroundColor(BACKGROUND_COLORS.YELLOW)
        screen.setTextColor(TEXT_COLORS.RED)
        screen.setFill("F")
        screen.fillRect(0,0,width//2,height//2)
    
    timeNow = perf_counter()
    avgTime = 1000 * (timeNow - loopTime) / iterations
    debug("[time = %0.9f] small fill loop took %0.9f seconds (%0.6f ms on average per iteration)" % (
        timeNow,
        timeNow - loopTime,
        avgTime
    ))
    if avgTime > 16.6:
        warning("Small fill calls time too high (average %0.6f ms), screen won't be able to maintain 60 fps" % (avgTime))
    info("Done.")
    #}===== end Small fill loop =====
    
    #===== Small stroke loop ====={
    timeNow = perf_counter()
    info("Starting small stroke loop test with %d iterations." % (iterations))
    loopTime = timeNow
    
    for i in range(0,iterations):
        
        screen.setBackgroundColor(BACKGROUND_COLORS.YELLOW)
        screen.setTextColor(TEXT_COLORS.RED)
        screen.setStroke("-")
        screen.strokeRect(width//2,height//2,width//2,height//2)
    
    timeNow = perf_counter()
    avgTime = 1000 * (timeNow - loopTime) / iterations
    debug("[time = %0.9f] small stroke loop took %0.9f seconds (%0.6f ms on average per iteration)" % (
        timeNow,
        timeNow - loopTime,
        avgTime
    ))
    if avgTime > 16.6:
        warning("Small stroke calls time too high (average %0.6f ms), screen won't be able to maintain 60 fps" % (avgTime))
    info("Done.")
    #}===== end Small stroke loop =====
    
    #===== Empty print loop ====={
    timeNow = perf_counter()
    info("Starting empty print loop test with %d iterations." % (iterations))
    loopTime = timeNow
    
    for i in range(0,iterations):
        
        screen.print(False)
    
    timeNow = perf_counter()
    avgTime = 1000 * (timeNow - loopTime) / iterations
    debug("[time = %0.9f] print loop took %0.9f seconds (%0.6f ms on average per iteration)" % (
        timeNow,
        timeNow - loopTime,
        avgTime
    ))
    if avgTime > 16.6:
        warning("Print calls time too high (average %0.6f ms), screen won't be able to maintain 60 fps" % (avgTime))
    info("Done.")
    #}===== End of Empty print loop =====
    
    timeNow = perf_counter()
    debug("[time = %0.9f] colored operations took %0.9f seconds" % (timeNow, timeNow - colorTime))
    info("Finished colored operations");
    #}========== End of Color operations ==========
    
    timeNow = perf_counter()
    info("Finished execution. Total time: %0.9f seconds" % (timeNow - totalTime))
    debug("[time = %0.9f]" % (timeNow))
    
    info("Success.\n")
        
        
        
        
        
        
        
        
