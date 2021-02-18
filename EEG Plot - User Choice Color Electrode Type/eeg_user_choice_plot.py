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
    eeg_data.rename(columns={"Unnamed: 0": "Electrode", "Peripheral Channel": "Peripheral Electrode"}, inplace=True)
    eeg_data["Peripheral Electrode"].fillna(0, inplace=True)

    eeg_10_20_data = pd.read_excel("../10-10 and 10-20 electrodes.xlsx", engine='openpyxl')

    # merging dfs
    all_eeg_data = eeg_data.merge(eeg_10_20_data, on='Electrode', how='left')
    all_eeg_data["10-10/10-20 Name"].fillna("N/A", inplace=True)
    all_eeg_data["10-20 Electrode"].fillna(0, inplace=True)
    all_eeg_data["10-10 Electrode"].fillna(0, inplace=True)

    # column for electrode color labels
    all_eeg_data["Electrode Type"] = ["Electrode"] * len(eeg_data)

    return all_eeg_data

# plotting electrodes with user choice group highlighted
def plot_eeg(eeg_data, plot_type):

    if plot_type is None:
        # no electrode group selected
        fig = px.scatter_3d(eeg_data, x='X', y='Y', z='Z', title='EEG Electrode Plot - No Category',
                            color='Electrode Type', text='Electrode', color_discrete_map={"Electrode": "grey"})
    else:
        # getting plot type variables
        highlighted_group_type = plot_type[0]
        highlighted_group_color = plot_type[1]
        # labeling electrode group to be highlighted
        eeg_data['Electrode Type'].where(cond=eeg_data[highlighted_group_type] != 1, other=highlighted_group_type,
                                         inplace=True)
        # plotting electrodes with highlighted group
        fig = px.scatter_3d(eeg_data, x='X', y='Y', z='Z', title='EEG Electrode Plot - '+highlighted_group_type+'s',
                            color='Electrode Type', text='Electrode',
                            color_discrete_map={"Electrode": "grey", highlighted_group_type: highlighted_group_color})
        
    fig.show()
    
def main():
    eeg_data = get_clean_data()
    choice = menu()

    choice_map = {1: None, 2: ["Peripheral Electrode", "red"], 3: ["10-10 Electrode", "green"], 4: ["10-20 Electrode", "blue"]}

    while 1:
        if choice == 5:
            return
        else:
            # plotting electrodes
            plot_eeg(eeg_data, choice_map[choice])
            # resetting column for electrode color labels
            eeg_data["Electrode Type"] = ["Electrode"] * len(eeg_data)
        # allowing user another choice
        choice = menu()

main()