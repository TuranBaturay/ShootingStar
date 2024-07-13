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
        if not self.visible : return
        super().draw(camera)

        if (
            self.is_current_message_over() 
            and self.state != "animating" 
            and bf.ResourceManager().get_sharedVar("player_has_control")
        ):
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
        self.background_image = bf.Image().add_constraints(bf.Center())
        self.dialogue_box = MyDialogueBox()

        self.hud_camera.set_clear_color((0, 0, 0, 0))
        self.set_clear_color((0, 0, 0, 100))
        
        self.debugger = (bf.FPSDebugger().set_color((0, 0, 0, 120)).set_text_color("white"))

        self.dialogue_box.set_alignment(bf.alignment.TOPLEFT)
        self.dialogue_box.set_shadow_color((*bf.color.LIGHTER_GB,120))
        self.dialogue_box.set_color((*bf.color.DARK_GB,120)).set_relief(2)
        self.dialogue_box.add_constraints(bf.FillX(),bf.FillY(),bf.Center())

        c = bf.Container()
        c.add_constraints(bf.MarginBottom(4),bf.CenterX(), bf.PercentageWidth(0.9),bf.PercentageHeight(0.3))
        c.set_color((0, 0, 0, 0))

        c.add(
            # self.title,
            self.background_image,
            self.dialogue_box)
        self.root.add(self.debugger)
        self.root.add(c)
        self.init()

    def init(self):
        self.end_callback_flag = False
        self.message_end_callback  = None
        
        self.show_background_scene = False
        self.background_scene = None

        self.show_background_image = False
        
        self.left_char = None
        self.right_char = None

        self.background_image.set_visible(self.show_background_image)
        self.dialogue_box.set_visible(False)
        self.set_clear_color(bf.color.DARKER_GB)


    def clear(self):
        self.init()

    def set_background_image(self,image:pygame.Surface):
        self.background_image.from_surface(image)

    def set_show_background_image(self,value:bool):
        self.show_background_image = value
        if self.background_image:
            self.background_image.set_visible(value)
    
    def set_show_text(self,value:bool):
        self.dialogue_box.set_visible(value)

    def say(self,text):

        self.dialogue_box.clear_queue()
        self.dialogue_box.say(text)
        self.dialogue_box.set_visible(True)
        self.callback_flag = False
    
    def set_message_end_callback(self,func):
        self.message_end_callback= func


    def do_update(self, dt):
        if not self.dialogue_box.visible:
            return
        if not self.actions.is_active("next"):
            return
        if not self.callback_flag and self.dialogue_box.is_current_message_over():
            self.dialogue_box.next_message()
            if not self.dialogue_box.is_queue_empty():return
            self.callback_flag = True
            if self.message_end_callback : self.message_end_callback()                