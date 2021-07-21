import pandas as pd
import json
from operator import itemgetter

def dot_product(vec1, vec2):
    sum_ = 0
    for i in range(len(vec1)):
        sum_ += vec1[i]*vec2[i]
    return sum_

def cos_sim(vec1, vec2):
    size1 = 0
    size2 = 0
    for i in range(len(vec1)):
        size1 += vec1[i]**2
        size2 += vec2[i]**2
    size1 = size1 ** 0.5
    size2 = size2 ** 0.5
    
    if size1 == 0 or size2 == 0:
        return 0
    
    return dot_product(vec1, vec2) / (size1*size2)
    
def get_article_vectors(topics, file_path):
    with open(file_path, 'r') as f:
        s = json.load(f)
    _vectors = {_['id']: [] for _ in s}
    for art in s:
        for topic in topics: 
            lowered =[rel_top.lower() for rel_top in art['related_topics']]
            if topic in lowered:
                _vectors[art['id']].append(1)
            else:
                _vectors[art['id']].append(0)
    return _vectors

def get_topics(file_path):
    df = pd.read_csv(file_path)
    return list(df.columns)

def find_related_articles(user_profile_idx):
    N = 10
    file_path = 'data.csv'
    topics = get_topics(file_path)
    
    df = pd.read_csv(file_path)
    df = df.fillna(0)
    tas = df.iloc[user_profile_idx,:]
    user_profile = list(tas)
    
    _vectors = get_article_vectors(topics, 'CrawledPapers.json')
    article_rel = {}
    
    for _id in _vectors:
        _vector = _vectors[_id]
        article_rel[_id] = cos_sim(user_profile, _vector)
    res = dict(sorted(article_rel.items(), key = itemgetter(1), reverse = True)[:N])
    return list(res.keys())