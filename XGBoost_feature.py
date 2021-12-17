import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,  precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.naive_bayes import GaussianNB

data=pd.read_csv(r"F:/haodf-prediction/final data/2020_textual features.csv")

X =  data.iloc[:,0:27]
y= data.iloc[:,-1]
# print(X)

#划分数据集，按照6：2：2
X_train_vali, X_test, y_train_vali, y_test = train_test_split(X, y, test_size = 0.20, random_state = 10)
X_train, X_vali, y_train, y_vali = train_test_split(X_train_vali, y_train_vali, test_size = 0.25, random_state = 10)


# 不均匀采样
from imblearn.over_sampling import SMOTE
smt = SMOTE(random_state=10)#random_statei相当于随机数种子的作用
X_train, y_train = smt.fit_resample(X_train, y_train)
X_train = pd.DataFrame(X_train, columns=list(X_train.columns))
print("nums of train/test set: ", len(X_train), len(X_test), len(y_train), len(y_test))


print('--- XGBoost model ---')
model = xgb.XGBClassifier(random_state=10)
model.fit(X_train, y_train)

preds= model.predict(X_test)
y_preds = model.predict_proba(X_test)[:,1]  ###预测概率


# Testing the outcome
# cm= confusion_matrix(test_y, y_pred)
# score=accuracy_score(test_y, y_pred)*100
acc = accuracy_score(y_test, preds)
precision = precision_score(y_test,preds)
recall = recall_score(y_test,preds)
f1 = f1_score(y_test, preds)
auc1 = roc_auc_score(y_test, y_preds)
print("Accuracy: ", acc)
print("Precision:",precision)
print("Recall:",recall)
print("F1 score: ", f1)
print("AUC: ", auc1)


# #ROC绘制
# # Compute ROC curve and ROC area for each class
# fpr,tpr,threshold = roc_curve(y_test, y_preds)#计算真正率和假正率
# roc_auc =auc(fpr, tpr)#计算auc的值
#
#
# # plt.figure()
# plt.rcParams['font.sans-serif']=['Times New Roman']  #用来显示英文标签
#
#
# #定义一种字体属性
# font1 = {'family': 'Times New Roman',
#          'weight': 'normal',
#          'size': 25}
#
#
# lw = 2
# plt.figure(figsize=(10,10))
# plt.plot(fpr, tpr, color='darkorange',
#          lw=lw, label='ROC curve (area = %0.3f)' % roc_auc) ###假正率为横坐标，真正率为纵坐标做曲线
# plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate', fontsize=25)
# plt.ylabel('True Positive Rate', fontsize=25)
# plt.title('Receiver Operating Characteristic of BERT-AdaBoost', fontdict=font1)
# plt.legend(loc="lower right", fontsize=25)
# # plt.savefig('./images/BERT-AdaBoost ROC.tif')
# plt.show()

# fpr2 = np.array(fpr)
# test1 = pd.DataFrame(fpr2)
# test1.to_csv("fpr_BERT-AdaBoost.csv")
#
# tpr2 = np.array(tpr)
# test2 = pd.DataFrame(tpr2)
# test2.to_csv("tpr_BERT-AdaBoost.csv")

#绘制特征重要性排序
feature_names = X_train.columns
feature_imports = model.feature_importances_
print(feature_names)
print(feature_imports)
most_imp_features = pd.DataFrame([f for f in zip(feature_names, feature_imports)],
                                 columns=["Feature", "Importance"]).nlargest(27, "Importance")

most_imp_features.sort_values(by="Importance", inplace=True)

plt.rcParams['font.sans-serif']=['Times New Roman']  #用来显示英文标签

plt.figure(figsize=(19, 11))
plt.rc('xtick', labelsize=22)
plt.barh(range(len(most_imp_features)), most_imp_features.Importance, align='center', alpha=0.8)
plt.yticks(range(len(most_imp_features)), most_imp_features.Feature, fontsize=22)
plt.xlabel('Importance', fontsize=25)
plt.title('Feature Importance for Answer Quality', fontsize=25)
plt.savefig('./images/XGBoost Importance.tif')
plt.show()