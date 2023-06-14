import pandas as pd
import os
os.environ["NUMEXPR_MAX_THREADS"] = "32"


df2=pd.read_excel(r'C:\Users\PC\Desktop\test\能耗月数据_20230601.xlsx')
with open(r'C:\Users\PC\Desktop\test\企业.csv',encoding='utf-8') as f:
    df1=pd.read_csv(f)
# print(df1.columns)
# print(df2.columns)
#企业明细表关联能耗明细表
df3=pd.merge(df1,df2,how='left',left_on=['企业名称','ym'],right_on=['企业名','年月'])
#关联为空 是否追补数据新增为1
df3.loc[(df3["综合能耗(标准煤)"].isnull()),'是否补数据']='1'
#提取宽表中对应能耗明细表企业的数据
df3=df3[df3['企业名称'].isin(df2['企业名'])]
#去重
#df3=df3.drop_duplicates()
#分组，对能耗等级、行业、pq求和
df4=df3.groupby(["企业名称","统一信用代号","ym","地市","电(千瓦时)","煤(标准煤)","油(标准煤)","天然气(标准煤)","热力(标准煤)","综合能耗(标准煤)","是否补数据"],dropna=False,).agg({"能耗等级":"max","行业":"max","pq":"sum"}).reset_index()
#df4=df3.groupby(["企业名称","统一信用代号","ym","行业","地市","能耗等级","电(千瓦时)","煤(标准煤)","油(标准煤)","天然气(标准煤)","热力(标准煤)","综合能耗(标准煤)","是否补数据"],dropna=False,).agg({"pq":"sum"}).reset_index()
#获取需要的字段
df3=df4[['企业名称','统一信用代号','ym','行业','地市','能耗等级','pq','电(千瓦时)','煤(标准煤)','油(标准煤)','天然气(标准煤)','热力(标准煤)','综合能耗(标准煤)','是否补数据']]
print(df3)
#导出数据
df3.to_excel(r'C:\Users\PC\Desktop\test\tmp.xlsx', index=False)







