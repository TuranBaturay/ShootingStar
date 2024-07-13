import batFramework as bf
from .utils import *


class PauseScene(DefaultScene):
    def __init__(self):
        super().__init__("pause")

    def do_when_added(self):
        # self.set_clear_color((0, 0, 0, 120))
        # self.hud_camera.set_clear_color((0, 0, 0, 0))
        self.debugger = (
            bf.FPSDebugger().set_color((0, 0, 0, 120)).set_text_color("white")
        )
        self.root.add(self.debugger)
        self.debugger.add_dynamic(
            "uid", lambda: self.root.hovered.uid if self.root.hovered else None
        )

        self.add_actions(
            bf.Action("resume").add_key_control(pygame.K_ESCAPE), *bf.WASDControls()
        )
        self.init_widgets()

    def init_widgets(self) -> None:
        c = bf.Container(bf.Column(2).set_child_constraints(bf.FillX())).set_padding(20)
        buttons = [
            bf.Button(
                "RESUME",
                lambda: self.manager.transition_to_scene("game"),
            ).set_uid(-4),
            bf.Button("MAIN MENU", lambda: self.manager.transition_to_scene("title")),
            bf.Button("OPTIONS", lambda: self.manager.transition_to_scene("options")),
        ]
        c.add(*buttons)
        c.set_padding(0)
        c.add_constraints(bf.constraints.PercentageMarginTop(0.5),bf.CenterX())

        self.root.add(c)
        c.get_focus()

    def do_on_enter(self) -> None:
        # self.manager.set_scene("game",1)
        # self.manager.get_scene_at(1).set_active(False)
        # self.manager.get_scene_at(1).set_visible(True)
        bf.AudioManager().play_sound("click_fade")

    def do_on_enter_early(self):
        self.root.get_by_uid(-4).set_silent_focus(True).get_focus()

    def do_on_exit(self) -> None:
        bf.AudioManager().play_sound("click_fade")

    def do_update(self, dt):
        if self.actions.is_active("resume"):
            self.manager.transition_to_scene(self.manager.get_scene_at(1).name)
        if self.actions.is_active("up"):
            self.hud_camera.move_by(0, -2)
        if self.actions.is_active("down"):
            self.hud_camera.move_by(0, 2)
