import batFramework as bf
from .utils import *
import pygame


class BootScene(bf.Scene):
    def __init__(self):
        super().__init__("boot")


    def do_when_added(self):
        self.set_clear_color(bf.color.LIGHTER_GB)

        self.debugger = bf.FPSDebugger()
        self.debugger.set_color((30, 30, 30, 120)).set_text_color("white")
        self.root.add(self.debugger)

        self.enter_time = 0.5
        self.wait_time = 3
        self.exit_time_start = 2
        self.exit_time_end = 1

        self.booted = False
        self.transition1 = bf.transition.FadeColor(
            bf.color.DARKER_GB, self.enter_time, 0
        )
        self.transition2 = bf.transition.FadeColor(
            bf.color.LIGHTER_GB, self.exit_time_start, self.exit_time_end
        )


        self.init_widgets()
        self.add_actions(bf.Action("space").add_key_control(pygame.K_SPACE))

    def init_widgets(self):
        title = bf.Label("- POWERED BY PYGAME -")  # .set_text_size(16)
        # title.set_italic(True)
        title.add_constraints(bf.constraints.Center())
        self.root.add(title)
        title.set_color((0, 0, 0, 0)).set_outline_width(0)
        title.set_text_outline_color(bf.color.LIGHT_GB)

    def do_on_enter(self) -> None:
        self.timer = None
        if self.booted:
            self.timer = bf.Timer(
                self.wait_time,
                lambda: bf.AudioManager().play_music("main_theme",-1,500) and self.manager.transition_to_scene("title", self.transition2),
            ).start()
            return
        self.booted = True
        self.manager.transition_to_scene("boot", self.transition1)
        bf.AudioManager().play_sound("boot")

    def do_update(self, dt):
        if self.actions.is_active("space"):
            self.transition1.skip(no_callback=True)
            self.transition2.skip(no_callback=True)
            if self.timer is not None:
                self.timer.delete()
            bf.AudioManager().stop_sound("boot")
            self.manager.transition_to_scene("title")
