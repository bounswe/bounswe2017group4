#!/usr/local/bin/python
import math
import operator

usersAndRatings = [[7,6,7,4,5,4],[6,7,0,4,3,4],[0,3,3,1,1,0],[1,2,2,3,3,4],[1,0,1,2,3,3]]
itemCount = 6
userCount = 5


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
	
def mean(user):
	sum = 0
	nonzero = 0
	for x in range(0,itemCount):
		if usersAndRatings[user][x] > 0:
			nonzero = nonzero + 1
		sum += usersAndRatings[user][x]
	return (sum*1.0)/nonzero
	
def commonRated(user1,user2):
	common = []
	for x in range(0,itemCount):
		if (usersAndRatings[user1][x])*(usersAndRatings[user2][x]) > 0:
			common.append(x)
	return common