import batFramework as bf
import pygame
from scripts.myManager import MyManager
bf.init(
    (320,240),pygame.SCALED,
    # (1280,720),0,
    # False,
    False,
    12,"fonts/batFont.ttf",
    "data","Shooting Star",
    fps_limit=0
)

if __name__ == "__main__":
     MyManager().run()

