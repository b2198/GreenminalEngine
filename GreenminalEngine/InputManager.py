from pynput import keyboard

if __name__ == "__main__":
    input = InputManager()
    input.start()

PRESSED = 0
JUST_PRESSED = 1
RELEASED = 2
JUST_RELEASED = 3
    
class InputManager:

    def __init__(self):
        self.keyPool = {}
        self.pressedKeys = []
        self.releasedKeys = []
        self.listener = None
        
    def start(self):
        for key in self.keyPool:
            self.keyPool[key] = RELEASED
        if self.listener is None:
            self.listener = keyboard.Listener(
                on_press = self.onPress,
                on_release = self.onRelease
            )
            self.listener.start()

    def onPress(self,key):
        try: pressedKey = key.char
        except: pressedKey = key.name
        
        #print("new key press: %s" % (pressedKey))
        
        self.pressedKeys.append(pressedKey)
        
    def onRelease(self,key):
        try: releasedKey = key.char
        except: releasedKey = key.name
        
        #print("new key release: %s" % (releasedKey))
        
        self.releasedKeys.append(releasedKey)
        
    def update(self):
        
        #print(self.pressedKeys)
        #print(self.releasedKeys)
        #print(self.keyPool)
        
        
        for key in self.keyPool:
            if self.keyPool[key] == JUST_PRESSED:
                self.keyPool[key] = PRESSED
            elif self.keyPool[key] == JUST_RELEASED:
                self.keyPool[key] = RELEASED
        
        
        for pressedKey in self.pressedKeys:
            if pressedKey not in self.keyPool.keys():
                self.keyPool[pressedKey] = JUST_PRESSED
                continue
            poolValue = self.keyPool[pressedKey]
            if(poolValue == RELEASED or poolValue == JUST_RELEASED):
                self.keyPool[pressedKey] = JUST_PRESSED
    
        for releasedKey in self.releasedKeys:
            if releasedKey not in self.keyPool.keys():
                self.keyPool[releasedKey] = JUST_RELEASED
                continue
            poolValue = self.keyPool[releasedKey]
            if(poolValue == PRESSED or poolValue == JUST_PRESSED):
                self.keyPool[releasedKey] = JUST_RELEASED
                
        self.pressedKeys.clear()
        self.releasedKeys.clear()
        
    def isPressed(self, key):
        if key not in self.keyPool.keys():
            return False
        poolValue = self.keyPool[key]
        return poolValue == PRESSED or poolValue == JUST_PRESSED
        
    def isJustPressed(self, key):
        if key not in self.keyPool.keys():
            #print("key not in pool")
            return False
        poolValue = self.keyPool[key]
        #print("key state: %d" % (poolValue))
        return poolValue == JUST_PRESSED
        
    def isReleased(self, key):
        if key not in self.keyPool.keys():
            return True
        poolValue = self.keyPool[key]
        return poolValue == RELEASED or poolValue == JUST_RELEASED
        
    def isJustReleased(self, key):
        if key not in self.keyPool.keys():
            return False
        poolValue = self.keyPool[key]
        return poolValue == JUST_RELEASED
            

        

        