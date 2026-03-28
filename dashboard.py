import matplotlib.pyplot as plt
from matplotlib.figure import Figure

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

    for i, grafico in enumerate(sugestoes):
        ax = axes[i]
        ax.set_facecolor('#16213e')
        ax.tick_params(colors='white')
        ax.title.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        for spine in ax.spines.values():
            spine.set_edgecolor('#4361ee')

        tipo = grafico['tipo']
        col_x = grafico['coluna_x']
        col_y = grafico.get('coluna_y')
        titulo = grafico['titulo']
        cor = cores[i % len(cores)]

        try:
            if tipo == 'barra' and col_y:
                dados = df.groupby(col_x)[col_y].sum().sort_values(ascending=False).head(10)
                ax.bar(dados.index, dados.values, color=cor)
                ax.set_xlabel(col_x)
                ax.set_ylabel(col_y)
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')

            elif tipo == 'linha' and col_y:
                dados = df.groupby(col_x)[col_y].sum()
                ax.plot(dados.index, dados.values, color=cor, linewidth=2, marker='o')
                ax.set_xlabel(col_x)
                ax.set_ylabel(col_y)
                # Mostra no máximo 10 labels no eixo X
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

            elif tipo == 'histograma' and col_x in df.select_dtypes('number').columns:
                ax.hist(df[col_x].dropna(), bins=15, color=cor, edgecolor='white')
                ax.set_xlabel(col_x)
                # Limita labels do eixo X
                ticks = ax.get_xticks()
                passo = max(1, len(ticks) // 10)
                ax.set_xticks(ticks[::passo])
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')

            elif tipo == 'dispersao' and col_y:
                ax.scatter(df[col_x].dropna(), df[col_y], color=cor, alpha=0.6)
                ax.set_xlabel(col_x)
                ax.set_ylabel(col_y)
                ticks = ax.get_xticks()
                passo = max(1, len(ticks) // 10)
                ax.set_xticks(ticks[::passo])
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')

        except Exception as e:
            ax.text(0.5, 0.5, f'Erro: {str(e)}', transform=ax.transAxes,
                    ha='center', color='red')

        ax.set_title(titulo, fontsize=11, pad=10)

    for j in range(qtd, len(axes)):
        axes[j].set_visible(False)

    fig.tight_layout(pad=3.0)
    return fig