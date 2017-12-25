from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import numpy as np
import math
import pandas as pd
import matplotlib as mpl
import matplotlib.pylab as plt

	
corpus = [];
ratings= [];
user_profile = [];
tf = TfidfVectorizer(analyzer='word', ngram_range=(1,1), min_df = 0, stop_words = 'english');
document_matrix=[];
def init_sim(corpus,ratings):
	corpus = corpus;
	ratings = ratings;
	get_user_profile();

	
def cos_sim():
	return document_matrix*np.transpose(user_profile[0])
	
	
def get_user_profile():
	global user_profile
	global document_matrix
	tfidf_matrix =  tf.fit_transform(corpus);
	user_profile =  tfidf_matrix.multiply(ratings[:, np.newaxis]).sum(axis=0);
	norm = np.linalg.norm(user_profile);
	user_profile = user_profile/norm;
	tfidf_matrix = tfidf_matrix.todense();
	document_matrix = tfidf_matrix;
	
def get_tf_idf_matrix():
		return document_matrix;
		
	



