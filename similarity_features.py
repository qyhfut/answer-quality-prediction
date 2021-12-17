#-*- coding = utf-8 -*-
#@Time : 2021/1/14 16:07
#@Author : 张彩云
#@File ：features.py
#@Software: PyCharm


import re
import xlwt
import jieba
import jieba.posseg as psg
import jieba.analyse
import math





def main():
    filename = 'F:/haodf-prediction/2020/2020text/2020-60001-70000.txt'  # 读取文件
    filepath2 = 'F:/haodf-prediction/stopwords/cn_stopwords.txt'  # 停用词列表
    save_path = 'F:/haodf-prediction/2020/2020similarity/2020-60001-70000.xls'  # 保存位置

    source = open(filename, 'r', encoding='utf-8')
    diff_line = source.readlines()

    id_line = find_idline(diff_line)
    print("共有数据个数:",(len(id_line)-1))
    text_list = cut_text(diff_line, id_line)


    sum_satis_list = []

    for i in range(0, len(id_line)-1):
        satis_list = []
        each_list = text_list[i]
        print("-----------------------正在处理{}数据--------------------------".format(each_list[0].split()))
        satis_list.append(each_list[0].split())      #添加第一列id
############################ 医生文本 ##############################################################################
        # print("-------------------- 医生 --------------------")
        Doctor_talk_list = find_each_Doctor_talk(each_list)
        # print("Doctor_talk_list", Doctor_talk_list)
        Doctor_satis_list = num_Statistics(Doctor_talk_list, filepath2)
        satis_list.extend(Doctor_satis_list)
        #总字符数 num_doctor_characters   总标点符号数 num_doctor_punctuations   总字数 num_doctor_words   句子总数num_doctor_sentences
        #名词总数 num_doctor_nouns, 动词总数 num_doctor_verbs, 形容词总数 num_doctor_adjs, 副词总数 num_doctor_dvs, 总词语数 num_doctor_tagging



############################ 患者文本 ##############################################################################
        # print("-------------------- 患者 --------------------")
        Patient_talk_list = find_each_patient_talk(each_list)
        # print("Patient_talk_list", Patient_talk_list)
        Patient_satis_list = num_Statistics(Patient_talk_list,filepath2)
        satis_list.extend(Patient_satis_list)


############################# 相似度 ##############################################################################
        DP_similarity = similarity(Doctor_talk_list, Patient_talk_list)
        satis_list.append(DP_similarity)

############################ 保存文件 ##############################################################################
        sum_satis_list.append(satis_list)

    save_data(sum_satis_list, save_path)


def save_data(sum_satis_list, save_path):

    # 创建workbook对象
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)

    # 创建工作表
    sheet = book.add_sheet('文本特征统计', cell_overwrite_ok=True)
    # 创建一个列的元组
    col = ('id', 'num_doctor_characters', 'num_doctor_punctuations', 'num_doctor_words', 'num_doctor_sentences',
           'num_doctor_nouns', 'num_doctor_verbs', 'num_doctor_adjs', 'num_doctor_dvs', 'num_doctor_tagging',
            'num_patient_characters', 'num_patient_punctuations', 'num_patient_words', 'num_patient_sentences',
            'num_patient_nouns', 'num_patient_verbs', 'num_patient_adjs', 'num_patient_dvs', 'num_patient_tagging',
            'DP_similarity')

    for i in range(0, 20):
        sheet.write(0, i, col[i])


    for i in range(0, len(sum_satis_list)):
        satis_list = sum_satis_list[i]
        for j in range(0, 20):
            sheet.write(i+1, j, satis_list[j])

    book.save(save_path)





def num_Statistics(talk_list, filepath2):
    a = 0
    m = 0
    s = 0
    num_nouns = 0
    num_verbs = 0
    num_adjs = 0
    num_dvs = 0
    num_tagging = 0
    for n in range(0, len(talk_list)):
        content = talk_list[n]
        sentences, characters_len, punctuations_len = cut_sentences(content)
        # print('\n\n'.join(sentences))
        # print("医生句子数量：", len(doctor_sentences))
        a += characters_len  # 字数
        m += len(sentences)
        s += punctuations_len
        stopwordslist(filepath2)  # 停用词列表
        nouns_len, verbs_len, adjs_len, dvs_len, tagging_len = pretext(content, filepath2)
        num_nouns += nouns_len
        num_verbs += verbs_len
        num_adjs += adjs_len
        num_dvs += dvs_len
        num_tagging += tagging_len

    satis_list = []
    num_characters = a
    satis_list.append(num_characters)
    print("总字符数：", num_characters)

    num_punctuations = s
    satis_list.append(num_punctuations)
    print("总标点符号数：", num_punctuations)

    num_words = a - s
    satis_list.append(num_words)
    print("总字数：", num_words)

    num_sentences = m
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
    print("总词语：", num_tagging)
    satis_list.append(num_tagging)

    return satis_list

