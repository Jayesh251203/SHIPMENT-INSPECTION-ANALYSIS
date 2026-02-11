import pandas as pd
try:
    df = pd.read_csv(r'c:\Users\Jayesh\Desktop\development\Fischer Jordan\FJ Assignment - FJ Assignment - Sheet1.csv')
    unique_charges = df['Charge Type'].unique()
    with open('charge_types_utf8.txt', 'w', encoding='utf-8') as f:
        for charge in unique_charges:
            f.write(str(charge) + '\n')
    print("Charge types written to charge_types_utf8.txt in UTF-8")
except Exception as e:
    print(e)
