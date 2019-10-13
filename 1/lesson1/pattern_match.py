import random
#基于模式匹配的对话机器人实现
def is_variable(pat):
    return pat.startswith('?') and all(s.isalpha for s in pat[1:])
#isalpha方法检查s是否是由字母组成
#all() 函数用于判断给定的可迭代参数 iterable 中的所有元素是否都为 TRUE，如果是返回 True，否则返回 False。
# def pat_match(pattern, saying):
#     if is_variable(pattern[0]):
#         return True
#     else:
#         if pattern[0]!=saying[0]:return False;
#         else:
#             return pat_match(pattern[1:],saying[1:])
#
# print(pat_match('I want ?X'.split(), "I want holiday".split()))
# print(pat_match('I have dreamed a ?X'.split(), "I dreamed about dog".split()))
# 对于面的函数只能判断两个pattern是不是相符合的，我们需要得到value值
# def pat_match(pattern, saying):
#     if is_variable(pattern[0]):
#         return pattern[0],saying[0]
#     else:
#         if pattern[0]!= saying[0]:return False
#         else:
#             return pat_match(pattern[1:],saying[1:])
# print(pat_match('I want ?X'.split(), "I want holiday".split()))
# 但是上面的代码只能针对一个变量，如果是多个变量,比如 ?x is ?y -> a is b 那么结果就会出现问题
def pat_match(pattern,saying):
    if not pattern or not saying: return []
    if is_variable(pattern[0]):
        return [(pattern[0],saying[0])]+pat_match(pattern[1:],saying[1:])
    else:
        if pattern[0] != saying[0]: return []
        else:
            return pat_match(pattern[1:],saying[1:])
# print(pat_match("?X greater than ?Y".split(), "3 greater than 2".split()))
# 下面新建两个函数，一个将我们解析出来的结果变成一个dictionary，一个是依据这个dictionary依照我们定义的方式进行替换
# def pat_to_dict(patterns):
#     return {k:v for k,v in patterns}
def subsitite(rule,parsed_rule):# parsed_rule就是规则
    if not rule: return []
    return [parsed_rule.get(rule[0],rule[0])] + subsitite(rule[1:],parsed_rule)
# #dict.get(key, default=None)
# got_patterns = pat_match("I want ?X".split(), "I want iPhone".split())
# print(got_patterns)
# print(subsitite("What if you mean if you got a ?X".split(), pat_to_dict(got_patterns)))
# print(' '.join(subsitite("What if you mean if you got a ?X".split(), pat_to_dict(got_patterns))))
# 为了合成一句话,使用join函数
defined_patterns = {
    "I need ?X": ["Image you will get ?X soon", "Why do you need ?X ?"],
    "My ?X told me something": ["Talk about more about your ?X", "How do you think about your ?X ?"]
}

def get_response(saying):
    """please implement the code, to get the response as followings:
    >>> get_response('I need iPhone')
    >>> Image you will get iPhone soon
    >>> get_response("My mother told me something")
    >>> Talk about more about your monther.
    """
    for k,v in defined_patterns.items():
        print(pat_match(k.split(),saying.split()))
        print(type(random.sample(v,1)))
        if(pat_match(k.split(),saying.split()) != []):
            return ' '.join(subsitite(''.join(random.sample(v,1)).split(),pat_to_dict(pat_match(k.split(),saying.split()))))
    return None
# print(get_response('I need iphone'))
# segment match，我们上面的形式可以进行简单的基础的会话，但是还需要继续增强，比如 I need an iphone 和I need ?* 匹配
def is_pattern_segment(pattern:str):
    return pattern.startswith('?*') and all(a.isalpha() for a in pattern[2:])
# print(is_pattern_segment('?*p'))
from collections import defaultdict
fail = [True,None]
def pat_match_with_seg(pattern:list,saying:list)->list:
    if not pattern or not saying: return []
    pat = pattern[0]
    if is_pattern_segment(pat):
        match, index = segment_match(pattern, saying)
        return [match] + pat_match_with_seg(pattern[1:], saying[index:])
    elif is_variable(pat):#这里要匹配多的
        return [(pat, saying[0])] + pat_match_with_seg(pattern[1:], saying[1:])
    elif pat == saying[0]:
        return pat_match_with_seg(pattern[1:], saying[1:])
    else:
        return fail
# 上面这段代码比较强的就是使用了多匹配的模式,最大可能进行匹配，写一个新函数
def segment_match(pattern:list,saying:list):
    seg_pat,rest = pattern[0],pattern[1:]
    seg_pat = seg_pat.replace('?*','?')
    if not rest: return (seg_pat,saying),len(saying)#假如没有剩余的直接返回长度
    for i,token in enumerate(saying):
        if rest[0]== token and is_match(rest[1:],saying[(i+1):]):#知道*？遍历完了，并且和saying进行比较成功，说明*？后面的都是相同的
            return (seg_pat,saying[:i]),i
    return (seg_pat,saying),len(saying)
def is_match(rest,saying):
    if not rest and not saying:
        return  True
    if not all(a.isalpha() for a in rest[0]):#判断每一位字符都是字母
        return True
    if rest[0]!= saying[0]:
        return False
    return is_match(rest[1:],saying[1:])
# print(segment_match('?*P is very good'.split(), "My dog and my cat is very good".split()))
# print(pat_match_with_seg('?*P is very good and ?*X'.split(), "My is very good and my cat is very cute".split()))
response_pair = {
    'I need ?X': [
        "Why do you neeed ?X"
    ],
    "I dont like my ?X": ["What bad things did ?X do for you?"]
}
#print(pat_match_with_seg('I need ?*X'.split(), "I need an iPhone".split()))
def pat_to_dict(patterns):
    return {k: ' '.join(v) if isinstance(v, list) else v for k, v in patterns}
# isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()。
#print(subsitite("Why do you neeed ?X".split(), pat_to_dict(pat_match_with_seg('I need ?*X'.split(),
                  #"I need an iPhone".split()))))
#这里会出现一个小问题['an',' iphone']，为了解决问题，复写一下dict函数
#print(subsitite("Hi, how do you do?".split(), pat_to_dict(pat_match_with_seg('?*X hello ?*Y'.split(),
                  #"I am mike, hello ".split()))))
# 我们给大家一些例子:

rules = {
    "?*X hello ?*Y": ["Hi, how do you do?"],
    "I was ?*X": ["Were you really ?X ?", "I already knew you were ?X ."]
}
def get_response(saying,response_rules):
    # for k,v in response_rules.items():
    #     print(pat_match_with_seg(k.split(),saying.split()))
    for k, v in response_rules.items():
        if pat_match_with_seg(k.split(), saying.split()):
            pat = pat_match_with_seg(k.split(), saying.split())
            dict1 = pat_to_dict(pat)
            # print(dict1)
            # print(type(dict1.values()))
            # print(list(dict1.values())[0])
            # print(len(list(dict1.values())[0].split()))
            # print(k.split())
            # print(len(k.split()))
            # print(len(dict1)==1)
            if len(dict1)==1 and len(list(dict1.values())[0].split())==len(saying.split()):
                continue
            return ' '.join(subsitite(random.choice(v).split(), pat_to_dict(pat)))
#print(get_response("I was bad boy",rules))

