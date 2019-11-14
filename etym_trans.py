import sys
import nltk
import string
from nltk.corpus import wordnet as wn
import urllib2
from lxml import html
from lxml import etree
import requests
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

def reader(input_text):
  f_in = open(input_text)
  text = f_in.readlines()
  text_list = []
  for line in text:
    sub_list = line.rstrip().split(" ")
    for word in sub_list:
      word = word.translate(None, string.punctuation)
      text_list.append(word)
  #text_list = [item for sublist in text_list for item in sublist]
  return text_list


def syn(word):
  syns_set = list(wn.synsets(word))
  synonyms = []
  for syns in syns_set:
    for j in range(len(syns.lemma_names()) - 1):
      name = syns.lemma_names()[j + 1]
      synonyms.append(name)
  return synonyms

def etym_parse(word):
  stem_word = wnl.lemmatize(word)
  page = requests.get('http://www.etymonline.com/index.php?term=' + stem_word)
  tree = html.fromstring(page.content)
  dictionary = tree.xpath('//div[@id="dictionary"]')
  for thing in dictionary:
    etym = etree.tostring(thing, pretty_print=True)
  return etym

def check_etym(word):
  text = etym_parse(word)
  G = text.find("German")
  L = text.find("Latin")
  if(G > 0 and L > 0):
    if (G < L):
      return "German"
    else:
      return "Latin"
  elif (G > 0):
    return "German"
  elif (L > 0):
    return "Latin"
  else:
    return "None"

def translator(word, lang):
  if (lang == "Latin"):
    lang2 = "German"
  elif (lang == "German"):
    lang2 = "Latin"
  if (check_etym(word) == lang2):
    stem_word = wnl.lemmatize(word)
    syns = syn(stem_word)
    for s in syns:
      if (check_etym(s) == lang):
        return s
  return word
  
    

#
#syn('cars')
#print reader(sys.argv[1])
#word_list = reader(sys.argv[1])
#filtered_words = [word for word in word_list if word not in stopwords.words('english')]
#print word_list
#print filtered_words
#for word in filtered_words:
#  check_etym(word)

print(translator("word", "Latin"))
