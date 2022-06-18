from summarizer import SummPip
import sys
def trial(filename):
    text = open(filename, "r",encoding='utf-8').read()
    docs = [text]
    pipe = SummPip(nb_clusters = 10, nb_words = 15)
    src_list = pipe.split_sentences(docs)
    final_dict = pipe.summarize(src_list)
    summary = pipe.t5(final_dict)
    return summary

