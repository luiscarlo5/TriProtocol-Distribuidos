# Script de Teste de Performance

### **String**, **JSON** e **Protobuf**

Funcionamento completo dos scripts responsáveis por medir o desempenho dos três protocolos de comunicação usados no
sistema: **String**, **JSON** e **Protobuf**.\
O objetivo é padronizar a lógica de medição, possibilitando comparação
entre os protocolos quanto a **tempo de envio**, **tempo de resposta** e
**tempo total** de execução das operações.

------------------------------------------------------------------------

## 1. Visão Geral

O script executa múltiplas operações suportadas pelo servidor ---
*echo*, *soma*, *status*, *historico* e *timestamp* --- e captura tempos
de latência para cada uma delas.

Esses tempos são então consolidados em um **DataFrame Pandas**,
permitindo análise estatística e exportação dos resultados.

------------------------------------------------------------------------

## 2. Importações Principais

``` python
import pandas as pd
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from json_.main_json import operacoes_disponiveis, autenticar, logout
import socket
```

O script funciona da mesma forma para **String**, **JSON** e
**Protobuf**.\
A única diferença ficará na importação:

-   Para **String**:

    ``` python
    from string_.main_string import operacoes_disponiveis, autenticar, logout
    ```

-   Para **JSON**:

    ``` python
    from json_.main_json import operacoes_disponiveis, autenticar, logout
    ```

-   Para **Protobuf**:

    ``` python
    from protobuf_.main_protobuf import operacoes_disponiveis, autenticar, logout
    ```

Todo restante do script funciona de forma idêntica.

------------------------------------------------------------------------

## 3. Função `teste_performance()`

Esta função executa repetidas operações no servidor e mede tempos de
execução:

``` python
def teste_performance(sock, token, repeticoes=10):
```

### Parâmetros:

-   **sock** -- socket TCP conectado ao servidor\
-   **token** -- token retornado pela etapa de autenticação\
-   **repeticoes** -- número de vezes que cada operação será executada

------------------------------------------------------------------------

## 4. Operações medidas

O script executa, para cada repetição, as seguintes operações:

  Operação      Descrição
  ------------- --------------------------------------------
  `echo`        Retorna a mesma mensagem enviada
  `soma`        Soma números enviados
  `status`      Retorna informações sobre a sessão/conexão
  `historico`   Retorna últimos registros armazenados
  `timestamp`   Solicita timestamp atual do servidor

Cada execução retorna 3 tempos:

-   **tempo_envio**: tempo entre criar o pacote e enviá-lo\
-   **tempo_resposta**: tempo entre o servidor responder e processar
    devolução\
-   **tempo_total**: envio + processamento + retorno

------------------------------------------------------------------------

## 5. Armazenamento dos resultados

Cada operação é armazenada como um dicionário:

``` python
resultados.append({
    "operacao": "echo",
    "tempo_envio": tempo_envio,
    "tempo_resposta": tempo_resposta,
    "tempo_total": tempo_total
})
```

Ao final:

``` python
df = pd.DataFrame(resultados)
print(df)
return df
```

O mesmo DataFrame é válido para **todos os protocolos**, facilitando
comparações.

------------------------------------------------------------------------

## 6. Conexão com o servidor

``` python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))
```

Independente do protocolo, a comunicação é sempre **TCP**.

------------------------------------------------------------------------

## 7. Autenticação

``` python
res, token, _,_,_ = autenticar(sock, "509022")
```

Cada protocolo implementa seu formato de mensagem,\
mas todos retornam um **token** utilizado nas chamadas seguintes.

------------------------------------------------------------------------

## 8. Execução dos testes

``` python
df = teste_performance(sock, token, repeticoes=10)
```

O número de repetições pode ser ajustado conforme o experimento.

------------------------------------------------------------------------

## 9. Logout e finalização

``` python
logout(sock, token)
print("Arquivo salvo: resultados_teste.csv")
```

------------------------------------------------------------------------

## 10. Aplicação para os 3 protocolos

O mesmo script é reutilizado para cada protocolo, bastando trocar o
módulo de importação:

### **String**

``` python
from string_.main_string import operacoes_disponiveis, autenticar, logout
```

###  **JSON**

``` python
from json_.main_json import operacoes_disponiveis, autenticar, logout
```

### **Protobuf**

``` python
from protobuf_.main_protobuf import operacoes_disponiveis, autenticar, logout
```

Após gerar três DataFrames (um para cada protocolo),\
é possível compará-los estatisticamente ou graficamente.

------------------------------------------------------------------------
