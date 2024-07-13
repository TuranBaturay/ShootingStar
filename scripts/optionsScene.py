import batFramework as bf
import pygame
from .utils import *

class OptionsScene(DefaultScene):
    def __init__(self):
        super().__init__("options")

    def do_when_added(self):
        self.root.add(bf.BasicDebugger())


        main = bf.Container(bf.Column(2).set_child_constraints(bf.FillX()))
        
        main.add(
            bf.Button("BACK",lambda : self.manager.transition_to_scene(self.manager.get_scene_at(1).name)).set_uid(-5),
            bf.Toggle("FULLSCREEN",lambda v : pygame.display.toggle_fullscreen()),
            bf.Slider("MUSIC",bf.AudioManager().get_music_volume())
            .set_modify_callback(lambda v : bf.AudioManager().set_music_volume(v)),
            bf.Slider("SFX",bf.AudioManager().get_sound_volume())
            .set_modify_callback(lambda v : bf.AudioManager().set_sound_volume(v)),
            bf.Toggle("Particles",lambda v : self.set_sharedVar("particles",v),self.get_sharedVar("particles"))
        ).add_constraints(
            bf.MarginLeft(10),
            bf.PercentageRectMarginTop(0.5),
            bf.PercentageWidth(0.35)
        ).set_outline_width(0)
        
        self.root.add(main)
        main.get_focus()
        for child in main.children:
            child.set_alignment(bf.alignment.LEFT)

    def do_on_enter_early(self) -> None:
        self.root.get_by_uid(-5).set_silent_focus(True).get_focus()