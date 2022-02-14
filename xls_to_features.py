#-*- coding = utf-8 -*- 
#@Time : 2021/3/16 15:29
#@Author : Yan Qiu
#@File ：xls_to_features.py
#@Software: PyCharm

'''
        #总字符数 num_doctor_characters   总标点符号数 num_doctor_punctuations   总字数 num_doctor_words   句子总数num_doctor_sentences
        #名词总数 num_doctor_nouns, 动词总数 num_doctor_verbs, 形容词总数 num_doctor_adjs, 副词总数 num_doctor_dvs, 总词语数 num_doctor_tagging
        #余弦相似度 DP_similarity
'''



import re
import xlwt
import jieba
import jieba.posseg as psg
import jieba.analyse
import math
from snownlp import SnowNLP
import numpy as np
import xlrd



def main():
    filename = 'F:/haodf-prediction/2020/2020text/2020-60001-70000.xls'
    filepath2 = 'F:/haodf-prediction/stopwords/cn_stopwords.txt'  # 停用词列表
    filepath3 = r'F:/haodf-prediction/pos-neg/负面.txt'
    filepath4 = r'F:/haodf-prediction/pos-neg//正面.txt'
    doctor_save_path = 'F:/haodf-prediction/2020/2020text/2020-60001-70000_doctor_features.xls'
    patient_save_path = 'F:/haodf-prediction/2020/2020text/2020-60001-70000_patient_features.xls'

    id, questions, answers = read_excel(filename)
############################ 医生文本 ##############################################################################
    doctor_list = []
    ans_cnt = 0
    for ans in answers:
        doctor_satis_list = []
        ans_cnt += 1
        print("-------------------- 医生 --------------------")
        print("第{}条".format(ans_cnt), ans_cnt)
        print("ans:", ans)
        print("id[ans_cnt-1]:", id[ans_cnt-1])
        doctor_satis_list = num_Statistics(ans, filepath2, filepath3, filepath4)
        doctor_satis_list.append(id[ans_cnt-1])
        print("doctor_satis_list:", doctor_satis_list)
        doctor_list.append(doctor_satis_list)

    save_doctor_data(doctor_list, doctor_save_path)

############################ 患者文本 ##############################################################################
    patient_list = []
    que_cnt = 0
    for que in questions:
        que_cnt += 1
        print("-------------------- 患者 --------------------")
        print("第{}条".format(que_cnt), que_cnt)
        print("ans:", que)
        patient_satis_list = num_Statistics(que, filepath2, filepath3, filepath4)
        patient_satis_list.append(id[que_cnt - 1])
        patient_list.append(patient_satis_list)

    save_patient_data(patient_list, patient_save_path)



def read_excel(filename):
    # 打开文件

    workBook = xlrd.open_workbook(filename)

    ## 按sheet名字获取sheet内容
    sheet_content = workBook.sheet_by_name('病例文本')

    # 3. sheet的名称，行数，列数
    print(sheet_content.name, sheet_content.nrows, sheet_content.ncols)

    # 4. 获取整行和整列的值（数组）
    # rows = sheet1_content1.row_values(3); # 获取第四行内容
    # cols = sheet1_content1.col_values(2); # 获取第三列内容
    id = sheet_content.col_values(0)
    questions = sheet_content.col_values(4)  # 获取第五列内容，问题
    answers = sheet_content.col_values(5)
    print("id:", id)
    print("questions:", questions)
    print("answers", answers)
    return id, questions, answers

def save_doctor_data(doctor_list, save_path):
    # 创建workbook对象
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建工作表
    sheet = book.add_sheet('医生文本特征统计', cell_overwrite_ok=True)
    # 创建一个列的元组
    col = ('ans', '总字符数', '总标点符号数', '总字数', '句子总数',
           '名词总数', '动词总数', '形容词总数', '副词总数', '包含停用词的总词语',
           '不包含停用词的总词语', '总消极词语', '总积极词语', '情感分值', 'id')

    for i in range(0, 15):
        sheet.write(0, i, col[i])


    for i in range(0, len(doctor_list)):
        satis_list = doctor_list[i]
        for j in range(0, 15):
            sheet.write(i+1, j, satis_list[j])
    book.save(save_path)

