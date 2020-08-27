
import os

from Document import Document
from Indexer import Indexer
from Clusterer import Clusterer

path = 'Document/'
doc_titles = []
for root, directories, files in os.walk(path):
    for file in files:
        if '.txt' in file:
            doc_titles.append(os.path.join(root, file))

if len(doc_titles) > 1:
    corpus = []
    for i in range(0, len(doc_titles)):
        doc_id = 'doc_' + str(i)
        doc_content = open(doc_titles[i], 'r').read().replace('\n', '')
        doc_i = Document(doc_id, os.path.splitext(doc_titles[i])[0].replace(path, ''), doc_content)
        corpus.append(doc_i)
    
    # Build an inverted index.
    indexer = Indexer()
    for i in range(0, len(corpus)):
        indexer.index(corpus[i])
    index = indexer.get_inverted_index(len(corpus))
    
    # Do document clustering.
    clusterer = Clusterer()
    clusterer.cluster(index, corpus)