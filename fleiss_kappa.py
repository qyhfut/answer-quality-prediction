# Author: Yan Qiu
# November 08/11 2021

import numpy as np
import pandas as pd


'''
第一种实现方式
'''
def fleiss_kappa(M):
  N, k = M.shape
  n_annotators = float(np.sum(M[0, :]))
  p = np.sum(M, axis=0) / (N * n_annotators)
  P = (np.sum(M * M, axis=1) - n_annotators) / (n_annotators * (n_annotators - 1))
  # print P
  # print p
  Pbar = np.sum(P) / N
  PbarE = np.sum(p * p)
  kappa = (Pbar - PbarE) / (1 - PbarE)
  return kappa


# def transfer(T):
#     R
#     return R

"""
# Below is a test table in wikipedia's format, the result of this table should be 0.210.
table = np.array([[0, 0, 0, 0, 14],
                  [0, 2, 6, 4, 2],
                  [0, 0, 3, 5, 6],
                  [0, 3, 9, 2, 0],
                  [2, 2, 8, 1, 1],
                  [7, 7, 0, 0, 0],
                  [3, 2, 6, 3, 0],
                  [2, 5, 3, 2, 2],
                  [6, 5, 2, 1, 0],
                  [0, 2, 2, 3, 7]])
"""


data=np.loadtxt("E:/haodf-prediction/inter-rater data/fleiss_kappa_researchers5.csv",delimiter=",",skiprows=1)
print(data)
res = fleiss_kappa(data)
print(res)


'''
第二种实现方式
'''
# def fleiss_kappa(testData, N, k, n):  # testData表示要计算的数据
#   # (N,k）表示矩阵的形状，说明数据是N行k列的，一共有n个标注人员。 N=任务数量，k=划分为几个类别，n=标注人员数
#   dataMat = np.mat(testData, float)
#   oneMat = np.ones((k, 1))
#   sum = 0.0
#   P0 = 0.0
#   for i in range(N):
#     temp = 0.0
#     for j in range(k):
#       sum += dataMat[i, j]
#       temp += 1.0 * dataMat[i, j] ** 2
#     temp -= n
#     temp /= (n - 1) * n
#     P0 += temp
#   P0 = 1.0 * P0 / N
#   ysum = np.sum(dataMat, axis=0)
#   for i in range(k):
#     ysum[0, i] = (ysum[0, i] / sum) ** 2
#   Pe = ysum * oneMat * 1.0
#   ans = (P0 - Pe) / (1 - Pe)
#   return ans[0, 0]
#
# # data = pd.read_csv(r'E:/haodf-prediction/inter-rater data/fleiss_kappa.csv', delimiter=",", skiprows=1)
# # print(data)
# # results = fleiss_kappa(data, 10, 5, 14) #N=总任务数，k=类别数，n=评分人数量
# # print(results)
#
#
# data=np.loadtxt("E:/haodf-prediction/inter-rater data/fleiss_kappa_researchers456.csv",delimiter=",",skiprows=1)
# print(data)
# res = fleiss_kappa(data, 3, 2, 1)
# print(res)