def save_patient_data(patient_list, save_path):

    # 创建workbook对象
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)

    # 创建工作表
    sheet = book.add_sheet('患者文本特征统计', cell_overwrite_ok=True)
    # 创建一个列的元组
    col = ('que', '总字符数', '总标点符号数', '总字数', '句子总数',
           '名词总数', '动词总数', '形容词总数', '副词总数', '包含停用词的总词语',
           '不包含停用词的总词语', '总消极词语', '总积极词语', '情感分值', 'id')

    for i in range(0, 15):
        sheet.write(0, i, col[i])


    for i in range(0, len(patient_list)):
        satis_list = patient_list[i]
        for j in range(0, 15):
            sheet.write(i+1, j, satis_list[j])
    book.save(save_path)

def num_Statistics(content, filepath2, filepath3, filepath4):

    sentences, characters_len, punctuations_len = cut_sentences(content)
    #    punctuations_len:标点符号数  characters_len：字符数  sentences：句子

    num_characters = characters_len  # 字符数
    num_sentences = len(sentences)   # 句子数
    num_punctuations = punctuations_len   # 标点符号数

    num_nouns, num_verbs, num_adjs, num_dvs, num_tagging1, num_tagging2, num_negative, num_positive = pretext(content, filepath2, filepath3, filepath4)

    satis_list = []
    satis_list.append(content)
    satis_list.append(num_characters)
    print("总字符数：", num_characters)

    satis_list.append(num_punctuations)
    print("总标点符号数：", num_punctuations)

    num_words = num_characters - num_punctuations
    satis_list.append(num_words)
    print("总字数：", num_words)

    satis_list.append(num_sentences)
    print("句子总数：", num_sentences)

    print("名词总数：", num_nouns)
    satis_list.append(num_nouns)
    print("动词总数：", num_verbs)
    satis_list.append(num_verbs)
    print("形容词总数：", num_adjs)
    satis_list.append(num_adjs)
    print("副词总数：", num_dvs)
    satis_list.append(num_dvs)

    print("包含停用词的总词语：", num_tagging1)
    satis_list.append(num_tagging1)

    print("不包含停用词的总词语：", num_tagging2)
    satis_list.append(num_tagging2)

    print("总消极词语：", num_negative)
    satis_list.append(num_negative)

    print("总积极词语：", num_positive)
    satis_list.append(num_positive)

    sentiment_score = SnowNLP(content).sentiments  # 情感分值
    print("情感分值：", sentiment_score)
    satis_list.append(format(sentiment_score, '.4f'))

    return satis_list

def stopwordslist(filepath2):  # 创建停用词列表
    stopword = [line.strip() for line in open(filepath2, 'r', encoding="utf-8").readlines()]  # 以行的形式读取停用词表，同时转换为列表
    return stopword

def negative_wordslist(filepath3):
    negative_words = [line.strip() for line in open(filepath3, 'r', encoding="utf-8").readlines()]  # 以行的形式读取负向情感词，同时转换为列表
    return negative_words

def positive_wordslist(filepath4):
    positive_words = [line.strip() for line in open(filepath4, 'r', encoding="utf-8").readlines()]  # 以行的形式读取正向情感词，同时转换为列表
    return positive_words

