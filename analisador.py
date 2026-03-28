from groq import Groq
import json

cliente = Groq(api_key='SUA_API_KEY')

def analisar_e_sugerir(df):
    resumo = f"""
    Colunas: {list(df.columns)}
    Tipos: {df.dtypes.to_dict()}
    Primeiras linhas: {df.head(3).to_dict()}
    Estatísticas: {df.describe().to_dict()}
    Total de registros: {len(df)}
    """

    prompt = f"""
    Você é um analista de dados. Com base nos dados abaixo, sugira até 4 gráficos
    relevantes para um dashboard. Para cada gráfico, retorne um JSON com:
    - tipo: "barra", "linha", "pizza", "dispersao" ou "histograma"
    - coluna_x: nome da coluna para o eixo X (ou categoria)
    - coluna_y: nome da coluna para o eixo Y (ou None se não aplicável)
    - titulo: título do gráfico
    - insight: 1 frase de insight sobre esse gráfico

    Retorne APENAS um array JSON válido, sem texto antes ou depois, sem markdown.
    Exemplo:
    [
      {{"tipo": "barra", "coluna_x": "Produto", "coluna_y": "Vendas",
        "titulo": "Vendas por Produto", "insight": "Produto A lidera as vendas."}}
    ]

    Dados:
    {resumo}
    """

    resposta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    texto = resposta.choices[0].message.content.strip()

    # Remove markdown
    texto = texto.replace("```json", "").replace("```", "").strip()

    # Pega só do [ até o último ]
    inicio = texto.find("[")
    fim = texto.rfind("]")
    if inicio == -1 or fim == -1:
        raise ValueError(f"IA não retornou JSON válido. Resposta recebida:\n{texto}")

    texto = texto[inicio:fim + 1]

    return json.loads(texto)