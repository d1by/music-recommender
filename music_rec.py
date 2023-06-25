import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
#import re

music = pd.read_csv('spotify_millsongdata.csv')

music = music.sample(n=5000).drop('link', axis=1).reset_index(drop=True)

music['text'] = music['text'].replace("\n", "", regex=True).replace("\r", "", regex=True)

# for x in range(len(music)):
#     music['text'][x] = re.sub('[\n\r]', '', music['text'][x])

# print(music.head())

tfidf = TfidfVectorizer(analyzer='word', stop_words='english')

tfidf_matrix = tfidf.fit_transform(music['text'])

tfidf.fit_transform(music['text'])

cos_similarities = cosine_similarity(tfidf_matrix)
# print(cos_similarities[0][123])

similarities = {}
for i in range(len(cos_similarities)):
    similar_indices = cos_similarities[i].argsort()[:-50:-1]
    similarities[music['song'][i]] = [(cos_similarities[i][x], music['song'][x], music['artist'][x]) for x in similar_indices][1:]

class music_recommender:
    def __init__(self, matrix):
        self.matrix = matrix

    def _print_message(self, music_in, sim_music):
        print("------")
        print(f"Music similar to {music_in}: ")
        print("------")
        for i in range(len(sim_music)):
            print(f"{i+1}. {sim_music[i][1]} - {sim_music[i][2]} (Similarity score: {round(sim_music[i][0], 3)})")
        print("------")

    def recommend(self, music_rec):
        sim_music = self.matrix[music_rec['song']][:music_rec['number']]
        self._print_message(music_in=music_rec['song'], sim_music=sim_music)

rand_inp = []
for i in range(10):
    rand_inp.append(music['song'][random.randint(0, len(music))])

print("Pick a song: ")

def pick():
    for i in range(10):
        print(f"{i+1}. {rand_inp[i]}")
    inp = int(input())
    return inp-1

while(True):
    try:
        inp_song = rand_inp[pick()]
        break
    except:
        print("Incorrect input.")
        pick()

num = int(input("Enter number of recommended songs: "))

recs = music_recommender(similarities)

music_rec = {
    "song": inp_song,
    "number": num
}

recs.recommend(music_rec)