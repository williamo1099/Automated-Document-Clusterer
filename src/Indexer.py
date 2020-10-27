
from Tokenizer import Tokenizer
from LinguisticPreprocesser import LinguisticPreprocesser

class Indexer:
    
    def __init__(self):
        self.inverted_index = {}
        
    def get_inverted_index(self):
        """
        Method untuk mendapatkan nilai atribut inverted_index, yang merupakan indeks yang telah dibangun.
        Inverted index menyimpan pemetaan term ke lokasi term tersebut berada.

        Returns
        -------
        inverted_index : dictionary
            Inverted index.
            Ditulis sebagai {term1: {doc1: freq, doc2: freq}, term2: {doc1: freq}}.

        """
        return self.inverted_index
    
    def preprocess(self, document):
        """
        Method untuk mengambil daftar term dari dokumen teks.
        Proses yang dilakukan adalah proses tokenisasi dan pre-pemrosesan linguistik.

        Parameters
        ----------
        document : Document
            Dokumen teks.

        Returns
        -------
        dictionary : list
            Daftar term yang ada dalam dokumen teks.

        """
        # Melakukan proses tokenisasi.
        tokenizer = Tokenizer()
        token_list = tokenizer.tokenize(document.get_content())
        # Melakukan pre-pemrosesan linguistik (stop words removal, stemming).
        preprocesser = LinguisticPreprocesser()
        dictionary = preprocesser.preprocess(token_list)
        return dictionary
    
    def index(self, document):
        """
        Method untuk membangun inverted index dan menyimpannya sebagai nilai atribut inverted_index.
        Pembangunan inverted index dilakukan untuk sebuah dokumen teks (satu per satu).
        Inverted index yang dibangun ditulis sebagai {term1: {doc1: freq, doc2: freq}, term2: {doc1: freq}}.

        Parameters
        ----------
        document : Document
            Dokumen teks.

        Returns
        -------
        None.

        """
        # Mendapatkan daftar term dari dokumen teks.
        dictionary = self.preprocess(document)
        # Mengambil id dari dokumen teks.
        doc_id = document.get_id()
        for term in dictionary:
            # Melihat apakah term ada dalam inverted index.
            if term not in self.inverted_index:
                # Jika term belum ada, dibuat key baru dalam index.
                # Sebuah key berisi dictionary kosong, untuk menyimpan dokumen teks dan frekuensinya.
                # Contohnya, {doc1 : 1, doc2 : 3}.
                self.inverted_index[term] = {}
            # Melihat apakah sebuah dokumen teks sudah tercatat dalam daftar posting index.
            if doc_id not in self.inverted_index[term]:
                # Jika belum ada, init frekuensinya 1.
                self.inverted_index[term][doc_id] = 1
            else:
                # Jika sudah ada, frekuensinya ditambah sebesar 1.
                self.inverted_index[term][doc_id] += 1