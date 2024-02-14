print("[MultinominalNB]")

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def trainClassifier(labeled_data):

    # Separate labels and text
    labels, texts = zip(*labeled_data)

    # Vectorize the text data
    vectoriser = CountVectorizer()
    X = vectoriser.fit_transform(texts)

    # Train the classifier
    clf = MultinomialNB()
    clf.fit(X, labels)
    return(clf, vectoriser)

def predictOnReports(clf, vectoriser, reports):
    # Predict topics for new text reports
    X_new = vectoriser.transform(reports)
    predicted_topics = clf.predict(X_new)

    print("Predicted topics for new reports:")
    for report, topic in zip(reports, predicted_topics):
        print(f"Report: {report} | Topic: {topic}")
    return(predicted_topics)
