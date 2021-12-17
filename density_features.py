#-*- coding = utf-8 -*- 
#@Time : 2021/3/18 21:19
#@Author : 张彩云
#@File ：density.py
#@Software: PyCharm


import xlrd
import re
import xlwt

def main():
    filename = 'F:/haodf-prediction/2020/2020xls/2020-60001-70000.xls'
    filepath2 = 'F:/haodf-prediction/medical terms/医学词汇完整.txt'  # 医学词汇列表
    save_path = 'F:/haodf-prediction/2020/2020density/2020-60001-70000.xls'

    Medicalword = Medicalwordslist(filepath2)
    # print("Medicalword:", Medicalword)
    id, answers = read_excel(filename)

############################ 医生文本 ##############################################################################
    density_list = []
    ans_cnt = 0
    for ans in answers:
        doctor_satis_list = []
        ans_cnt += 1
        print("-------------------- 医生 --------------------")
        print("第{}条".format(ans_cnt))
        print("ans:", ans)
        print("id[ans_cnt-1]:", id[ans_cnt-1])

        sentences, num_characters, num_punctuations = cut_sentences(ans)
        num_words = num_characters - num_punctuations
        print("总字数：", num_words)

        words = []  # 医学专业词的总长度
        for word in Medicalword:
            if word in ans:
                print("word:", word)
                words.append(word)

        words_len = 0
        for i in range(len(words)):
            words_len += len(words[i])


        density = words_len/num_words  # 医学专业词的密度

        doctor_satis_list.append(id[ans_cnt - 1])
        doctor_satis_list.append(words_len)
        doctor_satis_list.append(num_words)
        doctor_satis_list.append(density)
        density_list.append(doctor_satis_list)

    save_doctor_data(density_list, save_path)



def read_excel(filename):
    # 打开文件

    workBook = xlrd.open_workbook(filename)

    ## 按sheet名字获取sheet内容
    sheet_content = workBook.sheet_by_name('病例文本')

    # 3. sheet的名称，行数，列数
    print(sheet_content.name, sheet_content.nrows, sheet_content.ncols)

    id = sheet_content.col_values(0)
    print("id:", id)

    answers = sheet_content.col_values(5)
    print("answers", answers)
    return id,  answers


def Medicalwordslist(filepath2):  # 创建专业医学词汇列表
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    Medicalword = [re.sub(pattern, "", line.strip().replace(" ", '')) for line in open(filepath2, 'r', encoding="utf-8").readlines()]  # 以行的形式读取停用词表，同时转换为列表
    return Medicalword

def find_chinese(file):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, '', file)
    print(chinese)

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



def save_doctor_data(doctor_list, save_path):
    # 创建workbook对象
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建工作表
    sheet = book.add_sheet('医生文本特征统计', cell_overwrite_ok=True)
    # 创建一个列的元组
    col = ('id', '专业医学词汇字数', '总字数', '关键词密度')

    for i in range(0, 4):
        sheet.write(0, i, col[i])


    for i in range(0, len(doctor_list)):
        satis_list = doctor_list[i]
        for j in range(0, 4):
            sheet.write(i+1, j, satis_list[j])
    book.save(save_path)


if __name__ == '__main__':
    main()