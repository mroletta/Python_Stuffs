import wx
from PIL import Image
import math
import numpy
import pylab
import os


class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.quote = wx.StaticText(self, label="EL Image and Grayscale Analyzer", pos=(20, 30))

        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        self.listbox = wx.ListBox(self, pos=(300,20), size=(200,300))

        # A button
        self.button = wx.Button(self, label="Save", pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)

   
       
    #Luminance conversion formula from http://en.wikipedia.org/wiki/Luminance_(relative)
    def luminosity(rgb, rcoeff=0.2126, gcoeff=0.7152, bcoeff=0.0722):
        return rcoeff*rgb[0]+gcoeff*rgb[1]+bcoeff*rgb[2]

    # Take a PIL rgb image and produce a factory that yields
    # ((x,y), r,g,b)), where (x,y) are the coordinates
    # of a pixel, (x,y), and its RGB values. 
    def gen_pix_factory(im):
        num_cols, num_rows = im.size
        r,c = 0,0
        while r != num_rows:
            c = c % num_cols
            yield ((c,r), im.getpixel((c,r)))
            if c  == num_cols - 1: r += 1
            c += 1

    # take a PIL RGB image and a luminosity conversion formula,
    # and return a new gray level PIL image in which each pixel
    # is obtained by applying the luminosity formula to the
    # corresponding pixel in the RGB values.
    def rgb_to_gray_level(rgb_img, conversion = luminosity):
        gl_img = Image.new('L', rgb_img.size)
        gen_pix = gen_pix_factory(im)
        lum_pix = ((gp[0], conversion(gp[1])) for gp in gen_pix)
        for lp in lum_pix:
            gl_img.putpixel(lp[0], int(lp[1]))
        return gl_img

    # Take a gray level image and a gray level threshold and
    # replace a pixel's gray level with 0 (black) if it's gray
    # level value is <= than the threshold and with 
    # 255 (white) if it's > than the threshold.
    def binarize(gl_img, thresh=140):
        gen_pix = gen_pix_factory(gl_img)
        for pix in gen_pix:
            if pix[1] <= thresh:
                gl_img.putpixel(pix[0],0)
            else:
                gl_img.putpixel(pix[0], 255)

    # Take a binarized image and count every pixel that is black
    def pixel_counter(binarized_image, black = 0):
        gen_pix = gen_pix_factory(binarized_image)
        count = 0
        for pix in gen_pix:
            if pix[1] == black:
                count = count + 1
        return count

    # Calculates and returns a list from the vertical grayscale (row average) values.
    def vertical_grayscale(gl_img):
        gen_pix = gen_pix_factory(gl_img)
        vert_list = []
        avg = 0
        row = 0
        num_cols, num_rows = gl_img.size
        # print gl_img.size
        for pix in gen_pix:
            x,y = pix[0]
            if y == row:
                avg += pix[1]
            else:
                avg = avg / num_rows
                vert_list.append(avg)
                avg = 0 
                row +=1
        return vert_list

    def OnOpen(self,e):
        """Open a file"""
        self.dirname=''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.jpeg", wx.OPEN)
        if dlg.ShowModel() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()



    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
    def OnClick(self,event):
        self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())



app = wx.App(False)
frame = wx.Frame(None)
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()