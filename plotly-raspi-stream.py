import plotly.plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout, Figure, Data, Stream, YAxis
import time
import readadc
from datetime import datetime
import board
import busio
import time
import os
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c, gain=2/3)
chan1 = AnalogIn(ads, ADS.P1)
chan0 = AnalogIn(ads, ADS.P0)

#temphead = (chan1.voltage - 1.25) / 0.005

username = 'Toto'
api_key = ''
stream_token_temp = ''
stream_token_pressure = ''

py.sign_in(username, api_key)

trace1 = Scatter(
    x=[],
    y=[],
    name='Brew Temp',
    stream=dict(
        token=stream_token_temp,
        maxpoints=10000
    )
)
trace2 = go.Scatter(
    x=[],
    y=[],
    name='Brew pressure',
    stream=dict(
        token=stream_token_pressure,
        maxpoints=10000
    ),
    yaxis='y2'
)
#layout = Layout(
#    title='Oscar'
#)

layout = go.Layout(
    title='Oscar',
    yaxis=dict(
        title='Celcius'
    ),
    yaxis2=dict(
        title='Bar',
        titlefont=dict(
            color='rgb(148, 103, 189)'
        ),
        tickfont=dict(
            color='rgb(148, 103, 189)'
        ),
        overlaying='y',
        side='right'
    )
)


fig = Figure(data=[trace1, trace2], layout=layout)

print(py.plot(fig, filename='Head temperature'))

# temperature sensor connected channel 0 of mcp3008
#sensor_pin = 0
#readadc.initialize()

i = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
stream_temp = py.Stream(stream_token_temp)
stream_temp.open()
stream_pressure = py.Stream(stream_token_pressure)
stream_pressure.open()


#the main sensor reading loop
while 1:
	temphead1 = (chan1.voltage - 1.25) / 0.005
	pheadv1 = chan0.value
	time.sleep(.1)
	temphead2 = (chan1.voltage - 1.25) / 0.005
	pheadv2 = chan0.value
	time.sleep(.1)
	temphead3 = (chan1.voltage - 1.25) / 0.005
	pheadv3 = chan0.value
	time.sleep(.1)
	temphead = (temphead1+temphead2+temphead3)/3
	temphead = round(temphead,1)
	pheadv = (pheadv1+pheadv2+pheadv3)/3
        #phead = chan0.voltage
        # Ratio of 15 bit value to max volts determines volts
	volts = pheadv / 32767.0 * 6.144
	bar=volts *6.24540778839 - 3.07274063189
	bar = round(bar,2)
	#sensor_data = readadc.readadc(sensor_pin, readadc.PINS.SPICLK, readadc.PINS.SPIMOSI, readadc.PINS.SPIMISO, readadc.PINS.SPICS)
	stream_temp.write({'x': i, 'y': temphead })
	stream_pressure.write({'x': i, 'y': bar })
	i = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # delay between stream posts
	time.sleep(.3)