def pretext(contents, filepath2, filepath3, filepath4):  # 去除停用词、词性标注

    '''
    nouns_len:名词数
    verbs_len：动词数
    adjs_len：形容词数
    dvs_len：副词数
    tagging_len1：包括停用词的词语数量
    tagging_len2：不包括停用词的词语数量
    negative_words_len：消极词数
    positive_words_len：积极词数
    '''

    content1 = contents.replace(' ', '')  # 去掉文本中的空格

    pattern = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")  # 只保留中英文、数字，去掉符号
    content2 = re.sub(pattern, '', content1)  # 把文本中匹配到的字符替换成空字符，去除符号后的文本

    cutwords = jieba.lcut(content2, cut_all=False)  # 精确模式分词

    lastword1 = psg.lcut(content2)   #进行词性标注
    tagging = [(words.word, words.flag) for words in lastword1]   # 转换为列表
    tagging_len1 = len(tagging)  # 词语数量，包括停用词


    stopwords = stopwordslist(filepath2)  # 这里加载停用词的路径
    words = ''
    words_list = []  #去除停用词后的分词列表
    for word in cutwords:  # for循环遍历分词后的每个词语
        if word not in stopwords:  # 判断分词后的词语是否在停用词表内
            if word != '\t':
                words += word
                words += "/"
                words_list.append(word)
    tagging_len2 = len(words_list)  # 词语数量，不包括停用词

    # print("【去除停用词后的分词列表：", words_list)
    content3 = words.replace('/', '')  # 去掉文本中的斜线

    negative_words = negative_wordslist(filepath3)   ## 这里加载消极词的路径
    positive_words = positive_wordslist(filepath4)   ## 这里加载积极词的路径
    negative_words_list = []
    positive_words_list = []
    for word in words_list:
        if word in negative_words:
            negative_words_list.append(word)
            if word in positive_words:
                positive_words_list.append(word)

    negative_words_len = len(negative_words_list)
    positive_words_len = len(positive_words_list)
    # print("消极词数：", negative_words_len)
    # print("积极词数：", positive_words_len)


    lastword2 = psg.lcut(content3)  # 使用for循环逐一获取划分后的词语进行词性标注
    # print('\n【对去除停用词后的分词进行词性标注：】' + '\n')

    # print([(words.word, words.flag) for words in lastword])  # 转换为列表
    # print("tagging", tagging)
    # print("共有{}个词语".format(len(tagging)))

    noun = ['n', 'nr', 'nr1', 'nr2', 'nrj', 'ns', 'nsf', 'nt', 'nz', 'nl', 'nx', 'ng', 'nrt', 'nrfg']
    nouns = []   #名词

    verb = ['v', 'vd', 'vg', 'vi', 'vn', 'vq', 'vshi', 'vyou', 'vf', 'vx', 'vl']
    verbs = []   #动词

    adj = ['a', 'ad', 'an', 'ag', 'al']
    adjs = []    #形容词

    dv = ['d', 'df', 'dg']
    dvs = []     #副词

    for word, flag in lastword2:
        if flag in noun:
            nouns.append(word)
        if flag in verb:
            verbs.append(word)
        if flag in adj:
            adjs.append(word)
        if flag in dv:
            dvs.append(word)



    nouns_len = len(nouns)
    verbs_len = len(verbs)
    adjs_len = len(adjs)
    dvs_len = len(dvs)

    # allow_pos_n = ('n')  #名词
    # nouns = jieba.analyse.extract_tags(content3, topK=50, withWeight=False, allowPOS=allow_pos_n)
    # print("nouns", nouns)
    #
    # allow_pos_v = ('v')  #动词
    # verbs = jieba.analyse.extract_tags(content3, topK=50, withWeight=False, allowPOS=allow_pos_v)
    # print("verbs", verbs)
    #
    # allow_pos_a = ('a')  #形容词
    # adjs = jieba.analyse.extract_tags(content3, topK=50, withWeight=False, allowPOS=allow_pos_a)
    # print("adjs", adjs)
    #
    # allow_pos_d = ('d')  #副词
    # advs = jieba.analyse.extract_tags(content3, topK=50, withWeight=False, allowPOS=allow_pos_d)
    # print("advs", advs)
    #
    # allow_pos_t = ('t')  #时间词
    # times = jieba.analyse.extract_tags(content3, topK=50, withWeight=False, allowPOS=allow_pos_t)
    # print("times", times)
    #
    # allow_pos_s = ('s')  #所处词
    # sites = jieba.analyse.extract_tags(content3, topK=50, withWeight=False, allowPOS=allow_pos_s)
    # print("sites", sites)
    #
    # allow_pos_f = ('f')  #方位词
    # fangs = jieba.analyse.extract_tags(content3, topK=50, withWeight=False, allowPOS=allow_pos_f)
    # print("fangs", fangs)
    #
    # allow_pos_r = ('r')  #代词
    # pronouns = jieba.analyse.extract_tags(content3, topK=50, withWeight=False, allowPOS=allow_pos_r)
    # print("pronouns", pronouns)
    #
    # allow_pos_m = ('m')  #数词
    # numerals = jieba.analyse.extract_tags(content3, topK=50, withWeight=False, allowPOS=allow_pos_m)
    # print("numerals", numerals)
    #
    # allow_pos_p = ('p')  #介词
    # prepositions = jieba.analyse.extract_tags(content3, topK=50, withWeight=False, allowPOS=allow_pos_p)
    # print("prepositions", prepositions)

    return nouns_len, verbs_len, adjs_len, dvs_len, tagging_len1, tagging_len2, negative_words_len, positive_words_len

