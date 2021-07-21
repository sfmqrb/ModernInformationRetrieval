import json
import numpy as np

class page_rank():

    def get_pageid_by_i(self, i):
        key_list = list(self.id_map.keys())
        val_list = list(self.id_map.values())
    
        if i not in val_list:
            return  None
        position = val_list.index(i)
        return key_list[position]

    def load_file(self, file_name):
        with open(file_name) as f:
            self.s = json.load(f)

    def calc_page_rank(self, alpha = 0.1, file_name = "CrawledPapers.json", output_fn = 'PageRankTest.json'):
        
        self.load_file(file_name)
        self.id_map = dict()

        i = 0
        for article in self.s:
            self.id_map[article['id']] = i
            i += 1

        adj_ls = []
        i = len(self.id_map)
        for article in self.s:
            id_mapped = self.id_map[article['id']]
            for id_str in article['references']:
                if id_str not in self.id_map.keys():
                    self.id_map[id_str] = i
                    i += 1
            ls = [self.id_map[id_str] for id_str in article['references']]
            
            adj_ls.append({id_mapped: set(ls)})

        
        self.adj_mat = np.zeros((len(self.id_map), len(self.id_map)), dtype = 'float64')
        for dic in adj_ls:
            row = list(dic.keys())[0]
            cols = dic[row]
            for col in cols:
                self.adj_mat[row, col] = 1

        self.adj_mat[np.sum(self.adj_mat, axis=1) == 0, :] += 1

        for j in range(len(self.adj_mat)):
            arr = self.adj_mat[j, :]
            arr /= sum(arr)

        self.tran_mat = self.adj_mat * (1 - alpha) + alpha * 1/len(self.adj_mat)

        # mat_pow = np.linalg.matrix_power(self.tran_mat, 10)
        # self.one_row = mat_pow[0,:]

        N = self.tran_mat.shape[1]
        self.one_row = np.random.rand(N)
        self.one_row = self.one_row / np.linalg.norm(self.one_row, 1)
        for i in range(15):
            self.one_row = self.one_row @ self.tran_mat
        
        with open(output_fn, 'w') as f:
            f.write('{\n')
            
        for i in range(len(self.s)):
            id_str = self.s[i]['id']
            id_mapped_int = self.id_map[id_str]  
            with open(output_fn, 'a+') as f:
                q = "    " + '"' + id_str + '"' + str(': ') + str(self.one_row[id_mapped_int])
                f.write(q)
                if i != len(self.s) - 1:
                    f.write(',\n')
                else: 
                    f.write('\n}')
