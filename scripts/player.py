import batFramework as bf
import pygame
import random
from pygame.math import Vector2
from math import cos
from .utils import *
class Player(bf.Sprite,bf.DynamicEntity):
    def __init__(self) -> None:
        super().__init__("graphics/sprites/spaceship.png",(32,32))
        self.light = bf.ResourceManager().get_image("graphics/sprites/spaceship_light.png",True)
        self.light_on : bool = False
        self.actions = bf.ActionContainer(
            *bf.DirectionalKeyControls(),
            bf.Action("space").add_key_control(pygame.K_SPACE)
        )
        self.h_speed = self.v_speed = 50
        self.spawner = bf.SceneTimer(0.07,self.spawn_particles,True,"game").start()
        self.shoot_timer : bf.Timer = bf.SceneTimer(0.1,self.close_light,False,"game")


    def shoot(self):
        self.open_light()
        self.shoot_timer.start()
        bf.AudioManager().play_sound("laserShoot")
        self.parent_scene.add_world_entity(Bullet(self.rect.midtop,(0,-400)))

    def open_light(self):
        self.light_on = True

    def close_light(self):
        self.light_on = False

    def spawn_particles(self):
        if not self.parent_scene.get_sharedVar("particles"):
            return 
        for i in range(-2,2):
            start_pos = self.rect.move(i,-4).midbottom
            start_vel = Vector2(0,100)
            start_vel.rotate_ip(70 * (random.random() - 0.5))
            start_vel.x *= 1 + max(self.velocity.y/60,0)
            start_vel.y += -(min(0,self.velocity.y/2))
            if self.velocity.y > 0:
                start_vel.y += self.velocity.y
            self.pg.add_particle(FireParticle(start_pos,start_vel,0.6,bf.color.LIGHTER_GB))

        if self.velocity.y < -2 and len(self.pg.particles)<80: 
            bf.SceneTimer(0.14,self.spawn_particles,scene_name="game").start()
    def do_when_added(self):
        self.pg : bf.ParticleGenerator = self.parent_scene.pg

    def do_process_actions(self, event: pygame.Event) -> None:
        self.actions.process_event(event)

    def do_reset_actions(self) -> None:
        self.actions.reset()

    def do_update(self, dt: float) -> None:
        self.velocity *= 0.8
        if self.actions.is_active("up"):
            self.velocity.y -= self.v_speed
        if self.actions.is_active("down"):
            self.velocity.y += self.v_speed
        if self.actions.is_active("left"):
            self.velocity.x -= self.h_speed
        if self.actions.is_active("right"):
            self.velocity.x += self.h_speed
        if self.actions.is_active("space") and self.shoot_timer:
            self.shoot()
        self.move_by_velocity(dt)

        if self.parent_scene:
            self.rect.clamp_ip(self.parent_scene.camera.rect)
        # if random.random() < 0.2:
        #     self.light_on = not self.light_on


    def draw(self, camera: bf.Camera) -> None:
        super().draw(camera)
        if self.light_on:
            camera.surface.blit(self.light,self.rect.move(-camera.rect.x,-camera.rect.y).topleft,special_flags=pygame.BLEND_RGB_ADD)