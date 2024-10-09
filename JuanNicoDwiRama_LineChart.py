
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import DatetimeTickFormatter
import re

def read_speed_data(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    timestamps = re.findall(r'Timestamp:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', content)
    speed_lines = re.findall(r'Timestamp:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?sender.*?(\d+\.\d+)\s*(MBytes|KBytes|Mbps)', content, re.DOTALL)

    print(f"Found {len(speed_lines)} speed entries related to 'sender': {speed_lines}")

    speeds_mbps = []
    timestamp_dict = {}

    for line in speed_lines:
        timestamp = line[0]
        speed_value = float(line[1])
        speed_unit = line[2]

        if speed_unit == 'MBytes':
            speed_mbps = speed_value * 8
        elif speed_unit == 'KBytes':
            speed_mbps = speed_value * 0.008
        else:
            speed_mbps = speed_value

        if timestamp not in timestamp_dict:
            timestamp_dict[timestamp] = speed_mbps

    if timestamp_dict:
        timestamps, speeds_mbps = zip(*timestamp_dict.items())
    else:
        return [], []

    return timestamps, speeds_mbps

file_path = 'soal_chart_bokeh.txt'
timestamps, speeds_mbps = read_speed_data(file_path)

if len(timestamps) != len(speeds_mbps):
    print(f"Warning: Number of timestamps ({len(timestamps)}) does not match number of speeds ({len(speeds_mbps)}).")

if speeds_mbps:
    data = {
        'timestamp': pd.to_datetime(timestamps),
        'speed': speeds_mbps
    }
    df = pd.DataFrame(data)

    output_file("line_chart.html")

    p = figure(title="Testing Jaringan", 
               x_axis_label='Date Time', 
               y_axis_label='Kecepatan (Mbps)',
               x_axis_type='datetime', 
               width=800, 
               height=400)

    p.line(df['timestamp'], df['speed'], line_width=2, color='blue', legend_label="Kecepatan")

    p.line(x=[df['timestamp'].min(), df['timestamp'].max()], 
            y=[75, 75], 
            color='gray', 
            line_dash='dashed')

    p.xaxis.formatter = DatetimeTickFormatter(hours="%H:%M:%S")

    show(p)
else:
    print("No speed data available to plot.")
