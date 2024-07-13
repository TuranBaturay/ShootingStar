import batFramework as bf
import pygame
from scripts.myManager import MyManager
bf.init(
    (320,240),pygame.SCALED,
    False,
    12,"fonts/batFont.ttf",
    "data","Shooting Star",
    fps_limit=60
)

if __name__ == "__main__":
     MyManager().run()

