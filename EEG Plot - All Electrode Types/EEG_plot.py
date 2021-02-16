import pandas as pd
import matplotlib.pyplot as plt

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

# setting up plot space
fig = plt.figure(figsize=(12, 8))
plt.style.use('seaborn-deep')
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X', c='firebrick')
ax.set_ylabel('Y', c='firebrick')
ax.set_zlabel('Z', c='firebrick')
ax.set_title('EEG Data Plot', c='firebrick')

# iterating through data frame to plot and label each point
for index, row in all_eeg_data.iterrows():
    # plotting point
    #ax.scatter(row["X"], row["Y"], row["Z"], c='firebrick', marker='o')

    # plotting and labeling 10-10/10-20 electrodes
    # if row["10-10 Electrode"]:
    if row["10-20 Electrode"]:
        # it's not ucla blue so it's ok
        #ax.scatter(row["X"], row["Y"], row["Z"], c='blue', marker='o', label="10-10 Electrode")
        ax.scatter(row["X"], row["Y"], row["Z"], c='blue', marker='o', label="10-20 Electrode")
        # labeling point with 10-10/10-20 Name name
        ax.text(row["X"], row["Y"], row["Z"], row["10-10/10-20 Name"], fontsize=6)
    # not 10-10/10-20 electrode
    else:
        # plotting point with peripheral channels in a different color
        if row["Peripheral Channel"] == 1:
            # peripheral channel
            ax.scatter(row["X"], row["Y"], row["Z"], c='gold', marker='o', label="Peripheral Channel")
        else:
            # not peripheral channel
            ax.scatter(row["X"], row["Y"], row["Z"], c='firebrick', marker='o', label="Non-Peripheral Channel")

        # labeling point with sensor name
        ax.text(row["X"], row["Y"], row["Z"], row["Electrode"], fontsize=6)

# fixing legend duplicates
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

# displaying graph
plt.show()
