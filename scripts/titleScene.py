import batFramework as bf
import pygame
from .utils import *
from .star import *
from .cutscenes import *

class TitleScene(DefaultScene):
    def __init__(self):
        super().__init__("title")
        self.vignette = bf.utils.draw_spotlight((255,100,100),(0,0,0),50,200,None,(1000,1000))
    def do_when_added(self):
        self.root.add(bf.BasicDebugger())
        
        main = bf.Container(bf.Column(4).set_child_constraints(bf.FillX()))
        
        main.add(
            bf.Button("PLAY",lambda :         bf.CutsceneManager().play(Chapter1())),
            bf.Button("OPTIONS",lambda : self.manager.transition_to_scene("options")),
            bf.Button("QUIT",self.manager.stop)
        ).add_constraints(bf.MarginLeft(10),bf.PercentageRectMarginTop(0.5)
        ).set_outline_width(0).set_color((0,0,0,0))
        
        for c in main.children:c.set_alignment(bf.alignment.LEFT)

        self.root.add(main)
        main.get_focus()

        title = bf.Label("Shooting").set_text_size(32).set_color((0,0,0,0))
        title.set_relief(0).set_text_outline_matrix(None)
        title2 = bf.Label("STAR").set_text_size(32).set_color((0,0,0,0))
        title2.set_relief(0).set_text_outline_matrix(None)
        title.set_center(*self.hud_camera.rect.move(-200,30).topright)
        title2.set_center(*title.rect.move(44,50).center)
        
        author = bf.Label("* Baturay TURAN *").add_constraints(bf.AnchorBottomRight()).set_alpha(100)
        author.set_color((0,0,0,0)).set_relief(0).set_text_outline_matrix(None)
        author.set_text_color(bf.color.LIGHTER_GB)
        self.root.add(title,title2,author)

        self.add_world_entity(Star().set_factor(0.4).set_width(2).set_rotate(True).set_points(5).set_position(*title2.rect.move(90,4).center))


    def do_on_enter(self) -> None:
        if self.manager.get_scene_at(1).name == "boot" and bf.AudioManager().get_current_music() is None:
            bf.AudioManager().play_music("main_theme",-1)

    # def do_post_world_draw(self, surface: pygame.Surface):
    #     # super().do_final_draw(surface)

    #     surface.blit(self.vignette,self.vignette.get_rect(center=pygame.mouse.get_pos()).topleft,special_flags=pygame.BLEND_MULT)
