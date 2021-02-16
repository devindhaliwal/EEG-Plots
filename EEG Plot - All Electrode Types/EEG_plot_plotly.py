import pandas as pd
import plotly.express as px
import chart_studio
import chart_studio.plotly as py

#username = 'devindha'
#api_key = ''
#chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

# getting and cleaning data
eeg_data = pd.read_csv("../129Channels_v2.csv")
eeg_data.rename(columns={"Unnamed: 0": "Electrode"}, inplace=True)
eeg_data["Peripheral Channel"].fillna(0, inplace=True)

eeg_10_20_data = pd.read_excel("10-10 and 10-20 electrodes.xlsx", engine='openpyxl')

# merging dfs
all_eeg_data = eeg_data.merge(eeg_10_20_data, on='Electrode', how='left')
all_eeg_data["10-10/10-20 Name"].fillna("N/A", inplace=True)
all_eeg_data["10-20 Electrode"].fillna(0, inplace=True)
all_eeg_data["10-10 Electrode"].fillna(0, inplace=True)

# creating a column for electrode color labels
all_eeg_data.loc[all_eeg_data['Peripheral Channel'] == 1.0, 'Electrode Type'] = "Peripheral Channel"
all_eeg_data.loc[all_eeg_data['Peripheral Channel'] == 0.0, 'Electrode Type'] = "Non-Peripheral Channel"
all_eeg_data.loc[all_eeg_data['10-10 Electrode'] == 1.0, 'Electrode Type'] = "10-10 Electrode"

# creating a column for electrode names
all_eeg_data['Electrode Label'] = all_eeg_data['Electrode'].where(all_eeg_data['10-10 Electrode'] == 0, all_eeg_data['10-10/10-20 Name'])

# creating 3D interactive plot
fig = px.scatter_3d(all_eeg_data, x='X', y='Y', z='Z', color='Electrode Type', title='EEG Data', text='Electrode Label'
                    , color_discrete_map={'Peripheral Channel':'blue', 'Non-Peripheral Channel':'gold', '10-10 Electrode':'crimson'})

fig.show()
#py.plot(fig, filename = 'eeg_data_10-10', auto_open=True)
