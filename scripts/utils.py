import batFramework as bf
import pygame
from math import cos
from typing import Self
import math
from pygame.math import Vector2
from functools import cache
# Function to rotate a point around another point
def rotate_point(point, angle, center):
    angle_rad = math.radians(angle)
    x, y = point
    cx, cy = center

    new_x = cx + math.cos(angle_rad) * (x - cx) - math.sin(angle_rad) * (y - cy)
    new_y = cy + math.sin(angle_rad) * (x - cx) + math.cos(angle_rad) * (y - cy)
    
    return new_x, new_y

# Function to draw a star polygon
def draw_star(surface, color, center, radius, points, rotation_angle,factor:float=0.5,width:int=0):
    cx, cy = center
    angle_step = 360 / points
    vertices = []

    for i in range(points):
        angle = i * angle_step + rotation_angle - 90
        x = cx + radius * math.cos(math.radians(angle))
        y = cy + radius * math.sin(math.radians(angle))
        vertices.append((x, y))

        inner_angle = angle + angle_step / 2
        inner_radius = radius * factor
        x_inner = cx + inner_radius * math.cos(math.radians(inner_angle))
        y_inner = cy + inner_radius * math.sin(math.radians(inner_angle))
        vertices.append((x_inner, y_inner))

    pygame.draw.polygon(surface, color, vertices,width)

def nearest_color(color, palette):
    r, g, b = color[:3]  # Extract RGB values
    min_distance = float("inf")
    nearest = palette[0]
    for pal_color in palette:
        if len(color) == 4 and len(pal_color) == 4:
            r2, g2, b2, a2 = pal_color  # Extract RGBA values
            distance = math.sqrt(
                (r - r2) ** 2 + (g - g2) ** 2 + (b - b2) ** 2 + (color[3] - a2) ** 2
            )
        else:
            r2, g2, b2 = pal_color[:3]  # Extract RGB values
            distance = math.sqrt((r - r2) ** 2 + (g - g2) ** 2 + (b - b2) ** 2)

        if distance < min_distance:
            min_distance = distance
            nearest = pal_color

    return nearest


def convert_surface_to_palette(surface, palette):
    width, height = surface.get_size()
    for x in range(width):
        for y in range(height):
            original_color = surface.get_at((x, y))
            new_color = nearest_color(original_color, palette)
            surface.set_at((x, y), new_color)
    return surface


def draw_arrow(
    surface,
    center: tuple,
    size: int,
    color,
    direction: bf.direction = bf.direction.RIGHT,
):

    match direction:
        case bf.direction.RIGHT:
            p1 = (center[0] + size, center[1])
            p2 = (center[0], center[1] - size)
            p3 = (center[0], center[1] + size)
        case bf.direction.LEFT:
            p1 = (center[0] - size, center[1])
            p2 = (center[0], center[1] - size)
            p3 = (center[0], center[1] + size)
        case bf.direction.UP:
            p1 = (center[0], center[1] - size)
            p2 = (center[0] - size, center[1])
            p3 = (center[0] + size, center[1])
        case bf.direction.DOWN:
            p1 = (center[0], center[1] + size)
            p2 = (center[0] - size, center[1])
            p3 = (center[0] + size, center[1])
        case _:
            raise ValueError("Direction must be 'right', 'left', 'up', or 'down'")

    pygame.draw.polygon(surface, color, (p1, p2, p3))


def draw_focused_arrow(self: bf.InteractiveWidget, camera: bf.Camera):
    offset = 0
    if isinstance(self, bf.Shape):
        offset = self.relief
    origin = camera.world_to_screen_point(
        self.rect.move(-4 + 2 * cos(pygame.time.get_ticks() / 100), -offset).midleft
    )
    center = origin[0] + 4, origin[1]
    draw_arrow(camera.surface, center, 6, bf.color.DARKER_GB)
    center = origin
    draw_arrow(camera.surface, center, 6, bf.color.LIGHTER_GB)

def draw_focused_star(self: bf.InteractiveWidget, camera: bf.Camera):
    offset = 0
    if isinstance(self, bf.Shape):
        offset = self.relief
    origin = camera.world_to_screen_point(
        self.rect.move(-4 + 2 * cos(pygame.time.get_ticks() / 100), -offset).midleft
    )
    center = origin[0] + 4, origin[1]

    draw_star(camera.surface,bf.color.DARKER_GB,center,6,5,int(pygame.time.get_ticks() / 10),0.4)
    center = origin
    draw_star(camera.surface,bf.color.LIGHTER_GB,center,6,5,int(pygame.time.get_ticks() / 10),0.55)

