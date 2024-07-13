import batFramework as bf
import pygame
from .utils import *

class MyDialogueBox(bf.DialogueBox):
    def __init__(self) -> None:
        super().__init__()
        self.state = "default"

    def resume(self) -> Self:
        super().resume()
        self.state = "default"
        return self

    def draw(self, camera: bf.Camera) -> None:
        super().draw(camera)
        if self.is_current_message_over() and self.state != "animating":
            offset = 2 * cos(pygame.time.get_ticks() / 100)
            center = self.rect.move(-10 + offset, -10).bottomright
            if len(self.message_queue) == 1:
                draw_arrow(
                    camera.surface, (center[0] + 3, center[1]), 4, bf.color.DARKER_GB
                )

            draw_arrow(camera.surface, center, 4, bf.color.LIGHT_GB)


class DialogueScene(bf.Scene):
    def __init__(self):
        super().__init__("dialogue")
        self.camera = bf.Camera(pygame.SRCALPHA)
        self.add_actions(
            bf.Action("next").add_key_control(pygame.K_SPACE).add_mouse_control(1)
        )
    
    def do_when_added(self):
        self.init()
        self.dialogue_box = MyDialogueBox()
        # self.title = bf.Label("")

        self.hud_camera.set_clear_color((0, 0, 0, 0))
        self.set_clear_color((0, 0, 0, 100))
        
        self.debugger = (bf.FPSDebugger().set_color((0, 0, 0, 120)).set_text_color("white"))

        self.dialogue_box.set_alignment(bf.alignment.TOPLEFT)
        self.dialogue_box.set_shadow_color((*bf.color.LIGHTER_GB,120))
        self.dialogue_box.set_color((*bf.color.DARK_GB,120)).set_relief(2)
        self.dialogue_box.add_constraints(bf.FillX(),bf.FillY())

        # self.title.set_relief(0).set_border_radius((0, 0, 4)).set_padding((4, 4, 4, 1))
        # self.title.set_relief(0).set_border_radius((0, 0, 4)).set_padding((4, 4, 4, 1))

        
        c = bf.Container()
        c.add_constraints(bf.MarginBottom(2), bf.CenterX(), bf.PercentageWidth(0.9),bf.PercentageHeight(0.3))
        c.set_color((0, 0, 0, 0))

        c.add(
            # self.title,
            self.dialogue_box)
        self.root.add(self.debugger)
        self.root.add(c)

    def init(self):
        self.show_background_scene = False
        self.background_scene = None
        
        self.show_background_image = False
        self.background_image = None
        
        self.left_char = None
        self.right_char = None



    def do_on_enter(self) -> None:
        self.setup()
    
    def setup(self):
        pass