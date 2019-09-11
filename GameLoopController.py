from time import time_ns

UNLIMITED_FPS = -1

class GameLoopController:
    
    #ups -> updates per second
    #fps -> frames per second
    #mps -> measures per second
    def __init__(self, expectedUps = 60, expectedFps = 60, maxFrameSkip = 5, expectedMps = 1):
        self.expectedUps = expectedUps
        self.expectedFps = expectedFps
        self.expectedMps = expectedMps
        self.maxFrameSkip = maxFrameSkip
        
        self.countedUpdates = 0
        self.countedFrames = 0
        self.skippedFrames = 0
        
        self.measuredUps = 0
        self.measuredFps = 0
        
        self.updateIncrement = 1e9/self.expectedUps
        self.renderIncrement = 1e9/self.expectedFps
        self.measureIncrement = 1e9/self.expectedMps
        
        self.nextUpdateTime = 0
        self.nextRenderTime = 0
        self.nextMeasureTime = 0
        
        
    def start(self):
        startTime = time_ns()
        self.nextUpdateTime = startTime + self.updateIncrement
        self.nextRenderTime = startTime + self.renderIncrement
        self.nextMeasureTime = startTime + self.measureIncrement
        
    def registerUpdate(self):
        self.countedUpdates += 1
        self.skippedFrames += 1
        self.nextUpdateTime += self.updateIncrement
        
    def registerRender(self):
        self.countedFrames += 1
        self.skippedFrames = 0
        self.nextRenderTime += self.renderIncrement
        
    def measure(self):
        self.measuredUps = self.countedUpdates * self.expectedMps
        self.measuredFps = self.countedFrames * self.expectedMps
        self.countedUpdates = 0
        self.countedFrames = 0
        self.nextMeasureTime += self.measureIncrement
        
    def getUps(self):
        return self.measuredUps
    
    def getFps(self):
        return self.measuredFps
        
    def isTimeForUpdate(self):
        return time_ns() > self.nextUpdateTime and self.skippedFrames <= self.maxFrameSkip
        
    def isTimeForRender(self):
        if self.expectedFps == UNLIMITED_FPS:
            return True
        return time_ns() > self.nextRenderTime
        
    def isTimeForMeasure(self):
        return time_ns() > self.nextMeasureTime
        
        
        
        
        
        
