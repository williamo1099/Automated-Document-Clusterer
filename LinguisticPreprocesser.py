
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer 

class LinguisticPreprocesser:
    
    def remove_stopwords(self, token_list):
        stop_list = stopwords.words('english')
        result = []
        for tokens in token_list:
            if tokens not in stop_list:
                result.append(tokens)
        return result
    
    def stem(self, token_list):
        stemmer = PorterStemmer()
        result = []
        for tokens in token_list:
            result.append(stemmer.stem(tokens))
        return result
    
    def lemmatize(self, token_list):
        lemmatizer = WordNetLemmatizer()
        result = []
        for tokens in token_list:
            result.append(lemmatizer.lemmatize(tokens))
        return result
    
    def preprocess(self, token_list):
        return self.lemmatize(self.stem(self.remove_stopwords(token_list)))