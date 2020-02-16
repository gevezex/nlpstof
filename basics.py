import spacy 

def tokenize_sentence(sentence):
    '''input: sentence string
       output: tokenized list of words'''
    nlp = spacy.load('nl')
    doc = nlp(sentence)
    return [token.text for token in doc]

def tokenize_sentences(sentences):
    '''input: list of sentences in strings
       output: tokenized list of tokenized sentences'''
    nlp = spacy.load('nl')
    list_of_sentence_tokens = [[token.text for token in nlp(sent)] for sent in sentences]
    return list_of_sentence_tokens

import nltk 

def paragraph2sentences(paragraph):
    '''input: large string document
       output: list of sentences in string format'''
    sent_text = nltk.sent_tokenize(paragraph)
    return sent_text