class DefaultScene(bf.Scene):
    def __init__(self,name):
        super().__init__(name)
        self.set_clear_color(bf.color.DARKER_GB)




class FireParticle(bf.DirectionalParticle):
    cache : dict[tuple,pygame.Surface]= {}
    def __init__(self, start_pos: tuple[float, float], start_vel: tuple[float, float], duration=1, color=None, *args, **kwargs):
        super().__init__(start_pos, start_vel, duration, color, (9,9), *args, **kwargs)
    def start(self):
        self.surface = bf.ResourceManager().get_image("graphics/sprites/fire.png",True)
        return super().start()

    def update_surface(self):
        angle = int(self.velocity.angle_to(Vector2(1, 0)))
        prog = self.timer.get_progression()
        key = (angle,round(0.5+2*prog,1))
        alpha = 255 - int(prog* 255)
        if (key,alpha) not in FireParticle.cache :
            FireParticle.cache[(key,alpha)] = pygame.transform.rotozoom(self.original_surface,*key)
            FireParticle.cache[(key,alpha)].set_alpha(alpha)
        self.surface = FireParticle.cache[(key,alpha)]
        self.rect = self.surface.get_frect(center=self.rect.center)

class Bullet(bf.DynamicEntity):
    cache = {}
    def __init__(self,pos,vel):
        s = bf.ResourceManager().get_image("graphics/sprites/fire.png",True)
        
        super().__init__(s.get_size(),convert_alpha=True)
        self.surface = pygame.transform.rotate(s,90)
        self.rect.center = pos
        self.velocity.update(vel)
        self.add_tags("bullet")
    def do_update(self, dt: float) -> None:
        self.move_by_velocity(dt)
        if self.parent_scene:
            if not self.parent_scene.camera.rect.colliderect(self.rect):
                self.parent_scene.remove_world_entity(self)

    def draw(self, camera: bf.Camera) -> None:
        super().draw(camera)
        # value = 8 + int(4 * cos(pygame.time.get_ticks() / 10))
        value = 8
        s = Bullet.cache.get(value)
        if not s:
            s =pygame.Surface((value*2,value*2),pygame.SRCALPHA)
            # s.fill((100,100,100))
            bf.utils.draw_spotlight((100,100,100),(0,0,0),int(value/2),int(value*1.2),s)
            Bullet.cache[value] = s
        camera.surface.blit(s,(self.rect.move(-value,-value).center),special_flags=pygame.BLEND_RGBA_ADD)


class Explosion(bf.AnimatedSprite):
    def __init__(self):
        super().__init__((32,32))
        self.add_animState(
            "explosion",
            bf.ResourceManager().get_image("graphics/animations/explosion.png",True),
            (32,32),[3,5,6,6,3,1]
        )

    def do_update(self, dt: float) -> None:
        if self.float_counter == 0:
            if self.parent_scene:
                self.parent_scene.remove_world_entity(self)


@cache
def draw_rotating_star(size, rotation_angle, surface_size,color,outline_color=None):
    """
    Creates a surface with a fake 3D rotating star around the X-axis.

    :param size: The size of the star.
    :param rotation_angle: The angle of rotation around the x-axis in radians.
    :param surface_size: The size of the surface (width, height) to create for the star.
    :return: A Pygame surface with the drawn rotating star.
    """
    num_points = 5
    radius_outer = size
    radius_inner = size / 2.5
    star_points = []

    # Calculate the vertices of the 2D star
    for i in range(num_points * 2):
        angle = i * math.pi / num_points - 90
        radius = radius_outer if i % 2 == 0 else radius_inner
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        star_points.append((x, y))
    
    # Create a surface
    surface = pygame.Surface(surface_size, pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # Fill with transparent background

    # Rotate the star around the y-axis (affects x and z in 3D space)
    rotated_star_points = []
    for x, y in star_points:
        # Apply perspective transformation to simulate 3D rotation around Y-axis
        z = x * math.sin(rotation_angle)  # Simulate Z depth
        x_new = x * math.cos(rotation_angle) - z
        y_new = y
        
        rotated_star_points.append((x_new, y_new))

    # Translate the points to the center of the surface
    center = (surface_size[0] // 2, surface_size[1] // 2)
    translated_points = [(center[0] + x, center[1] - y) for x, y in rotated_star_points]

    # Draw the outline of the star
    if color is not None : pygame.draw.polygon(surface, color, translated_points, 0)
    if outline_color is not None : pygame.draw.polygon(surface, outline_color, translated_points, 1)
    
    
    # Optionally draw lines between points to make the star outline more prominent
    # pygame.draw.lines(surface, "red", True, translated_points, 0)

    return surface