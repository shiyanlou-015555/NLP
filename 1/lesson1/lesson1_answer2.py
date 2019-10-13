import jieba
import random
from collections import Counter
corpus = './train.txt'
# readline in path of corpus
FILE = open(corpus,encoding='utf-8').readlines()
# FILE2 = [line.split('++$++')[2]for line in FILE]
# print(FILE2)
# data cleaning
def getCleaning(FILE):
    return ''.join([line.split('++$++')[2]for line in FILE])
# jieba cut
def cut(string):
    return list(jieba.cut(string))
# 1-gram model
# def get_1_gram_count(word):
#     if word in words_count: return words_count[word]
#     else:
#         return words_count.most_common()[-1][-1]
# 2-gram model
# def get_2_gram_count(word):
#     if word in _2_gram_words_counts: return _2_gram_words_counts[word]
#     else:
#         return _2_gram_words_counts.most_common()[-1][-1]
# N-gram model
def get_gram_count(word, wc):
    if word in wc: return wc[word]
    else:
        return wc.most_common()[-1][-1]


# 给出现的频次计数
TOKENS = cut(getCleaning(FILE))# 这里必须要进行结巴分词
words_count = Counter(TOKENS)
_2_gram_words = [
    TOKENS[i] +TOKENS[i+1] for i in range(len(TOKENS)-1)
]
_2_gram_words_counts = Counter(_2_gram_words)
# 整合的，2-gram的语言模型整合
def two_gram_model(sentence):
    tokens = cut(sentence)
    probability = 1
    for i in range(len(tokens) - 1):
        word = tokens[i]
        next_word = tokens[i + 1]
        _two_gram_c = get_gram_count(word + next_word, _2_gram_words_counts)
        _one_gram_c = get_gram_count(next_word, words_count)
        pro = _two_gram_c / _one_gram_c

        probability *= pro
    return probability
# 生成语法树
def generate(grammar_rule, target):
    if target in grammar_rule: # names
        candidates = grammar_rule[target]  # ['name names', 'name']
        candidate = random.choice(candidates) #'name names', 'name'
        return ''.join(generate(grammar_rule, target=c.strip()) for c in candidate.split())
    else:
        return target
host = """
host = 寒暄 报数 询问 业务相关 结尾 
报数 = 我是 数字 号 ,
数字 = 单个数字 | 数字 单个数字 
单个数字 = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 
寒暄 = 称谓 打招呼 | 打招呼
称谓 = 人称 ,
人称 = 先生 | 女士 | 小朋友
打招呼 = 你好 | 您好 
询问 = 请问你要 | 您需要
业务相关 = 玩玩 具体业务
玩玩 = 耍一耍 | 玩一玩
具体业务 = 喝酒 | 打牌 | 打猎 | 赌博
结尾 = 吗？"""
# print(get_generation_by_gram(host, target='host', stmt_split='='))
def generate_n(grammar_str: str,n, target, stmt_split='=', or_split='|'):
    rules = dict()  # key is the @statement, value is @expression
    # building a spanning tree dictionary
    for line in  grammar_str.split('\n'):
        if not line: continue
        # if none choose to skip it
        stmt, expr = line.split(stmt_split)
        rules[stmt.strip()] = expr.split(or_split)


    return [generate(rules,target=target) for i in range(n)]

def generate_best(): # you code here······························································
    rs = generate_n(host,10, target='host', stmt_split='=')
    result = [(i,two_gram_model(i)) for i in rs]
    return result
best = generate_best()
print(best)
best_real = sorted(best,key=lambda x:x[1],reverse=True)
print(best_real)
print(best_real[0][0])
