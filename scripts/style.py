import batFramework as bf
from .utils import *

class MyStyle(bf.Style):
    def apply(self, w: bf.Widget):

        if isinstance(w, bf.Debugger):
            w.set_text_size(8).set_text_color("white").set_color((0,0,0,180))
            return

        if isinstance(w, bf.Shape):
            w.set_color(bf.color.DARKER_GB).set_outline_color(bf.color.LIGHT_GB).set_border_radius(2)

        if isinstance(w, bf.Container):
            w.set_outline_width(0).set_padding(4)

        if isinstance(w, bf.Label):
            w.set_padding((4,3))
            w.set_relief(2).set_outline_width(0)
            w.set_text_color(bf.color.LIGHTER_GB).set_text_outline_color(
                bf.color.DARKER_GB
            )
            w.set_color(bf.color.DARK_GB).set_shadow_color(bf.color.LIGHTER_GB)
            w.enable_text_outline()
            w.set_text_outline_mask_size((5,5))
            w.set_text_outline_matrix(
                [
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1]
                ])

            # w.set_text_outline_matrix(
            #     [[1,1,1],
            #      [1,0,1],
            #      [1,1,1]])

        if isinstance(w, bf.DialogueBox):
            w.set_padding((4, 4, 14, 4))

        if isinstance(w, bf.InteractiveWidget):
            w.draw_focused = lambda cam: draw_focused_star(w, cam)

        if isinstance(w, bf.ClickableWidget) and isinstance(w,bf.Shape):
            w.set_color(bf.color.LIGHT_GB).set_shadow_color(
                bf.color.DARK_GB
            )  # .set_outline_color(bf.color.LIGHTER_GB)
            w.set_pressed_relief(2).set_unpressed_relief(3)

            # w.enable_effect()
            default = w.outline_width
            w.do_on_enter = lambda: w.set_outline_width(default)
            w.do_on_exit = lambda: w.set_outline_width(0)
            w.set_click_down_sound("click_fade")
            w.set_get_focus_sound("click")

        if isinstance(w, bf.Toggle) or isinstance(w, bf.Slider):
            w.set_spacing(bf.spacing.MAX)
            w.set_alignment(bf.alignment.LEFT)
            w.set_clip_children(False)
            w.set_gap(4)
            if isinstance(w, bf.Slider):
                w.meter.add_constraints(bf.PercentageWidth(0.5))
                w.handle.add_constraints(bf.AspectRatio(0.7,bf.axis.VERTICAL))

                w.handle.set_color(bf.color.DARKER_GB
                ).set_outline_color(bf.color.LIGHTER_GB
                ).set_padding(0)
                w.handle.do_on_enter = lambda: w.handle.set_color(bf.color.LIGHT_GB)
                w.handle.do_on_exit = lambda: w.handle.set_color(bf.color.DARKER_GB)


        if isinstance(w, bf.indicator.ToggleIndicator):
            w.set_color(bf.color.LIGHTER_GB if w.value else bf.color.DARKER_GB)
            w.set_callback(
                lambda value, w=w: w.set_color(
                    bf.color.LIGHTER_GB if value else bf.color.DARKER_GB
                )
            )
            w.set_outline_width(2).set_outline_color(bf.color.DARKER_GB)
            # w.add_constraints(bf.AspectRatio(1,bf.axis.VERTICAL),bf.PercentageHeight(0.5),bf.CenterY())
        if isinstance(w, bf.Meter):
            w.set_padding((3, 4))
            w.content.set_color(bf.color.LIGHTER_GB)
            w.set_outline_color(bf.color.DARKER_GB).set_outline_width(1)