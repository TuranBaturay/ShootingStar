import batFramework as bf
from .common import *
from batFramework.cutsceneBlocks import *

class Chapter1(Chapter):
    def init_blocks(self):
        self.add_blocks(
            # Control(False),
            # SceneTransitionBlock("title"),
            # DelayBlock(1),
            SceneTransitionBlock("game"),
            # DelayBlock(3),
            # SceneTransitionBlock("options"),
            # Control(True),
        )
