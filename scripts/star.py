import batFramework as bf
import pygame
from .utils import *
from typing import Self

class Star(bf.Entity):
    cache : dict[tuple,pygame.Surface] = {}
    def __init__(self,size=(30,30)):
        super().__init__(size=size,convert_alpha=True)
        self.angle = 0
        self.factor = 0.3
        self.points = 5
        self.color = bf.color.LIGHTER_GB
        self.do_rotate : bool = False
        self.width : int = 0
        self.update_surface()

    def set_width(self, width:int)->Self:
        self.width = width
        self.update_surface()
        return self

    def set_points(self,points:int)->Self:
        self.points = points
        self.update_surface()
        return self

    def set_rotate(self,rotate:bool)->Self:
        self.do_rotate= rotate
        self.update_surface()

        return self

    def set_factor(self,factor:float)->Self:    
        self.factor = factor   
        self.update_surface()

        return self
    
    def set_color(self,color)->Self:
        self.color = color
        self.update_surface()
        
        return self

    def update_surface(self):
        r = self.surface.get_rect()
        key = (self.color,r.center,r.w//2,self.points,((self.angle//4) * 4),self.factor,self.width,r.size)
        if key not in Star.cache:
            self.surface.fill((0,0,0,0))
            draw_star(self.surface,*key[:-1])
            Star.cache[key] = self.surface.copy()
        else:
            self.surface = Star.cache[key]


    def do_update(self,dt:float):
        if not self.do_rotate : 
            return
        self.angle += dt*50
        # self.angle %= 360
        self.update_surface()

class Star3D(bf.Entity):
    cache: dict[tuple, pygame.Surface] = {}

    def __init__(self, size=(32, 32)):
        super().__init__(size=size, convert_alpha=True)
        self.angle = 0
        self.size = size[0]/3  # Assuming width and height are the same for size
        self.color = bf.color.LIGHTER_GB
        self.outline_color = None
        self.update_surface()

    def set_size(self, size: int) -> Self:
        self.size = size
        self.update_surface()
        return self

    def set_color(self, color) -> Self:
        self.color = color
        self.update_surface()
        return self

    def set_outline_color(self, outline_color) -> Self:
        self.outline_color = outline_color
        self.update_surface()
        return self

    def set_rotation_angle(self, angle: float) -> Self:
        self.angle = angle
        self.update_surface()
        return self

    def update_surface(self):
        r = self.surface.get_rect()
        self.surface.fill((0, 0, 0, 0))
        key = (self.size, self.angle, r.size , self.color, self.outline_color)
        surf = Star3D.cache.get(key)
        if surf is None:
            surf = draw_rotating_star(*key)
            Star3D.cache[key] = surf

        topleft = surf.get_rect(center = self.rect.move(-self.rect.x,-self.rect.y).center).topleft
        self.surface.blit(surf,topleft)

    def do_update(self, dt: float):
        self.angle += dt 
        self.update_surface()