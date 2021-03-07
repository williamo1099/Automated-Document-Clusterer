
from scipy.spatial.distance import cosine

import math

class Document:
    
    def __init__(self, doc_id, title, content):
        """
        The constructor for Document class.

        Parameters
        ----------
        doc_id : string
            The document's id.
        title : string
            The document's title.
        content : string
            The document's content.

        Returns
        -------
        None.

        """
        self.doc_id = doc_id
        self.title = title
        self.content = content
    
    def get_id(self):
        """
        The method to get the id of document.

        Returns
        -------
        string
            The document's id.

        """
        return self.doc_id
    
    def get_title(self):
        """
        The method to get the title of document.

        Returns
        -------
        string
            The document's title.

        """
        return self.title
    
    def get_content(self):
        """
        The method to get the content of document.

        Returns
        -------
        string
            The document's content.

        """
        return self.content
    
    def get_vector(self):
        """
        The method to get the vector as the document's representation.

        Returns
        -------
        list
            The vector as the document's representation.

        """
        return self.vector
    
    def set_vector(self, index, dictionary, corpus_size):
        """
        Build a vector as the document's representation.
        Each dimension of the vector is a term's weight.

        Parameters
        ----------
        index : dictionary
            The inverted index.
        dictionary : list
            The list of terms.
        corpus_size : int
            The size of corpus.

        Returns
        -------
        None.

        """
        self.vector = []
        for term in dictionary:
            weight = 0
            
            # Check whether a term is contained in a document.
            # If a term is not contained in a document, its weight equals to 0.
            if self.get_id() in index[term]:
                # Calculate tf weight for a term.
                tf = math.log10(index[term][self.get_id()] + 1)
                
                # Calculate idf weight for a term.
                idf = math.log10((corpus_size) / len(index[term]))
                    
                # Calculate tf-idf weight for a term.
                weight = tf * idf
            self.vector.append(weight)
    
    def calc_distance(self, other_doc):
        """
        A method to calculate the cosine distance between two documents.

        Parameters
        ----------
        other_doc : Document
            Another document to compare.

        Returns
        -------
        distance : float
            The cosine distance between two documents.

        """
        # Check whether the other document is the same document as this.
        # If two documents are equal, the distance is set to 0.
        if other_doc.get_id() == self.doc_id:
            return 0
        
        # Get vectors of two documents and count distance between those two vectors.
        vector_i = self.vector
        vector_j = other_doc.get_vector()
        return cosine(vector_i, vector_j)