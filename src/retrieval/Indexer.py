
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class Indexer:
    
    def __init__(self):
        """
        The constructor for Indexer class.

        Returns
        -------
        None.

        """
        self.inverted_index = {}
        
    class Tokenizer:
        
        @staticmethod
        def tokenize(sequence):
            """
            The method to tokenize a character sequence into a list of tokens.

            Parameters
            ----------
            sequence : string
                The character sequence to be tokenized.

            Returns
            -------
            result : list
                The list of tokens.

            """
            return word_tokenize(sequence)
        
    class LinguisticPreprocesser:
        
        @staticmethod
        def remove_stopwords(token_list):
            """
            The method to remove stop words from a list of tokens.
            Language supported is English.

            Parameters
            ----------
            token_list : list
                The list of tokens.

            Returns
            -------
            result : list
                The list of terms (list of tokens without stop words).

            """
            stop_list = stopwords.words('english')
            result = []
            for token in token_list:
                
                # Check whether a token is a stop word or not.
                # If a token is a stop word, the token will be removed.
                if token not in stop_list:
                    result.append(token)
            return result
    
        @staticmethod
        def stem(token_list):
            """
            The method to stem all tokens in a list of tokens.
            Technique used is suffix-stripping technique, with Porter stemming algorithm.
            Language supported is English.

            Parameters
            ----------
            token_list : list
                The list of tokens.

            Returns
            -------
            result : list
                The list of terms (list of stemmed tokens).

            """
            stemmer = PorterStemmer()
            result = []
            for token in token_list:
                stemmed = stemmer.stem(token)
                result.append(stemmed)
            return result
        
        @staticmethod
        def case_fold(token_list):
            """
            The method to case fold all tokens in a list of tokens.
            
            Parameters
            ----------
            token_list : list
                The list of tokens.

            Returns
            -------
            result : list
                The list of terms (list of lowered tokens).

            """
            result = []
            for token in token_list:
                result.append(token.lower())
            return result
        
        @staticmethod
        def normalize(token_list):
            """
            The method to normalize all tokens in a list of tokens.

            Parameters
            ----------
            token_list : list
                The list of tokens.

            Returns
            -------
            result : list
                The list of terms (list of normalized tokens).

            """
            result = []
            for token in token_list:
                normalized_token = ''.join(char for char in token if char.isalpha())
                if normalized_token != '':
                    result.append(normalized_token)
            return result
    
    def get_inverted_index(self):
        """
        The method to get inverted index built by method index.

        Returns
        -------
        dictionary
            The inverted index built.
            Written as {term1: {doc1: freq, doc2: freq}, term2: {doc1: freq}, etc.}.

        """
        return self.inverted_index
    
    def preprocess(self, document):
        """
        The method to get a list of terms in a document.
        Each term is a result of linguistic preprocessing of each tokens in the document.

        Parameters
        ----------
        document : Document
            The document.

        Returns
        -------
        dictionary : list
            The list of terms in the document.

        """
        # Do tokenization process.
        token_list = self.Tokenizer.tokenize(document.get_content())
        
        # Do linguistic preprocessing (stop words removal, stemming, case folding and normalization).
        dictionary = self.LinguisticPreprocesser.normalize(
                    self.LinguisticPreprocesser.case_fold(
                    self.LinguisticPreprocesser.stem(
                    self.LinguisticPreprocesser.remove_stopwords(token_list))))
        return dictionary
    
    def index(self, document):
        """
        The method to build an inverted index.

        Parameters
        ----------
        document : Document
            The document.

        Returns
        -------
        None.

        """
        # Get the list of terms in a document.
        dictionary = self.preprocess(document)
        
        # Get the document's id.
        doc_id = document.get_id()
        for term in dictionary:
            
            # Check whether a term is already stored in the index.
            # If a term is not stored yet, the term will be stored as a new key in the index.
            if term not in self.inverted_index:
                self.inverted_index[term] = {}
                
            # Check whether the document is stored in the posting list.
            # If the document is not stored yet, the frequency will be set to 1.
            # If the document is stored already, the frequency will be set to the previous frequency + 1.
            if doc_id not in self.inverted_index[term]:
                self.inverted_index[term][doc_id] = 1
            else:
                self.inverted_index[term][doc_id] += 1