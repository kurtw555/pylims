import numpy as np
import pandas as pd
import ntpath

import wx
import wx.grid as gridlib
#import wx.lib.inspection

from lims.plugins.plugin_collection import PluginCollection

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
        self.tc_input = None
        self.tc_id = None
        self.tc_name = None
        self.tc_desc = None
        self.tc_file_type = None
        self.cb_proc = None
        self.processors = {}
        self.processor_names = []

        self.get_processors()
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

    def get_processors(self):
        plugins = PluginCollection('lims.processors')
        for proc in plugins.plugins:
            self.processors[proc.name] = proc
            self.processor_names.append(proc.name)


    def InitUI(self):

        #self.SetSize(wx.Size(500, 500))        
        processors = ["AAAA", "BBBB", "CCCC"]

        panel = wx.Panel(self, name="MainPanel")
        #self.data_grid = self.create_grid(panel, self.data)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        #fgs = wx.FlexGridSizer(5, 5, 9, 35)
        gbs = wx.GridBagSizer(9, 30)
        self.gbs = gbs
        
        stat_txt1 = wx.StaticText(panel, label='')
        #stat_txt2 = wx.StaticText(panel, label='')
        stat_txt3 = wx.StaticText(panel, label='')
        stat_txt3b = wx.StaticText(panel, label='')
        stat_txt4 = wx.StaticText(panel, label='')
        stat_txt4b = wx.StaticText(panel, label='')
        #stat_txt5 = wx.StaticText(panel, label='')        

        #Row 1
        lbl_processor = wx.StaticText(panel, label="Processor")
        #tc_proc = wx.TextCtrl(panel, wx.EXPAND)
        self.cb_proc = wx.Choice(panel, wx.EXPAND, choices = self.processor_names)
        self.Bind(wx.EVT_CHOICE , self.on_select_combo, self.cb_proc)
        gbs.Add(lbl_processor, pos=(0,0),flag=wx.EXPAND)
        #gbs.Add(tc_proc, pos=(0,1),flag=wx.EXPAND)
        gbs.Add(self.cb_proc, pos=(0,1),flag=wx.EXPAND)

        gbs.Add(stat_txt1, pos=(0,2),flag=wx.EXPAND)

        lbl_id = wx.StaticText(panel, label="ID:")
        self.tc_id = wx.TextCtrl(panel, wx.EXPAND)
        self.tc_id.SetEditable(False)
        gbs.Add(lbl_id, pos=(0,3),flag=wx.EXPAND)
        gbs.Add(self.tc_id, pos=(0,4),flag=wx.EXPAND)
        

        #Row 2
        lbl_input = wx.StaticText(panel, label="Input File")
        self.tc_input = wx.TextCtrl(panel)
        btn_select_file = wx.Button(panel, wx.ID_ANY, '...')
        gbs.Add(lbl_input, pos=(1,0),flag=wx.EXPAND)
        gbs.Add(self.tc_input, pos=(1,1),flag=wx.EXPAND)

        #gbs.Add(stat_txt2, pos=(1,2),flag=wx.EXPAND)
        gbs.Add(btn_select_file, pos=(1,2),flag=wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.on_select_file, btn_select_file)

        lbl_name = wx.StaticText(panel, label="Name:")
        self.tc_name = wx.TextCtrl(panel)
        self.tc_name.SetEditable(False)
        gbs.Add(lbl_name, pos=(1,3),flag=wx.EXPAND)
        gbs.Add(self.tc_name, pos=(1,4),flag=wx.EXPAND)


        #Row 3
        gbs.Add(stat_txt3, pos=(2,0),flag=wx.EXPAND)
        btn_run = wx.Button(panel, wx.ID_ANY, 'Run')
        self.Bind(wx.EVT_BUTTON, self.on_run, btn_run)
        gbs.Add(btn_run, pos=(2,1),flag=wx.EXPAND)

        gbs.Add(stat_txt3b, pos=(2,2),flag=wx.EXPAND)

        lbl_desc = wx.StaticText(panel, label="Description:")
        self.tc_desc = wx.TextCtrl(panel)
        self.tc_desc.SetEditable(False)
        gbs.Add(lbl_desc, pos=(2,3),flag=wx.EXPAND)
        gbs.Add(self.tc_desc, pos=(2,4),flag=wx.EXPAND)

        #Row 4
        gbs.Add(stat_txt4, pos=(3,0),flag=wx.EXPAND)
        btn_save = wx.Button(panel, wx.ID_ANY, 'Save')
        self.Bind(wx.EVT_BUTTON, self.on_save, btn_save)        
        gbs.Add(btn_save, pos=(3,1),flag=wx.EXPAND)

        gbs.Add(stat_txt4b, pos=(3,2),flag=wx.EXPAND)        

        lbl_file_type = wx.StaticText(panel, label="File Type:")
        self.tc_file_type = wx.TextCtrl(panel)
        self.tc_file_type.SetEditable(False)
        gbs.Add(lbl_file_type, pos=(3,3),flag=wx.EXPAND)
        gbs.Add(self.tc_file_type, pos=(3,4),flag=wx.EXPAND)
        
        self.grid = wx.grid.Grid(panel, -1, size= wx.Size(900, 400), name="DataGrid")                
        
        gbs.Add(self.grid, pos=(4,0), span = (1, 5), flag= wx.SYS_VSCROLL_X | wx.SYS_HSCROLL_Y)        

        #hbox.Add(gbs, proportion=1, flag=wx.ALL, border=15)        
        #panel.SetSizer(hbox)        
        
        self.CreateStatusBar()
        self.SetStatusText("")

        self.set_empty_table()
        
    def on_select_file(self, event):
        with wx.FileDialog(self, "Select instrument file", wildcard="All file (*.*)|*.*",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            file_name = ntpath.basename(pathname)
            self.tc_input.SetValue(file_name)

    def on_select_combo(self, event):
        print("Combobox handler")
        idx = self.cb_proc.GetSelection()
        proc_name = self.cb_proc.GetString(idx)
        print("Processor: " + proc_name)
        if self.processors is not None:
            for proc in self.processors.plugins:
                if proc.name == proc_name:
                    self.tc_name.SetValue(proc.name)                    
                    self.tc_desc.SetValue(proc.description)                    
                    self.tc_file_type.SetValue(proc.file_type)                    


    def on_run(self, event):
        
        idx = self.cb_proc.GetSelection()
        proc_name = self.cb_proc.GetString(idx)
        if proc_name == '':
            return
        if self.processors is not None:
            proc = self.processors[proc_name]
            proc.execute()

        print('onOK handler')
        #item = self.gbs.FindItemAtPosition((4,0))
        #if self.grid != None:
        #    self.gbs.Hide(self.grid)            
        
        df = pd.DataFrame(np.random.random((100, 10)))
        table = DataTable(df)

        
        self.grid.SetTable(table, takeOwnership=True)
        self.grid.AutoSizeColumns()
        
        self.gbs.Layout()
        self.Layout()
 
    def on_save(self, event):        
        ival = 1

    def set_empty_table(self):
        data = {'Aliquot':[''],
            	'Analyte Identifier':[''],
                'Measured Value':[''],
                'Units':[''],
                'Dilution Factor':[''],
                'Analysis Date/Time':[''],
                'Comment':[''],
                'Description':[''],
                'User Defined 1':[''],
                'User Defined 2':[''],
                'User Defined 3':[''],
                'User Defined 4':[''],
                'User Defined 5':[''],
                'User Defined 6':[''],
                'User Defined 7':[''],
                'User Defined 8':[''],
                'User Defined 9':[''],
                'User Defined 10':[''],
                'User Defined 11':[''],
                'User Defined 12':[''],
                'User Defined 13':[''],
                'User Defined 14':[''],
                'User Defined 15':[''],
                'User Defined 16':[''],
                'User Defined 17':[''],
                'User Defined 18':[''],
                'User Defined 19':[''],
                'User Defined 20':['']
        }
        df = pd.DataFrame(data)
        table = DataTable(df)
        self.grid.SetTable(table, takeOwnership=True)
        self.grid.AutoSizeColumns()
        
        self.gbs.Layout()
        self.Layout()
        return table
                

def main():
    
    app = wx.App()
    ex = LIMS(None, title='Laboratory Information Management System')
    ex.Show()    
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()


if __name__ == '__main__':
    main()