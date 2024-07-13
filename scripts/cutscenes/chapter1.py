import batFramework as bf
from .common import *
from batFramework.cutsceneBlocks import *

class Chapter1(Chapter):
    def init_blocks(self):
        self.add_blocks(
            bf.FunctionBlock(bf.CutsceneManager().manager.get_scene("title").story_button.disable),
            Clear(),
            SceneTransitionBlock("dialogue"),
            DelayBlock(1),
            Say("Story will be available in the near future..."),
            Say("We are sorry for the inconvenience :("),
            SceneTransitionBlock("title",bf.FadeColor(bf.color.LIGHTER_GB,0.5,0.3,0.3)),

        )
