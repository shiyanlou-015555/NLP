import random

simple_grammar = """
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun
Adj* => Adj | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>   蓝色的 |  好看的 | 小小的"""
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

print(get_generation_by_gram(simple_grammar, target='sentence', stmt_split='=>'))