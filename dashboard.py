import matplotlib.pyplot as plt

def gerar_figura(df, sugestoes):
    qtd = len(sugestoes)

    cols = 2 if qtd > 1 else 1
    rows = (qtd + 1) // 2

    fig, axes = plt.subplots(rows, cols, figsize=(12, 5 * rows))
    fig.patch.set_facecolor('#1a1a2e')

    if qtd == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    cores = ['#4361ee', '#f72585', '#4cc9f0', '#7209b7']
    colunas_numericas = df.select_dtypes(include='number').columns.tolist()

    for i, grafico in enumerate(sugestoes):
        ax = axes[i]
        ax.set_facecolor('#16213e')
        ax.tick_params(colors='white')
        ax.title.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        for spine in ax.spines.values():
            spine.set_edgecolor('#4361ee')

        tipo  = grafico['tipo']
        col_x = grafico['coluna_x']
        col_y = grafico.get('coluna_y')
        titulo = grafico['titulo']
        cor   = cores[i % len(cores)]

        if col_x not in df.columns:
            ax.text(0.5, 0.5, f'Coluna "{col_x}" não encontrada',
                    transform=ax.transAxes, ha='center', color='red')
            ax.set_title(titulo, fontsize=11, pad=10)
            continue
        if col_y and col_y not in df.columns:
            col_y = None

        if col_y and col_y not in colunas_numericas:
            col_y = None

        try:
            if tipo == 'barra':
                if col_y:
                    dados = df.groupby(col_x)[col_y].sum().sort_values(ascending=False).head(10)
                    ax.bar(dados.index.astype(str), dados.values, color=cor)
                    ax.set_ylabel(col_y)
                else:
                    dados = df[col_x].value_counts().head(10)
                    ax.bar(dados.index.astype(str), dados.values, color=cor)
                    ax.set_ylabel('Contagem')
                ax.set_xlabel(col_x)
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')

            elif tipo == 'linha':
                df_temp = df.copy()
                if df_temp[col_x].dtype in ['int64', 'float64']:
                    q_low  = df_temp[col_x].quantile(0.05)
                    q_high = df_temp[col_x].quantile(0.95)
                    df_temp = df_temp[(df_temp[col_x] >= q_low) & (df_temp[col_x] <= q_high)]
                if col_y:
                    dados = df_temp.groupby(col_x)[col_y].sum()
                    ax.set_ylabel(col_y)
                else:
                    dados = df_temp[col_x].value_counts().sort_index()
                    ax.set_ylabel('Contagem')
                ax.plot(range(len(dados)), dados.values, color=cor, linewidth=2, marker='o')
                ax.set_xlabel(col_x)
                ticks = list(range(len(dados)))
                passo = max(1, len(ticks) // 10)
                ax.set_xticks(ticks[::passo])
                ax.set_xticklabels(
                    [str(dados.index[t])[:10] for t in ticks[::passo]],
                    rotation=30, ha='right'
                )

            elif tipo == 'pizza':
                coluna = col_y if col_y else col_x
                dados = df[coluna].value_counts().head(6)
                wedges, texts, autotexts = ax.pie(
                    dados.values,
                    labels=dados.index,
                    autopct='%1.1f%%',
                    colors=cores
                )
                for text in texts:
                    text.set_color('white')
                for autotext in autotexts:
                    autotext.set_color('white')

            elif tipo == 'histograma':
                coluna_num = col_x if col_x in colunas_numericas else col_y
                if coluna_num:
                    ax.hist(df[coluna_num].dropna(), bins=15, color=cor, edgecolor='white')
                    ax.set_xlabel(coluna_num)
                    ax.set_ylabel('Frequência')
                    ticks = ax.get_xticks()
                    passo = max(1, len(ticks) // 10)
                    ax.set_xticks(ticks[::passo])
                    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')
                else:
                    raise ValueError("Nenhuma coluna numérica para histograma")

            elif tipo == 'dispersao' and col_y:
                df_temp = df.copy()
                for col in [col_x, col_y]:
                    if df_temp[col].dtype in ['int64', 'float64']:
                        q_low  = df_temp[col].quantile(0.05)
                        q_high = df_temp[col].quantile(0.95)
                        df_temp = df_temp[(df_temp[col] >= q_low) & (df_temp[col] <= q_high)]
                ax.scatter(df_temp[col_x], df_temp[col_y], color=cor, alpha=0.6)
                ax.set_xlabel(col_x)
                ax.set_ylabel(col_y)
                ticks = ax.get_xticks()
                passo = max(1, len(ticks) // 10)
                ax.set_xticks(ticks[::passo])
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')

            else:
                dados = df[col_x].value_counts().head(10)
                ax.bar(dados.index.astype(str), dados.values, color=cor)
                ax.set_xlabel(col_x)
                ax.set_ylabel('Contagem')
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')

        except Exception as e:
            ax.text(0.5, 0.5, f'Erro: {str(e)}', transform=ax.transAxes,
                    ha='center', color='red')

        ax.set_title(titulo, fontsize=11, pad=10)

    for j in range(qtd, len(axes)):
        axes[j].set_visible(False)

    fig.tight_layout(pad=3.0)
    return fig