"""TALN.py
TP Conception et implémentation d’un système de
questions réponses en langue naturelle sur des données structurées
"""

import math
import re

import nltk
import spacy
from lxml import etree
from nltk.metrics import *
from spacy.lang.fr import French
from spacy.tokenizer import Tokenizer
from SPARQLWrapper import JSON, SPARQLWrapper

LANGUAGE = "en"

nlp = spacy.load("en_core_web_sm")
tokenizer = nlp.tokenizer

questions = []
réponsesAttendues = []
réponses = []

#Parsing XML du fichier questions.xml  
tree = etree.parse("./questions.xml")
root = tree.getroot()

#Récupérer les questions
for q in root.findall('question/string'):
     question = q.text
     lang = q.get('lang')

     if(lang == LANGUAGE):
       questions.append(str(question))

#Récupérer les réponses URI
for a in root.findall('question/answers/answer/uri'):
     answer = a.text
     réponses.append(a.text)

#REGEX sur le token du pronom intérrogatif
def réponseAttendue(token):
  if re.match(r"[Ww]ho",token):
      réponsesAttendues.append("PERS")
  elif re.match(r"[Ww]here",token):
      réponsesAttendues.append("GEO")
  elif re.match(r"[Ww]hen",token):
      réponsesAttendues.append("TIM")
  else:
      réponsesAttendues.append('')

#Trouver l'entité nommé pour une question donnée
def NER(question):
  ner = ""
  doc = nlp(question)
  for ent in doc.ents:
      ner = (ent.text)# On récupère l'entité nommé par Spacy 
  if(len(ner)== 0):#Si Spacy ne trouve l'entité nommé
      ner = "NOT_FOUND"
  
  #Traitement sur l'entité nommé pour préparer la requête
  ner = str(ner).replace("the ", "")
  ner = str(ner).replace(" ", "_")
  return ner
  
#Retourner la relation avec la distance de Levenshtein la plus proche des mots de la phrases
def relationsAvec(question):
  tokens = []
  doc = nlp(question)
  for token in doc:
    tokens.append(token.text)
  min_score = math.inf
  relation = None
  with open("relations.txt") as f:
    for line in f:
        line = line.replace("\n", "")
        line_compare = re.sub(r'([a-z].*):',"",line)
        for token in tokens:
          score = edit_distance(token,line_compare)
          if score < min_score:
            min_score = score
            relation = line
  return relation

#Préparation et envoie d'une requête vers DBpedia
def requête(relation,entité):
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  query = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX res: <http://dbpedia.org/resource/> SELECT DISTINCT ?uri WHERE { res:"
  query += entité + " " + relation + " ?uri . }"
  sparql.setQuery(query)
  sparql.setReturnFormat(JSON)
  result = sparql.query().convert()
  return result

#### Traitement des questions #####
tab_result = []
for question in questions:

  doc = nlp(question)
  for i, token in enumerate(doc):
    if(i==0):# PRONOM INTERROGATIF EN DEBUT DE PHRASE
      réponseAttendue(token.text)
      
  if(NER(question) != "NOT_FOUND"):
    results = requête(relationsAvec(question),NER(question))
  for result in results["results"]["bindings"]:
   tab_result.append(result["uri"]["value"])

def recall(réponses,tab_result):
  nb_correct = 0
  for res in tab_result:
    if res in réponses:
      nb_correct += 1
  return nb_correct/len(réponses)

def précision(tab_result):
  nb_correct = 0
  for res in tab_result:
    if res in réponses:
      nb_correct += 1
  return nb_correct/len(tab_result)

def fmeasure(recall,précision):
  return  (2*précision*recall)/(précision+recall)


recall = recall(réponses,tab_result)
précision = précision(tab_result)
fmeasure = fmeasure(recall,précision)

print("(---- Evaluation du système de questions et réponses en langage naturel ----)")
print("      Rappel du sytème : " + str(recall))
print("      Précision du système : " + str(précision))
print("      F-measure : " + str(fmeasure))
print("(---------------------------------------------------------------------------)")
