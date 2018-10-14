import wx
import wx.grid as gridlib

__author__ = 'darkzena'

import wx, sys, os

from Lib import GCode

'''

'''

class Frame(wx.Frame):
    def __init__(self, title, fileGCode = "" ):
        wx.Frame.__init__(self, None, title=title) # , size=(800, 200)
        self.Center()
        self.panel = wx.Panel(self)

        # Get the file
        if not fileGCode:
            wildcard = "All (*.*)|*.*"
            dlg = wx.FileDialog(self, "Select GCode file", "", "", wildcard, wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_CANCEL:
                return     # the user changed idea...
            fileGCode = dlg.GetPath()

        # Get info GCode
        gcode = GCode(open(fileGCode, "rU"))

        xdims = (gcode.xmin, gcode.xmax, gcode.width)
        ydims = (gcode.ymin, gcode.ymax, gcode.depth)
        zdims = (gcode.zmin, gcode.zmax, gcode.height)
        self.filamenUse = gcode.filament_length
        layersN =  gcode.layers_count
        estimateTime =  gcode.estimate_duration()[1]

        self.gcodeTitle = wx.StaticText(self.panel, label="GCode Info")
        self.gcodeFileName = wx.StaticText(self.panel, label="FileName:")
        self.gcodeFileNameV = wx.StaticText(self.panel, label=fileGCode)
        self.gcodeX = wx.StaticText(self.panel, label="Dimension X:")
        self.gcodeXV =wx.StaticText(self.panel, label= ("Min %0.02f - Max %0.02f (%0.02f)" % xdims))
        self.gcodeY = wx.StaticText(self.panel, label="Dimension Y:")
        self.gcodeYV =wx.StaticText(self.panel, label= ("Min %0.02f - Max %0.02f (%0.02f)" % ydims))
        self.gcodeZ = wx.StaticText(self.panel, label="Dimension Z:")
        self.gcodeZV =wx.StaticText(self.panel, label= ("Min %0.02f - Max %0.02f (%0.02f)" % zdims))
        self.gcodeFilUse = wx.StaticText(self.panel, label="Filament used:")
        self.gcodeFilUseV = wx.StaticText(self.panel, label=("%0.02f mm - %0.02f cm" % (self.filamenUse, self.filamenUse/100)))
        self.gcodeLayers = wx.StaticText(self.panel, label="Number of layers:")
        self.gcodeLayersV = wx.StaticText(self.panel, label=(" %d" % layersN))
        self.gcodeTime = wx.StaticText(self.panel, label="Estimate Time")
        self.gcodeTimeV = wx.StaticText(self.panel, label=("%s" % estimateTime))

        # price calculate
        self.priceLabel = wx.StaticText(self.panel, label="Price Eur/1Kg")
        self.priceLabelObj = wx.StaticText(self.panel, label="Price Object")
        self.priceCtr = wx.TextCtrl(self.panel, style=wx.TE_RIGHT)
        self.priceObject = wx.StaticText(self.panel, label="")
        self.priceObject.SetForegroundColour(wx.RED)

        # Buttons
        self.btQuit = wx.Button(self.panel, label='Close', size=(70, 30))
        self.btPrice = wx.Button(self.panel, label='Price Calculate', size=(200, 30))

        # Set sizer for the frame, so we can change frame size to match widgets
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)

        # Set sizer for the panel content
        self.sizer = wx.GridBagSizer(12, 4)
        self.sizer.Add(self.gcodeTitle, pos=(0,0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=3)

        self.sizer.Add(self.gcodeFileName,  (1, 0))
        self.sizer.Add(self.gcodeFileNameV, (1, 2))
        self.sizer.Add(self.gcodeX,         (2, 0))
        self.sizer.Add(self.gcodeXV,        (2, 2))
        self.sizer.Add(self.gcodeY,         (3, 0))
        self.sizer.Add(self.gcodeYV,        (3, 2))
        self.sizer.Add(self.gcodeZ,         (4, 0))
        self.sizer.Add(self.gcodeZV,        (4, 2))
        self.sizer.Add(self.gcodeFilUse,    (5, 0))
        self.sizer.Add(self.gcodeFilUseV,   (5, 2))
        self.sizer.Add(self.gcodeLayers,    (6, 0))
        self.sizer.Add(self.gcodeLayersV,   (6, 2))
        self.sizer.Add(self.gcodeTime,      (7, 0))
        self.sizer.Add(self.gcodeTimeV,     (7, 2))
        # Price
        self.sizer.Add(self.priceLabel,     (9,  0))
        self.sizer.Add(self.priceCtr,       (9,  1))
        self.sizer.Add(self.btPrice,        (9,  2))

        self.sizer.Add(self.priceLabelObj,  (10, 0))
        self.sizer.Add(self.priceObject,    (10, 1))

        # Quit
        self.sizer.Add(self.btQuit,     (11, 3))

        #self.sizer.Add(self.button, (2, 0), (1, 2), flag=wx.EXPAND)

        # Set simple sizer for a nice border
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)

        # Use the sizers
        self.panel.SetSizerAndFit(self.border)
        self.SetSizerAndFit(self.windowSizer)

        # Set event handlers
        self.btQuit.Bind(wx.EVT_BUTTON,  self.OnQuit)
        self.btPrice.Bind(wx.EVT_BUTTON,  self.OnPrice)

    def OnPrice(self, e):
        val = self.priceCtr.GetValue()
        cost = float(val)

        densityABS = 0.00105
        densityPLA = 0.00125

        # Extruder Diameter mm
        diameter = 1.75
        # Calculate the area of the end of the filament
        radius = diameter / 2
        area = radius * radius * 3.1415926535897932384626433832795
        # Multiply the area times the length of filament to determine the area a cylinder of material,
        # and then multiply times the density to get the total weight of the object
        weightObject = (area * self.filamenUse * densityPLA)
        #Calculate the cost of the item
        price = (cost / 1000) * weightObject
        self.priceObject.SetLabel("%0.02f Euro" % price)

    def OnQuit(self, e):
        self.Close()


# Main app
app = wx.App()

if len(sys.argv) > 1:
    top = Frame("GCode info", open(sys.argv[1]))
else:
    top = Frame("GCode info")

top.Show()
app.MainLoop()