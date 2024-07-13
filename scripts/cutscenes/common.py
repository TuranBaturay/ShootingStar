import batFramework as bf


class Chapter(bf.Cutscene):...

class Control(bf.FunctionBlock):
    def __init__(self,value:bool)->None:
        if value:
            func = bf.CutsceneManager().enable_player_control  
        else:
            func = bf.CutsceneManager().disable_player_control
        super().__init__(func)

##############################################################################################  DIALOGUE SCENE

"""
Shows the textbox (no change to the content)
"""
class ShowText(bf.FunctionBlock):
    def __init__(self):
        func =  lambda : bf.CutsceneManager().manager.get_scene("dialogue").set_show_text(True)
        super().__init__(func)    

"""
Hides the textbox
"""
class HideText(bf.FunctionBlock):
    def __init__(self):
        super().__init__(lambda : bf.CutsceneManager().manager.get_scene("dialogue").set_show_text(False))    

"""
Puts text to the textbox
if textbox is hidden -> ShowText
"""
class Say(bf.CutsceneBlock):
    def __init__(self, text:str) -> None:
        super().__init__()
        self.text = text
    def start(self):
        bf.CutsceneManager().manager.get_scene("dialogue").say(self.text)
        bf.CutsceneManager().manager.get_scene("dialogue").set_message_end_callback(self.end)
        

"""
Set the background 
    image/color
    fadein and fadout are available
    if None the bg will be empty (if a scene is below it will show)
"""
class BG(bf.FunctionBlock):
    def __init__(self,image=None,color=None):
        super().__init__(None)
        if image == color and color == None:
            return
        def func():
            d = bf.CutsceneManager().manager.get_scene("dialogue")
            if image:
                d.set_background_image(image)
            if color:
                d.set_clear_color(color)

        self.function =  func


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



class Clear(bf.FunctionBlock):
    def __init__(self) -> None:
        super().__init__(None)
        self.function = bf.CutsceneManager().manager.get_scene("dialogue").clear
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




class GameOver(bf.CutsceneBlock):
    def __init__(self):
        super().__init__()
        bf.SceneTransitionBlock("dialogue")
        Say(f"GAME OVER\nYour score is {bf.ResourceManager().get_sharedVar("score")}")
        bf.SceneTransitionBlock("title")
