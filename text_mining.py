#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:54:00 2020

@author: rahul
"""
#import libraries
import pandas as pd
import re
import heapq
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import gensim
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
import warnings
pd.set_option("display.max_colwidth", 200)
warnings.filterwarnings("ignore")
###############

# Open a file on a different location: f = open("D:\\myfiles\welcome.txt", "r")
#or directly open the file if the file is in the same location as Python
f = open("buddha.txt", "r")
print(f.readline())
text = f.read()
print("length of text:", len(text))
lines = text.splitlines()
print("number of lines:", len(lines))

#removing square brackets and extra spaces
lines = re.sub('[^a-zA-Z]', ' ', text)
lines_format = re.sub(r'\s+', ' ',lines)

#Tokenizing sentences from original text as lines & lines_format are stripped with full stop
#So sent_tokenize will not work on those variables
sentence_list = nltk.sent_tokenize(text)

#-------------------Method-1 Start finding important sentences by calculating word frequences and
### sentence scores ---------------------- ######

#Finding weighted frequence of occurance
stop = nltk.corpus.stopwords.words('english')
word_freq = {}
for word in nltk.word_tokenize(lines_format):
    if word.lower() not in stop:
        if word not in word_freq.keys():
            word_freq[word] = 1
        else:
            word_freq[word] += 1

max_freq = max(word_freq.values())
for word in word_freq.keys():
    word_freq[word] = (word_freq[word]/max_freq)

"""
calculate the scores for each sentence by adding weighted frequencies of the words that occur in that particular sentence
"""

sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_freq.keys():
            if sent not in sentence_scores.keys():
                sentence_scores[sent] = word_freq[word]
            else:
                sentence_scores[sent] += word_freq[word]

summary_sentences = heapq.nlargest(50, sentence_scores, key =sentence_scores.get)
summary = ' '.join(summary_sentences)
#print(summary)

###------- End of implementing Method-1 -------------------###########

#------ Method-2 extractive summarization using Gensim Textrank algorithm ----

summary_gen = summarize(text, ratio = 0.10)  #5 percent summary of original text

summary_gen_words = summarize(text,word_count = 500)


print("Summarised text length:", len(summary_gen))
#print("/n Summary of your uploaded text : /n {} ".format(summary_gen))
userInput = input("\n Do you wish to download the summary? (y or yes or sure for yes , n or no for no) : ").strip()
if userInput.lower() == 'y' or 'yes' or 'sure':

    with open("summaryText.txt", "w", encoding = 'utf-8') as fd:
        newLines = re.sub('[^a-zA-Z]', ' ', summary_gen)
        lines_format = re.sub(r'\s+', ' ',newLines)
        fd.write(lines_format)

        print("Your Summarised document is downloaded successfully in your current working directory! Check it out.")
        fd.close()
        
    
    
    

else:
    #print("/n Summary of your uploaded text : /n {} ".format(summary_gen))
    print("-----End of Summary, Thanks for using the application. ------")
    


#---- end of implementing Method-2 ---------- #############


