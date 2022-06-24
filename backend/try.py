import gensim.downloader as api
vec = api.load("glove-wiki-gigaword-100")
vec.save('vectors.bin')