import pandas as pd
import plotly.express as px

df = pd.read_csv("129Channels_with_coresponding_voltage_potentials.csv")
df.rename(columns={"Unnamed: 0": "Electrode"}, inplace=True)
print(df)

fig = px.scatter_3d(df, x='X', y='Y', z='Z', color='Voltage (uV)', title='EEG Voltage Heatmap', text='Electrode')

fig.show()

