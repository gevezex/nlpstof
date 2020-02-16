import spacy 

def tokenize_sentence(sentence, spacy_model="nl"):
    """
    input: sentence string
    output: tokenized list of words'''
    nlp = spacy.load(spacy_model)
    doc = nlp(sentence)
    return [token.text for token in doc]
    """

def tokenize_sentences(sentences, spacy_model="nl"):
    """
    input: list of sentences in strings
    input: spacy_model, default = dutch
    output: tokenized list of tokenized sentences
    """

    nlp = spacy.load(spacy_model)
    #list_of_sentence_tokens = [[token.text for token in nlp(sent)] for sent in sentences]
    list_of_sentence_tokens = [[token.text for token in doc] for doc in nlp.pipe(sentences)]
    return list_of_sentence_tokens

import nltk 

def document2sentences(document):
    """
    input: large string document
    output: list of sentences in string format
    sent_text = nltk.sent_tokenize(document)
    return sent_text
    """

def document2sent2tokens(document, spacy_model="nl"):
    """
    input: large string document
    input: spacy_model, default = dutch
    output: list of tokens per sentence
    """
    
    sent_text = document2sentences(document)
    tokenized_sentences = tokenize_sentences(sent_text, spacy_model)
    return tokenized_sentences