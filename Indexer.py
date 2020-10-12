
from Tokenizer import Tokenizer
from LinguisticPreprocesser import LinguisticPreprocesser

class Indexer:
    
    def __init__(self):
        self.inverted_index = {}
        
    def get_inverted_index(self):
        """
        Method untuk mendapatkan inverted index yang telah dibangun.

        Returns
        -------
        inverted_index
            Inverted index yang menyimpan pemetaan term ke lokasi term tersebut berada..

        """
        return self.inverted_index
    
    def preprocess(self, document):
        """
        Method untuk mengambil daftar term dari dokumen teks.
        Proses yang dilakukan adalah tokenizing dan linguistic preprocessing.

        Parameters
        ----------
        document : Document.Document
            Dokumen teks.

        Returns
        -------
        dictionary : list
            Daftar term dalam dokumen teks.

        """
        tokenizer = Tokenizer()
        preprocesser = LinguisticPreprocesser()
        token_list = tokenizer.tokenize(document.get_content())
        dictionary = preprocesser.preprocess(token_list)
        return dictionary
    
    def index(self, document):
        """
        Method untuk membangun inverted index.
        Pembangunan inverted index dilakukan untuk dokumen teks satu per satu.

        Parameters
        ----------
        document : Document.Document
            Dokumen teks.

        Returns
        -------
        None.

        """
        dictionary = self.preprocess(document)
        doc_id = document.get_id()
        
        for term in dictionary:
            if term not in self.inverted_index:
                self.inverted_index[term] = {}
            
            if doc_id not in self.inverted_index[term]:
                self.inverted_index[term][doc_id] = 1
            else:
                self.inverted_index[term][doc_id] += 1