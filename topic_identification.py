print("[topic_identification] importing library")

#perform NB with training
print("using MultinominalNB for training labelled topics")

#grab documents for training
import read_reports
# Use list comprehension to join the items in each sublist into a single string
reports = read_reports.read_all("test reports", "report.txt")
reports_join = [". ".join(sublist) for sublist in reports]

# Make labels
labeled_data = [
    ("Unsafe", reports_join[0]),
    ("Safe", reports_join[1]),
    ("Safe", reports_join[2]),
    ("Safe", reports_join[3]),
]

import MultinomialNB
clf, vectoriser = MultinomialNB.trainClassifier(labeled_data)

#make the predictions
test_reports = read_reports.read_all("test reports", "report_test.txt")
test_reports = [" ".join(sublist) for sublist in test_reports]
predictions = MultinomialNB.predictOnReports(clf, vectoriser, test_reports)

import gensim_lda
#identify unsafe
for report, topic in zip(reports, predictions):
    if (topic == "Unsafe"):
        #for predictions that are problematic
        #identify topic words using LDA
        print("using LDA for vectorisation of words to identify topics with a finer comb")

        #perform gensim_lda
        print("Identifying theme words from unsafe report")
        tokend_docs = gensim_lda.tokenisedocs(report)
        lda_model = gensim_lda.buildLDA(tokend_docs, numTopics=1, passes=4)
        gensim_lda.printResults(lda_model, numWords=5)
