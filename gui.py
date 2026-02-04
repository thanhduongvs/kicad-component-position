# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6-dirty)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

import gettext
_ = gettext.gettext

###########################################################################
## Class ComponentPlacementDialog
###########################################################################

class ComponentPositionDialog ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Component Placement"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        radioOriginChoices = [ _(u"Grid Origin"), _(u"Drill Origin"), _(u"Page Origin") ]
        self.radioOrigin = wx.RadioBox( self, wx.ID_ANY, _(u"Origin:"), wx.DefaultPosition, wx.DefaultSize, radioOriginChoices, 1, wx.RA_SPECIFY_ROWS )
        self.radioOrigin.SetSelection( 0 )
        bSizer1.Add( self.radioOrigin, 0, wx.ALL|wx.EXPAND, 5 )

        radioXAxisChoices = [ _(u"Increases right"), _(u"Increases left") ]
        self.radioXAxis = wx.RadioBox( self, wx.ID_ANY, _(u"X Axis:"), wx.DefaultPosition, wx.DefaultSize, radioXAxisChoices, 1, wx.RA_SPECIFY_ROWS )
        self.radioXAxis.SetSelection( 0 )
        bSizer1.Add( self.radioXAxis, 0, wx.ALL|wx.EXPAND, 5 )

        radioYAxisChoices = [ _(u"Increases up"), _(u"Increases down") ]
        self.radioYAxis = wx.RadioBox( self, wx.ID_ANY, _(u"Y Axis:"), wx.DefaultPosition, wx.DefaultSize, radioYAxisChoices, 1, wx.RA_SPECIFY_ROWS )
        self.radioYAxis.SetSelection( 0 )
        bSizer1.Add( self.radioYAxis, 0, wx.ALL|wx.EXPAND, 5 )

        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"DNP field name:") ), wx.VERTICAL )

        self.checkDNP = wx.CheckBox( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Remove Components with DNP"), wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizer2.Add( self.checkDNP, 0, wx.ALL, 5 )

        self.m_staticText1 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Components with this field not empty will be ignored"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        sbSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )


        bSizer1.Add( sbSizer2, 0, wx.ALL|wx.EXPAND, 5 )

        sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Add custom fields:") ), wx.VERTICAL )

        self.dataFields = wx.dataview.DataViewListCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.dataFields.SetMinSize( wx.Size( -1,200 ) )

        self.columnItem = self.dataFields.AppendTextColumn( _(u"Item"), wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE )
        self.columnAdd = self.dataFields.AppendToggleColumn( _(u"Add"), wx.dataview.DATAVIEW_CELL_ACTIVATABLE, -1, wx.ALIGN_CENTER, wx.dataview.DATAVIEW_COL_SORTABLE )
        self.columnName = self.dataFields.AppendTextColumn( _(u"Name"), wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_SORTABLE )
        sbSizer3.Add( self.dataFields, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer1.Add( sbSizer3, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

        self.buttonCopy = wx.Button( self, wx.ID_ANY, _(u"Copy Log"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer4.Add( self.buttonCopy, 0, wx.ALL, 5 )

        self.buttonClear = wx.Button( self, wx.ID_ANY, _(u"Clear Log"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer4.Add( self.buttonClear, 0, wx.ALL, 5 )


        bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.buttonGenerate = wx.Button( self, wx.ID_ANY, _(u"Generate File"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer4.Add( self.buttonGenerate, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer4, 0, wx.ALL|wx.EXPAND, 5 )

        sbSizer31 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Logs:") ), wx.HORIZONTAL )

        self.textLog = wx.TextCtrl( sbSizer31.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY )
        self.textLog.SetMinSize( wx.Size( -1,100 ) )

        sbSizer31.Add( self.textLog, 1, wx.ALL, 5 )


        bSizer1.Add( sbSizer31, 0, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()
        bSizer1.Fit( self )

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.OnClose )
        self.buttonCopy.Bind( wx.EVT_BUTTON, self.OnCopy )
        self.buttonClear.Bind( wx.EVT_BUTTON, self.OnClear )
        self.buttonGenerate.Bind( wx.EVT_BUTTON, self.OnGenerate )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnClose( self, event ):
        event.Skip()

    def OnCopy( self, event ):
        event.Skip()

    def OnClear( self, event ):
        event.Skip()

    def OnGenerate( self, event ):
        event.Skip()

