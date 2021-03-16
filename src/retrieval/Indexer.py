
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class Indexer:
    
    def __init__(self, inverted_index=None):
        """
        The constructor for Indexer class.
        
        Parameters
        ----------
        inverted_index : dict
            The inverted index. The default is None.

        Returns
        -------
        None.

        """
        if inverted_index is not None:
            self.inverted_index = inverted_index
        else:
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
        
    class LinguisticPreprocessor:
        
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
            extended_stop_list = ['a', 'able', 'about', 'above', 'abst', 'accordance', 'according', 'accordingly', 'across', 'act', 'actually', 'added', 'adj', 'affected', 'affecting', 'affects', 'after', 'afterwards', 'again', 'against', 'ah', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apparently', 'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'at', 'auth', 'available', 'away', 'awfully', 'b', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings', 'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'biol', 'both', 'brief', 'briefly', 'but', 'by', 'c', 'ca', 'came', 'can', 'cannot', "can't", 'cause', 'causes', 'certain', 'certainly', 'co', 'com', 'come', 'comes', 'contain', 'containing', 'contains', 'could', 'couldnt', 'd', 'date', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', 'done', "don't", 'down', 'downwards', 'due', 'during', 'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'especially', 'et', 'et-al', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'except', 'f', 'far', 'few', 'ff', 'fifth', 'first', 'five', 'fix', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'found', 'four', 'from', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'gone', 'got', 'gotten', 'h', 'had', 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 'hers', 'herself', 'hes', 'hi', 'hid', 'him', 'himself', 'his', 'hither', 'home', 'how', 'howbeit', 'however', 'hundred', 'i', 'id', 'ie', 'if', "i'll", 'im', 'immediate', 'immediately', 'importance', 'important', 'in', 'inc', 'indeed', 'index', 'information', 'instead', 'into', 'invention', 'inward', 'is', "isn't", 'it', 'itd', "it'll", 'its', 'itself', "i've", 'j', 'just', 'k', 'keep\tkeeps', 'kept', 'kg', 'km', 'know', 'known', 'knows', 'l', 'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets', 'like', 'liked', 'likely', 'line', 'little', "'ll", 'look', 'looking', 'looks', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg', 'might', 'million', 'miss', 'ml', 'more', 'moreover', 'most', 'mostly', 'mr', 'mrs', 'much', 'mug', 'must', 'my', 'myself', 'n', 'na', 'name', 'namely', 'nay', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'ninety', 'no', 'nobody', 'non', 'none', 'nonetheless', 'noone', 'nor', 'normally', 'nos', 'not', 'noted', 'nothing', 'now', 'nowhere', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'omitted', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'ord', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'owing', 'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp', 'predominantly', 'present', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'put', 'q', 'que', 'quickly', 'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really', 'recent', 'recently', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively', 'resulted', 'resulting', 'results', 'right', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'sec', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sent', 'seven', 'several', 'shall', 'she', 'shed', "she'll", 'shes', 'should', "shouldn't", 'show', 'showed', 'shown', 'showns', 'shows', 'significant', 'significantly', 'similar', 'similarly', 'since', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'somethan', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specifically', 'specified', 'specify', 'specifying', 'still', 'stop', 'strongly', 'sub', 'substantially', 'successfully', 'such', 'sufficiently', 'suggest', 'sup', 'sure\tt', 'take', 'taken', 'taking', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', "that'll", 'thats', "that've", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'thered', 'therefore', 'therein', "there'll", 'thereof', 'therere', 'theres', 'thereto', 'thereupon', "there've", 'these', 'they', 'theyd', "they'll", 'theyre', "they've", 'think', 'this', 'those', 'thou', 'though', 'thoughh', 'thousand', 'throug', 'through', 'throughout', 'thru', 'thus', 'til', 'tip', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'ts', 'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', "'ve", 'very', 'via', 'viz', 'vol', 'vols', 'vs', 'w', 'want', 'wants', 'was', 'wasnt', 'way', 'we', 'wed', 'welcome', "we'll", 'went', 'were', 'werent', "we've", 'what', 'whatever', "what'll", 'whats', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whim', 'whither', 'who', 'whod', 'whoever', 'whole', "who'll", 'whom', 'whomever', 'whos', 'whose', 'why', 'widely', 'willing', 'wish', 'with', 'within', 'without', 'wont', 'words', 'world', 'would', 'wouldnt', 'www', 'x', 'y', 'yes', 'yet', 'you', 'youd', "you'll", 'your', 'youre', 'yours', 'yourself', 'yourselves', "you've", 'z', 'zero']
            result = []
            for token in token_list:
                
                # Check whether a token is a stop word or not.
                # If a token is a stop word, the token will be removed.
                if token not in stop_list and token not in extended_stop_list:
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
    
    def preprocess(self, document, stopwords_removal=True, stemming=True, case_folding=True, normalization=True):
        """
        The method to get a list of terms in a document.
        Each term is a result of linguistic preprocessing of each tokens in the document.

        Parameters
        ----------
        document : Document
            The document.
        stopwords_removal : boolean
            The stopwords removal status (if true, stopwords removal step will be done). The default is True.
        stemming : boolean
            The stemming status (if true, stemming step will be done). The default is True.
        case_folding : boolean
            The case folding status (if true, case folding step will be done). The default is True.
        normalization : boolean
            The normalization status (if true, normalization step will be done). The default is True.

        Returns
        -------
        dictionary : list
            The list of terms in the document.

        """
        # Do tokenization process.
        token_list = self.Tokenizer.tokenize(document.get_content())
        
        # Do linguistic preprocessing (stop words removal, stemming, case folding and normalization).
        dictionary = []
        if stopwords_removal is True:
            dictionary = self.LinguisticPreprocessor.remove_stopwords(token_list)
        
        if stemming is True:
            if dictionary == []:
                dictionary = self.LinguisticPreprocessor.stem(token_list)
            dictionary = self.LinguisticPreprocessor.stem(dictionary)
        
        if case_folding is True:
            if dictionary == []:
                dictionary = self.LinguisticPreprocessor.case_fold(token_list)
            dictionary = self.LinguisticPreprocessor.case_fold(dictionary)
        
        if normalization is True:
            if dictionary == []:
                dictionary = self.LinguisticPreprocessor.normalize(token_list)
            dictionary = self.LinguisticPreprocessor.normalize(dictionary)
        
        if dictionary != []:
            return dictionary
        else:
            return token_list
    
    def index(self, document, stopwords_removal=True, stemming=True, case_folding=True, normalization=True):
        """
        The method to build an inverted index.

        Parameters
        ----------
        document : Document
            The document.
        stopwords_removal : boolean
            The stopwords removal status (if true, stopwords removal step will be done). The default is True.
        stemming : boolean
            The stemming status (if true, stemming step will be done). The default is True.
        case_folding : boolean
            The case folding status (if true, case folding step will be done). The default is True.
        normalization : boolean
            The normalization status (if true, normalization step will be done). The default is True.


        Returns
        -------
        None.

        """
        # Get the list of terms in a document.
        dictionary = self.preprocess(document, stopwords_removal=True, stemming=True, case_folding=True, normalization=True)
        
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