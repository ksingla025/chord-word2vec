import sys
import codecs
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
 
 
def main():
 
    embeddings_file = sys.argv[1]
    wv, vocabulary = load_embeddings(embeddings_file)
 
    tsne = TSNE(n_components=2, random_state=0)
 #   np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(wv)
 
    plt.scatter(Y[:, 0], Y[:, 1])
    for label, x, y in zip(vocabulary, Y[:, 0], Y[:, 1]):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.savefig(sys.argv[2])
 
 
def load_embeddings(file_name):
 
        f_in = open(file_name,'r').readlines()

        vocabulary = []
        wv = []
        for i in range(0,len(f_in)):
#            print(f_in[i])
            line = f_in[i].strip().split(" ")
            if len(line) == 201:
                vector = [float(x) for x in line[1:]]
#                print(len(vector))
                wv.append(vector)
                vocabulary.append(line[0])
#        vocabulary, wv = zip(*[line.strip().split(' ', 1) for line in 
#f_in])
        print(vocabulary)
        print(wv)

        wv = np.array(wv)
        print(wv.shape)
        return wv, vocabulary
 
if __name__ == '__main__':
    main()
