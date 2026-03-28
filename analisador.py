from groq import Groq
import json

cliente = Groq(api_key="SUA_CHAVE_GROQ_AQUI")

def _limpar_json(texto: str) -> str:
    texto = texto.replace("```json", "").replace("```", "").strip()
    inicio = texto.find("[")
    fim = texto.rfind("]")
    if inicio == -1 or fim == -1:
        raise ValueError(f"Nenhum JSON encontrado na resposta:\n{texto}")
    return texto[inicio:fim + 1]

def analisar_e_sugerir(df, tentativa=1):
    resumo = f"""
    Colunas: {list(df.columns)}
    Tipos: {df.dtypes.to_dict()}
    Primeiras linhas: {df.head(3).to_dict()}
    Estatísticas: {df.describe().to_dict()}
    Total de registros: {len(df)}
    """

    colunas_numericas = df.select_dtypes(include='number').columns.tolist()
    colunas_texto = df.select_dtypes(exclude='number').columns.tolist()

    if tentativa == 1:
        prompt = f"""
        Você é um analista de dados. Com base nos dados abaixo, sugira EXATAMENTE 4 gráficos
        relevantes para um dashboard. Para cada gráfico, retorne um JSON com:
        - tipo: "barra", "linha", "pizza", "dispersao" ou "histograma"
        - coluna_x: nome EXATO de uma coluna existente
        - coluna_y: nome EXATO de uma coluna NUMÉRICA (ou null se não aplicável)
        - titulo: título descritivo do gráfico
        - insight: 1 frase de insight sobre esse gráfico

        REGRAS OBRIGATÓRIAS:
        - coluna_y deve ser SEMPRE uma dessas colunas numéricas: {colunas_numericas}
        - coluna_x pode ser qualquer coluna: {list(df.columns)}
        - Retorne EXATAMENTE 4 gráficos, nem mais nem menos
        - Retorne APENAS o array JSON, sem texto antes ou depois, sem markdown

        Exemplo:
        [
          {{"tipo": "barra", "coluna_x": "Produto", "coluna_y": "Vendas", "titulo": "Vendas por Produto", "insight": "Produto A lidera."}},
          {{"tipo": "linha", "coluna_x": "Data", "coluna_y": "Receita", "titulo": "Receita ao Longo do Tempo", "insight": "Crescimento em 2023."}},
          {{"tipo": "pizza", "coluna_x": "Categoria", "coluna_y": null, "titulo": "Distribuição por Categoria", "insight": "Categoria X domina."}},
          {{"tipo": "histograma", "coluna_x": "Idade", "coluna_y": null, "titulo": "Distribuição de Idade", "insight": "Maioria entre 25-35."}}
        ]

        Dados:
        {resumo}
        """
    else:
        prompt = f"""
        Retorne APENAS um array JSON com EXATAMENTE 4 gráficos, sem nenhum texto extra.
        Colunas numéricas disponíveis: {colunas_numericas}
        Colunas de texto disponíveis: {colunas_texto}

        Formato obrigatório (4 itens):
        [
          {{"tipo":"barra","coluna_x":"{colunas_texto[0] if colunas_texto else colunas_numericas[0]}","coluna_y":"{colunas_numericas[0] if colunas_numericas else 'null'}","titulo":"Titulo 1","insight":"Insight 1."}},
          {{"tipo":"linha","coluna_x":"{colunas_texto[0] if colunas_texto else colunas_numericas[0]}","coluna_y":"{colunas_numericas[0] if colunas_numericas else 'null'}","titulo":"Titulo 2","insight":"Insight 2."}},
          {{"tipo":"pizza","coluna_x":"{colunas_texto[1] if len(colunas_texto) > 1 else colunas_texto[0] if colunas_texto else colunas_numericas[0]}","coluna_y":null,"titulo":"Titulo 3","insight":"Insight 3."}},
          {{"tipo":"histograma","coluna_x":"{colunas_numericas[0] if colunas_numericas else 'null'}","coluna_y":null,"titulo":"Titulo 4","insight":"Insight 4."}}
        ]
        """

    resposta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    texto = resposta.choices[0].message.content.strip()

    try:
        texto_limpo = _limpar_json(texto)
        return json.loads(texto_limpo)
    except Exception as e:
        if tentativa < 3:
            print(f"Tentativa {tentativa} falhou ({e}), tentando novamente...")
            return analisar_e_sugerir(df, tentativa + 1)
        else:
            raise ValueError(f"A IA não retornou um JSON válido após 3 tentativas.\nÚltima resposta:\n{texto}")