
import math

class Document:
    
    def __init__(self, doc_id, title, content):
        self.doc_id = doc_id
        self.title = title
        self.content = content
    
    def get_id(self):
        return self.doc_id
    
    def get_title(self):
        return self.title
    
    def get_content(self):
        return self.content
    
    def set_vector(self, index, corpus_size):
        dictionary = list(index.keys())
        self.vector = []
        for term in dictionary:
            weight = 0
            if self.get_id() in index[term]:
                # Pembobotan dengan tf-idf.
                weight = math.log10(index[term].count(self.get_id()) + 1) * (math.log10((corpus_size + 1) / len(set(index[term]))) / math.log10(2))
            self.vector.append(weight)
    
    def get_vector(self):
        return self.vector
    
    def count_distance(self, other_doc):
        if other_doc.get_id() == self.doc_id:
            return 0
        vector_i = self.get_vector()
        vector_j = other_doc.get_vector()
        
        # Hitung jarak antar dua Document dengan menggunakan jarak cosine.
        def dotProduct(vector_i, vector_j):
            result = 0
            for i in range(0, len(vector_i)):
                result += (vector_i[i] * vector_j[i])
            return result
        
        numerator = dotProduct(vector_i, vector_j)
        denominator = math.sqrt(dotProduct(vector_i, vector_i) *
                                dotProduct(vector_j, vector_j))
        distance = math.acos(numerator/denominator)
        return distance