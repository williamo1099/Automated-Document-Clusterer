
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class LinguisticPreprocesser:
    
    def remove_stopwords(self, token_list):
        """
        Method untuk membuang token yang merupakan stop words.
        Daftar stop words adalah stop words dalam bahasa Inggris.

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
        for token in token_list:
            # Melihat apakah token termasuk sebuah stop words.
            if token not in stop_list:
                result.append(token)
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
        for token in token_list:
            # Melakukan proses stemming terhadap token.
            stemmed = stemmer.stem(token)
            result.append(stemmed)
        return result
    
    def preprocess(self, token_list):
        """
        Method untuk melakukan keseluruhan pre-pemrosesan linguistik.

        Parameters
        ----------
        token_list : list
            Daftar token.

        Returns
        -------
        result : list
            Daftar term.

        """
        return self.stem(self.remove_stopwords(token_list))