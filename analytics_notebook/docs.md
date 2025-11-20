# Análise de Protocolos -- Notebook em Markdown

Este Notebook é utilizado para analisar tempos de resposta dos protocolos **String**, **JSON** e **Protobuf**,
calculando **médias**, **desvios padrão** e gerando visualizações.

------------------------------------------------------------------------

## \## 1. Leitura de Bibliotecas

``` python
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
```

------------------------------------------------------------------------

## \## 2. Visualização de exemplo (Protobuf -- operação soma)

``` python
df_protobuf[df_protobuf['operacao'] == 'soma']
df_protobuf.shape
```

------------------------------------------------------------------------

## \## 3. Impressão das médias por operação

O código itera por cada tipo de operação e cada protocolo, calculando a
média:

``` python
nomes = ["String", "JSON", "Protobuf"]

for tipo in ['echo', 'soma', 'status', 'historico', 'timestamp']:
    print(f"\nOperação {tipo.upper()}")
    for nome, df_main in zip(nomes, df_todos):
        df_aux = df_main[df_todos[0]['operacao'] == tipo ]
        print(f"Protocolo {nome}: Média {round(df_aux['tempo_resposta'].mean(), 3)}")
```

------------------------------------------------------------------------

## \## 4. Construção do DataFrame consolidado

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

## \## 5. Gráficos de média por operação

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

## \## 6. Gráficos de desvio padrão por operação

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

## \## 7. Comparação por protocolo (FacetGrid)

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

## \## 8. Conclusão

O notebook fornece:

-   Comparação clara entre protocolos\
-   Média e variação do tempo de resposta\
-   Visualizações individuais e agrupadas por protocolo

------------------------------------------------------------------------