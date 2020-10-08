
from Tokenizer import Tokenizer
from LinguisticPreprocesser import LinguisticPreprocesser

class Indexer:
    
    def __init__(self):
        self.inverted_index = {}
        
    def get_inverted_index(self):
        """
        Method untuk mendapatkan inverted index yang telah dibangun.
        
        :return inverted_index: inverted index
        :type inverted_index: dict
        """
        return self.inverted_index
    
    def preprocess(self, document):
        """
        Method untuk mengambil daftar term dari dokumen teks.
        Proses yang dilakukan adalah tokenizing dan linguistic preprocessing.
        
        :param document: dokumen teks
        :type document: Document.Document
        :return dictionary: daftar term dalam dokumen teks
        :type dictionary: list
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
        
        :param document: dokumen teks
        :type document: Document.Document
        """
        # Mengambil id dari dokumen teks.
        doc_id = document.get_id()
        # Mengambil daftar term dari dokumen teks.
        dictionary = self.preprocess(document)
        
        for term in dictionary:
            # Jika term belum ada dalam inverted index.
            if term not in self.inverted_index:
                # Membuat key term tersebut dan menyiapkan sebuah dictionary kosong.
                # Dictionary kosong digunakan untuk menyimpan daftar dokumen teks yang mengandung term terkait dan frekuensi kemunculannya.
                self.inverted_index[term] = {}
            
            # Jika dokumen teks belum tersimpan dalam dictionary term tersebut.
            if doc_id not in self.inverted_index[term]:
                # Menyimpan frekuensi kemunculan term dalam dokumen teks sebagai 1.
                self.inverted_index[term][doc_id] = 1
            else:
                # Menambah 1 frekuensi kemunculan term dalam dokumen teks.
                self.inverted_index[term][doc_id] += 1