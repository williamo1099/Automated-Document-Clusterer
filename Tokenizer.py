
from nltk.tokenize import word_tokenize

class Tokenizer:
    
    def tokenize(self, sequence):
        tokens = word_tokenize(sequence.lower()) # Case folding and tokenizing.
        result = []
        for token in tokens:
            if token.isalpha():
                result.append(token)
            else:
                # Normalization.
                normalized = ''.join(char for char in token if char.isalpha())
                if normalized != '':
                    result.append(normalized)
        return result
        # return [token for token in tokens if token.isalpha()]