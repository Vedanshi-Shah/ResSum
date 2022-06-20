from sentence_graph import SentenceGraph
from utils import *
from sklearn.cluster import SpectralClustering
import torch
import nltk.data
from nltk.tokenize import sent_tokenize, word_tokenize
# T5_PATH = "t5-large"
# t5_model = T5ForConditionalGeneration.from_pretrained(T5_PATH)
# t5_tokenizer = T5Tokenizer.from_pretrained(T5_PATH)
from fastT5 import get_onnx_model, get_onnx_runtime_sessions, OnnxT5
from transformers import T5Config,AutoTokenizer
from pathlib import Path
import os

trained_model_path = './t5-large'

pretrained_model_name = Path(trained_model_path).stem

encoder_path = os.path.join(trained_model_path, f"{pretrained_model_name}-encoder-quantized.onnx")
decoder_path = os.path.join(trained_model_path, f"{pretrained_model_name}-decoder-quantized.onnx")
init_decoder_path = os.path.join(trained_model_path, f"{pretrained_model_name}-init-decoder-quantized.onnx")

model_paths = encoder_path, decoder_path, init_decoder_path
model_sessions = get_onnx_runtime_sessions(model_paths)
t5_model = OnnxT5(trained_model_path, model_sessions)

t5_tokenizer = AutoTokenizer.from_pretrained(trained_model_path)
class SummPip():
    def __init__(self, nb_clusters,nb_words):
        """
        This is the SummPip class

        :param nb_clusters: this determines the number of sentences in the output summary
        :param nb_words: this controls the length of each sentence in the output summary
        :param ita: threshold for determining whether two sentences are similar by vector similarity
        :param seed: the random state to reproduce summarization
        :param w2v_file: file for storing w2v matrix
        :param lm_path: path for langauge model
        :param use_lm: use language model or not 
        """

        self.nb_clusters = nb_clusters
        self.nb_words = nb_words
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

        # set seed
        torch.manual_seed(88)
        torch.cuda.manual_seed(88)

    def construct_sentence_graph(self, sentences_list):
        """
		Construct a sentence graph

		:return: adjacency matrix 
        """

        graph = SentenceGraph(sentences_list)
        X = graph.build_sentence_graph()
        return X
    def cluster_graph(self, X, sentences_list):
        """
		Perform graph clustering

		:return: a dictionary with key, value pairs of cluster Id and sentences
        """
         # ???? n
        clustering = SpectralClustering(n_clusters = self.nb_clusters, random_state = 88).fit(X)
        clusterIDs = clustering.labels_
        #print('Cluster Id',clusterIDs)
        num_clusters = max(clusterIDs)+1
        cluster_dict={new_list:[] for new_list in range(num_clusters)}
		# group sentences by cluster ID
        for i, clusterID in enumerate(clusterIDs):
            cluster_dict[clusterID].append(sentences_list[i])
        return cluster_dict
    def split_sentences(self, docs):
        tag="story_separator_special_tag"
        src_list = []
        for doc in docs:
            doc = doc.replace(tag,"")
            sent_list = sent_tokenize(doc)
            src_list.append(sent_list)
        return src_list
    def summarize(self, src_list):
        """
		Construct a graph, run graph clustering, compress each cluster, then concatenate sentences

		:param src_list: a list of input documents each of whose elements is a list of multiple documents
		:return: a list of summaries
        """
        #TODO: split sentences
        summary_list = []
        # iterate over all docs
        # for idx, sentences_list in enumerate(src_list):
        sentences_list = src_list[0]
        num_sents = len(sentences_list)
        # handle short doc
        if num_sents <= self.nb_clusters:
            summary_list.append(" ".join(sentences_list))
            print("continue----")
        X = self.construct_sentence_graph(sentences_list)
        cluster_dict = self.cluster_graph(X, sentences_list)
        # print("-----------------------------------------")
        # print(cluster_dict)
        # print("-----------------------------------------")
        for num, text in cluster_dict.items():
            cluster_dict[num] = ' '.join(text)
        # final_dict = {}
            # summary = self.compress_cluster(cluster_dict)
            # summary_list.append(summary)
        return cluster_dict
    def t5(self, cluster_dict):
        final_dict = {}
        for num, sents in cluster_dict.items():
            inputs = t5_tokenizer.encode("summarize: " + sents, return_tensors="pt", max_length=512, padding="max_length", truncation=True)
            summary_ids = t5_model.generate(inputs, num_beams=int(2),no_repeat_ngram_size=3,length_penalty=2.0,min_length=50,max_length=500,early_stopping=True)
            output = t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
            final_dict[num] = output
        summary = ""
        # for num, text in final_dict.items():
        #     summary += text + " "
        summary = ' '.join([n.strip().capitalize() for n in final_dict.values()])
        return summary