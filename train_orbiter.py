print("[train_orbiter] importing libraries")
import pandas as pd
import extract_arxiv
import model_funcs.MultinomialNB as MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train(source_data_filename, targetPerc=.2):
    #grab documents for training
    reports = pd.read_csv(source_data_filename, dtype=str)
    reports['paper_info'] = reports['URL'].apply(extract_arxiv.extract_paper_info)

    # Split the data into training and testing sets
    train_reports, test_reports = train_test_split(reports, test_size=targetPerc, random_state=42)

    # Make labels for training data
    labeled_data = list(zip(train_reports['label'], train_reports['paper_info']))

    #perform NB with training
    print("[train_orbiter::train] using MultinominalNB for training labelled topics")
    clf, vectoriser = MultinomialNB.trainClassifier(labeled_data)
    print(f"[train_orbiter::train] training completed")

    #make the predictions
    test_predictions = MultinomialNB.predictOnReports(clf, vectoriser, test_reports['paper_info'])
    # Calculate the accuracy
    accuracy = accuracy_score(test_reports['label'], test_predictions)
    print(f"Training Accuracy: {accuracy * 100:.2f}%")

