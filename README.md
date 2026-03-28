# 📊 Dashboard Inteligente com IA

Aplicação desktop desenvolvida em Python que lê planilhas Excel ou CSV, analisa os dados automaticamente com Inteligência Artificial e gera um dashboard interativo com gráficos — tudo com poucos cliques.

Projeto complementar ao [GeradorRelatorioIA](https://github.com/RVitaliano/GeradorRelatorioIA).

---

## 🖥️ Interface

> Selecione sua planilha, adicione observações opcionais e clique em Gerar Dashboard.

---

## ⚙️ Tecnologias utilizadas

| Tecnologia | Função |
|---|---|
| Python 3.x | Linguagem principal |
| CustomTkinter | Interface gráfica desktop |
| Pandas + OpenPyXL | Leitura e processamento de planilhas |
| Groq API (LLaMA 3.3 70B) | Análise dos dados e sugestão de gráficos com IA |
| Matplotlib | Geração e renderização dos gráficos |
| Threading | Processamento assíncrono |

---

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/RVitaliano/GeradorDashboardIA
cd GeradorDashboardIA
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install customtkinter pandas openpyxl groq matplotlib
```

### 4. Configure sua chave da API

Acesse [console.groq.com](https://console.groq.com), crie uma conta gratuita e gere uma chave de API.

No arquivo `analisador.py`, substitua:

```python
cliente = Groq(api_key="SUA_CHAVE_GROQ_AQUI")
```

pela sua chave real.

### 5. Execute o projeto

```bash
python app.py
```

---

## 📁 Estrutura do projeto

```
DashboardIA/
│
├── app.py          # Interface gráfica principal
├── leitor.py       # Leitura e processamento da planilha
├── analisador.py   # Integração com a IA (Groq API)
├── dashboard.py    # Geração dos gráficos com Matplotlib
└── README.md
```

---

## 📋 Como usar

1. Abra o programa com `python app.py`
2. Clique em **Selecionar CSV/Excel** e escolha sua planilha
3. Adicione **observações** opcionais para guiar a análise da IA
4. Clique em **Gerar Dashboard**
5. Aguarde — os gráficos serão gerados automaticamente!

---

## 🤖 O que a IA faz

- **Escolhe automaticamente** os melhores tipos de gráfico para os dados
- **Gera insights** sobre cada gráfico gerado
- **Sugere filtros** relevantes com base nas colunas da planilha

---

## ⚠️ Observações

- A chave da API Groq é **gratuita** — crie a sua em [console.groq.com](https://console.groq.com)
- Compatível com arquivos `.xlsx`, `.xls` e `.csv`
- O tempo de geração depende do tamanho da planilha e da velocidade da API

---