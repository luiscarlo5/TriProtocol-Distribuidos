# Documentação do Cliente TCP usando Protocol String

Este documento descreve todas as funções presentes no código fornecido e explica como cada parte foi construída e qual é sua função dentro do fluxo geral da aplicação.

---

## **1. Função `enviar_mensagem(sock, mensagem)`**

### **Objetivo:**

Enviar uma mensagem ao servidor usando o socket TCP.

### **Estrutura:**

* Garante que a mensagem termine com `\n`.
* Converte a string para UTF-8.
* Envia pelo socket usando `sendall()`.
* Qualquer erro é capturado e exibido.

### **Fluxo interno:**

1. Verifica se existe quebra de linha.
2. Codifica como UTF-8.
3. Envia pela rede.
4. Retorna exceção caso falhe.

---

## **2. Função `receber_resposta(sock)`**

### **Objetivo:**

Ler e decodificar respostas vindas do servidor.

### **Estrutura:**

* Recebe até 4096 bytes.
* Decodifica UTF-8.
* Remove quebras de linha e espaços extras.

### **Fluxo interno:**

1. `sock.recv(4096)` → lê os dados.
2. Decodifica e faz `.strip()`.
3. Retorna a resposta limpa.

---

## **3. Função `autenticar(sock, aluno_id, print_resposta=True)`**

### **Objetivo:**

Enviar uma mensagem de autenticação e extrair o token retornado.

### **Estrutura:**

* Monta mensagem no formato:
  `AUTH|aluno_id=...|timestamp=...|FIM`
* Mede tempo de envio e tempo de resposta.
* Faz parsing da resposta para extrair `token=`.

### **Fluxo interno:**

1. Cria timestamp.
2. Monta a mensagem AUTH.
3. Envia e mede tempo.
4. Recebe resposta e mede tempo.
5. Procura pelo token na resposta.
6. Retorna resposta, token e métricas.

---

## **4. Função `operacoes_disponiveis(sock, token, operacao, parametros=None, print_resposta=True)`**

### **Objetivo:**

Enviar solicitações gerais ao servidor após autenticação.

### **Estrutura:**

* Identifica o nome da chave do parâmetro enviado.
* Monta a mensagem no formato:
  `OP|token=...|operacao=...|param=valor|timestamp=...|FIM`
* Caso operação seja `timestamp`, não envia parâmetros adicionais.
* Mede tempo de envio e resposta.
* Imprime cada linha da resposta separada por `|`.

### **Fluxo interno:**

1. Obtém timestamp.
2. Identifica chave e valor dos parâmetros.
3. Monta a mensagem conforme a operação.
4. Envia e mede tempo.
5. Recebe e mede tempo.
6. Formata/imprime resposta.

---

## **5. Função `logout(sock, token, print_resposta=True)`**

### **Objetivo:**

Encerrar sessão no servidor.

### **Estrutura:**

* Envia comando:
  `LOGOUT|token=...|timestamp=...|FIM`
* Mede tempo.
* Recebe resposta e a exibe.

### **Fluxo interno:**

1. Cria timestamp.
2. Monta mensagem LOGOUT.
3. Envia.
4. Recebe resposta.
5. Retorna métricas.

---

## **6. Função `menu_operacoes(sock, token)`**

### **Objetivo:**

Interface interativa no terminal para seleção de operações.

### **Estrutura:**

* Exibe menu com 5 operações + logout.
* Coleta entradas do usuário.
* Chama `operacoes_disponiveis()` conforme operação escolhida.
* Para cada operação: coleta parâmetros necessários.

### **Operações disponíveis:**

* **ECHO** → envia texto.
* **SOMA** → múltiplos números.
* **STATUS** → detalhado ou simples.
* **HISTORICO** → requer valor limite.
* **TIMESTAMP** → sem parâmetros.

---

## **7. Função `main()`**

### **Objetivo:**

Controlar o fluxo principal da aplicação.

### **Estrutura:**

* Cria socket com contexto `with`.
* Tenta conectar ao servidor por 5 segundos.
* Se conectar, executa autenticação.
* Se autenticar, inicia o menu.
* Caso algo falhe, encerra.

### **Fluxo interno:**

1. Cria socket TCP.
2. Loop tentando conectar:

   * Se falhar, tenta até 5 segundos.
3. Chama autenticação.
4. Se token for válido → abre menu.
5. Usuário escolhe operações.
6. Ao sair → encerra socket.

---

## **8. Estrutura geral da comunicação**

### **Formato das mensagens enviadas:**

```
TIPO|param1=valor1|param2=valor2|timestamp=...|FIM
```

### **Tipos possíveis:**

* AUTH
* OP
* LOGOUT
* INFO

### **Parsing básico:**

O código utiliza `split("|")` para quebrar a resposta em partes.

---

## **9. Fluxo completo resumido**

1. Criar socket.
2. Tentar conectar (máx 5 segundos).
3. Enviar AUTH.
4. Receber TOKEN.
5. Exibir menu.
6. Enviar operações.
7. Receber e exibir respostas.
8. Enviar LOGOUT.
9. Fechar conexão.

---

Se desejar, posso gerar uma versão mais formal, mais detalhada ou com tabelas.
