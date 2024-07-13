import batFramework as bf
from .titleScene import TitleScene 
from .gameScene import GameScene
from .optionsScene import OptionsScene
from .bootScene import BootScene
from .pauseScene import PauseScene
from .dialogueScene import DialogueScene
from .style import MyStyle


class MyManager(bf.Manager):
    def __init__(self):
        self.dialogue_scene = DialogueScene()
        super().__init__(
            BootScene(),
            TitleScene(),
            GameScene(),
            OptionsScene(),
            PauseScene(),
            self.dialogue_scene
        )

    def do_pre_init(self) -> None:
        self.load_styles()
        self.load_audio()
        self.set_sharedVar("particles",False)

    def load_styles(self):
        bf.StyleManager().add(MyStyle())

    def load_audio(self):
        bf.AudioManager().load_music("main_theme", "audio/music/main_theme.mp3")
        bf.AudioManager().load_sounds(
            [
                ("click", "audio/sfx/click.mp3"),
                ("click_fade", "audio/sfx/click_fade.mp3"),
                ("boot", "audio/sfx/boot.mp3"),
            ]
        )
        bf.AudioManager().set_music_volume(0.0)
        bf.AudioManager().set_sound_volume(0.0)
