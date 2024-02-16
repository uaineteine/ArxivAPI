print("[train_topics] importing libraries")
import pandas as pd
import extract_arxiv
import model_funcs.MultinomialNB as MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from joblib import dump, load

#perform NB with training
print("[train_topics] using MultinominalNB for training labelled topics")

#grab documents for training
reports = pd.read_csv("source data/papers.csv", dtype=str)
reports['paper_info'] = reports['URL'].apply(extract_arxiv.extract_paper_info)

# Split the data into training and testing sets
train_reports, test_reports = train_test_split(reports, test_size=0.2, random_state=42)

# Make labels for training data
labeled_data = list(zip(train_reports['label'], train_reports['paper_info']))

print("[train_topics] training...")
clf, vectoriser = MultinomialNB.trainClassifier(labeled_data)
print("[train_topics] training completed")

#make the predictions
test_predictions = MultinomialNB.predictOnReports(clf, vectoriser, test_reports['paper_info'])
# Calculate the accuracy
accuracy = accuracy_score(test_reports['label'], test_predictions)
print(f"Training Accuracy: {accuracy * 100:.2f}%")

# Save the model
dump(clf, "trained_models/processing/filename.joblib") 

# Load the model
#clf = load('filename.joblib') 
