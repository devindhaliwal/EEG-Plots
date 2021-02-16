import pandas as pd
import plotly.express as px

# function to display user choice menu and get correct option
def menu():
    choice = input("Which category of electrodes would you like highlighted?\n1. None\n2. Peripheral Electrodes"
                   "\n3. 10-20 Electrodes\n4. 10-10 Electrodes\n5. Quit\nEnter number choice: ")
    # checking if valid
    while choice.isdigit() == False or int(choice) > 5 or int(choice) < 1:
        choice = input("Which category of electrodes would you like highlighted?\n1. None\n2. Peripheral Electrodes"
                       "\n3. 10-20 Electrodes\n4. 10-10 Electrodes\n5. Quit\nEnter number choice: ")
    return int(choice)

# getting and cleaning data
def get_clean_data():
    eeg_data = pd.read_csv("../129Channels_v2.csv")
    eeg_data.rename(columns={"Unnamed: 0": "Electrode"}, inplace=True)
    eeg_data["Peripheral Channel"].fillna(0, inplace=True)

    eeg_10_20_data = pd.read_excel("../10-10 and 10-20 electrodes.xlsx", engine='openpyxl')

    # merging dfs
    all_eeg_data = eeg_data.merge(eeg_10_20_data, on='Electrode', how='left')
    all_eeg_data["10-10/10-20 Name"].fillna("N/A", inplace=True)
    all_eeg_data["10-20 Electrode"].fillna(0, inplace=True)
    all_eeg_data["10-10 Electrode"].fillna(0, inplace=True)

    # column for electrode color labels
    all_eeg_data["Electrode Type"] = ["Electrode"] * len(eeg_data)

    return all_eeg_data

# plotting eeg electrodes with no category highlighted
def no_category_plot(eeg_data):
    fig = px.scatter_3d(eeg_data, x='X', y='Y', z='Z', title='EEG Electrode Plot - No Category',
                        color='Electrode Type', text='Electrode', color_discrete_map={"Electrode": "grey"})
    fig.show()

# plotting eeg electrodes with peripheral electrodes highlighted
def peripheral_plot(eeg_data):
    # labeling peripheral electrodes
    eeg_data['Electrode Type'].where(cond=eeg_data['Peripheral Channel'] != 1, other="Peripheral Electrode", inplace=True)
    fig = px.scatter_3d(eeg_data, x='X', y='Y', z='Z', title='EEG Electrode Plot - Peripheral Electrodes',
                        color='Electrode Type', text='Electrode', color_discrete_map={"Electrode": "grey",
                                                                                      "Peripheral Electrode": "red"})
    fig.show()

# plotting eeg electrodes with 10-20 electrodes highlighted
def plot_10_20(eeg_data):
    # labeling 10-20 electrodes
    eeg_data['Electrode Type'].where(cond=eeg_data['10-20 Electrode'] != 1, other="10-20 Electrode",
                                     inplace=True)
    fig = px.scatter_3d(eeg_data, x='X', y='Y', z='Z', title='EEG Electrode Plot - 10-20 Electrodes',
                        color='Electrode Type', text='Electrode', color_discrete_map={"Electrode": "grey",
                                                                                      "10-20 Electrode": "green"})
    fig.show()

# plotting eeg electrodes with 10-10 electrodes highlighted
def plot_10_10(eeg_data):
    # labeling 10-10 electrodes
    eeg_data['Electrode Type'].where(cond=eeg_data['10-10 Electrode'] != 1, other="10-10 Electrode",
                                     inplace=True)
    fig = px.scatter_3d(eeg_data, x='X', y='Y', z='Z', title='EEG Electrode Plot - 10-10 Electrodes',
                        color='Electrode Type', text='Electrode', color_discrete_map={"Electrode": "grey",
                                                                                      "10-10 Electrode": "blue"})
    fig.show()

def main():
    eeg_data = get_clean_data()
    choice = menu()

    while 1:
        if choice == 1:
            no_category_plot(eeg_data)
        elif choice == 2:
            peripheral_plot(eeg_data)
        elif choice == 3:
            plot_10_20(eeg_data)
        elif choice == 4:
            plot_10_10(eeg_data)
        else:
            return
        # allowing user another choice
        choice = menu()

main()