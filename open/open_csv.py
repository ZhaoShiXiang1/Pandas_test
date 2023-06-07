import pandas as pd
##打开CSV文件
with open(r'D:\Users\PC\Desktop\pandas_files\电力销售明细.csv',encoding='utf-8') as f:
    df=pd.read_csv(f)
    print(df)

