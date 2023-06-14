import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# 生成100个随机样本点
np.random.seed(0)
X = np.random.randn(100,2)

# 创建KMeans模型，指定聚类数为3
model = KMeans(n_clusters=3, random_state=0)

# 使用数据训练模型
model.fit(X)

# 获取聚类标签
labels = model.labels_

# 获取质心坐标
centers = model.cluster_centers_

# 获取SSE
SSE = model.inertia_

# 绘制散点图，并用不同颜色区分不同的聚类
plt.scatter(X[:,0], X[:,1], c=labels)
plt.scatter(centers[:,0], centers[:,1], marker='x', s=200, linewidths=3, color='r')

# 添加标题和SSE信息
plt.title('KMeans Clustering (SSE={:.2f})'.format(SSE))
plt.show()