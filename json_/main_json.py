"""
Cliente TCP em Python para comunicação com servidor conforme especificações do Trabalho 1.
    -> sendall() para enviar mensagens ao servidor
    -> recv() para receber mensagens do servidor
    -> encode("utf-8") para converter string em bytes
    -> decode("utf-8") para converter bytes em string
    -> datetime.now().isoformat() para gerar timestamps no formato ISO 8601
    -> Uso de with para gerenciar o socket e garantir fechamento adequado
    -> with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock para criar o socket TCP
    -> Formato das mensagens:
        AUTH|aluno_id=SEU_ID|=FIM\n
        OP|token=SEU_TOKEN|operacao=OPERACAO|mensagem=MENSAGEM|timestamp=TIMESTAMP|=FIM\n
        LOGOUT|token=SEU_TOKEN|timestamp=TIMESTAMP|=FIM\n
    -> Operações suportadas:
        ECHO: Retorna a mesma mensagem enviada.
        SOMA: Retorna a soma de uma lista de números.
        HISTORICO: Retorna o histórico de operações realizadas.
        TIMESTAMP: Retorna o timestamp atual do servidor.
        STATUS: Retorna o status da conexão.

"""


"""
    -> Exemplo de uso de JSON em Python
    
    import json

    dados = {
        "comando": "AUTH",
        "token": token,
        "parametros": {
            "tipo_de_parametro": "valor_do_parametro"
        },  
        "timestamp": "2025-11-12T15:30:00"
    }

    json_str = json.dumps(dados)  # transforma em string JSON
    print(json_str)
"""

import socket
from datetime import datetime
import json
import time
# Configurações do servidor (substitua pelo IP real fornecido pelo professor)
SERVER_IP = "3.88.99.255"   # exemplo local — altere para o IP público AWS
SERVER_PORT = 8081

def enviar_mensagem(sock, mensagem: str):
    """Envia mensagem JSON codificada em UTF-8."""
    try:
        sock.sendall(mensagem.encode("utf-8"))
    except Exception as e:
        print("Erro ao enviar mensagem:", e)
        raise

def receber_resposta(sock):
    """Recebe JSON do servidor."""
    try:
        data = sock.recv(2048)
        resposta_str = data.decode("utf-8").strip()
        resposta_json = json.loads(resposta_str)
        return resposta_json
    except Exception as e:
        print("Erro ao receber resposta:", e)
        raise


def autenticar(sock, aluno_id, print_resposta=True):
    try:
        timestamp = datetime.now().isoformat()
        msg_json = {
            "tipo": "autenticar",
            "aluno_id": aluno_id,
            "timestamp": timestamp
        }

        msg = json.dumps(msg_json)

        # Tempo de envio
        t0 = time.time()
        enviar_mensagem(sock, msg)
        t1 = time.time()
        tempo_envio = round(t1 - t0, 3)

        # Tempo de resposta
        t0_ = time.time()
        resposta = receber_resposta(sock)
        t1_ = time.time()
        tempo_resposta = round(t1_ - t0_, 3)

        tempo_total = round(t1_ - t0, 3)

        if print_resposta:
            print("\nRESPOSTA AUTH2")
            # print(resposta)
            print(json.dumps(resposta, indent=4, ensure_ascii=False))

            print(f"Tempo total AUTH: {tempo_total}s")

        return resposta, resposta.get("token"), tempo_total, tempo_envio, tempo_resposta

    except Exception as e:
        print("Erro na autenticação:", e)
        return None, None, None, None, None

def enviar_info(sock, tipo="basico", print_resposta=True):

    try:
        timestamp = datetime.now().isoformat()
        msg_json =  {   
                            "tipo": tipo,
                            "operacao": "info",
                            "timestamp": timestamp
                    } 

        msg = json.dumps(msg_json)

        t0 = time.time()
        enviar_mensagem(sock, msg)
        t1 = time.time()
        tempo_envio = round(t1 - t0, 3)

        t0_ = time.time()
        resposta = receber_resposta(sock)
        t1_ = time.time()
        tempo_resposta = round(t1_ - t0_, 3)

        tempo_total = round(t1_ - t0, 3)

        if print_resposta:
            print(f"\nRESPOSTA INFO:")
            print(json.dumps(resposta, indent=4, ensure_ascii=False))

            print(f"Tempo total INFO: {tempo_total}s")

        return resposta, tempo_total, tempo_envio, tempo_resposta
    except Exception as e:
        print("Erro ao enviar INFO:", e)
        return None, None, None, None

