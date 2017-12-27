#!/usr/local/bin/python
import math
import operator

#simple example, rows correspond to users, columns correspond to books, item at i,j is the given rating to book j by user i
#the users and ratings should be imported from the database
usersAndRatings = [[7,6,7,4,5,4],[6,7,0,4,3,4],[0,3,3,1,1,0],[1,2,2,3,3,4],[1,0,1,2,3,3]]
itemCount = 6
userCount = 5

#calculates pearson similarity between two users, pearson similarity is between [-1,1], when it's positive the users are positively associated, when negative they are negatively
#associated 
def pearson(user1,user2):
	nominator = 0
	denominator1=0
	denominator2=0
	common = commonRated(user1,user2)
	mean1 = mean(user1)
	mean2 = mean(user2)
	for x in range(0,len(common)):
		nominator += (usersAndRatings[user1][common[x]]-mean1)*(usersAndRatings[user2][common[x]]-mean2)
	
	for x in range(0,len(common)):
		denominator1 += math.pow((usersAndRatings[user1][common[x]]-mean1),2)
		denominator2 += math.pow((usersAndRatings[user2][common[x]]-mean2),2)
		
	return (nominator*1.0)/(math.sqrt(denominator1)*math.sqrt(denominator2))

#returns the mean of ratings of given user
def mean(user):
	sum = 0
	nonzero = 0
	for x in range(0,itemCount):
		if usersAndRatings[user][x] > 0:
			nonzero = nonzero + 1
		sum += usersAndRatings[user][x]
	return (sum*1.0)/nonzero

#returns books rated by both users given in the parameters
def commonRated(user1,user2):
	common = []
	for x in range(0,itemCount):
		if (usersAndRatings[user1][x])*(usersAndRatings[user2][x]) > 0:
			common.append(x)
	return common

#predict the rating of user for given book
def predictRating(user,book):
	mean1 = mean(user)
	nominator = 0
	denominator = 0
	similarity = 0
	for x in range(0,userCount):
		if x == user:
			continue
			
		similarity = pearson(user,x)
		if abs(similarity) > 0.85:
			nominator +=  similarity*(usersAndRatings[x][book]-mean(x))
			denominator += abs(similarity)
		
	return mean1+((nominator*1.0)/denominator)	