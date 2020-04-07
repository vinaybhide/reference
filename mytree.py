from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext as tkst
from tkinter import messagebox as msgbx
from tkinter.filedialog import *

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import pandas as pd
from pandas import DataFrame
from matplotlib.pyplot import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import interactive
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import warnings
from datetime import date


root = Tk()
tree = ttk.Treeview(root)

tree.grid(row=1, column=0, rowspan=1, columnspan=11)

dfstockname = DataFrame()
dfstockname = pd.read_csv("E:\\python_projects\\TestData\\global_quote.csv")
dfstockname.insert(1, 'Purchase Price', "123.12")
dfstockname.insert(2, 'Purchase Date', "2020-01-01")

tree['columns']=list(dfstockname.columns[0:12])
tree.column("#0", width=100, anchor='center')
tree.heading("#0", text='Script', anchor='center')
for each_column in list(dfstockname.columns[0:12]):
    column_str = str(each_column)
    column_str = column_str[4:]
    tree.column(str(each_column), width=100, anchor='center')
    tree.heading(str(each_column), text=str(each_column), anchor='center')



