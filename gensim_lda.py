print("[gensim_lda]")

import gensim
from gensim import corpora
from gensim.parsing.preprocessing import STOPWORDS

# Tokenize and preprocess the documents
def tokenisedocs(documents):
    tokenised_docs = [doc.lower().split() for doc in documents]
    tokenised_docs = [[token for token in doc if token not in STOPWORDS] for doc in tokenised_docs]
    tokenised_docs = [[token for token in doc if token not in ["isn't", "i'll"]] for doc in tokenised_docs]
    return(tokenised_docs)

def buildLDA(tokens_docs, numTopics, passes):
    # Create a dictionary from the tokenized documents
    dictionary = corpora.Dictionary(tokens_docs)

    # Create a document-term matrix
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in tokens_docs]

    # Build the LDA model
    lda_model = gensim.models.LdaModel(
        doc_term_matrix,
        num_topics=numTopics,  # Specify the number of topics you want to extract
        id2word=dictionary,
        passes=passes  # Number of iterations
    )
    return(lda_model)

def printResults(lda_model, numWords=1):
    # Print the topics
    # Store topics and their word counts in a dictionary
    if (numWords == 0):
        topics = lda_model.print_topics()
    else:
        topics = lda_model.print_topics(num_words=numWords)
    topic_word_counts = {}
    for idx, topic in enumerate(topics):
        # The print_topics method returns a list of tuples, where each tuple contains a topic index and a string of words and their probabilities.
        # We need to extract the word counts from this string.
        word_counts = topic[1].split("+")
        total_count = 0

        for word_count in word_counts:
            count, word = word_count.split("*")
            total_count += float(count)

        topic_word_counts[idx] = total_count
    
        #print(topic)

    # Find the topic with the minimum word count
    min_topic = min(topic_word_counts, key=topic_word_counts.get)

    print(f"The topic with the minimum word count is topic {min_topic} with a total word count of {topic_word_counts[min_topic]}")
    print(f"The words for this topic are: {topics[min_topic][1]}")
