#pdfminer document testen
import json
import os
import pdfminer
 
from pathlib import Path
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
 
 
#extract text from pdf
def pdf_2_txt(pdf_filepath):
 
    # Open a PDF file.
    fp = open(pdf_filepath, 'rb')
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)
    # Create a PDF document object that stores the document structure.
    # Supply the password for initialization.
    document = PDFDocument(parser, "")
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
 
    #outlines = document.get_outlines()
    #for (level,title,dest,a,se) in outlines:
    #    print (level, title)
 
    document = open(pdf_filepath, 'rb')
    #Create resource manager
    rsrcmgr = PDFResourceManager()
    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(document):
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):              
                if(len(str(element.get_text())) >4):                                   
                    yield{'text': element.get_text()}
 
 
#split text to sentences                
def convert_file_to_output(pdf_filepath): 
    separator=None
    output = []
 
    for texts in pdf_2_txt(pdf_filepath):
        if not callable(separator):
            def separator(line): return line[-1] == '.'
        paragraph = []
        for key, text in texts.items(): #text is json output
 
            for token in text.split():           
                if separator(token):
                    #pdb.set_trace()
                    if paragraph:
                        paragraph.append(token)
                        task = {'text': ' '.join((" ".join(paragraph)).split()) }  # create one task for each line of text , join for concatentating the list, join/split for removing the whitespaces             
                        print(json.dumps(task))
                        #output.append(task)
                        paragraph = []
                else:
                    paragraph.append(token)
 
#loop through directory
def get_files_from_dir(pdf_dir):
    for file_path in os.listdir(pdf_dir):  # iterate over directory
            if(file_path.lower().endswith(".pdf")):
                convert_file_to_output(pdf_dir+'/'+file_path)
               
pdf_dir = './'
 
get_files_from_dir(pdf_dir)