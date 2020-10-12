
import math

class Document:
    
    def __init__(self, doc_id, title, content):
        self.doc_id = doc_id
        self.title = title
        self.content = content
    
    def get_id(self):
        """
        Method untuk mendapatkan id dari dokumen teks.

        Returns
        -------
        doc_id : str
            Id dari dokumen teks.

        """
        return self.doc_id
    
    def get_title(self):
        """
        Method untuk mendapatkan judul dari dokumen teks.

        Returns
        -------
        title : str
            Judul dari dokumen teks.

        """
        return self.title
    
    def get_content(self):
        """
        Method untuk mendapatkan isi dari dokumen teks.

        Returns
        -------
        content : str
            Isi dari dokumen teks.

        """
        return self.content
    
    def get_vector(self):
        """
        Method untuk mendapatkan vektor sebagai representasi dokumen teks.

        Returns
        -------
        vector : list
            Vektor sebagai representasi dokumen teks.

        """
        return self.vector
    
    def set_vector(self, index, corpus_size):
        """
        Method untuk membangun vektor sebagai representasi dokumen teks.
        Vektor yang digunakan berisi bobot tf-idf dari setiap term yang ada. Jika tidak ada, bobot bernilai 0.

        Parameters
        ----------
        index : dict
            Inverted index yang menyimpan pemetaan term ke lokasi term tersebut berada.
        corpus_size : int
            Jumlah seluruh dokumen teks yang ada dalam corpus.

        Returns
        -------
        None.

        """
        dictionary = sorted(list(index.keys()), key=str.lower)
        self.vector = []
        for term in dictionary:
            weight = 0
            if self.get_id() in index[term]:
                # Pembobotan term dengan bobot tf-idf.
                weight = (math.log10(index[term][self.get_id()] + 1)) * (math.log10((corpus_size) / len(index[term])))
            self.vector.append(weight)
    
    def count_distance(self, other_doc):
        """
        Method untuk menghitung kemiripan dengan dokumen teks lain.
        Perhitungan jarak (cosine) dilakukan berdasarkan vektor representasi dokumen teks.

        Parameters
        ----------
        other_doc : Document.Document
            Dokumen teks lain yang akan diukur jaraknya.

        Returns
        -------
        float
            Jarak dengan other_doc.

        """
        # Jika other_doc yang dibandingkan adalah dokumen teks ini sendiri.
        if other_doc.get_id() == self.doc_id:
            return 0
        
        # Mengambil vektor dari masing-masing dokumen teks.
        vector_i = self.get_vector()
        vector_j = other_doc.get_vector()
        
        # Fungsi nested dotProduct (untuk menghitung hasil kali dua vektor).
        def dotProduct(vector_i, vector_j):
            """
            Method untuk menghitung hasil kali titik (dot product) antara dua vektor.

            Parameters
            ----------
            vector_i : list
                Vektor pertama.
            vector_j : list
                Vektor kedua.

            Returns
            -------
            result : float
                Hasil kali titik antara vector_i dan vector_j.

            """
            result = 0
            for i in range(0, len(vector_i)):
                result += (vector_i[i] * vector_j[i])
            return result
        
        # Menghitung jarak antara dua vektor dengan menggunakan jarak cosine.
        numerator = dotProduct(vector_i, vector_j)
        denominator = math.sqrt(dotProduct(vector_i, vector_i) *
                                dotProduct(vector_j, vector_j))
        distance = math.acos(numerator/denominator)
        return distance