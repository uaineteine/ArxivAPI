# STATUS

[![Execution Tests](https://github.com/uaineteine/OrbitOracle_Exoplanet/actions/workflows/execution-tests.yml/badge.svg)](https://github.com/uaineteine/OrbitOracle_Exoplanet/actions/workflows/execution-tests.yml)

[Arxiv Status][https://status.arxiv.org/]

# Purpose

The purpose of this script is to automate the process of identifying and flagging potentially interesting research papers on arxiv. The model will train topic identification based on a CSV of URLs to papers.


# How it works    

...

# Requirements

1. **Python**
2. **sklearn**
* This script uses the following methods from scikit-learn:
  - CountVectorizer from sklearn.feature_extraction.text: This is used to convert the text data into a matrix of token counts, which is a necessary step before training the classifier.
  - MultinomialNB from sklearn.naive_bayes: This is a Naive Bayes classifier model suitable for classification of text features. It is used to train the classifier on the vectorised text data and the corresponding labels.
3. **pickle**

#### Daniel Stamer-Squair
