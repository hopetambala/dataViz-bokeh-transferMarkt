from queries import *

import numpy as np
import pandas as pd

from bokeh.io import output_file, show
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure

df = pandas_get_teams()
'''
Columns
['Id', 'Name', 'Nickname', 'Squad', 'AverageAge', 'NumberofForeigners', 'TotalMarketValue', 'AverageMarketValue', 'League']
'''
print(df.columns.tolist())

source = ColumnDataSource(df)

p = figure()
p.circle(x='NumberofForeigners', y='TotalMarketValue', 
         source=source, 
         size=10, color='green')

p.title.text = 'Number of Foreign League Players and Total Market Value'
p.xaxis.axis_label = 'NumberofForeigners'
p.yaxis.axis_label = 'TotalMarketValue'

hover = HoverTool()
hover.tooltips=[
    ('Name', '@Name'),
    ('Average Age', '@AverageAge'),
    ('League', '@League')]

p.add_tools(hover)

show(p)