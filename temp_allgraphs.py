from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msgbx
from datetime import date
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from matplotlib.pyplot import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import interactive
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from addnewmodifyscript import classAddNewModifyScript
from testdata import *

class classAllGraphs(Toplevel):
    def __init__(self, master=None, argistestmode=False, argkey='XXXX', argscript='', 
        argmenucalled=False, arggraphid=-1, argoutputtree=None, **kw):
        super().__init__(master=master, **kw)
        
        self.wm_state(newstate='zoomed')
        self.wm_title("Graphs")
        self.key = argkey
        self.script = argscript
        self.bool_test = argistestmode
        self.bool_menucalled = argmenucalled
        self.graphid = arggraphid
        self.output_tree = argoutputtree
        self.pastdate = str(date.today())

        self.wm_protocol("WM_DELETE_WINDOW", self.OnClose)

        self.frame1 = ttk.Frame(self, borderwidth=5, relief="sunken")
        self.frame2 = ttk.Frame(self, borderwidth=5, relief="sunken")

        #search script related widgets
        self.search_symbol_label = ttk.Label(self.frame1, text='*Search Symbol: ')
        self.search_symbol_combo_text = StringVar()
        self.search_symbol_combo = ttk.Combobox(self.frame1, width=60, textvariable=self.search_symbol_combo_text,state='normal')
        self.search_symbol_combo.bind('<Return>', self.commandEnterKey)

        self.btn_search_script = ttk.Button(self.frame1, text="Search Script", command=self.btnSearchScript)
        self.btn_add_script = ttk.Button(self.frame1, text="Add to portfolio", command=self.btnAddScript)

        self.btn_cancel = ttk.Button(self.frame1, text="Close", command=self.OnClose)

        self.graph_select_label = ttk.Label(self.frame1, text='*Select Graph: ')
        self.graph_select_combo_text = StringVar()
        self.graph_select_combo = ttk.Combobox(self.frame1, width=60, textvariable=self.graph_select_combo_text,
                values=['Daily Price', 'Intraday', 'Simple Moving Avg', 'Volume weighted avg price', 
                'Relative Strength Index', 'Avg directional movement index', 'stochastic oscillator',
                'moving average convergence / divergence', 'Aroon', 'Bollinger bands'], state='readonly')
        
        self.graph_select_combo_text.set('Daily Price')
        self.graph_select_combo.current(0)
        self.graph_select_combo.bind('<<ComboboxSelected>>', self.OnGraphSelectionChanged)

        self.btn_show_graph = ttk.Button(self.frame1, text="Show selected graphs", command=self.btnShowGraph)

        self.outputsize_label = ttk.Label(self.frame2, text='Output size: ')
        self.outpusize_combo_text = StringVar()
        self.outputsize_combo = ttk.Combobox(self.frame2, width=10, textvariable=self.outpusize_combo_text, values=['compact', 'full'], state='normal')
        self.outpusize_combo_text.set('compact')
        self.outputsize_combo.current(0)

        self.interval_label = ttk.Label(self.frame2, text='Interval: ')
        self.interval_combo_text = StringVar()
        self.interval_combo = ttk.Combobox(self.frame2, width=10, textvariable=self.interval_combo_text, 
            values=['1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'], state='normal')
        self.interval_combo_text.set('15min')
        self.interval_combo.current(2)

        self.time_period_label = ttk.Label(self.frame2, text='Time period(positive int:10/20): ')
        self.time_period_text = StringVar(10)
        self.time_period_entry = ttk.Entry(self.frame2, textvariable=self.time_period_text, width=3)

        self.series_type_label = ttk.Label(self.frame2, text='Series Type: ')
        self.series_type_combo_text = StringVar()
        self.series_type_combo = ttk.Combobox(self.frame2, width=10, textvariable=self.series_type_combo_text, 
            values=['open', 'high', 'low', 'close'], state='normal')
        self.series_type_combo_text.set('close')
        self.series_type_combo.current(3)

        self.fastkperiod_label = ttk.Label(self.frame2, text='Time period fastk moving avg(positive int): ')
        self.fastkperiod_text = StringVar('5')
        self.fastkperiod_entry = ttk.Entry(self.frame2, textvariable=self.fastkperiod_text, width=3)

        self.slowkperiod_label = ttk.Label(self.frame2, text='Time period slowk moving avg(positive int): ')
        self.slowkperiod_text = StringVar('3')
        self.slowkperiod_entry = ttk.Entry(self.frame2, textvariable=self.slowkperiod_text, width=3)

        self.slowdperiod_label = ttk.Label(self.frame2, text='Time period slowd moving avg(positive int): ')
        self.slowdperiod_text = StringVar('3')
        self.slowdperiod_entry = ttk.Entry(self.frame2, textvariable=self.slowdperiod_text, width=3)

        self.slowkmatype_label = ttk.Label(self.frame2, text='Slowk mov avg: ')
        self.slowkmatype_combo_text = StringVar()
        self.slowkmatype_combo = ttk.Combobox(self.frame2, width=10, textvariable=self.slowkmatype_combo_text, 
            values=['Simple Moving Average (SMA)', 'Exponential Moving Average (EMA)',
                    'Weighted Moving Average (WMA)', 'Double Exponential Moving Average (DEMA)',
                    'Triple Exponential Moving Average (TEMA)', 'Triangular Moving Average (TRIMA)',
                    'T3 Moving Average', 'Kaufman Adaptive Moving Average (KAMA)',
                    'MESA Adaptive Moving Average (MAMA)'], state='normal')
        self.slowkmatype_combo_text.set('Simple Moving Average (SMA)')
        self.slowkmatype_combo.current(0)

        self.slowdmatype_label = ttk.Label(self.frame2, text='Slowd mov avg: ')
        self.slowdmatype_combo_text = StringVar()
        self.slowdmatype_combo = ttk.Combobox(self.frame2, width=10, textvariable=self.slowdmatype_combo_text, 
            values=['Simple Moving Average (SMA)', 'Exponential Moving Average (EMA)',
                    'Weighted Moving Average (WMA)', 'Double Exponential Moving Average (DEMA)',
                    'Triple Exponential Moving Average (TEMA)', 'Triangular Moving Average (TRIMA)',
                    'T3 Moving Average', 'Kaufman Adaptive Moving Average (KAMA)',
                    'MESA Adaptive Moving Average (MAMA)'], state='normal')
        self.slowdmatype_combo_text.set('Simple Moving Average (SMA)')
        self.slowdmatype_combo.current(0)

        self.fastperiod_label = ttk.Label(self.frame2, text='Fast period(positive int): ')
        self.fastperiod_text = StringVar('12')
        self.fastperiod_entry = ttk.Entry(self.frame2, textvariable=self.fastperiod_text, width=3)

        self.slowperiod_label = ttk.Label(self.frame2, text='Slow period(positive int): ')
        self.slowperiod_text = StringVar('26')
        self.slowperiod_entry = ttk.Entry(self.frame2, textvariable=self.slowperiod_text, width=3)

        self.signalperiod_label = ttk.Label(self.frame2, text='Signal period(positive int): ')
        self.signalperiod_text = StringVar('9')
        self.signalperiod_entry = ttk.Entry(self.frame2, textvariable=self.signalperiod_text, width=3)

        self.nbdevup_label = ttk.Label(self.frame2, text=' Standard deviation multiplier of the upper band(positive int): ')
        self.nbdevup_text = StringVar('2')
        self.nbdevup_entry = ttk.Entry(self.frame2, textvariable=self.nbdevup_text, width=3)

        self.nbdevdn_label = ttk.Label(self.frame2, text=' Standard deviation multiplier of the lower band(positive int): ')
        self.nbdevdn_text = StringVar('2')
        self.nbdevdn_entry = ttk.Entry(self.frame2, textvariable=self.nbdevdn_text, width=3)

        self.matype_label = ttk.Label(self.frame2, text='Moving avg type: ')
        self.matype_combo_text = StringVar()
        self.matype_combo = ttk.Combobox(self.frame2, width=10, textvariable=self.matype_combo_text, 
            values=['Simple Moving Average (SMA)', 'Exponential Moving Average (EMA)',
                    'Weighted Moving Average (WMA)', 'Double Exponential Moving Average (DEMA)',
                    'Triple Exponential Moving Average (TEMA)', 'Triangular Moving Average (TRIMA)',
                    'T3 Moving Average', 'Kaufman Adaptive Moving Average (KAMA)',
                    'MESA Adaptive Moving Average (MAMA)'], state='normal')
        self.slowdmatype_combo_text.set('Simple Moving Average (SMA)')
        self.slowdmatype_combo.current(0)

        self.f = Figure(figsize=(12.6,8.55), dpi=100, facecolor='w', edgecolor='k', tight_layout=True, linewidth=0.5)
        self.output_canvas=FigureCanvasTkAgg(self.f, master=self)
        self.toolbar_frame=Frame(master=self)
        self.toolbar = NavigationToolbar2Tk(self.output_canvas, self.toolbar_frame)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame1.grid_configure(row=0, column=0,columnspan=8, rowspan=2, sticky=(N, S, E, W), padx=5, pady=5)
        self.search_symbol_label.grid_configure(row=0, column=0, sticky=(E))
        self.search_symbol_combo.grid_configure(row=0, column=1, sticky=(W))
        self.btn_search_script.grid_configure(row=0, column=2, padx=5, pady=5)
        self.btn_add_script.grid_configure(row=0, column=3, padx=5, pady=5)
        self.graph_select_label.grid_configure(row=0, column=4, sticky=(E))
        self.graph_select_combo.grid_configure(row=0, column=5, sticky=(W))
        self.btn_show_graph.grid_configure(row=0, column=6, padx=5, pady=5)
        self.btn_cancel.grid_configure(row=0, column=7, padx=5, pady=5)

        self.frame2.grid_configure(row=1, column=0,columnspan=8, rowspan=4, sticky=(N, S, E, W), padx=5, pady=5)

        self.output_canvas.get_tk_widget().grid(row=6, column=0, columnspan=17, sticky=(N, E, W, S))
        self.toolbar_frame.grid(row=7, column=0, columnspan=17, rowspan=1, sticky=(N, E, W, S))
        self.toolbar.grid(row=0, column=2, sticky=(N, W))

        if(self.bool_menucalled == False):
            self.wm_title("Graphs - "+ self.script)
            self.search_symbol_combo_text.set(self.script)
            self.search_symbol_combo['values'] = (self.script)
            self.search_symbol_combo.current(0)
            self.search_symbol_combo.configure(state='disabled')
            self.btn_search_script.configure(state='disabled')
            self.graph_select_combo.current(self.graphid)
            self.btn_add_script.configure(state='disabled')


    def OnClose(self):
        self.destroy()

    def commandEnterKey(self, event):
        #self.commandSearchSymbol()
        self.btnSearchScript()

    def btnSearchScript(self):
        try:
            ts = TimeSeries(self.key, output_format='pandas')

            self.searchTuple=ts.get_symbol_search(self.search_symbol_combo.get())
            
            search_values_list = list()
            self.search_symbol_combo['values']=search_values_list
            for i in range(len(self.searchTuple[0].values)):
                search_values_list.append(self.searchTuple[0].values[i][0] + "--" + self.searchTuple[0].values[i][1])

            self.search_symbol_combo['values']=search_values_list
            self.search_symbol_combo.focus_force()
            self.search_symbol_combo.event_generate('<Down>')

        except Exception as e:
            msgbx.showerror("Search Symbol Error", str(e))
            #self.focus_force()
            return

    def btnAddScript(self):
        curr_selection = self.search_symbol_combo.current()
        if(curr_selection >= 0):
            self.script = self.searchTuple[0].values[curr_selection][0]
            dnewscript = dict()
            dnewscript = classAddNewModifyScript(master=self, argisadd=True, argscript=self.script, argkey=self.key).show()
            # returns dictionary - {'Symbol': 'LT.BSE', 'Price': '1000', 'Date': '2020-02-22', 'Quantity': '10', 'Commission': '1', 'Cost': '10001.0'}
            if((dnewscript != None) and (len(dnewscript['Symbol']) >0)):
                stock_name = dnewscript['Symbol']
                listnewscript = list(dnewscript.items())
                self.output_tree.get_stock_quote("", stock_name, listnewscript[1][0] + '=' +listnewscript[1][1],
                                                listnewscript[2][0] + '=' + listnewscript[2][1],
                                                listnewscript[3][0] + '=' + listnewscript[3][1],
                                                listnewscript[4][0] + '=' + listnewscript[4][1],
                                                listnewscript[5][0] + '=' + listnewscript[5][1])
                #dnewscript['Price'], dnewscript['Date'], 
                #   dnewscript['Quantity'], dnewscript['Commission'], dnewscript['Cost'])
            else:
                msgbx.showerror("Add Script", "Error: Values not provided")
        else:
            msgbx.showerror('All Graphs', 'No script selected')
            #self.focus_force()
            return

def btnShowGraph(self):
    return

"""values=['Daily Price', 'Intraday', 'Simple Moving Avg', 'Volume weighted avg price', 
'Relative Strength Index', 'Avg directional movement index', 'stochastic oscillator',
'moving average convergence / divergence', 'Aroon', 'Bollinger bands']"""
def showRespectiveFields(self):
    return    
    """selectedGraph = self.graph_select_combo.current()
    if(selectedGraph == 0):
    elif(selectedGraph == 1):
    elif(selectedGraph == 2):
    elif(selectedGraph == 3):
    elif(selectedGraph == 4):
    elif(selectedGraph == 5):
    elif(selectedGraph == 6):
    elif(selectedGraph == 7):
    elif(selectedGraph == 8):
    elif(selectedGraph == 9):"""

def OnGraphSelectionChanged(self, event):
    
    return