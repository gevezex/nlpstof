import spacy 
import nltk

# PdfMiner
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


class documentTokenizer:
    """Tokenizer for documents"""

    def __init__(self, language='nl', eol=True):
        self.language = language
        self.eol = eol

    def tokenize_sentence(self, sentence):
        """Input: sentence string
        output: tokenized list of words
        """
        nlp = spacy.load(self.language)
        doc = nlp(sentence)
        return [token.text for token in doc]

    def tokenize_sentences(self, sentences, spacy_model=None):
        """Input: list of sentences in strings
        input: spacy_model, default = dutch
        output: tokenized list of tokenized sentences
        """
        
        if spacy_model is None:
            spacy_model = self.language
        nlp = spacy.load(spacy_model)
        #list_of_sentence_tokens = [[token.text for token in nlp(sent)] for sent in sentences]
        list_of_sentence_tokens = [[token.text for token in doc] for doc in nlp.pipe(sentences)]
        return list_of_sentence_tokens


    def document2sentences(self, document, language='dutch', eol=None):
        """Input: large string document
        output: list of sentences in string format
        """
        if eol is None:
            eol = self.eol
        sent_text = nltk.sent_tokenize(document)
        if eol:
            tmp_list = ['Eerste zin']
            for sentence in sent_text:
                tmp_list.extend(sentence.split('\n'))
            del tmp_list[0]
            sent_text = tmp_list

        return sent_text

    def document2sent2tokens(self, document, spacy_model=None):
        """Input: large string document
        input: spacy_model, default = dutch
        output: list of tokens per sentence
        """
        
        if spacy_model is None:
            spacy_model = self.language
        sent_text = self.document2sentences(document)
        tokenized_sentences = self.tokenize_sentences(sent_text, spacy_model)
        return tokenized_sentences
    
    def pdf2text(self, fname, pages=None):
        """Input:
            fname: path/filename
            pages: list of page numbers (integers) or None for whole document
        output: 
            dictionary with: 
                key = pagenumber (int)
                value = page text (str)
        """
        if not pages:
            pagenums = set()
        else:
            pagenums = list(set(pages))

        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)

        page_text = {}

        infile = open(fname, 'rb')
        for page_nr, page in enumerate(PDFPage.get_pages(infile, pagenums)):
            interpreter.process_page(page)
            data = output.getvalue()
            if pages is None:
                page_text[page_nr+1] = data
            else:
                page_text[pagenums[page_nr]] = data

            # empty StringIO after every page and go back to position 0 
            output.truncate(0)
            output.seek(0)

        infile.close()
        converter.close()
        output.close
            
        return page_text