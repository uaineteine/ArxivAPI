# ! There is actually a working script in this, you can find the detail at the bottom of the readme

## ! A word of caution: that process will likely result in the exposure of not safe for work language. However, given the context and the nature of the content that the script is expected to handle, encountering such language is anticipated. 

# Purpose

The purpose of this script is to automate the process of identifying and flagging potentially unsafe content in text reports. It achieves this by training a machine learning model on a set of labeled data, where each text report is marked as either “Safe” or “Unsafe”. Once trained, the model can then classify new, unseen reports.

This functionality is particularly useful in content moderation, helping to ensure that only appropriate content is displayed. Additionally, the script can perform content identification on reports flagged as “Unsafe”, providing a summary of the content for further analysis. This could be applied to other methods of unsafe word analysis, enhancing the ability to detect and manage inappropriate content.

Please note that due to the nature of the content it handles, the script will likely expose NSFW language with the samples I've made.

# Requirements

1. **Python**
2. **sklearn**
* This script uses the following methods from scikit-learn:
  - CountVectorizer from sklearn.feature_extraction.text: This is used to convert the text data into a matrix of token counts, which is a necessary step before training the classifier.
  - MultinomialNB from sklearn.naive_bayes: This is a Naive Bayes classifier model suitable for classification of text features. It is used to train the classifier on the vectorised text data and the corresponding labels.
3. **gensim**
* This package is used for unsupervised semantic modelling from plain text. It is used for performing Latent Dirichlet Allocation (LDA) for content identification, specifically on reports that are classified as “Unsafe” to get further detail about them should they have been detected as unsafe.

# Explanation and Process Psuedocode

## Training a model to label reports as safe and unsafe

1. **Import necessary libraries**
  - Import CountVectorizer from sklearn.feature\_extraction.text.
  - Import MultinomialNB from sklearn.naive\_bayes.
  - Gensim and STOPWORDS for limitation on words to analyse
2. **Perform report reading**
  - Define a function to read\_all reports line by line, strip any leading/trailing whitespace, and append the lines to the reports list.

```python
def read_reports(dirname, fileext):
    reports = []
    for filename in dirs(dirname):
        if filename.endswith(fileext):
            filepath = path.join(dirname, filename)
            with open(filepath) as f:
                reports.append(striplines(f))
    return(reports)
```

3. **Classifier Training**
  - Define a function trainClassifier that takes labeled data as input.
  - Separate the labels and the text from the labeled data.
  - Vectorise the text data using CountVectorizer. This converts the text data into a matrix of token counts.
  - Train the Multinomial Naive Bayes classifier on the text data and the corresponding labels.

```python
def trainClassifier(labeled_data):
    labels, texts = zip(*labeled_data)
    vectoriser = CountVectorizer()
    X = vectoriser.fit_transform(texts)
    clf = MultinomialNB()
    clf.fit(X, labels)
    return(clf, vectoriser)
```

  - Create a list labeled\_data of tuples, where each tuple contains a label ("Unsafe" or "Safe") and a corresponding report from reports\_join.

```python
reports = read_reports("test reports", "report.txt")
labeled_data = [
    ("Unsafe", reports[0]),
    ("Safe", reports[1]),
    ("Safe", reports[2]),
    ("Safe", reports[3]),
    ...
]

clf, vectoriser = trainClassifier(labeled_data)
```

4. **Perform the predictions**
  - Vectorise the new text reports and predict the topics for the new text reports using the trained classifier.
  - Call the read\_all function to read all text files in the "test reports" directory that end with "test.txt". 
  - Define a function predictOnReports that takes the trained classifier, the vectoriser, and new text reports as input.

```python
test_reports = read_reports.read_all("test reports", "test.txt")

def predictOnReports(clf, vectoriser, reports):
    X_new = vectoriser.transform(reports)
    predicted_topics = clf.predict(X_new)

    print("Predicted topics for new reports:")
    for report, topic in zip(reports, predicted_topics):
        print(f"Report: {report} | Topic: {topic}")
    return(predicted_topics)

predictions = predictOnReports(clf, vectoriser, test_reports)
```

