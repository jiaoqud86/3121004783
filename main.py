import jieba
import gensim
import re
import difflib
import os

# 获取指定路径的文件内容
def get_file_contents(path):
    if not os.path.exists(path):
        print("File path does not exist. Please check!")
        return None
    str = ''
    f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        str = str + line
        line = f.readline()
    f.close()
    return str

def filter(str):
    # 将读取到的文件内容先进行jieba分词，
    str = jieba.lcut(str)
    result = []
    # 把标点符号、转义符号等特殊符号过滤掉
    for i in str:
        if (re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", i)):
            result.append(i)
    return result

# 传入过滤之后的数据，通过调用gensim.similarities.Similarity计算余弦相似度
def gen_sim(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    sim = similarity[test_corpus_1][1]
    return sim

def diff_sim(text1,text2):
    sim = difflib.SequenceMatcher(None, text1, text2).ratio()
    return sim

def main(path1, path2):
    save_path = 'D:\\Cprogram\\papercheak\\res.txt'  # 输出结果绝对路径
    str1 = get_file_contents(path1)
    str2 = get_file_contents(path2)
    text1 = filter(str1)
    text2 = filter(str2)
    gensim = gen_sim(text1, text2)
    diffsim=diff_sim(text1,text2)
    print("使用difflib库文章相似度:  %.4f" % diffsim)
    print("使用gensim库文章相似度： %.4f" % gensim)
    f = open(save_path, 'w', encoding="utf-8")
    f.write("使用difflib库文章相似度:  %.4f" % diffsim)
    f.write("\n使用gensim库文章相似度： %.4f" % gensim)
    f.close()


if __name__ == '__main__':
    path1 = "D:\\Cprogram\\papercheak\\test_text\\orig_0.8_dis_10.txt"  # 论文原文的文件的绝对路径（作业要求）
    path2 = "D:\\Cprogram\\papercheak\\test_text\\orig_0.8_dis_1.txt"  # 抄袭版论文的文件的绝对路径
    main(path1, path2)
