
from Tokenizer import Tokenizer
from LinguisticPreprocesser import LinguisticPreprocesser

class Indexer:
    
    def __init__(self):
        self.inverted_index = {}
        
    def get_inverted_index(self, corpus_size):
        return self.inverted_index
    
    def preprocess(self, document):
        tokenizer = Tokenizer()
        preprocesser = LinguisticPreprocesser()
        token_list = tokenizer.tokenize(document.get_content())
        dictionary = preprocesser.preprocess(token_list)
        return dictionary
    
    def index(self, document):
        dictionary = self.preprocess(document)
        doc_id = document.get_id()
        
        for term in dictionary:
            if term not in self.inverted_index:
                self.inverted_index[term] = []
            self.inverted_index[term].append(doc_id)