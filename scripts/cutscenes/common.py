import batFramework as bf


class Chapter(bf.Cutscene):...

class Control(bf.CutsceneBlock):
    def __init__(self,value:bool)->None:
        super().__init__()
        self.value = value

    def start(self):
        bf.CutsceneManager().enable_player_control() if self.value else bf.CutsceneManager().disable_player_control()
        super().start()
        self.end()
##############################################################################################  DIALOGUE SCENE

"""
Shows the textbox (no change to the content)
"""
class ShowText(bf.CutsceneBlock):...

"""
Hides the textbox
"""
class HideText(bf.CutsceneBlock):...
"""
Puts text to the textbox
if textbox is hidden -> ShowText
"""
class Say(bf.CutsceneBlock):...


"""
Set the background 
    image/color
    fadein and fadout are available
    if None the bg will be empty (if a scene is below it will show)
"""
class BG(bf.CutsceneBlock):...



"""
Shows a character sprite on the screen
can flip the sprite on X axis
can fade the character over fadein time
if char is None the char is made invisible
if char is None and fadout is specified the char will fade out over time
"""
class Char(bf.CutsceneBlock):...


"""
Clears the dialogue scene
    Remove bg (turns to blank color)
    removes chars
    removes text
"""



class Clear(bf.CutsceneBlock):...
##############################################################################################

"""
Conditional block
will only continue when callback returns true
"""
class WaitUntil(bf.CutsceneBlock):...



"""
Starts a wave of enemies to defeat
sets a shared flag to true when over
"""
class Wave(bf.CutsceneBlock):...
