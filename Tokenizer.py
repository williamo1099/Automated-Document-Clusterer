
from nltk.tokenize import word_tokenize

class Tokenizer:
    
    def tokenize(self, sequence):
        """
        Method untuk melakukan tokenisasi terhadap char sequence.
        Char sequence adalah serangkaian kata-kata dalam sebuah dokumen teks.

        Parameters
        ----------
        sequence : string
            Sebuah char sequence dari dokumen teks.

        Returns
        -------
        result : list
            Daftar token.

        """
        # Melakukan tokenisasi dari sequence yang telah diubah menjadi huruf kecil (case folding).
        tokens = word_tokenize(sequence.lower())
        result = []
        for token in tokens:
            # Melihat apakah dalam token terdapat sebuah tanda baca.
            if token.isalpha():
                result.append(token)
            else:
                # Jika ada tanda baca, seluruh tanda baca yang ada akan dibuang.
                normalized = ''.join(char for char in token if char.isalpha())
                if normalized != '':
                    result.append(normalized)
        return result