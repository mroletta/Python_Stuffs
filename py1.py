import wx
from PIL import Image
import math
import numpy
import pylab
import os
import fnmatch


class Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.quote = wx.StaticText(self, label="EL Image and Grayscale Analyzer", pos=(20, 30))

        self.selected_image = wx.GenericDirCtrl(self, -1, size=(250,225), pos=(20, 50), style=wx.DIRCTRL_SHOW_FILTERS, filter="JPG files (*.jpg)|*.jpg")
        selected_image = self.selected_image.GetTreeCtrl()
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnDoubleClick, selected_image)


    def OnDoubleClick(self, event):
        self.MaxImageSize_x = 235
        self.MaxImageSize_y = 500
        self.Image = wx.StaticBitmap(self, bitmap=wx.EmptyBitmap(self.MaxImageSize_x, self.MaxImageSize_y), pos=(300,50))
        #self.Image = wx.StaticBitmap(self, bitmap=wx.EmptyBitmap(1, 1), pos=(300,50))
        
        self.jpg = self.selected_image.GetFilePath()
        
        if(self.jpg):
            Img = wx.Image(self.jpg, wx.BITMAP_TYPE_JPEG)
            W = Img.GetWidth()
            H = Img.GetHeight()
            if H > W:
                NewW = self.MaxImageSize_x
                NewH = self.MaxImageSize_y * H / W
            else:
                NewH = self.MaxImageSize_y
                NewW = self.MaxImageSize_x * W / H  
            Img = Img.Scale(NewW, NewH)


            self.Image.SetBitmap(wx.BitmapFromImage(Img))
         




        #self.MaxImageSize=800
       # 
       # filepath = self.selected_image.GetFilePath()
       # print filepath
       # if(filepath):
       #     
       #     jpg1 = wx.Image(filepath, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
       #     # bitmap upper left corner is in the position tuple (x, y) = (5, 5)
       #     wx.StaticBitmap(self, -1, jpg1, (10 + jpg1.GetWidth(), 5), (jpg1.GetWidth(), jpg1.GetHeight()))
        
           
        
        event.Skip()


    def loljpgs(self, imagepath):
    #shit here make this thingy take the path and display a jpg

        pass

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
        
    
app = wx.App(False)
frame = wx.Frame(None, size=(1000,800))
panel = Panel(frame)
frame.Show()
app.MainLoop()