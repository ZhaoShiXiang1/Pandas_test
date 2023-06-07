import pandas as pd
import os
os.environ["NUMEXPR_MAX_THREADS"] = "32"


df2=pd.read_excel(r'C:\Users\PC\Desktop\test\能耗月数据_20230601.xlsx')
with open(r'C:\Users\PC\Desktop\test\企业.csv',encoding='utf-8') as f:
    df1=pd.read_csv(f)
# print(df1.columns)
# print(df2.columns)
df3=pd.merge(df1,df2,how='left',left_on=['企业名称','ym'],right_on=['企业名','年月'])

df3.loc[(df3["综合能耗(标准煤)"].isnull()),'是否补数据']='1'
df3=df3[df3['企业名称'].isin(df2['企业名'])]
df3=df3.drop_duplicates()
df4=df3.groupby(["企业名称","统一信用代号","ym","地市","电(千瓦时)","煤(标准煤)","油(标准煤)","天然气(标准煤)","热力(标准煤)","综合能耗(标准煤)","是否补数据"],dropna=False,).agg({"能耗等级":"max","行业":"max","pq":"sum"}).reset_index()
df3=df4[['企业名称','统一信用代号','ym','行业','地市','能耗等级','pq','电(千瓦时)','煤(标准煤)','油(标准煤)','天然气(标准煤)','热力(标准煤)','综合能耗(标准煤)','是否补数据']]
df3.to_excel(r'C:\Users\PC\Desktop\test\结果.xlsx', index=False)









#df3=pd.merge(df3,df2,how='inner',left_on=['企业名称'],right_on=['企业名'])h
#包含



#print(df3.columns)
#df3.reset_index(drop=False)




# print(df3)


#
# # df3=df3.drop_duplicates()
# #
#df4.to_excel(r'D:\Users\PC\Desktop\test\结果.xlsx', index=False)
# print(df3)

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