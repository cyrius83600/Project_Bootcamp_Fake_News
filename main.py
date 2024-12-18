from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def get_wordnet_pos(pos_tag):
     output = np.asarray(pos_tag)
     for i in range(len(pos_tag)):
         if pos_tag[i][1].startswith('J'):
             output[i][1] = wordnet.ADJ
         elif pos_tag[i][1].startswith('V'):
             output[i][1] = wordnet.VERB
         elif pos_tag[i][1].startswith('R'):
             output[i][1] = wordnet.ADV
         else:
             output[i][1] = wordnet.NOUN
     return output

 def Tokenize(text):
     text = text.lower()
     stop_words = stopwords.words('english')
     lemmatizer = WordNetLemmatizer()
     token_liste = [token for token in word_tokenize(text) if token.isalpha() and token not in stop_words]
     test = False
     alphabet = 'abcdefghijklmnopqrstuvwxyz'
     for mot in token_liste:
         for char in mot:
             if char not in alphabet:
                test = True
     if test == False:
         final_liste = [token for token in token_liste]
         tags = nltk.pos_tag(final_liste)
         wordnet_input = get_wordnet_pos(tags)
         lem_tokens = [lemmatizer.lemmatize(t,tag) for t,tag in wordnet_input]
         return lem_tokens
     return [' ']


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def installNltk():
     nltk.download('stopwords')
     nltk.download('punkt_tab')
     nltk.download('averaged_perceptron_tagger_eng')
     nltk.download('wordnet')

def getModelTfidf():
     with open('tfidf.pickle','rb') as file:
         return pickle.load(file)

def getModelLreg():
     with open('lreg.pickle','rb') as file:
         return pickle.load(file)

@app.get("/")
async def say_hi():
     return "Ca marche"

@app.get("/geturl")
def say_hi(url):
    with open('tfidf.pickle','rb') as file:
       vectorizer = pickle.load(file)
     with open('lreg.pickle','rb') as file:
         lreg = pickle.load(file)
     article_tokenized = Tokenize(url)
     print(vectorizer.get_feature_names_out()[0])
     X = vectorizer.transform([' '.join(article_tokenized)])
     y = lreg.predict(X)
     if y[0] == 1:
         return "Cet article est une Fake News"
     return "Cet article n'est pas une Fake News"
