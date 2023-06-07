import pandas as pd
df=pd.read_excel(r'D:\Users\PC\Desktop\pandas_files\电力销售明细.xls')
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', None)#加入数值显示固定行&列数
pd.set_option('display.width', 1000)
#取消科学计数法并保留三位小数
pd.set_option('display.float_format', lambda x: f'{x:.3f}')
# 显示所有行
pd.set_option('display.max_rows', None)
df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
print(df.head(10))

