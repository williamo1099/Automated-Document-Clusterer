
import math

class Document:
    
    def __init__(self, doc_id, title, content):
        self.doc_id = doc_id
        self.title = title
        self.content = content
    
    def get_id(self):
        """
        Method untuk mendapatkan nilai atribut doc_id.
        Atribut doc_id menyimpan id dari dokumen teks.

        Returns
        -------
        doc_id : string
            Id dari dokumen teks.

        """
        return self.doc_id
    
    def get_title(self):
        """
        Method untuk mendapatkan nilai atribut title.
        Atribut title menyimpan judul dari dokumen teks.

        Returns
        -------
        title : string
            Judul dari dokumen teks.

        """
        return self.title
    
    def get_content(self):
        """
        Method untuk mendapatkan nilai atribut content.
        Atribut content menyimpan isi dari dokumen teks.

        Returns
        -------
        content : string
            Isi dari dokumen teks.

        """
        return self.content
    
    def set_content_to_empty(self):
        """
        Method untuk mengosongkan nilai atribut content.
        Dapat digunakan ketika index sudah disimpan (menandakan term-term yang ada sudah tersimpan).
        Dilakukan untuk menghemat biaya penyimpanan index karena daftar dokumen teks (beserta nilai atributnya ikut disimpan sebagai metadata).
        
        Returns
        -------
        None.

        """
        self.content = ''
    
    def get_vector(self):
        """
        Method untuk mendapatkan nilai atribut vector yang merupakan representasi dari dokumen teks.
        Vektor yang digunakan berisi bobot tf-idf dari masing-masing term yang ada.

        Returns
        -------
        vector : list
            Vektor sebagai representasi dokumen teks.

        """
        return self.vector
    
    def set_vector(self, index, corpus_size):
        """
        Method untuk menghitung vektor yang digunakan sebagai representasi dokumen teks dan disimpan sebagai nilai atribut vector.
        Proses yang dilakukan adalah menghitung bobot untuk masing-masing term.
        Jika term tidak ada dalam dokumen teks, bobotnya adalah 0.

        Parameters
        ----------
        index : dictionary
            Inverted index.
        corpus_size : int
            Jumlah seluruh dokumen teks yang ada.

        Returns
        -------
        None.

        """
        # Mengambil setiap term yang ada dalam index, diurutkan menaik menurut alphabet.
        dictionary = sorted(list(index.keys()), key=str.lower)
        self.vector = []
        for term in dictionary:
            weight = 0
            # Mengecek apakah term ada dalam dokumen teks, jika tidak ada maka bobotnya 0.
            if self.get_id() in index[term]:
                # Menghitung nilai tf ketika term ada.
                tf = math.log10(index[term][self.get_id()] + 1)
                # Menghitung nilai idf.
                idf = math.log10((corpus_size) / len(index[term]))
                # Menghitung bobot term dengan pembobotan tf-idf.
                weight = tf * idf
            self.vector.append(weight)
    
    def count_distance(self, other_doc):
        """
        Method untuk menghitung kemiripan dengan dokumen teks lain.
        Perhitungan jarak (cosine) dilakukan berdasarkan vektor representasi dokumen teks.

        Parameters
        ----------
        other_doc : Document
            Dokumen teks lain yang diukur jaraknya.

        Returns
        -------
        distance : float
            Jarak dengan other_doc.

        """
        # Jika other_doc yang dibandingkan adalah dokumen teks ini sendiri.
        if other_doc.get_id() == self.doc_id:
            return 0
        # Mengambil vektor dari kedua dokumen teks.
        vector_i = self.get_vector()
        vector_j = other_doc.get_vector()
        
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
        
        # Menghitung besar sudut antara kedua vektor tersebut dengan jarak cosine.
        numerator = dotProduct(vector_i, vector_j)
        denominator = math.sqrt(dotProduct(vector_i, vector_i) *
                                dotProduct(vector_j, vector_j))
        distance = 1 - numerator/denominator
        return distance