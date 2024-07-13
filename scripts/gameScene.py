import batFramework as bf
import pygame
from .utils import *
from .player import Player
from .enemy import Enemy
from .star import Star
import random

import batFramework as bf
import pygame
from .utils import *
from .player import Player
from .star import Star
import random
from .cutscenes import Chapter1

class BGStar(Star):
    effect = {}
    def __init__(self, size=...):
        self.scale_factor = 1.0
        self.speed = 1
        super().__init__(size)
        self.set_factor(0.5)

    def set_speed(self, speed) -> Self:
        self.speed = speed
        return self

    def set_scale_factor(self, factor) -> Self:
        self.scale_factor = factor
        return self

    def update_surface(self):
        if self.rect.w <= 4:
            self.surface.fill(self.color)
        else:
            super().update_surface()
        scaled_size = (int(self.rect.w * self.scale_factor), int(self.rect.h * self.scale_factor))
        if scaled_size not in BGStar.effect:
            r = self.rect.inflate(self.rect.w * self.scale_factor, self.rect.h * self.scale_factor)
            circle = pygame.Surface(r.size).convert_alpha()
            circle.fill((0,0,0,0))
            BGStar.effect[scaled_size] = circle
            pygame.draw.circle(circle, (30,30,30), (r.w // 2, r.h // 2), r.w//2)
        self.set_alpha(255 - self.render_order/19 * 255)

    def do_update(self, dt: float):
        super().do_update(dt)
        dx = self.speed * ((self.rect.centerx - bf.const.RESOLUTION[0] // 2) / bf.const.RESOLUTION[0]) * 0.8
        self.rect.move_ip(dx * dt * 60, self.speed * dt * 60)
        if self.parent_scene:
            if not self.parent_scene.camera.rect.colliderect(self.rect):
                if self.rect.y < self.parent_scene.camera.rect.bottom:
                    return
                self.parent_scene.remove_world_entity(self)

    def draw(self, camera: bf.Camera) -> None:
        super().draw(camera)
        scaled_size = (int(self.rect.w * self.scale_factor), int(self.rect.h * self.scale_factor))
        camera.surface.blit(
            BGStar.effect[scaled_size],
            (self.rect.x - scaled_size[0] / 2 - camera.rect.x, self.rect.y - scaled_size[1] / 2 - camera.rect.y),
            special_flags=pygame.BLEND_RGB_ADD)

class GameScene(DefaultScene):
    def __init__(self):
        super().__init__("game")
        self.max_life = 100

    def do_when_added(self):
        self.pg = bf.ParticleGenerator()
        self.add_world_entity(self.pg)
        self.debugger = bf.BasicDebugger()
        self.root.add(self.debugger)
        self.debugger.add_dynamic("Particles",lambda : len(self.pg.particles))
        self.player = Player().set_render_order(99)
        self.player.set_center(*self.camera.get_center())
        self.add_world_entity(self.player)
        self.player.set_render_order(12)
        self.add_actions(bf.Action("escape").add_key_control(pygame.K_ESCAPE))
        timer_duration = 0.4
        self.speed_factor = 5
        self.star_spawner = bf.SceneTimer(timer_duration, self.spawn_stars, True,"game").start()
        self.enemy_spawner = bf.SceneTimer(2,self.spawn_enemies,True,"game").start()
        bf.ResourceManager().set_sharedVar("wave",0)
        bf.ResourceManager().set_sharedVar("score",0)
        bf.ResourceManager().set_sharedVar("life",100)


        for _ in range(20):
            render_order = random.randint(1, 20)
            size, speed = self.calculate_star_properties(render_order)
            position = random.randrange(0, int(self.camera.rect.w)), random.randrange(0, int(self.camera.rect.h))
            self.add_world_entity(
                BGStar((size, size)).set_speed(speed).set_render_order(render_order).set_center(*position)
            )

        self.life_meter = bf.Meter(0,100,1).add_constraints(bf.AnchorBottom(),bf.PercentageWidth(0.2)).set_size((None,20))
        self.life_meter.set_outline_width(2).set_outline_color(bf.color.DARK_GB)
        self.life_meter.set_border_radius(4)
        self.life_meter.content.set_border_radius(2)
        
        self.score_label = bf.Label("0").add_constraints(bf.AnchorTopRight())
        self.score_label.set_color((0,0,0,0)).set_relief(0)

        self.root.add(self.life_meter)
        self.root.add(self.score_label)



    def init(self):
        bf.ResourceManager().set_sharedVar("wave",0)
        bf.ResourceManager().set_sharedVar("score",0)
        bf.ResourceManager().set_sharedVar("life",self.max_life)
        self.player.set_center(*self.camera.rect.center)

        self.world_entities.clear()
        self.add_world_entity(self.pg,self.player)
    def do_on_enter(self) -> None:
        if self.manager.get_scene_at(1).name == "title":
            self.init()

    def spawn_enemies(self):
        num = random.randint(1,3)
        for _ in range(num):
            x,y = random.randint(-100+bf.const.RESOLUTION[0]//2,100+bf.const.RESOLUTION[0]//2),-40-random.randint(0,100)
            enemy = Enemy().set_center(x,y)
            self.add_world_entity(enemy)

    def spawn_stars(self):
        if not self.get_sharedVar("particles"):
            return 
        num = random.randint(1, 20)
        for _ in range(num):
            render_order = random.randint(1, 20)
            size, speed = self.calculate_star_properties(render_order)
            position = random.randrange(0, int(self.camera.rect.w)), random.randrange(-int(self.camera.rect.h / 2), -30)
            self.add_world_entity(
                BGStar((size, size)).set_speed(speed).set_render_order(render_order).set_center(*position)
            )

    def do_update(self, dt):
        if self.actions.is_active("escape"):
            self.manager.transition_to_scene("pause")

        self.life_meter.set_value(bf.ResourceManager().get_sharedVar("life"))
        self.score_label.set_text(str(bf.ResourceManager().get_sharedVar("score")))

    def calculate_star_properties(self, render_order):
        """Determine size and speed based on render order."""
        size = max(1,render_order//2)
        speed = self.speed_factor * render_order / 10.0  # Higher render order means faster speed
        return size, speed

