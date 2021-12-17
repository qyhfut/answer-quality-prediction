#-*- coding = utf-8 -*- 
#@Time : 2021/1/5 16:06
#@Author : 张彩云
#@File ：text_cut.py
#@Software: PyCharm


######将TXT文件按照问答导入到excel文件中，问题一列，答案一列######

import re
import xlwt

def main():
    filename = 'F:/haodf-prediction/2020/2020text/2019_60001-70000.txt'
    source = open(filename, 'r', encoding='utf-8')
    diff_line = source.readlines()
    # print("diff_line", diff_line)

###########################################################################################################
    save_path = 'F:/haodf-prediction/2020/2020text/2020_60001-70000.xls'
    # 创建workbook对象
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建工作表
    sheet = book.add_sheet('病例文本', cell_overwrite_ok=True)
    # 创建一个列的元组
    col = ('1id=？', '2href', '3疾病', '4病情描述', '5que', '6ans')
    for i in range(0, 6):
        sheet.write(0, i, col[i])

###########################################################################################################
    id_line = find_idline(diff_line)
    # print("id_line", id_line)

    print("共有数据个数:",(len(id_line)-1))
    text_list = cut_text(diff_line, id_line)

    for i in range(0, len(id_line)-1):
        each_list = text_list[i]
        # print("each_list", each_list)
        # print("id={}".format(i))
        print('----------------------------------------------------------------------')
        print("正在写入第id={}条数据".format(i))


        each_Dia_line = find_each_Dialine(each_list)

        que_talk = ''
        ans = ''
        if each_Dia_line == 0:
            continue
        else:
            match_id = each_list[0]
            sheet.write(i + 1, 0, match_id)
            match_href = each_list[1]
            sheet.write(i + 1, 1, match_href)

            for z in range(0, (len(each_list)-each_Dia_line)):
                if '医生：' in each_list[each_Dia_line+z]:
                    ans += add_punc_if(each_list[each_Dia_line+z+1].strip().replace("\n", ""))
                    if len(ans) < 15:
                        continue
                    sheet.write(i + 1, 5, ans)
                if '患者：' in each_list[each_Dia_line+z]:
                    que_talk += add_punc_if(each_list[each_Dia_line+z+1].strip().replace("\n", ""))


        que = ''
        for x in range(0, each_Dia_line):
            if '疾病：' in each_list[x]:
                matchObj = add_punc_if(each_list[x + 1].strip().replace("\n", ""))
                sheet.write(i + 1, 2, matchObj.strip().replace("\n", ""))  # 3、疾病
                que += matchObj.strip().replace("\n", "").replace("疾病：", "")

            if '病情描述：' in each_list[x]:
                match_desc = add_punc_if(each_list[x + 1].strip().replace("\n", ""))
                sheet.write(i + 1, 3, match_desc.strip().replace("\n", ""))  # 4、病情描述
                que += match_desc.strip().replace("\n", "").replace("病情描述：", "")

            else:
                pass

        que += que_talk
        if len(que) < 15:
            continue
        sheet.write(i + 1, 4, que)
    book.save(save_path)

def cut_text(diff_line,id_line):
    text_list=[]

    for c in range(0, len(id_line)-1):
        m = id_line[c]
        n = id_line[c+1]
        rows_list = []
        for y, rows in enumerate(diff_line):

            if y in range(m, n):
            # print("rows",rows)
                rows_list.append(rows)
        text_list.append(rows_list)
    # print("text_list",text_list)

    return text_list

def add_punc_if(content):

    end_flag = [',', '?', '!', '.', ';', '，', '？', '！', '。', '；', '…', ' ', ' ']

    content_len = len(content)
    tmp_char = ''
    for idx, char in enumerate(content):
        # 拼接字符
        tmp_char += char
        # 判断是否已经到了最后一位
        if (idx + 1) == content_len:
            if char in end_flag:
                break
            else:
                content += '。'
    return content


def cut_Diatext(id_line, Dia_line, diff_line):
    Dia_list = []

    for c in range(0, len(id_line)-1):
        m = id_line[c+1]
        n = Dia_line[c]
        rows_list = []
        for y, rows in enumerate(diff_line):

            if y in range(n, m):
            # print("rows",rows)
                rows_list.append(rows)
        Dia_list.append(rows_list)
    # print("Dia_list",Dia_list)

    return Dia_list

def find_idline(diff_line):
    id_line = []
    i = 0
    for line in diff_line:

        match_id = re.search(r'id=(\d*\n)', line)  # id=?

        if match_id:
            # print("match_id: ", match_id.group())
            # print("id所在行数：", i)
            id_line.append(i)
        i = i + 1
    id_line.append(len(diff_line))
    # print("id_line", id_line)
    return id_line

def find_each_Dialine(each_list):        #查找Dialogue

    i = 0
    each_Dia = []
    for line in each_list:
        i += 1
        match_Dia = re.search(r'Dialogue\n', line)

        if match_Dia:
            each_Dia.append(i)
            break

    if each_Dia == []:
        each_Dia.append(0)


    each_Dia_line = each_Dia[0]
    print("each_Dia_line", each_Dia_line)
    return each_Dia_line



if __name__ == "__main__":
    main()