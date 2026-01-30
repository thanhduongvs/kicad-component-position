#!/usr/bin/env python

import wx
from component_position import ComponentPosition

def main():
    app = wx.App()
    plugin = ComponentPosition()
    plugin.ShowModal()
    plugin.Destroy()

if __name__ == "__main__":
    main()