def stopwordslist(filepath2):  # 创建停用词列表
    stopword = [line.strip() for line in open(filepath2, 'r', encoding="utf-8").readlines()]  # 以行的形式读取停用词表，同时转换为列表
    return stopword

def pretext(contents,filepath2):  # 去除停用词、词性标注

    content1 = contents.replace(' ', '')  # 去掉文本中的空格
    # print('\n【去除空格后的文本：】' + '\n' + content1)

    pattern = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")  # 只保留中英文、数字，去掉符号
    content2 = re.sub(pattern, '', content1)  # 把文本中匹配到的字符替换成空字符
    # print('\n【去除符号后的文本：】' + '\n' + content2)


    cutwords = jieba.lcut(content2, cut_all=False)  # 精确模式分词
    # print('\n【精确模式分词后:】' + '\n' + "/".join(cutwords))
    lastword1 = psg.lcut(content2)
    tagging = [(words.word, words.flag) for words in lastword1]   # 转换为列表
    tagging_len = len(tagging)



    stopwords = stopwordslist(filepath2)  # 这里加载停用词的路径
    words = ''
    for word in cutwords:  # for循环遍历分词后的每个词语
        if word not in stopwords:  # 判断分词后的词语是否在停用词表内
            if word != '\t':
                words += word
                words += "/"
    # print('\n【去除停用词后的分词：】' + '\n' + words)
    content3 = words.replace('/', '')  # 去掉文本中的斜线

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

    return nouns_len, verbs_len, adjs_len, dvs_len, tagging_len

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

def cut_text(diff_line,id_line):
    text_list = []
    for c in range(0, len(id_line)-1):
        m = id_line[c]
        n = id_line[c+1]
        rows_list = []
        for y, rows in enumerate(diff_line):

            if y in range(m, n):
                rows_list.append(rows)
        text_list.append(rows_list)
    return text_list

def cut_Diatext(id_line,Dia_line,diff_line):
    Dia_list = []
    for c in range(0, len(id_line)-1):
        m = id_line[c+1]
        n = Dia_line[c]
        rows_list = []
        for y, rows in enumerate(diff_line):
            if y in range(n, m):
                rows_list.append(rows)
        Dia_list.append(rows_list)
    return Dia_list

def find_idline(diff_line):
    id_line = []
    i = 0
    for line in diff_line:
        match_id = re.search(r'id=(\d*\n)', line)  # id=?

        if match_id:
            id_line.append(i)
        i = i + 1
    id_line.append(len(diff_line)+3)
    return id_line

def find_each_Dialine(each_list):        #查找Dialogue
    i = 0
    global each_Dia_line
    for line in each_list:
        match_Dia = re.search(r'Dialogue', line)  # id=?

        if match_Dia:
            each_Dia_line = i
        i = i + 1
    return each_Dia_line

def find_each_Doctor_talk(each_list):        #查找Dialogue
    i = 0

    Doctor_talk_list = []
    for line in each_list:
        match = re.search(r'医生：\n', line)  # id=?

        if match:
            Doctor_talk_list.append(each_list[i+1].strip('\n'))
        i = i + 1
    # print("Doctor_talk_list", Doctor_talk_list)

    return Doctor_talk_list

def find_each_patient_talk(each_list):        #查找Dialogue
    i = 0

    patient_talk_list = []
    for line in each_list:
        match_Obj = re.search(r'疾病：(.*)', line)  # 疾病
        match_time = re.search(r'患病时长:(.*)', line)  # 患病时长
        match_desc = re.search(r'病情描述：(.*)', line)  # 病情描述
        match_help = re.search(r'希望提供的帮助：(.*)', line)  # 希望提供的帮助
        match_hosp = re.search(r'所就诊医院科室：(.*)', line)  # 所就诊医院科室
        match_cure = re.search(r'治疗情况：(.*)', line)  # 治疗情况
        match_drugs = re.search(r'用药情况：(.*)', line)  # 用药情况
        match_hist = re.search(r'既往病史：(.*)', line)  # 既往病史

        match_patient = re.search(r'病人：\n', line)

        if match_Obj:
            patient_talk_list.append(match_Obj.group().replace("疾病：", ""))
        elif match_time:
            patient_talk_list.append(match_time.group().replace("患病时长:", ""))
        elif match_desc:
            patient_talk_list.append(match_desc.group().replace("病情描述：", ""))
        elif match_help:
            patient_talk_list.append(match_help.group().replace("希望提供的帮助：", ""))
        elif match_cure:
            patient_talk_list.append(match_cure.group().replace("治疗情况：", ""))
        elif match_drugs:
            patient_talk_list.append(match_drugs.group().replace("用药情况：", ""))
        elif match_hist:
            patient_talk_list.append(match_hist.group().replace("既往病史：", ""))
        elif match_patient:
            patient_talk_list.append(each_list[i+1].strip('\n'))
        i = i + 1
    # print("patient_talk_list", patient_talk_list)
    return patient_talk_list


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

if __name__ == "__main__":
    main()