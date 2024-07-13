import batFramework as bf
from .utils import *
import random
from pygame.math import Vector2

class Enemy(bf.DynamicEntity):
    def __init__(self):
        super().__init__((32, 32), convert_alpha=True)
        self.surface = bf.ResourceManager().get_image("graphics/sprites/enemy.png", True)
        self.base_speed = 100  # Adjust base speed as needed
        self.velocity = Vector2(0, self.base_speed)  # Initially moving down
        self.behavior = "wander"  # Default behavior
        self.patrol_points = [Vector2(random.randint(0, 800), random.randint(0, 600)) for _ in range(3)]  # Random patrol points
        self.current_patrol_index = 0
        self.chase_radius = 200  # Distance at which the enemy starts chasing the player
        self.spawner = bf.SceneTimer(0.1, self.spawn_particles, True, "game").start()

    def set_speed(self, speed: float):
        self.base_speed = speed
        self.velocity.y = self.base_speed

    def set_behavior(self, behavior: str):
        self.behavior = behavior

    def do_when_added(self):
        self.pg: bf.ParticleGenerator = self.parent_scene.pg
        self.player = self.parent_scene.player

    def do_when_removed(self):
        self.spawner.delete()

    def spawn_particles(self):
        if not self.parent_scene:
            self.spawner.delete()
            return
        if not self.parent_scene.get_sharedVar("particles"):
            return 
        for i in range(1):
            start_pos = self.rect.move(i, 4).midtop
            start_vel = Vector2(0, -self.base_speed)
            start_vel.rotate_ip(30 * (random.random() - 0.5))
            start_vel.x *= 1 + max(self.base_speed / 60, 0)
            self.pg.add_particle(FireParticle(start_pos, start_vel, 0.6, bf.color.LIGHTER_GB))

    def update_wandering(self, dt: float):
        # Wandering just moves downwards slowly
        self.velocity = Vector2(0, self.base_speed * 0.5)
        self.move_by_velocity(dt)

    def update_chasing(self, dt: float):
        player_pos = Vector2(self.player.rect.center)
        enemy_pos = Vector2(self.rect.center)
        direction_to_player = (player_pos - enemy_pos).normalize()
        distance_to_player = (player_pos - enemy_pos).length()

        if distance_to_player < self.chase_radius:
            self.velocity = direction_to_player * self.base_speed
        else:
            self.velocity = Vector2(0, self.base_speed)  # Continue moving downwards

        self.move_by_velocity(dt)

    def update_patrolling(self, dt: float):
        patrol_point = self.patrol_points[self.current_patrol_index]
        direction_to_point = (patrol_point - Vector2(self.rect.center)).normalize()
        self.velocity = direction_to_point * self.base_speed
        self.move_by_velocity(dt)

        if (patrol_point - Vector2(self.rect.center)).length() < 10:
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)

    def do_update(self, dt: float) -> None:
        if self.behavior == "wander":
            self.update_wandering(dt)
        elif self.behavior == "chase":
            self.update_chasing(dt)
        elif self.behavior == "patrol":
            self.update_patrolling(dt)

        for e in self.parent_scene.get_by_tags("bullet"):
            if not e.has_tags("used") and e.rect.colliderect(self.rect):
                self.parent_scene.add_world_entity(Explosion().set_center(*self.rect.center))
                self.parent_scene.remove_world_entity(self, e)
                e.add_tags("used")

        if self.rect.y > self.parent_scene.camera.rect.bottom:
            self.parent_scene.remove_world_entity(self)