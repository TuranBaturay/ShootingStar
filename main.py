import batFramework as bf
import pygame
from scripts.myManager import MyManager
bf.init(
    (240,200),pygame.SCALED,
    False,
    16,"fonts/batFont.ttf",
    "data","Shooting Star",
    fps_limit=0
)

if __name__ == "__main__":
     MyManager().run()

 