
---

# Documentação R

## **String | JSON | Protobuf**

Este documento resume a estrutura, objetivo e funcionamento dos três protocolos utilizados na comunicação TCP entre cliente e servidor. O foco é apresentar uma visão clara e direta sobre **como cada protocolo opera** e **por que eles foram estudados comparativamente** por meio de métricas de desempenho.

---

# Objetivo do Estudo

O estudo busca avaliar os protocolos no lado do cliente na arquitetura cliente-servidor:

* **Protocol String**
* **JSON**
* **Protocol Buffers**

para comparar:

* Tempo de **envio**
* Tempo de **resposta**
* Tempo **total**
* Variação (desvio padrão)
* Custo de serialização e parsing
* Eficiência da comunicação TCP

Os testes foram executados usando o mesmo conjunto de operações:
- `auth`, `info`, `logout` e `op`
- `echo`, `soma`, `status`, `historico` e `timestamp`.

---

# Visão Geral de Cada Protocolo

---

## **1. Protocol String**

### Características

* Mensagens puramente textuais.
* Estrutura baseada em delimitadores:

  ```
  TIPO|chave=valor|chave=valor|...|FIM
  ```
* Simples de implementar.
* Parsing baseado em `split("|")`.

---

## **2. JSON**

### Características

* Mensagens estruturadas em formato JSON:

  ```json
  {
      "tipo": "OP",
      "token": "...",
      "operacao": "...",
      "parametros": {...},
      "timestamp": "..."
  }
  ```
* Envio linha a linha (termina com `\n`).
* Facilmente manipulável em qualquer linguagem.

---

## **3. Protocol Buffers (Protobuf)**

### Características

* Formato binário altamente compacto.
* Cada mensagem possui **prefixo de 4 bytes** indicando o tamanho:

  ```
  [tamanho][payload_binario]
  ```
* Estrutura definida em `.proto` usando *oneof*:

  * `auth`
  * `operacao`
  * `info`
  * `logout`

---

# Analytics

A mesma estrutura de script de performance foi usado para os três protocolos.
A única diferença: **o módulo importado** (`string_`, `json_`, `protobuf_`).

Fluxo:

1. Conectar ao servidor TCP
2. Enviar operação **AUTH**
3. Receber **token**
4. Executar repetidamente:

   * `echo`
   * `soma`
   * `status`
   * `historico`
   * `timestamp`
5. Coletar:

   * `tempo_envio`
   * `tempo_resposta`
   * `tempo_total`
6. Gerar DataFrame Pandas para análise

---

## Métricas Coletadas

Para cada operação × protocolo × repetição:

| Métrica            | Significado                    |
| ------------------ | ------------------------------ |
| **tempo_envio**    | Serializar + enviar pacote     |
| **tempo_resposta** | Receber + decodificar resposta |
| **tempo_total**    | Ciclo completo                 |

Essas métricas permitem avaliar:

* tempo médio
* desvio padrão
* estabilidade
* impacto da serialização
* impacto do tamanho das mensagens

---