import pandas as pd
import numpy as np
np.set_printoptions(suppress=True)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.rcParams['font.sans-serif'] = ['SimHei']

import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import MinMaxScaler #归一化
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.cluster import KMeans


# 读取数据(index_col=1即 index_col 的值 1 是从 0 开始计数的）设为DataFrame 的行索引,企业名称作为行索引，第二行作为行索引)
#  DataFrame 使用了 iloc 方法来筛选数据，保留从第二行（也就是索引为 1 的行）到最后一行的全部数据。
df = pd.read_excel(r'C:\Users\PC\Desktop\test\2021年10月能耗汇总.xlsx',index_col=1)[[
    '万元产值能耗(千克标准煤/万元)',
    '表三总用电量(万千瓦时)',
    '等价值综合能耗（吨标准煤）'
]].iloc[1:,:]
# 筛选数据（企业名称在名单内的）
df_energy = pd.read_excel(r'C:\Users\PC\Desktop\test\能耗月数据_20220622.xlsx')
df = df[df.index.isin(df_energy['企业名'].to_list())]
# #剔除异常点的数据~df不属于
df = df[~df.index.isin(['中国石油化工股份有限公司镇海炼化分公司',
                        '巨化集团公司',
                        '宁波钢铁有限公司',
                        '衢州元立金属制品有限公司',
                        '宁波中金石化有限公司'
                        ])]

# 构造需要的数据格式
df1 = pd.DataFrame()
#将原数据流的行索引同步到新索引中
df1.index = df.index
df1['万元产值能耗(千克标准煤/万元)'] = df['万元产值能耗(千克标准煤/万元)'].astype('float')
df1['电能占有率'] = df['表三总用电量(万千瓦时)'].astype('float')*1.229/df['等价值综合能耗（吨标准煤）'].astype('float')*100
df1['等价值综合能耗（吨标准煤）'] = df['等价值综合能耗（吨标准煤）'].astype('float')

#数据归一缩放转为多维数组(#默认将数据缩为0-1)
mm = MinMaxScaler()
data=mm.fit_transform(df1)


# #计算K取几类
# def juleiping(n):
#     julei= KMeans(n_clusters=n)
#     julei.fit(data)
#     label=julei.labels_
#     #
#     lkxs=silhouette_samples(data,label,metric='euclidean')
#     means=np.mean(lkxs)
#     return means
# y=[]
# for n in range (2,23):
#     means=juleiping(n)
#     y.append(means)
# #取第四类是最好的（取最接近1的）
# print(y)

# 创建KMeans模型,选择K=5进行聚类,分5类
model = KMeans(n_clusters=5, init='k-means++',max_iter=100) #分为k类，最多迭代100次，init='k-means++'自主选择最佳初始点位
# 使用数据训练模型
model.fit(data)
# 获取聚类标签
labels = model.labels_
# 获取质心坐标
centers = model.cluster_centers_
# 获取SSE
SSE = model.inertia_


#关于查看质心等指标数据
#查看质心
print(model.cluster_centers_)
#查看反归一化的质心
print(mm.inverse_transform(model.cluster_centers_))
#查看标签类别（数量与数据总量一致）
print(model.labels_)
#查看
#查看标签类别的数据分类情况
pd.Series(model.labels_).value_counts()

#查看聚类中心并反归一化（一个多维数组，K个数组元素，实际就是K的坐标）
center = mm.inverse_transform(model.cluster_centers_) #聚类中心反归一化
# 打标
df1['聚类类别'] = model.labels_#新增聚类类别列,数据为[0,K-1]的整数，分类标志

#将K个质点对应的坐标进行拆解，每个坐标对应一列特征数据
#center[x][0] 表示第 x 个类别的质心的第一个特征（‘万元产值能耗(千克标准煤/万元)’）的取值,对应K的
df1['万元产值能耗(千克标准煤/万元)_聚类中心'] = df1['聚类类别'].apply(lambda x:center[x][0])
df1['电能占有率_聚类中心'] = df1['聚类类别'].apply(lambda x:center[x][1])
df1['等价值综合能耗（吨标准煤）_聚类中心'] = df1['聚类类别'].apply(lambda x:center[x][2])

#重新输出df1进行查看
print(df1)
df1.to_excel(r'C:\Users\PC\Desktop\test\K_means算法2021年10月_聚类分析结果数据.xlsx')
fig = plt.figure(figsize=(10,10))
x = df1[df1['聚类类别']==0]['万元产值能耗(千克标准煤/万元)']
y = df1[df1['聚类类别']==0]['电能占有率']
z = df1[df1['聚类类别']==0]['等价值综合能耗（吨标准煤）']
#ax = fig.gca(projection="3d")
ax = fig.add_axes(Axes3D(fig))
ax.scatter(df1[df1['聚类类别']==0]['万元产值能耗(千克标准煤/万元)'],
           df1[df1['聚类类别']==0]['电能占有率'],
           df1[df1['聚类类别']==0]['等价值综合能耗（吨标准煤）'],
           zdir="z",c="r",marker="o", s=40)
ax.scatter(df1[df1['聚类类别']==1]['万元产值能耗(千克标准煤/万元)'],
           df1[df1['聚类类别']==1]['电能占有率'],
           df1[df1['聚类类别']==1]['等价值综合能耗（吨标准煤）']
           ,zdir="z",c="g",marker="o", s=40)
ax.scatter(df1[df1['聚类类别']==2]['万元产值能耗(千克标准煤/万元)'],
           df1[df1['聚类类别']==2]['电能占有率'],
           df1[df1['聚类类别']==2]['等价值综合能耗（吨标准煤）'],
           zdir="z",c="b",marker="o", s=40)
ax.scatter(df1[df1['聚类类别']==3]['万元产值能耗(千克标准煤/万元)'],
           df1[df1['聚类类别']==3]['电能占有率'],
           df1[df1['聚类类别']==3]['等价值综合能耗（吨标准煤）'],
           zdir="z",c="y",marker="o", s=40)
ax.scatter(df1[df1['聚类类别']==4]['万元产值能耗(千克标准煤/万元)'],
           df1[df1['聚类类别']==4]['电能占有率'],
           df1[df1['聚类类别']==4]['等价值综合能耗（吨标准煤）'],
           zdir="z",c="c",marker="o", s=40)
# ax.scatter(df1[df1['聚类类别']==5]['万元产值能耗(千克标准煤/万元)'],
#            df1[df1['聚类类别']==5]['电能占有率'],
#            df1[df1['聚类类别']==5]['等价值综合能耗（吨标准煤）'],
#            zdir="z",c="grey",marker="o", s=40)
# ax.scatter(df1[df1['聚类类别']==6]['万元产值能耗(千克标准煤/万元)'],
#            df1[df1['聚类类别']==6]['电能占有率'],
#            df1[df1['聚类类别']==6]['等价值综合能耗（吨标准煤）'],
#            zdir="z",c="k",marker="o", s=40)
# ax.scatter(df1[df1['聚类类别']==7]['万元产值能耗(千克标准煤/万元)'],
#            df1[df1['聚类类别']==7]['电能占有率'],
#            df1[df1['聚类类别']==7]['等价值综合能耗（吨标准煤）'],
#            zdir="z",c="m",marker="o", s=40)

ax.set(xlabel='万元产值能耗(千克标准煤/万元)', ylabel="电能占有率", zlabel="等价值综合能耗（吨标准煤）")
ax.set_title('3D Scatter Plot')
plt.savefig('3d.jpg')
plt.show()