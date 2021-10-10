import json
from operator import itemgetter

def get_crawled_file(file_rel_path):
    with open(file_rel_path) as f:
        s = json.load(f)
    return s

def find_article_by_id(id_str, s):
    for article in s:
        if article['id'] == id_str:
            return article
    return None

def is_in_dic_and_initialize1(dic, key):
    if key not in dic.keys():
        dic[key] = 1.0
        return False
    return True
    
def find_degree_in(ls_author, to):
    k = 0
    for aut in ls_author:
        if to == aut[1]:
            k += 1
    return k
    
def find_degree_out(ls_aut, fro):
    k = 0
    for aut in ls_aut:
        if fro == aut[0]:
            k += 1
    return k

def find_normalizing_factor(dic):
    _normalizing_factor = 0.0
    for key in dic:
        _normalizing_factor += dic[key]**2
    return _normalizing_factor**0.5

def get_author_pair(s):
    """
    s: crawled json loaded in s
    """
    ls_author = set()
    for article_from in s:
        for ref in article_from['references']:
            id_str = ref
            article_to = find_article_by_id(id_str, s)
            if article_to != None:
                for author_to in article_to['authors']:
                    for author_from in article_from['authors']:
                        ls_author.add((author_from, author_to))
    
    return list(ls_author)

def calc_top_hit(ls_author, N):
    hub_dic = {}
    aut_dic = {}
    MAX_ITERATION = 5
    
    for pair in ls_author:  
        fro = pair[0]
        to = pair[1]
        is_in_dic_and_initialize1(hub_dic, fro)
        is_in_dic_and_initialize1(aut_dic, to)
        is_in_dic_and_initialize1(hub_dic, to)
        is_in_dic_and_initialize1(aut_dic, fro)   
    
    for _ in range(MAX_ITERATION):
        visited_hub= set()
        visited_aut = set()  
        
        for pair in ls_author:
            fro = pair[0]
            to = pair[1]
            
            if to not in visited_aut:
                visited_aut.add(to)
                aut_dic[to] = 0.0

            aut_dic[to] += hub_dic[fro]

        _normalizing_factor_aut = find_normalizing_factor(aut_dic)
        for key in aut_dic:
            aut_dic[key] /= _normalizing_factor_aut 
        
        for pair in ls_author:
            fro = pair[0]
            to = pair[1]
            
            if fro not in visited_hub:
                visited_hub.add(fro)
                hub_dic[fro] = 0.0
            
            hub_dic[fro] += aut_dic[to]

        _normalizing_factor_hub = find_normalizing_factor(hub_dic)
        for key in hub_dic:
            hub_dic[key] /= _normalizing_factor_hub 

    aut_top_dic = dict(sorted(aut_dic.items(), key = itemgetter(1), reverse = True)[:N])
    return aut_top_dic

def get_top_hit(file_rel_path, N):
    s = get_crawled_file(file_rel_path)
    ls_author = get_author_pair(s)
    top_hit = calc_top_hit(ls_author, N)
    return list(top_hit.keys())