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
		
	

#Example Usage
corpus=[] 
#books
user1_books = ("computer architecture and cpu design and embedded systems computer architecture and cpu design and embedded systems computer architecture and cpu design and embedded systems"); # String of last 100 books  
user2_books = ("rock n roll music"); 
user3_books = ("deep learning and neural networks");
user4_books = ("age of technology"); 
user5_books = ("political science"); 
user6_books = ("embedded systems and internet of things"); 
user7_books = ("embbeded design"); # String of last 100 books  
user8_books = ("jazz music"); 
user9_books = ("convolutional neural networks");
user10_books = ("developments in technology"); 
user11_books = ("political debate"); 
user12_books = ("embedded system design"); 
user13_books = ("computer architecture and cpu design and embedded systems"); # String of last 100 books  
user14_books = ("rock n roll music"); 
user15_books = ("deep learning and neural networks");
user16_books = ("age of technology"); 
user17_books = ("political science"); 
user18_books = ("embedded systems and internet of things"); 
user19_books = ("embbeded design"); # String of last 100 books  
user20_books = ("jazz music"); 
user21_books = ("convolutional neural networks");
user22_books = ("developments in technology"); 
user23_books = ("political debate"); 
user24_books = ("political debates relating internet and technology"); 

#Generate Corpus
corpus.append(user1_books);
corpus.append(user2_books);
corpus.append(user3_books);
corpus.append(user4_books);
corpus.append(user5_books);
corpus.append(user6_books);
corpus.append(user7_books);
corpus.append(user8_books);
corpus.append(user9_books);
corpus.append(user10_books);
corpus.append(user11_books);
corpus.append(user12_books);
corpus.append(user13_books);
corpus.append(user14_books);
corpus.append(user15_books);
corpus.append(user16_books);
corpus.append(user17_books);
corpus.append(user18_books);
corpus.append(user19_books);
corpus.append(user20_books);
corpus.append(user21_books);
corpus.append(user22_books);
corpus.append(user23_books);
corpus.append(user24_books);


#Ratings for each user
# 0 for unrated profiles
ratings = np.array([5,1,3,3,1,5,5,1,3,3,1,5,5,1,3,3,1,5,5,1,3,3,1,0]);
#Initialize 
init_sim(corpus,ratings);
# Compute similarities
print(cos_sim());




