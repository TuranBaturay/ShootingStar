import batFramework as bf
from .utils import *
import random
from pygame.math import Vector2

class Enemy(bf.DynamicEntity):
    def __init__(self):
        super().__init__((32, 32), convert_alpha=True)
        self.add_tags("enemy")
        self.surface = bf.ResourceManager().get_image("graphics/sprites/enemy.png", True)
        self.base_speed = 100  # Adjust base speed as needed
        self.velocity = Vector2(0, self.base_speed)  # Initially moving down
        self.spawner = bf.SceneTimer(0.1, self.spawn_particles, True, "game").start()
        self.target = 0
        self.refresh_target = bf.SceneTimer(0.2,self.refresh,True,"game")
        self.accuracy_range = 20
        self.reaction_speed = 0.3
        self.shoot_timer : bf.Timer = bf.SceneTimer(1,None,False,"game")
        self.reaction_timer = bf.SceneTimer(self.reaction_speed,self.shoot,scene_name="game")
        self.bullet_speed = 150

    def refresh(self):
        self.target = self.player.rect.centerx + random.randint(-self.accuracy_range,self.accuracy_range)


    def set_speed(self, speed: float):
        self.base_speed = speed
        self.velocity.y = self.base_speed

    def set_behavior(self, behavior: str):
        self.behavior = behavior

    def do_when_added(self):
        self.pg: bf.ParticleGenerator = self.parent_scene.pg
        self.player: bf.DynamicEntity = self.parent_scene.player
        self.target = self.player.rect.centerx
        self.refresh_target.start()
    def do_when_removed(self):
        self.spawner.delete()

    def spawn_particles(self):
        if not self.parent_scene:
            self.spawner.delete()
            return
        if not self.parent_scene.get_sharedVar("particles"):
            return 
        for i in range(-1,1):
            start_pos = self.rect.move(i, 4).midtop
            start_vel = Vector2(0, -self.base_speed)
            start_vel.rotate_ip(30 * (random.random() - 0.5))
            start_vel.x *= 1 + max(self.base_speed / 60, 0)
            self.pg.add_particle(FireParticle(start_pos, start_vel, 0.2, bf.color.LIGHTER_GB))


    def shoot(self):
        if not self.parent_scene: return
        bf.AudioManager().play_sound("enemyLaserShoot")
        self.parent_scene.add_world_entity(Bullet(self.rect.midbottom,(0,self.bullet_speed)).add_tags("e_bullet"))
        self.shoot_timer.start()

    def do_update(self, dt: float) -> None:
        if self.rect.centery > 40:
            if abs(self.target - self.rect.centerx)>4:
                self.velocity.x = self.target - self.rect.centerx

        self.move_by_velocity(dt)

        for e in self.parent_scene.get_by_tags("bullet"):
            if not e.has_tags("used") and e.rect.colliderect(self.rect):
                bf.ResourceManager().set_sharedVar("score",bf.ResourceManager().get_sharedVar("score")+10)
                self.parent_scene.add_world_entity(Explosion().set_center(*self.rect.center))
                self.parent_scene.remove_world_entity(self, e)
                e.add_tags("used")
                return

        if self.rect.y > self.parent_scene.camera.rect.bottom:
            self.parent_scene.remove_world_entity(self)
            return
        if self.rect.centery < 20:
            return
        if self.player.rect.centerx > self.rect.centerx - self.accuracy_range and\
            self.player.rect.centerx < self.rect.centerx + self.accuracy_range:
            if not self.shoot_timer.has_started() and not self.reaction_timer.has_started():
                self.reaction_timer.start()