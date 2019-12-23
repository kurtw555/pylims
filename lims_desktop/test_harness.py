import numpy as np
import pandas as pd

import wx
import wx.grid as gridlib
import wx.lib.inspection

EVEN_ROW_COLOUR = '#CCE6FF'
GRID_LINE_COLOUR = '#ccc'

class DataTable(wx.grid.GridTableBase):
    def __init__(self, data=None):
        wx.grid.GridTableBase.__init__(self)
        self.headerRows = 1
        if data is None:
            data = pd.DataFrame()
        self.data = data

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data.columns) + 1

    def GetValue(self, row, col):
        if col == 0:
            return self.data.index[row]
        return self.data.iloc[row, col - 1]

    def SetValue(self, row, col, value):
        self.data.iloc[row, col - 1] = value

    def GetColLabelValue(self, col):
        if col == 0:
            if self.data.index.name is None:
                return 'Index'
            else:
                return self.data.index.name
        return str(self.data.columns[col - 1])

    def GetTypeName(self, row, col):
        return wx.grid.GRID_VALUE_STRING

    def GetAttr(self, row, col, prop):
        attr = wx.grid.GridCellAttr()
        if row % 2 == 1:
            attr.SetBackgroundColour(EVEN_ROW_COLOUR)
        return attr

class DataGrid(gridlib.Grid):
    def __init__(self, parent, size=wx.Size(1000, 500)):
        self.parent = parent
        gridlib.Grid.__init__(self, self.parent, -1)
        self.SetGridLineColour(GRID_LINE_COLOUR)
        self.SetRowLabelSize(0)
        self.SetColLabelSize(30)
        self.table = DataTable()        


class LIMS(wx.Frame):

    def __init__(self, parent, title):
        super(LIMS, self).__init__(parent, title=title, size=wx.Size(1025, 650))

        self.data = None
        self.gbs = None
        self.grid = None
        self.InitUI()
        self.Layout()
        self.Centre()
        self.Show()
        
        

    def create_grid(self, panel, data):
        table = DataTable(data)
        grid = DataGrid(panel)
        grid.CreateGrid(len(data), len(data.columns))
        grid.SetTable(table)
        grid.AutoSize()
        grid.AutoSizeColumns(True)
        return grid


    def InitUI(self):

        #self.SetSize(wx.Size(500, 500))        

        panel = wx.Panel(self)        
        #self.data_grid = self.create_grid(panel, self.data)

        hbox = wx.BoxSizer(wx.HORIZONTAL)        

        #fgs = wx.FlexGridSizer(5, 5, 9, 35)
        gbs = wx.GridBagSizer(9, 30)        
        self.gbs = gbs
        
        stat_txt1 = wx.StaticText(panel, label='')
        stat_txt2 = wx.StaticText(panel, label='')
        stat_txt3 = wx.StaticText(panel, label='')
        stat_txt3b = wx.StaticText(panel, label='')
        stat_txt4 = wx.StaticText(panel, label='')
        stat_txt4b = wx.StaticText(panel, label='')
        #stat_txt5 = wx.StaticText(panel, label='')        

        #Row 1
        lbl_processor = wx.StaticText(panel, label="Processor")
        tc_proc = wx.TextCtrl(panel, wx.EXPAND)
        gbs.Add(lbl_processor, pos=(0,0),flag=wx.EXPAND)
        gbs.Add(tc_proc, pos=(0,1),flag=wx.EXPAND)

        gbs.Add(stat_txt1, pos=(0,2),flag=wx.EXPAND)

        lbl_id = wx.StaticText(panel, label="ID:")
        tc_id = wx.TextCtrl(panel, wx.EXPAND)
        gbs.Add(lbl_id, pos=(0,3),flag=wx.EXPAND)
        gbs.Add(tc_id, pos=(0,4),flag=wx.EXPAND)
        

        #Row 2
        lbl_input = wx.StaticText(panel, label="Input File")
        tc_input = wx.TextCtrl(panel)
        gbs.Add(lbl_input, pos=(1,0),flag=wx.EXPAND)
        gbs.Add(tc_input, pos=(1,1),flag=wx.EXPAND)

        gbs.Add(stat_txt2, pos=(1,2),flag=wx.EXPAND)

        lbl_name = wx.StaticText(panel, label="Name:")
        tc_name = wx.TextCtrl(panel)
        gbs.Add(lbl_name, pos=(1,3),flag=wx.EXPAND)
        gbs.Add(tc_name, pos=(1,4),flag=wx.EXPAND)


        #Row 3
        gbs.Add(stat_txt3, pos=(2,0),flag=wx.EXPAND)
        btn_run = wx.Button(panel, wx.ID_ANY, 'Run')
        self.Bind(wx.EVT_BUTTON, self.on_run, btn_run)
        gbs.Add(btn_run, pos=(2,1),flag=wx.EXPAND)

        gbs.Add(stat_txt3b, pos=(2,2),flag=wx.EXPAND)

        lbl_desc = wx.StaticText(panel, label="Description:")
        tc_desc = wx.TextCtrl(panel)
        gbs.Add(lbl_desc, pos=(2,3),flag=wx.EXPAND)
        gbs.Add(tc_desc, pos=(2,4),flag=wx.EXPAND)

        #Row 4
        gbs.Add(stat_txt4, pos=(3,0),flag=wx.EXPAND)
        btn_save = wx.Button(panel, wx.ID_ANY, 'Save')
        self.Bind(wx.EVT_BUTTON, self.on_save, btn_save)        
        gbs.Add(btn_save, pos=(3,1),flag=wx.EXPAND)

        gbs.Add(stat_txt4b, pos=(3,2),flag=wx.EXPAND)        

        lbl_file_type = wx.StaticText(panel, label="File Type:")
        tc_file_type = wx.TextCtrl(panel)
        gbs.Add(lbl_file_type, pos=(3,3),flag=wx.EXPAND)
        gbs.Add(tc_file_type, pos=(3,4),flag=wx.EXPAND)

        #df = pd.DataFrame(np.random.random((10, 5)))
        #table = DataTable(df)

        
        self.grid = wx.grid.Grid(panel, -1, size= wx.Size(900, 400))                
        
        gbs.Add(self.grid, pos=(4,0), span = (1, 5), flag= wx.SYS_VSCROLL_X | wx.SYS_HSCROLL_Y)        

        hbox.Add(gbs, proportion=1, flag=wx.ALL, border=15)        
        panel.SetSizer(hbox)        
        
        self.CreateStatusBar()
        self.SetStatusText("")        
        

    def on_run(self, event):
        # Do something
        print('onOK handler')
        #item = self.gbs.FindItemAtPosition((4,0))
        #if self.grid != None:
        #    self.gbs.Hide(self.grid)            
        
        df = pd.DataFrame(np.random.random((100, 10)))
        table = DataTable(df)

        #self.grid = wx.grid.Grid(self, -1)
        self.grid.SetTable(table, takeOwnership=True)
        self.grid.AutoSizeColumns()

        #self.gbs.Add(self.grid, pos=(4,0), span = (1, 5), flag=wx.EXPAND)
        self.gbs.Layout()
        self.Layout()
 
    def on_save(self, event):
        ival = 1

def main():
    
    app = wx.App()
    ex = LIMS(None, title='Laboratory Information Management System')
    ex.Show()    
    wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()


if __name__ == '__main__':
    main()