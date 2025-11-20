# Documentação do Cliente TCP usando JSON

Este documento descreve todas as funções presentes no cliente TCP baseado em JSON, explicando como cada parte foi construída e para que ela é útil

---

## **1. Função `enviar_json(sock, dados)`**

### **Objetivo**
Enviar ao servidor um objeto JSON já convertido em string.

### **Estrutura**
- Converte o `dict` Python em JSON com `json.dumps()`.
- Garante que cada mensagem termine com `\n`.
- Envia usando `sock.sendall()` codificado em UTF-8.
- Captura e exibe erros de envio.

### **Fluxo interno**
1. Converte o dicionário em string JSON.
2. Adiciona `\n` ao final.
3. Codifica como UTF-8.
4. Envia com `sendall()`.
5. Retorna exceção caso falhe.

---

## **2. Função `receber_json(sock)`**

### **Objetivo**
Receber uma linha JSON do servidor, decodificar e converter para `dict`.

### **Estrutura**
- Lê até encontrar `\n`.
- Decodifica UTF-8.
- Usa `json.loads()` para converter a string em dicionário.
- Trata erros caso a resposta não seja JSON válido.

### **Fluxo interno**
1. Chama `recv(4096)` para receber bytes.
2. Decodifica como UTF-8.
3. Remove quebras de linha com `.strip()`.
4. Converte usando `json.loads()`.
5. Retorna um `dict`.

---

## **3. Função `autenticar(sock, aluno_id, print_resposta=True)`**

### **Objetivo**
Enviar uma requisição JSON do tipo AUTH, medir tempos e extrair o token retornado.

### **Estrutura**
Envia um JSON como:
```json
{
    "tipo": "AUTH",
    "aluno_id": "Matricula",
    "timestamp": "..."
}
```

### **Fluxo interno**
1. Gera timestamp.
2. Monta dicionário AUTH.
3. Envia e mede tempo.
4. Recebe resposta e mede tempo.
5. Extrai "token" da resposta.
6. Retorna resposta, token e métricas.

## **4. Função Função operacoes_disponiveis(sock, token, operacao, parametros=None, print_resposta=True)
### **Objetivo**
Enviar operações genéricas ao servidor após autenticação.

### **Estrutura**
Exemplo de mensagem enviada:
```json
{
    "tipo": "OP",
    "token": "...",
    "operacao": "...",
    "parametros": {...},
    "timestamp": "..."
}
```
### **Fluxo interno**
1. Gera timestamp.
2. Identifica e usa os parâmetros.
3. Monta dicionário JSON.
4. Envia e mede tempo.
5. Recebe resposta JSON.
6. Formata a saída de forma legível.

## **5. Função logout(sock, token, print_resposta=True)**
### **Objetivo**
Finalizar a sessão ativa no servidor.

### **Estrutura**
Mensagem enviada:
```json
{
    "tipo": "LOGOUT",
    "token": "...",
    "timestamp": "..."
}
```
### **Fluxo interno**
1. Gera timestamp.
2. Monta dicionário LOGOUT.
3. Envia.
4. Recebe JSON.
5. Exibe/retorna métricas.

## **6. Função menu_operacoes(sock, token)**

### **Objetivo**
Interface interativa terminal para escolha de operações.

### **Estrutura**

#### **Lista operações disponíveis e solicita entrada do usuário.**
#### **Operações comuns**

1. echo → envia texto.
2. soma → lista de números.
3. status → estado atual.
4. historico → limite do histórico.
5. timestamp → sem parâmetros.

### **Fluxo interno**
- Exibe menu.
- Usuário escolhe opção.
- Coleta parâmetros se necessário.
- Chama operacoes_disponiveis().
- Repete até o usuário escolher sair.

## **7. Função main()**
### **Objetivo**
Gerenciar todo o ciclo de vida do cliente JSON.

### **Estrutura**
1. Cria socket TCP.
2. Tenta conectar ao servidor por até 5 segundos.
3. Autentica.
4. Abre menu.
5. Finaliza com logout e fechamento do socket.
6. Fluxo interno
7. Criar socket.
8. Loop de conexão com timeout de 5s.
9. Se conectar: enviar AUTH.
10. Receber token.
11. Abrir menu interativo.
12. Usuário escolhe logout.
13. Fechar conexão.

## **8. Estrutura geral da comunicação**
Formato das mensagens
```json
{
    "tipo": "OP" | "AUTH" | "LOGOUT",
    "token": "...",
    "operacao": "...",
    "parametros": {...},
    "timestamp": "..."
}
```
### **Campos principais**
|    Campo    |    Descrição    |
|-------------|-----------------|
|    tipo    |    Tipo da operação (AUTH/OP/LOGOUT)    |
|    token    |    Token da sessão autenticada    |
|    operacao    |	Nome da operação    |
|    parametros    |    Dados enviados    |
|    timestamp    |    Momento do envio    |


## **9. Fluxo completo resumido**

⇒ Criar socket TCP.

⇒ Tentar conectar (timeout 5s).

⇒ Enviar JSON AUTH.

⇒ Receber token.

⇒ Abrir menu de operações.

⇒ Enviar operações via JSON.

⇒ Receber respostas estruturadas.

⇒ Enviar LOGOUT.

⇒ Encerrar conexão.
