from time import perf_counter

UNLIMITED_FPS = -1
UNLIMITED_FRAME_SKIP = -1

class GameLoopController:
    
    #ups -> updates per second
    #fps -> frames per second
    #mps -> measures per second
    def __init__(self, expectedUps = 60, expectedFps = 60, maxFrameSkip = 5, expectedMps = 1):
        self.expectedUps = expectedUps
        self.expectedFps = expectedFps
        self.expectedMps = expectedMps
        if expectedFps != UNLIMITED_FPS:
            self.maxFrameSkip = maxFrameSkip * expectedUps / expectedFps
        else:
            self.maxFrameSkip = UNLIMITED_FRAME_SKIP
        
        self.countedUpdates = 0
        self.countedFrames = 0
        self.skippedFrames = 0
        
        self.measuredUps = 0
        self.measuredFps = 0
        
        self.updateIncrement = 1/self.expectedUps
        self.renderIncrement = 1/self.expectedFps
        self.measureIncrement = 1/self.expectedMps
        
        self.nextUpdateTime = 0
        self.nextRenderTime = 0
        self.lastMeasureTime = 0
        self.nextMeasureTime = 0
        
        
    def start(self):
        startTime = perf_counter()
        self.nextUpdateTime = startTime + self.updateIncrement
        self.nextRenderTime = startTime + self.renderIncrement
        self.lastMeasureTime = startTime
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
        #import logging
        #logging.basicConfig(filename="log.txt",level=logging.DEBUG)
        #logging.debug("current time: {:0.9f} seconds\ntime since last measure: {:0.9f} seconds\n".format(perf_counter(), perf_counter() - self.lastMeasureTime))
        self.measuredUps = self.countedUpdates * (1 / (self.nextMeasureTime - self.lastMeasureTime) ) // 1
        self.measuredFps = self.countedFrames * (1 / (self.nextMeasureTime - self.lastMeasureTime) ) // 1
        self.countedUpdates = 0
        self.countedFrames = 0
        self.lastMeasureTime = self.nextMeasureTime
        self.nextMeasureTime += self.measureIncrement
        
    def getUps(self):
        return self.measuredUps
    
    def getFps(self):
        return self.measuredFps
        
    def isTimeForUpdate(self):
        if self.maxFrameSkip == UNLIMITED_FRAME_SKIP:
            return perf_counter() > self.nextUpdateTime
        return perf_counter() > self.nextUpdateTime and self.skippedFrames <= self.maxFrameSkip
        
    def isTimeForRender(self):
        if self.expectedFps == UNLIMITED_FPS:
            return True
        return perf_counter() > self.nextRenderTime
        
    def isTimeForMeasure(self):
        return perf_counter() > self.nextMeasureTime
        
        
        
        
        
        
