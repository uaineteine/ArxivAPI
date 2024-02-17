print("run_training] import libraries")
import os
import glob
import train_orbiter
import orbiter_io

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
    # Extract the filename from the selected_dataset path
    model_name = os.path.basename(selected_dataset).split('.')[0]
    print(f"You selected {model_name}")

    train_perc = 0.8
    clf, vectoriser, n_trained = train_orbiter.train(selected_dataset, testPerc=1-train_perc)

    orbiter_io.save_model(clf, vectoriser, f'trained_models/processing/{model_name}_{n_trained}.pkl') 

main()
