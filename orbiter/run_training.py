print("run_training] import libraries")
import os
import glob
import train_orbiter as train_orbiter

def list_csv_files(directory):
    return glob.glob(os.path.join(directory, '*.csv'))

def select_dataset():
    csv_files = list_csv_files('source data')
    for i, filename in enumerate(csv_files):
        print(f"{i+1}. {filename}")
    selected = int(input("Enter the number of the dataset you want to train on: ")) - 1
    return csv_files[selected]

def main():
    selected_dataset = select_dataset()
    print(f"You selected {selected_dataset}")
    clf, vectoriser = train_orbiter.train(selected_dataset)

main()
