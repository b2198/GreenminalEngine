from Game import Game
import logging
from GameLoopController import UNLIMITED_FPS

if __name__ == "__main__":
    #logging.basicConfig(filename="log.txt",level=logging.DEBUG)
    #logging.info("Starting program")
    game = Game(36,27,60,UNLIMITED_FPS,100)
    #logging.info("Game instance created")
    game.run()