# Main script #
from gensim.models import Word2Vec
import pandas as pd
import logging

class line_iterator(object):
    def __init__(self, fname):
        self.fname = fname
    def __iter__(self):
        for line in open(self.fname):
            yield line.split()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
patients = line_iterator('../data/patient_walks.txt')

## 10 dimensions, skip-gram ##
model = Word2Vec(patients,size=10,min_count=1,hs=1,sg=0)
X = pd.DataFrame(model.syn0,index=model.index2word)
X.to_csv("../data/vecs/sg_10d.csv")

## 20 dimensions, skip-gram ##
model = Word2Vec(patients,size=20,min_count=1,hs=1,sg=0)
X = pd.DataFrame(model.syn0,index=model.index2word)
X.to_csv("../data/vecs/sg_20d.csv")

## 50 dimensions, skip-gram ##
model = Word2Vec(patients,size=50,min_count=1,hs=1,sg=0)
X = pd.DataFrame(model.syn0,index=model.index2word)
X.to_csv("../data/vecs/sg_50d.csv")


## 100 dimensions, skip-gram ##
model = Word2Vec(patients,size=100,min_count=1,hs=1,sg=0)
X = pd.DataFrame(model.syn0,index=model.index2word)
X.to_csv("../data/vecs/sg_100d.csv")
