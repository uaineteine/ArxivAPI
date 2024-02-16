print("[train_topics] importing libraries")
import pandas as pd
import extract_arxiv
import model_funcs.MultinomialNB as MultinomialNB

#perform NB with training
print("[train_topics] using MultinominalNB for training labelled topics")

#grab documents for training
reports = pd.read_csv("source data/papers.csv", dtype=str)
reports['paper_info'] = reports['URL'].apply(extract_arxiv.extract_paper_info)

# filtering for training data on basis of both filters
training_reports = reports[reports['trainFlag'] == "y"]

# Make labels
# Assuming you have already filtered the DataFrame as 'training_reports'
# You can create the labeled_data list like this:
labeled_data = list(zip(training_reports['label'], training_reports['paper_info']))

print("[train_topics] training...")
clf, vectoriser = MultinomialNB.trainClassifier(labeled_data)
print("[train_topics] training completed")

#make the predictions
test_reports = reports[reports['trainFlag'] == "n"]
test_predictions = MultinomialNB.predictOnReports(clf, vectoriser, test_reports['paper_info'])
