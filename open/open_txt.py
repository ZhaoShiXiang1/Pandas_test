import pandas as pd
##打开TXT文件
df1 = pd.read_table(r"D:\Users\PC\Desktop\pandas_files\2.txt",header=None) #读取 txt 文件
print(df1)
print('----------------')
df2 = pd.read_table(r"D:\Users\PC\Desktop\pandas_files\2.txt", sep=',',header=None) #读取 txt 文件,','分割
print(df2)