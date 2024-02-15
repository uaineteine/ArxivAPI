#perform NB with training
print("[train_topics] using MultinominalNB for training labelled topics")

#grab documents for training
import pandas as pd
reports = pd.read_csv("source data/papers.csv", dtype=str)
# printing all columns of the dataframe 
print(reports)

# filtering for training data on basis of both filters
training_reports = reports[reports['trainFlag'] == "y"]
print(training_reports)

# Make labels
# Assuming you have already filtered the DataFrame as 'training_reports'
# You can create the labeled_data list like this:
labeled_data = list(zip(training_reports['label'], training_reports['URL']))

# Print the resulting list
print("Labeled data:")
for label, url in labeled_data:
    print(f"({label}, {url})")

import MultinomialNB
print("training")
clf, vectoriser = MultinomialNB.trainClassifier(labeled_data)

#make the predictions
