import random

human = """
human = 自己 寻找 活动
自己 = 我 | 俺 | 我们
寻找 = 看看 | 找找 | 想找点
活动 = 乐子 | 玩的
"""
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
def get_generation_by_gram(grammar_str: str, target, stmt_split='=', or_split='|'):
    rules = dict()  # key is the @statement, value is @expression
    for line in grammar_str.split('\n'):
        if not line: continue
        # skip the empty line
        #  print(line)
        stmt, expr = line.split(stmt_split)

        rules[stmt.strip()] = expr.split(or_split)

    generated = generate(rules, target=target)

    return generated
def generate(grammar_rule, target):
    if target in grammar_rule: # names
        candidates = grammar_rule[target]  # ['name names', 'name']
        candidate = random.choice(candidates) #'name names', 'name'
        return ''.join(generate(grammar_rule, target=c.strip()) for c in candidate.split())
    else:
        return target

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
print(generate_n(host,10, target='host', stmt_split='='))