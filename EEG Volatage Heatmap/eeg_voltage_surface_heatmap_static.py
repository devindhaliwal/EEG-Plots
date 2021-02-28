import pandas as pd
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv("129Channels_with_coresponding_voltage_potentials.csv")
print(df.columns)
'''
x, y = np.meshgrid(df.X, df.Y)
z = [df.Z.tolist()*len(df)]
z = np.reshape(z, x.shape)
print(z.shape)
'''
fig = go.Figure(data=[go.Mesh3d(x=df.X, y=df.Y, z=df.Z, color=df['Voltage (uV)'])])

fig.show()

