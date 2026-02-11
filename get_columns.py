import pandas as pd
try:
    df = pd.read_csv(r'c:\Users\Jayesh\Desktop\development\Fischer Jordan\FJ Assignment - FJ Assignment - Sheet1.csv')
    with open('columns.txt', 'w') as f:
        for col in df.columns:
            f.write(col + '\n')
    print("Columns written to columns.txt")
except Exception as e:
    print(e)
