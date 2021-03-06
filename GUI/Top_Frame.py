import wx
from Splitter_Window import Splitter_Window

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# myFrame
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
class Top_Frame( wx.Frame ):
    """ My frame class """
    
    def __init__( self, name ):

        wx.Frame.__init__( self, None, -1,
            name,
            pos = (50,50), size=(1300,600),
            style = wx.DEFAULT_FRAME_STYLE)
        
        self.sp = Splitter_Window( self )
        self.Bind( wx.EVT_TREE_SEL_CHANGED, self.OnNewInstance )
        self.CreateStatusBar( number = 1 )
        self.IndicateCurrentDesign()

    def OnNewInstance( self, event ):
        self.IndicateCurrentDesign()
        event.Skip()

    def IndicateCurrentDesign( self ):
        self.SetStatusText( self.sp.p1.cur_hier_path, 0 )
        self.SetTitle( self.sp.p1.cur_module_ref )   

