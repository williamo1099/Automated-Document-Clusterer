
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer 

class LinguisticPreprocesser:
    
    def remove_stopwords(self, token_list):
        """
        Method untuk membuang token yang merupakan stop words.
        Daftar stop words adalah stop words dalam bahasa Inggris yang didapatkan dari nltk.corpus.stopwords.

        Parameters
        ----------
        token_list : list
            Daftar token.

        Returns
        -------
        result : list
            Daftar token setelah pembuangan stop words.

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

        Parameters
        ----------
        token_list : list
            Daftar token.

        Returns
        -------
        result : list
            Daftar token yang telah di-stem.

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

        Parameters
        ----------
        token_list : list
            Daftar token.

        Returns
        -------
        result : list
            Daftar term yang didapatkan.

        """
        return self.stem(self.remove_stopwords(token_list))