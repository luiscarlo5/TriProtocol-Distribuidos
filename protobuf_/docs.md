# Documentação — Cliente TCP usando Protocol Buffers

Este documento descreve todo o funcionamento do cliente TCP que utiliza **Protocol Buffers** para comunicação com o servidor. Inclui explicações detalhadas das funções, formato das mensagens, prefixo de tamanho e lógica de construção das requisições.

---

# Visão Geral

O cliente TCP implementa um protocolo binário usando mensagens **Protocol Buffers**. A comunicação segue este padrão:

### - Envia e recebe mensagens com **prefixo de 4 bytes** indicando o tamanho (big endian)

### - Usa a mensagem `Requisicao` (oneof):

* `auth`
* `operacao`
* `info`
* `logout`

### - Usa a mensagem `Resposta` contendo:

* `ok` (dados de retorno)
* `erro` (mensagem e código)

O servidor recebe a requisição, interpreta o campo ativo do `oneof` e responde com um `Resposta` preenchido.

---

# Estrutura das Funções

---

## **1. Função `enviar_protobuf(sock, mensagem)`**

### **Objetivo**

Serializar a mensagem protobuf e enviar pelo socket com prefixo de tamanho.

### **estrutura**

* A mensagem é convertida para bytes com `SerializeToString()`.
* Cria um header de 4 bytes contendo o tamanho (big endian).
* Envia header + payload usando `sock.sendall()`.

### **Fluxo interno**

1. Serializa protobuf → `payload`
2. Cria header → `struct.pack(" >I ")`
3. Envia header + mensagem

---

## **2. Função `receber_protobuf(sock, classe_resposta)`**

### **Objetivo**

Ler uma mensagem protobuf enviada com tamanho prefixado e retornar o objeto `Resposta`.

### **Construção**

* Lê 4 bytes do início para obter o tamanho.
* Lê exatamente esse número de bytes.
* Constrói um objeto protobuf da classe recebida.

### **Fluxo interno**

1. `sock.recv(4)` lê tamanho
2. `struct.unpack` converte para inteiro
3. `sock.recv(tamanho)` lê payload
4. Instancia classe `Resposta`
5. Preenche com `ParseFromString`

---

## **3. Função `autenticar(sock, aluno_id, print_resposta=True)`**

### **Objetivo**

Realizar autenticação enviando um `Requisicao.auth` e extrair o token retornado.

### **Estrutura**

* Preenche o campo `auth` dentro de `Requisicao` (oneof).
* Mede tempo de envio e resposta (benchmark).
* Imprime resposta formatada em JSON.
* Se resposta contiver campo `ok`, extrai token.

### **Fluxo interno**

1. Cria `Requisicao`
2. Preenche `auth.aluno_id` e timestamp
3. Envia usando `enviar_protobuf`
4. Recebe resposta
5. Converte para JSON para depuração
6. Extrai token de `ok.dados`

---

## **4. Função `operacoes_disponiveis(sock, token, operacao, parametros=None, print_resposta=True)`**

### **Objetivo**

Enviar qualquer operação geral do sistema (`echo`, `soma`, `status`, `historico`, etc.).

### **Estrutura**

* Preenche `Requisicao.operacao` (oneof).
* Insere token, nome da operação e parâmetros.
* Mede tempos.
* Exibe resposta em JSON.

### **Fluxo interno**

1. Cria `Requisicao`
2. Preenche `operacao.token` e `operacao.operacao`
3. Adiciona parâmetros se existirem
4. Envia e recebe protobuf
5. Retorna objeto `Resposta`

---

## **5. Função `enviar_info(sock, tipo, print_resposta=True)`**

### **Objetivo**

Solicitar informações iniciais ao servidor antes da autenticação.

### **Estrutura**

* Preenche `Requisicao.info.tipo`.
* Envia e recebe protobuf.
* Exibe JSON da resposta.

### **Fluxo**

1. Preenche campo `info`
2. Envia para o servidor
3. Recebe `Resposta`
4. Imprime JSON

---

## **6. Função `logout(sock, token, print_resposta=True)`**

### **Objetivo**

Finalizar sessão com o servidor.

### **Estrutura**

* Preenche `Requisicao.logout.token`.
* Envia/recebe protobuf.
* Imprime tempo total.

### **Fluxo**

1. Cria `Requisicao` com campo `logout`
2. Envia
3. Recebe resposta
4. Exibe JSON

---

## **7. Função `menu_operacoes(sock, token)`**

### **Objetivo**

Interface de menu interativo para testar operações do servidor.

### **Operações Disponíveis**

1. **ECHO** → ecoa texto enviado
2. **SOMA** → soma vários números
3. **STATUS** → com opção detalhado/simples
4. **HISTORICO** → com limite
5. **TIMESTAMP** → sem parâmetros
6. **LOGOUT** → encerra sessão

### **Fluxo**

* Exibe menu e coleta escolha.
* Monta parâmetros corretos.
* Chama `operacoes_disponiveis()`.
* Imprime resposta protobuf.

---

## **8. Função `main()`**

### **Objetivo**

Fluxo principal do programa.

### **estrutura**

* Estabelece conexão TCP.
* Envia `INFO` inicial.
* Faz autenticação e obtém token.
* Abre menu.

### **Fluxo**

1. Conecta ao servidor usando TCP
2. Envia `INFO`
3. Autentica → obtém token
4. Entra no menu de operações
5. Usuário escolhe até fazer logout

---

# Formato das Mensagens Protocol Buffers

As mensagens seguem este esquema:

```
[4 bytes: tamanho em big endian][payload protobuf]
```

### Exemplo de envio:

```
00 00 01 2A | <bytes protobuf>
```

### Estrutura da mensagem `Requisicao` (oneof):

* `auth`
* `operacao`
* `info`
* `logout`

### Estrutura da mensagem `Resposta`:

* `ok.dados` (map<string,string>)
* `erro.codigo`
* `erro.mensagem`

---

# Fluxo Geral da Comunicação

1. Conectar via TCP
2. Enviar `INFO`
3. Enviar `AUTH`
4. Receber `token`
5. Interagir usando operações
6. Encerrar com `LOGOUT`

---
