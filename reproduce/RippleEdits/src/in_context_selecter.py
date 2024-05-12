import torch
from benchmark import Dataset
import random
from sentence_transformers import SentenceTransformer, util

class InContextSelector:

    def __init__(self, dataset: Dataset, selection_method = 'random', CoT = False):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dataset = dataset
        self.selection_method = selection_method
        self.CoT = CoT
        self.num_icls = 0
        self.icls = []
        self.icls_embedding = []
        self.icl_context = ''

    # type can be: 'Relation_Specificity'; 'Logical_Generalization'; 'Subject_Aliasing'; 'Compositionality_I';
    #              'Compositionality_II'; 'Forgetfulness'
    def select_random_noCoT_icls(self, k, type):
        print(f'_________________{type}___________________')
        samples = self.dataset.examples
        desired_set = []
        for sample in samples:
            icls = sample.fetch_icl(type)
            if len(icls) != 0:
                idx = random.randint(0, len(icls)-1)
                desired_set.append(icls[idx])
                print(icls[idx])
            if len(desired_set) >= k:
                print('Terminated')
                break
        return desired_set
    
    def select_random_CoT_icls(self, k, type):
        print(f'_________________{type}___________________')
        samples = self.dataset.examples
        desired_set = []
        for sample in samples:
            icls = sample.fetch_cot_icls(type)
            if len(icls) != 0:
                idx = random.randint(0, len(icls)-1)
                desired_set.append(icls[idx])
                print(icls[idx])
            if len(desired_set) >= k:
                print('Terminated')
                break
        return desired_set
        # raise NotImplementedError

    @staticmethod
    def ks_todict(ks):
        assert(len(ks) == 6)
        typedict = {'Relation_Specificity': ks[0], 'Logical_Generalization': ks[1], 'Subject_Aliasing': ks[2],
                    'Compositionality_I': ks[3], 'Compositionality_II': ks[4], 'Forgetfulness': ks[5]}
        return typedict

    def select_icls(self, ks, shuffle = True):
        typedict = self.ks_todict(ks)
        result = []
        if not self.CoT:
            for key in typedict:
                result.extend(icl for icl in self.select_random_noCoT_icls(typedict[key], key))
        # add more selection method and CoT option here
        if self.CoT:
            for key in typedict:
                result.extend(icl for icl in self.select_random_CoT_icls(typedict[key], key))
        if shuffle:
            random.shuffle(result)
        return result
    
    def set_constant_icls(self, ks, shuffle = True):
        self.icls = self.select_icls(ks, shuffle)
        self.icl_context = "\n".join(self.icls)

    def set_icls_embedding(self, ks):
        self.icls = self.select_icls(ks)
        self.icls_embedding = self.model.encode(self.icls)

    def search_similar_icls(self, question, topk = 6):
        question_embed = self.model.encode(question)
        hits = util.semantic_search(question_embed, self.icls_embedding, score_function=util.dot_score, top_k=topk)
        idx = [i['corpus_id'] for i in hits[0]]
        return "\n".join([self.icls[i] for i in idx])
        

    def set_num_icls(self, num_icls):
        self.num_icls = num_icls

    def get_icls(self, question):
        if self.selection_method == 'kNN':
            self.icl_context = self.search_similar_icls(question, self.num_icls)
        return self.icl_context