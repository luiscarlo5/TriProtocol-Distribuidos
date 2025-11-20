# Análise de Protocolos -- Notebook em Markdown

Este Notebook é utilizado para analisar tempos de resposta dos protocolos **String**, **JSON** e **Protobuf**,
calculando **médias**, **desvios padrão** e gerando visualizações.

------------------------------------------------------------------------

## **Leitura de Bibliotecas**

``` python
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
```
------------------------------------------------------------------------

## **Construção do DataFrame consolidado**

O código calcula **média** e **desvio padrão** de `tempo_resposta`:

``` python
nomes = ["String", "JSON", "Protobuf"]
operacoes = ['echo', 'soma', 'status', 'historico', 'timestamp']

resultados = []

for tipo in operacoes:
    for nome, df_main in zip(nomes, df_todos):
        df_aux = df_main[df_main['operacao'] == tipo]
        resultados.append({
            "operacao": tipo,
            "protocolo": nome,
            "media": df_aux["tempo_resposta"].mean(),
            "desvio": df_aux["tempo_resposta"].std()
        })

df_resultado = pd.DataFrame(resultados)
print(df_resultado)
```

------------------------------------------------------------------------

## **Gráficos de média por operação**

``` python
sns.barplot(
    data=df_resultado,
    x="operacao",
    y="media",
    hue="protocolo",
    palette=paleta_azul,
    edgecolor="black"
)
```

------------------------------------------------------------------------

## **Gráficos de desvio padrão por operação**

``` python
sns.barplot(
    data=df_resultado,
    x="operacao",
    y="desvio",
    hue="protocolo",
    palette=paleta_azul,
    edgecolor="black"
)
```

------------------------------------------------------------------------

## **Comparação por protocolo**

O notebook cria grids separados para cada protocolo:

``` python
g = sns.FacetGrid(df_resultado, col="protocolo", height=4, aspect=1.2)
g.map_dataframe(
    sns.barplot,
    x="operacao",
    y="media",
    hue="operacao",
    palette=paleta_azul,
    edgecolor="black",
    width=0.75,
    legend=False
)
```

O mesmo é repetido para o **desvio padrão**.

------------------------------------------------------------------------

## **Conclusão**

O notebook fornece: \##

-   Comparação clara entre protocolos\
-   Média e variação do tempo de resposta\
-   Visualizações individuais e agrupadas por protocolo

------------------------------------------------------------------------