5. **Extension: Perform LDA for content identification on unsafe reports**


For each report and its corresponding prediction in predictions, if the prediction is "Unsafe":
* Tokenise the report documents by splitting the text a part, removing basic words STOPWORDS like 'a', 'and'...
      
```python
extra_STOPWORDS = ["isn't", "i'll", ...]
tokenised_docs = [doc.lower().split() for doc in documents]
tokenised_docs = [[token for token in doc if token not in STOPWORDS] for doc in tokenised_docs]
tokenised_docs = [[token for token in doc if token not in extra_STOPWORDS] for doc in tokenised_docs]
```

* Build the LDA model on tokend\_docs, specifying the number of topics and the number of passes

```python
def buildLDA(tokens_docs, numTopics, passes):
    dictionary = corpora.Dictionary(tokens_docs)

    doc_term_matrix = [dictionary.doc2bow(doc) for doc in tokens_docs]

    lda_model = gensim.models.LdaModel(
        doc_term_matrix,
        num_topics=numTopics, 
        id2word=dictionary,
        passes=passes
    )
lda_model = gensim_lda.buildLDA(tokenised_docs, numTopics=1, passes=4)
```

* Present the results of the LDA model specifying a limit to the number of words

```python
topics = lda_model.print_topics(num_words=numWords)
topic_word_counts = {}
    for idx, topic in enumerate(topics):
        word_counts = topic[1].split("+")
        total_count = 0

        for word_count in word_counts:
            count, word = word_count.split("*")
            total_count += float(count)

        topic_word_counts[idx] = total_count
```
      

# Further extensions to process and predictions

* Flag for unsafe words themselves. You can maintain a list of unsafe words and phrases. When a report is processed, the script can check for the presence of these words and phrases. If found, the report can be immediately flagged as “Unsafe”. This can be an additional layer for priority investigation on flag.

* Further topics of trianing, instead of just “Safe” and “Unsafe”. For example, you can have categories like “Violence”, “Harassment”, “Profanity”, etc. This would require a labeled dataset for each of these new categories.

* Zero-shot learning can deal with new topic types that the model has not been trained on. 

# Live test

The script ```topic_identification.py``` is an executable for this process. This Python file, when executed, initiates a live test of topic identification. The term “live test” implies that the script is run in an environment that closely simulates its intended operational conditions, providing a realistic assessment of its performance. However, this is very basic and more of a proof of concept.

The script operates on sample data located in the “test reports” folder. During the execution, if the script encounters content that it deems unsafe, it triggers a deeper analysis of the content. This analysis is performed using Latent Dirichlet Allocation (LDA), an unsupervised model for topic analysis. LDA helps in identifying the underlying latent structure of the content, and presents the key words that characterise the identified topics.

A word of caution! This process may result in the exposure of NSFW language. However, given the context and the nature of the content that the script is expected to handle, encountering such language is anticipated.

It should present on final output the following:

```python
[topic_identification] importing library
using MultinominalNB for training labelled topics
[read_reports] importing library
[MultinominalNB]
Predicted topics for new reports:
Report: You gonna answer me Ill get you you cant ignore me **** you **** **** answer me ill be waiting for you im watching you im outside | Topic: Unsafe
Report: Rent electricity money Food gas water Thanks thx drinks | Topic: Safe
[gensim_lda]
using LDA for vectorisation of words to identify topics with a finer comb
Identifying theme words from unsafe report
The topic with the minimum word count is topic 0 with a total word count of 0.255
The words for this topic are: 0.051*"can't" + 0.051*"watching" + 0.051*"don't" + 0.051*"i'm" + 0.051*"answer"
```



#### Daniel Stamer-Squair
