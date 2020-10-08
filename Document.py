
import math

class Document:
    
    def __init__(self, doc_id, title, content):
        self.doc_id = doc_id
        self.title = title
        self.content = content
    
    def get_id(self):
        """
        Method untuk mendapatkan id dari dokumen teks.
        
        :return doc_id: id dokumen teks
        :type doc_id: str
        """
        return self.doc_id
    
    def get_title(self):
        """
        Method untuk mendapatkan judul dari dokumen teks.
        
        :return title: judul dokumen teks
        :type title: str
        """
        return self.title
    
    def get_content(self):
        """
        Method untuk mendapatkan isi dari dokumen teks.
        
        :return content: isi dari dokumen teks
        :type content: str
        """
        return self.content
    
    def get_vector(self):
        """
        Method untuk mendapatkan vektor sebagai representasi dokumen teks.
        
        :return vector: vektor sebagai representasi dokumen teks
        :type vector: list
        """
        return self.vector
    
    def set_vector(self, index, corpus_size):
        """
        Method untuk membangun vektor sebagai representasi dokumen teks.
        Vektor yang digunakan berisi bobot tf-idf dari setiap term yang ada. Jika tidak ada, bobot bernilai 0.
        
        :param index: inverted index yang telah dibanung
        :type index: dict
        :param corpus_size: jumlah dokumen teks keseluruhan dalam corpus
        :type corpus_size: int
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
        
        :param other_doc: dokumen teks lain yang akan diukur jaraknya
        :type other_doc: Document.Document
        :return distance: jarak dengan other_doc
        """
        # Jika other_doc yang dibandingkan adalah dokumen teks ini sendiri.
        if other_doc.get_id() == self.doc_id:
            # Jarak antara kedua dokumen teks yang sama adalah 0.
            return 0
        
        # Mengambil vektor dari masing-masing dokumen teks.
        vector_i = self.get_vector()
        vector_j = other_doc.get_vector()
        # Fungsi nested dotProduct (untuk menghitung hasil kali dua vektor).
        def dotProduct(vector_i, vector_j):
            """
            Method untuk menghitung hasil kali titik antara dua vektor.
            
            :param vector_i: vektor pertama
            :type vector_i: list
            :param vector_j: vektor kedua
            :type vector_j: list
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