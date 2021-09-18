# Raw Package
import numpy as np
import pandas as pd

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go

from music import MakeSound

# Get Bitcoin data
data = yf.download(tickers='BTC-USD', period = '22h', interval = '15m')

# Make sound
maker = MakeSound()
sound_schedules = maker.create_sound_timing(data)
maker.create_music(sound_schedules, 'test')


play_button = {
    "args": [
        None, 
        {
            "frame": {"duration": 300, "redraw": True},
            "fromcurrent": True, 
            "transition": {"duration": 100,"easing": "quadratic-in-out"}
        }
    ],
    "label": "Play",
    "method": "animate"
}

pause_button = {
    "args": [
        [None], 
        {
            "frame": {"duration": 0, "redraw": False},
            "mode": "immediate",
            "transition": {"duration": 0}
        }
    ],
    "label": "Pause",
    "method": "animate"
}

sliders_steps = [
    {"args": [
        [0, i], # 0, in order to reset the image, i in order to plot frame i
        {"frame": {"duration": 300, "redraw": True},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
    "label": i,
    "method": "animate"}
    for i in range(len(data))      
]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "data:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": sliders_steps,
}

initial_plot = go.Candlestick(
    x=data.index, 
    open=data.Open, 
    high=data.High, 
    low=data.Low, 
    close=data.Close
)

first_i_candles = lambda i: go.Candlestick(
    x=data.index, 
    open=data.Open[:i], 
    high=data.High[:i], 
    low=data.Low[:i], 
    close=data.Close[:i]
)

fig = go.Figure(
    data=[initial_plot],
    layout=go.Layout(
        xaxis=dict(title='Date', rangeslider=dict(visible=False)),
        title="Candles over time",
        updatemenus= [dict(type="buttons", buttons=[play_button, pause_button])],
        sliders = [sliders_dict]
    ),
    frames=[
        go.Frame(data=[first_i_candles(i)], name=f"{i}") # name, I imagine, is used to bind to frame i :) 
        for i in range(len(data))
    ]
)

fig.show()
