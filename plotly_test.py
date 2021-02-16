import pandas as pd
import plotly.express as px


# getting and cleaning data
eeg_data = pd.read_csv("129Channels_v2.csv")
eeg_data.rename(columns={"Unnamed: 0": "Electrode"}, inplace=True)
eeg_data["Peripheral Channel"].fillna(0, inplace=True)
eeg_data["Peripheral Channel"] = eeg_data["Peripheral Channel"].astype(str)

fig = px.scatter_3d(eeg_data, x='X', y='Y', z='Z', text='Electrode', color='Peripheral Channel', title="EEG Data", color_discrete_sequence=["red", "yellow"])

fig.show()