def operacoes_disponiveis(sock, token, operacao, parametros=None, print_resposta=True):
    try:
        timestamp = datetime.now().isoformat()

        if parametros != None:
            chave_parametro = next(iter(parametros))
            valor_parametro = parametros[chave_parametro]
        if operacao !='timestamp':
            msg_json =  {   "token": token,
                            "tipo": "operacao",
                            "operacao": operacao,
                            "parametros": {
                                chave_parametro: valor_parametro
                            } ,
                            "timestamp": timestamp
                        } 
        else:
            msg_json =  {   "token": token,
                            "tipo": "operacao",
                            "operacao": operacao,
                            "timestamp": timestamp }

        msg = json.dumps(msg_json)

        print("\nMensagem enviada:", msg)

        # Tempo de envio
        t0 = time.time()
        enviar_mensagem(sock, msg)
        t1 = time.time()
        tempo_envio = round(t1 - t0, 3)

        # Tempo de resposta
        t0_ = time.time()
        resposta = receber_resposta(sock)
        t1_ = time.time()
        tempo_resposta = round(t1_ - t0_, 3)

        tempo_total = round(t1_ - t0, 3)

        if print_resposta:
            print(f"\nRESPOSTA {operacao.upper()}:")
            print(json.dumps(resposta, indent=4, ensure_ascii=False))

            print(f"Tempo total {operacao.upper()}: {tempo_total}s")
        # print("Tempo envio:", tempo_envio)
        # print("Tempo resposta:", tempo_resposta)        
        # print("Tempo total:", tempo_total)
        return resposta, tempo_total, tempo_envio, tempo_resposta

    except Exception as e:
        print(f"Erro na operação {operacao}:", e)
        return None, None, None, None


def logout(sock, token, print_resposta=True):
    try:
        timestamp = datetime.now().isoformat()

        msg_json = {
            "tipo": "logout",
            "token": token,
            "timestamp": timestamp
        }

        msg = json.dumps(msg_json)

        # Tempo envio
        t0 = time.time()
        enviar_mensagem(sock, msg)
        t1 = time.time()
        tempo_envio = round(t1 - t0, 3)

        # Tempo resposta
        t0_ = time.time()
        resposta = receber_resposta(sock)
        t1_ = time.time()
        tempo_resposta = round(t1_ - t0_, 7)

        tempo_total = round(t1_ - t0, 3)

        if print_resposta:
            print("\nRESPOSTA LOGOUT:")
            # print(resposta)
            print(json.dumps(resposta, indent=4, ensure_ascii=False))
            print(f"Tempo total LOGOUT: {tempo_total}s")

        return resposta, tempo_total, tempo_envio, tempo_resposta

    except Exception as e:
        print("Erro no LOGOUT:", e)
        return None, None, None, None

def menu_operacoes(sock, token):

    while True:
        print("\n================ MENU ================")
        print("1 - ECHO")
        print("2 - SOMA")
        print("3 - STATUS")
        print("4 - HISTORICO")
        print("5 - TIMESTAMP")
        print("0 - LOGOUT e sair")
        print("=====================================")

        opc = input("Escolha uma opção: ").strip()

        if opc == "0":
            logout(sock, token)
            print("Saindo...")
            break

        elif opc == "1":
            mensagem = input("Digite a mensagem para ECO: ")
            operacoes_disponiveis(sock, token, "echo", parametros={"mensagem": mensagem})

        elif opc == "2":
            numeros = []
            while True:
                aux = input("Digite número ou 'q' para finalizar: ")
                if aux.lower() == 'q':
                    break
                try:
                    numeros.append(str(float(aux)))

                except:
                    print("Valor inválido.")

            print(f"Número {numeros} adicionado.")

            operacoes_disponiveis(sock, token, "soma", parametros={"numeros": numeros})

        elif opc == "3":
            det_status = ""
            detalhado = False
            while True:
                det_status = input("Deseja detalhar o status? (s/n): ")
                if det_status not in ('s', 'n', 'S', 'N'):
                    print("Opção inválida. Digite 's' para sim ou 'n' para não.")
                else:
                    if det_status in ('s', 'S'):
                        detalhado = True
                        break
                    else:
                        detalhado = False
                        break
            operacoes_disponiveis(sock, token, "status", parametros={"detalhado": detalhado})

        elif opc == "4":
            while True:
                limite = input("Digite o valor do limite: ")
                if limite.isdigit():
                    break
                else:
                    print("Valor inválido. Digite um número inteiro.")
            operacoes_disponiveis(sock, token, "historico", parametros={"limite": limite})

        elif opc == "5":
            operacoes_disponiveis(sock, token, "timestamp")

        else:
            print("Opção inválida!")
    logout(sock, token)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        inicio = time.time()

        while True:
            try:
                print(f"Conectando a {SERVER_IP}:{SERVER_PORT}...")
                sock.connect((SERVER_IP, SERVER_PORT))
                print("Conectado!")
                break  # saiu do loop, conexão OK

            except Exception as e:
                print("Falha na conexão:", e)

                # Verifica se já passou o tempo máximo
                if time.time() - inicio >= 5:
                    print("Não foi possível conectar dentro de 5 segundos. Desistindo...")
                    return

        # Autenticação
        enviar_info(sock, tipo="basico")
        resposta_auth, token, _, _, _ = autenticar(sock, "509022")
        if not token:
            print("Falha na autenticação.")
            return

        # Menu
        menu_operacoes(sock, token)


if __name__ == "__main__":
    main()

