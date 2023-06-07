
import pandas as pd
import pymysql as pymysql

conn=pymysql.connect(
    host='43.143.69.67',
    user='root',
    passwd='zsx.2468',
    db='game',
    port=3306,
    charset='utf8'
)
conn1=pymysql.connect(
    host='43.143.69.67',
    user='root',
    passwd='zsx.2468',
    db='game',
    port=3306,
    charset='utf8'
)
df1=pd.read_sql('select * from test',conn)
df2=pd.read_sql('select * from test2',conn1)
# # df=df['country'].value_counts()
# df.loc['6'] = ['曹操','魏']
# print(df)
# # print(df.describe())
# df=pd.merge(df1,df2,how='right',on=['name','country'])
df_pv_pivot=df2.pivot_table(index=['country'],columns='name',aggfunc={'num':sum,'num':'mean'})
# df3=df2.groupby(['country','name'])['num'].sum()
print(df_pv_pivot)