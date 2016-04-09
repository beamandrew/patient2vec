# Main script #
from gensim.models import Word2Vec
import logging

class line_iterator(object):
    def __init__(self, fname):
        self.fname = fname
    def __iter__(self):
        for line in open(self.fname):
            yield line.split()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
patients = line_iterator('../data/patient_walks.txt')
model = Word2Vec(patients,size=10)
