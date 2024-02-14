print("[topic_identification] importing library")

print("using LDA for vectorisation of words to make topics")
#grab documents 
import read_reports
reports = read_reports.read_all("test reports", "report.txt") 

#perform gensim_lda
import gensim_lda
k = 1
for documents in reports:
    print("Identifying topic from report " + str(k))
    tokend_docs = gensim_lda.tokenisedocs(documents)
    lda_model = gensim_lda.buildLDA(tokend_docs, numTopics=1, passes=2)
    gensim_lda.printResults(lda_model, numWords=3)
    k += 1


#perform NB with training
print("using MultinominalNB for training labelled topics")

#grab documents for training
import read_reports
# Use list comprehension to join the items in each sublist into a single string
reports = read_reports.read_all("test reports", "report.txt")
reports = [". ".join(sublist) for sublist in reports]

# Make labels
labeled_data = [
    ("Threatening language", reports[0]),
    ("Safe", reports[1]),
    ("Safe", reports[2]),
    ("Safe", reports[3]),
]

import MultinomialNB
clf, vectoriser = MultinomialNB.trainClassifier(labeled_data)

#make the predictions
test_reports = read_reports.read_all("test reports", "report_test.txt")
test_reports = [" ".join(sublist) for sublist in test_reports]
predictions = MultinomialNB.predictOnReports(clf, vectoriser, test_reports)
