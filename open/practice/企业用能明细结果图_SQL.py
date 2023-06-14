import pandas as pd
import os
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())
os.environ["NUMEXPR_MAX_THREADS"] = "32"


df2=pd.read_excel(r'C:\Users\PC\Desktop\test\能耗月数据_20230601.xlsx')
with open(r'C:\Users\PC\Desktop\test\企业.csv',encoding='utf-8') as f:
    df1=pd.read_csv(f)

q = r"""
    SELECT distinct 
    A.企业名称,
    A.统一信用代号,
    A.ym,
    max(A.行业),
    A.地市,
    max(A.能耗等级),
    sum(A.pq),
    D."电(千瓦时)",
    D."煤(标准煤)",
    D."油(标准煤)",
    D."天然气(标准煤)",
    D."热力(标准煤)",
    D."综合能耗(标准煤)",
    CASE
        WHEN D."综合能耗(标准煤)" is null then 1
        ELSE 0
    END AS 是否补数据
FROM
    df1 A
INNER JOIN
    df2 B
ON
    A.企业名称 = B.企业名
LEFT JOIN
    df2 D
ON
    A.企业名称 = D.企业名 AND
    A.ym = D.年月
group by 
    A.企业名称,
    A.统一信用代号,
    A.ym,
    A.地市,
    D."电(千瓦时)",
    D."煤(标准煤)",
    D."油(标准煤)",
    D."天然气(标准煤)",
    D."热力(标准煤)",
    D."综合能耗(标准煤)"    
;
    """
pandaSQL_solution = pysqldf(q)
pandaSQL_solution.to_excel(r'C:\Users\PC\Desktop\test\结果_SQL.xlsx', index=False)




#where A.企业名称 is not in (slelct df2.企业名 from df2 group by df2.企业名)
# df3=pd.merge(df1,df2,how='left',left_on=['企业名称','ym'],right_on=['企业名','年月'])
#
# df3.loc[(df3["综合能耗(标准煤)"].isnull()),'是否补数据']='1'
# df3=df3[df3['企业名称'].isin(df2['企业名'])]
# df3=df3.drop_duplicates()
# df4=df3.groupby(["企业名称","统一信用代号","ym","地市","电(千瓦时)","煤(标准煤)","油(标准煤)","天然气(标准煤)","热力(标准煤)","综合能耗(标准煤)","是否补数据"],dropna=False,).agg({"能耗等级":"max","行业":"max","pq":"sum"}).reset_index()
# df3=df4[['企业名称','统一信用代号','ym','行业','地市','能耗等级','pq','电(千瓦时)','煤(标准煤)','油(标准煤)','天然气(标准煤)','热力(标准煤)','综合能耗(标准煤)','是否补数据']]
# df3.to_excel(r'C:\Users\PC\Desktop\test\结果.xlsx', index=False)







