# Some cairo magic, thanks goes to Michael Urman for tutorials

import gtk
import cairo
import os


class DrawingArea(gtk.DrawingArea):
    __gsignals__ = {"expose-event": "override"}

    def do_expose_event(self, event):
        cr = self.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        cr.clip()

        self.draw(cr, *self.window.get_size())


class Pad(DrawingArea):
    def set_parameters(self, tablet=None):
        self.tablet = tablet
        if self.tablet:
            self.button_map = self.tablet.Buttons
            self.image = "images/pad/" + self.tablet.Model + ".png"
            try:
                os.stat(self.image)
            except:
                print ("No image for %s pad" % self.tablet.Model)
                self.image = ""

        else:
            self.button_map = []
            self.image = ""

    def draw(self, cr, width, height):
        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        if self.image:
            # Draw background image
            cr.set_source_surface(cairo.ImageSurface.create_from_png(self.image))
            cr.paint()

        if self.button_map:
            # Paint on buttons
            cr.select_font_face("Sans",cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(18)

            for button in self.button_map:
                cr.set_source_rgba(1,1,1,1)
                choffset = len(str(button.Number)) * 6
                cr.move_to(int((button.X1+button.X2)/2)-choffset,int((button.Y1+button.Y2)/2)+6)
                cr.show_text (str(button.Number))
                cr.set_source_rgba(1.0, 1.0, 1.0,0.4)
                cr.rectangle(button.X1, button.Y1, button.X2-button.X1, button.Y2-button.Y1)
                cr.stroke()
        else:
            cr.select_font_face("Sans",cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(10)
            cr.set_source_rgba(1,1,1,1)
            cr.move_to(0,16)
            cr.show_text ("No preview available for this model.")




