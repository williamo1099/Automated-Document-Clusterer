
from nltk.tokenize import word_tokenize

class Tokenizer:
    
    def tokenize(self, sequence):
        """
        Method untuk melakukan tokenisasi terhadap sebuah char sequence.

        Parameters
        ----------
        sequence : str
            Sebuah char sequence.

        Returns
        -------
        result : list
            Daftar tokne.

        """
        # Melakukan tokenisasi dari sequence yang telah diubah menjadi huruf kecil (case folding).
        tokens = word_tokenize(sequence.lower())
        result = []
        for token in tokens:
            if token.isalpha():
                result.append(token)
            else:
                # Melakukan proses normalisasi.
                # Normalisasi dilakukan dengan membuang seluruh tanda baca.
                normalized = ''.join(char for char in token if char.isalpha())
                if normalized != '':
                    result.append(normalized)
        return result