#-*- coding = utf-8 -*- 
#@Time : 2021/4/6 8:48
#@Author : Yan Qiu
#@File ：one_hot.py
#@Software: PyCharm

from sklearn import preprocessing
import pandas as pd
import xlwt
import numpy as np

#
# '''用于对离散数据进行one-hot编码操作'''
# # 1、转换成one-hot编码
# data_file = 'F:/haodf-prediction/data merge/2020match/lisan2.xls' # Excel文件存储位置
# data = pd.read_excel(data_file)
# data = data.values    # 转换成矩阵形式
# print("data:", data)
# enc = preprocessing.OneHotEncoder()
#
# enc.fit(data)
#
# # print("enc.n_values_ is:", enc.n_values_)     # n_values：是一个数组，长度为总的类别数量。即各个属性（feature）在 one hot 编码下占据的位数。
# # print("enc.feature_indices_ is:", enc.feature_indices_)  #feature_indices_：记录着属性在新 One hot 编码下的索引位置。 feature_indices_ 是对 n_values_ 的累积值，不过 feature_indices 的首位是 0；
# print(enc.transform(data).toarray())
# save_data = enc.transform(data).toarray()
#
# # 2、保存one-hot矩阵
# save_file = 'F:/haodf-prediction/data merge/2020match/lisan_02.xls'
# def save(data, path):
#   f = xlwt.Workbook() # 创建工作簿
#   sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True) # 创建sheet
#   [h, l] = data.shape # h为行数，l为列数
#   for i in range(h):
#     for j in range(l):
#       sheet1.write(i, j, data[i, j])
#   f.save(path)
# save(save_data, save_file)



# '''用于对连续数据进行归一化操作'''
# data_file = 'F:/haodf-prediction/data merge/2020match/lianxu2.xls' # Excel文件存储位置
# data = pd.read_excel(data_file)
# print(data)
#
# # 3、z-score归一化
# scaler = preprocessing.StandardScaler().fit(data)
#
# # print("scaler.mean_", scaler.mean_)      # 均值
# # print("scaler.std_", scaler.std_)        # 方差
# trans_data = scaler.transform(data)
# print(trans_data)
#
# # 4、保存归一化的数据
# trans_file = 'F:/haodf-prediction/data merge/2020match/lianxu_2.xls'
# def save(data, path):
#   f = xlwt.Workbook() # 创建工作簿
#   sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True) # 创建sheet
#   [h, l] = data.shape # h为行数，l为列数
#   for i in range(h):
#     for j in range(l):
#       sheet1.write(i, j, data[i, j])
#   f.save(path)
# save(trans_data, trans_file)


'''用于将连续型数据进行归一化操作，将其归一化到（0,1）'''
data_file = 'E:/haodf-prediction/data merge/2020match/one_hot/2020lianxu.xls' # Excel文件存储位置
data = pd.read_excel(data_file)
print(data)
data = data.values
print(data)

# 3、归一化
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
trans_data = min_max_scaler.fit_transform(data)

# 4、保存归一化的数据
trans_file = 'E:/haodf-prediction/data merge/2020match/one_hot/2020lianxu_01.xls'
def save(data, path):
  f = xlwt.Workbook() # 创建工作簿
  sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True) # 创建sheet
  [h, l] = data.shape # h为行数，l为列数
  for i in range(h):
    for j in range(l):
      sheet1.write(i, j, data[i, j])
  f.save(path)
save(trans_data, trans_file)
