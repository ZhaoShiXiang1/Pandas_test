import pandas as pd


df2=pd.read_excel(r'D:\Users\PC\Desktop\test\能耗月数据_20230601.xlsx')
with open(r'D:\Users\PC\Desktop\test\企业.csv',encoding='utf-8') as f:
    df1=pd.read_csv(f)
# print(df1.columns)
# print(df2.columns)
df3=pd.merge(df1,df2,how='left',left_on=['企业名称','ym'],right_on=['企业名','年月'])
df3=pd.merge(df3,df2,how='inner',left_on=['企业名称'],right_on=['企业名'])
# print(df3.columns)
df3.reset_index(drop=False)
df3=df3[['企业名称','统一信用代号','ym','行业','地市','能耗等级','pq','电(千瓦时)_x','煤(标准煤)_x','油(标准煤)_x','天然气(标准煤)_x','热力(标准煤)_x','综合能耗(标准煤)_x']]
df3=df3.drop_duplicates()
df3.loc[(df3['电(千瓦时)_x'].isnull().T.any()),'是否补数据']='1'
df3.to_excel(r'D:\Users\PC\Desktop\test\结果.xlsx', index=False)
print(df3)

# pd.set_option('display.unicode.ambiguous_as_wide', True)
# pd.set_option('display.unicode.east_asian_width', True)
# pd.set_option('display.max_columns', None)#加入数值显示固定行&列数
# pd.set_option('display.width', 1000)
# #取消科学计数法并保留三位小数
# pd.set_option('display.float_format', lambda x: f'{x:.3f}')
# # 显示所有行
# pd.set_option('display.max_rows', None)
# df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
# print(df.head(10))