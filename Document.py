
import math
import numpy as np

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
    
    def set_weighting_list(self, index, corpus_size):
        dictionary = list(index.keys())
        weighting_list = []
        for term in dictionary:
            weight = 0
            if self.get_id() in index[term]:
                # Pembobotan dengan tf-idf.
                weight = math.log10(index[term].count(self.get_id()) + 1) * (math.log10((corpus_size + 1) / len(set(index[term]))) / math.log10(2))
            weighting_list.append(weight)
        self.weighting_list = weighting_list
    
    def get_weighting_list(self):
        return self.weighting_list
    
    def count_distance(self, other_doc):
        if other_doc.get_id() == self.doc_id:
            return 0
        weighting_list_i = self.get_weighting_list()
        weighting_list_j = other_doc.get_weighting_list()
        # Hitung jarak antar dua Document dengan menggunakan jarak cosine.
        distance = math.acos(np.dot(weighting_list_i, weighting_list_j) / (math.sqrt(np.dot(weighting_list_i, weighting_list_i) * np.dot(weighting_list_j, weighting_list_j))))
        return distance