def cut_sentences(content):
    '''
    punctuations_len:标点符号数
    characters_len：字符数
    sentences：句子
    '''

    # 结束符号，包含中文和英文的
    end_flag = [',', '?', '!', '.', ';',
                '，', '？', '！', '。', '；', '…', ' ', ' ']

    content_len = len(content)

    sentences = []
    tmp_char = ''
    i = 0
    tmp_char_len2 = 0
    global punctuations_len
    global tmp_char_len1
    for idx, char in enumerate(content):
        # 拼接字符
        tmp_char += char

        # 判断是否已经到了最后一位
        if (idx + 1) == content_len:
            # print("content_len:", content_len)
            # print("tmp_char_len1", len(tmp_char.strip('\n')))
            tmp_char_len1 = len(tmp_char.strip('\n'))
            sentences.append(tmp_char.strip('\n'))
            # print("sentences", sentences)
            if char in end_flag:
                punctuations_len = i+1
                break

#########################################################################################
        if char in end_flag:  # 判断此字符是否为结束符号
            i += 1
            # 再判断下一个字符是否为结束符号，如果不是结束符号，则切分句子
            next_idx = idx + 1
            if not content[next_idx] in end_flag:
                sentences.append(tmp_char.strip('\n'))
                # print("tmp_char_len2", len(tmp_char.strip('\n')))
                tmp_char_len = len(tmp_char.strip('\n'))
                tmp_char_len2 += tmp_char_len
                tmp_char = ''
        punctuations_len = i
    characters_len = tmp_char_len1 + tmp_char_len2

    # print("句子数量：", len(sentences))

    return sentences, characters_len, punctuations_len


def similarity(Doctor_talk_list, Patient_talk_list):
    '''
    计算文本余弦相似度
    :param Doctor_talk_list: 医生文本
    :param Patient_talk_list: 患者文本
    :return:DP_similarity：相似度
    '''

    doctor_content = " ".join(Doctor_talk_list)
    # print("doctor_content:", doctor_content)
    s1_cut = [i for i in jieba.cut(doctor_content, cut_all=True) if i != '']

    patient_content = " ".join(Patient_talk_list)
    # print("patient_content:", patient_content)
    s2_cut = [i for i in jieba.cut(patient_content, cut_all=True) if i != '']
    # print("s1_cut:", s1_cut)
    # print("s2_cut:", s2_cut)
    word_set = set(s1_cut).union(set(s2_cut))
    # print("word_set:", word_set)

    word_dict = dict()
    i = 0
    for word in word_set:
        word_dict[word] = i
        i += 1
    # print("word_dict:", word_dict)

    s1_cut_code = [word_dict[word] for word in s1_cut]
    # print("s1_cut_code:", s1_cut_code)
    s1_cut_code = [0] * len(word_dict)

    for word in s1_cut:
        s1_cut_code[word_dict[word]] += 1
    # print("s1_cut_code:", s1_cut_code)

    s2_cut_code = [word_dict[word] for word in s2_cut]
    # print("s2_cut_code:", s2_cut_code)
    s2_cut_code = [0] * len(word_dict)
    for word in s2_cut:
        s2_cut_code[word_dict[word]] += 1
    # print("s2_cut_code:", s2_cut_code)

    # 计算余弦相似度
    sum = 0
    sq1 = 0
    sq2 = 0
    for i in range(len(s1_cut_code)):
        sum += s1_cut_code[i] * s2_cut_code[i]
        sq1 += pow(s1_cut_code[i], 2)
        sq2 += pow(s2_cut_code[i], 2)

    try:
        DP_similarity = round(float(sum) / (math.sqrt(sq1) * math.sqrt(sq2)), 2)
    except ZeroDivisionError:
        DP_similarity = 0.0
    print("DP_similarity:", DP_similarity)

    return DP_similarity



if __name__ == '__main__':
    main()
