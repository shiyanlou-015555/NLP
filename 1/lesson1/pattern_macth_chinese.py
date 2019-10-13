################################################
# 为了解决中文分词问题，我们使用c来表示吧
import jieba
def cut(respose:str):
    res = list(jieba.cut(respose))
    j=len(res);
    for i in range(j):
        if(i>=len(res)):
            break
        if res[i] == '?' and res[i+1]=='*':
            res[i] = res[i]+res[i+1]+res[i+2]
            res = res[:i+1]+res[i+3:]
            continue
        elif res[i] == '?':
            res[i] = res[i]+res[i+1]
            res = res[:i+1]+res[i+2:]
    return res
print(cut("?*y你就像猪一样?x"))
def subsitite(rule,parsed_rule):# parsed_rule就是规则
    if not rule: return []
    return [parsed_rule.get(rule[0],rule[0])] + subsitite(rule[1:],parsed_rule)
def pat_to_dict(patterns):
    return {k: ' '.join(v) if isinstance(v, list) else v for k, v in patterns}
# isinstance() 函数来判断一个对象是否是一个已知的类型，类似 type()
def is_pattern_segment(pattern:str):
    return pattern.startswith('?*')
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
fail = [True,None]
#基于模式匹配的对话机器人实现
def is_variable(pat):
    return pat.startswith('?') and all(s.isalpha for s in pat[1:])
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
print(''.join(subsitite(cut('ni是?x'), pat_to_dict(pat_match_with_seg(cut('我是?*x'),
                  cut("我是垃圾"))))))
#print(subsitite("Why do you neeed ?X".split(), pat_to_dict(pat_match_with_seg('I need ?*X'.split(),
                  #"I need an iPhone".split()))))
# #提取汉字
# # import re
# # str = '你不好好?*p'
# # p = re.compile('([\u4e00-\u9fa5]？*)|(\?\*.)')
# # res = re.findall(p, str)
# # # result = ''.join(res)
# # # print(result)
# # print(res)
# print('abc'.split('b'))
# 主谓语不行，比如如果是'我很蠢'那么结巴分词，'很蠢'就会被切出来