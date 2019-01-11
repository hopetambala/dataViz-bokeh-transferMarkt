from queries import *

import numpy as np
import pandas as pd

from bokeh.io import output_file, show
from bokeh.models import HoverTool, ColumnDataSource, LogColorMapper, ColorBar, LogTicker, LabelSet
from bokeh.plotting import figure
from bokeh.palettes import Accent8

def scatter_foreigners_totalMarketValue():
    df = pandas_get_teams()
    '''
    Columns
    ['Id', 'Name', 'Nickname', 'Squad', 'AverageAge', 'NumberofForeigners', 'TotalMarketValue', 'AverageMarketValue', 'League']
    '''    

    palette = ["#053061", "#2166ac", "#4393c3", "#92c5de", "#d1e5f0",
           "#f7f7f7", "#fddbc7", "#f4a582", "#d6604d", "#b2182b", "#67001f"]
    AverageAge = df["AverageAge"]
    low = min(AverageAge)
    high = max(AverageAge)
    AverageAge_inds = [int(10*(x-low)/(high-low)) for x in AverageAge] #gives items in colors a value from 0-10
    

    df['age_colors'] = [palette[i] for i in AverageAge_inds]
    
    color_mapper = LogColorMapper(palette=palette, low=low, high=high)

    
    source = ColumnDataSource(df)

    #Create Figure
    p = figure(width=900)

    #Configure Circles
    p.circle(x='TotalMarketValue', y='NumberofForeigners', 
            source=source, 
            size=10, color='age_colors',line_color="black", fill_alpha=0.8)
    
    #Configure Labes
    '''
    labels = LabelSet(x="NumberofForeigners", y="TotalMarketValue", text="Nickname", y_offset=8,
                  text_font_size="8pt", text_color="#555555",
                  source=source, text_align='center')
    p.add_layout(labels)
    '''

    #Configure Color of Average Ages
    color_bar = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),label_standoff=12, border_line_color=None, location=(0,0))
    p.add_layout(color_bar, 'right')

    #Configure Graph Titles and Axises
    p.title.text = 'Number of Foreign League Players and Total Market Value (Colored By Average Age)'
    p.xaxis.axis_label = 'Total Market Value'
    p.yaxis.axis_label = 'Number of Foreign Players Per Squad'

    #Hover Tools
    hover = HoverTool()
    hover.tooltips=[
        ('Name', '@Name'),
        ('Average Age', '@AverageAge'),
        ('Number of Foreign Players', '@NumberofForeigners'),
        ('League', '@League')]

    p.add_tools(hover)

    output_file("graphs/scatterPlot.html")

    show(p)

scatter_foreigners_totalMarketValue()