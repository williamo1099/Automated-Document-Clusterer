
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class LinguisticPreprocesser:
    
    def remove_stopwords(self, token_list):
        """
        Method untuk membuang token yang merupakan stop words.
        Daftar stop words adalah stop words dalam Bahasa Inggris yang didapatkan dari nltk.corpus.stopwords.
        
        :param token_list: daftar token
        :type token_list: list
        :return result: daftar token setelah pembuangan stop words
        :type result: list
        """
        stop_list = stopwords.words('english')
        result = []
        for tokens in token_list:
            if tokens not in stop_list:
                result.append(tokens)
        return result
    
    def stem(self, token_list):
        """
        Method untuk melakukan stemming terhadap setiap token.
        Proses stemming yang dilakukan menggunakan algoritma Porter.
        
        :param token_list: daftar token
        :type token_list: list
        :return result: daftar token yang telah di-stem
        :type result: list
        """
        stemmer = PorterStemmer()
        result = []
        for tokens in token_list:
            result.append(stemmer.stem(tokens))
        return result
    
    def preprocess(self, token_list):
        """
        Method untuk melakukan proses linguistic preprocessing secara keseluruhan.
        Linguistic preprocessing yang dilakukan adalah proses pembuangan stop words dan stemming.
        
        :param token_list: daftar token
        :type token_list: list
        :return result: daftar term yang didapatkan
        :type result: list
        """
        result = self.stem(self.remove_stopwords(token_list))
        return result