import pandas as pd

def ler_planilha(caminho):
    if caminho.endswith('.csv'):
        df = pd.read_csv(caminho)
    else:
        df = pd.read_excel(caminho)
    return df