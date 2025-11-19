"""
Cliente TCP para servidor que usa Protocol Buffers.

- Envia e recebe mensagens com prefixo de 4 bytes (big endian)
- Usa mensagem Requisicao (oneof) para AUTH, OPERACAO, INFO e LOGOUT
- Usa mensagem Resposta para OK ou ERRO
"""

import socket
import struct
from datetime import datetime
from google.protobuf import json_format
import Trabalho_1.protobuf_.sd_protocol_pb2 as sd_protocol_pb2
import time

SERVER_IP = "3.88.99.255"
SERVER_PORT = 8082


def enviar_protobuf(sock, mensagem):
    """Serializa a mensagem protobuf e envia com prefixo de tamanho."""
    try:
        payload = mensagem.SerializeToString()
        header = struct.pack(">I", len(payload))
        sock.sendall(header + payload)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)
        raise

def receber_protobuf(sock, classe_resposta):
    """Recebe resposta prefixada e converte para objeto protobuf."""
    try:
        header = sock.recv(4)
        if not header:
            return None

        tamanho = struct.unpack(">I", header)[0]
        dados = sock.recv(tamanho)

        resposta = classe_resposta()
        resposta.ParseFromString(dados)
        return resposta

    except Exception as e:
        print("Erro ao receber resposta:", e)
        raise

def autenticar(sock, aluno_id):

    try:
        req = sd_protocol_pb2.Requisicao()
        req.auth.aluno_id = aluno_id
        req.auth.timestamp_cliente = datetime.now().isoformat()

        t0 = time.time()
        enviar_protobuf(sock, req)
        t1 = time.time()
        tempo_envio = round(t1 - t0, 3)

        t0_ = time.time()
        resp = receber_protobuf(sock, sd_protocol_pb2.Resposta)
        t1_ = time.time()
        tempo_resposta = round(t1_ - t0_, 3)

        tempo_total = round(t1_ - t0, 3)

        print("\n=== RESPOSTA AUTH ===")
        print(json_format.MessageToJson(resp, indent=2))
        print(f"Tempo total AUTH: {tempo_total}s")

        if resp.HasField("ok"):
            token = resp.ok.dados.get("token", "")
            return resp, token, tempo_total, tempo_envio, tempo_resposta
        else:
            return resp, None, tempo_total, tempo_envio, tempo_resposta

    except Exception as e:
        print("Erro na autenticação:", e)
        return None, None, None, None, None

def operacos_disponiveis(sock, token, operacao, parametros_mensagem="", parametros_numeros=[]):

    try:
        req = sd_protocol_pb2.Requisicao()
        req.operacao.token = token
        req.operacao.operacao = operacao

        if parametros_mensagem != "":
            req.operacao.parametros["mensagem"] = parametros_mensagem
        elif len(parametros_numeros) > 1:
            print("Números para soma:", parametros_numeros)
            req.operacao.parametros["numeros"] = ",".join(parametros_numeros)

        t0 = time.time()
        enviar_protobuf(sock, req)
        t1 = time.time()
        tempo_envio = round(t1 - t0, 3)

        t0_ = time.time()
        resp = receber_protobuf(sock, sd_protocol_pb2.Resposta)
        t1_ = time.time()
        tempo_resposta = round(t1_ - t0_, 3)

        tempo_total = round(t1_ - t0, 3)

        print(f"\nRESPOSTA {operacao.upper()} ===")
        print(json_format.MessageToJson(resp, indent=2))
        print(f"Tempo total {operacao.upper()}: {tempo_total}s")

        return resp, tempo_total, tempo_envio, tempo_resposta
    except Exception as e:
        print(f"Erro na operação {operacao}:", e)
        return None, None, None, None

def enviar_info(sock, tipo):

    try:
        req = sd_protocol_pb2.Requisicao()
        req.info.tipo = tipo

        t0 = time.time()
        enviar_protobuf(sock, req)
        t1 = time.time()
        tempo_envio = round(t1 - t0, 3)

        t0_ = time.time()
        resp = receber_protobuf(sock, sd_protocol_pb2.Resposta)
        t1_ = time.time()
        tempo_resposta = round(t1_ - t0_, 3)

        tempo_total = round(t1_ - t0, 3)

        print(f"\nRESPOSTA INFO: {json_format.MessageToJson(resp, indent=2)}")
        print(f"Tempo total INFO: {tempo_total}s")

        return resp, tempo_total, tempo_envio, tempo_resposta

    except Exception as e:
        print("Erro ao enviar INFO:", e)
        return None, None

def logout(sock, token):

    try:
        req = sd_protocol_pb2.Requisicao()
        req.logout.token = token

        t0 = time.time()
        enviar_protobuf(sock, req)
        t1 = time.time()
        tempo_envio = round(t1 - t0, 3)

        t0_ = time.time()
        resp = receber_protobuf(sock, sd_protocol_pb2.Resposta)
        t1_ = time.time()
        tempo_resposta = round(t1_ - t0_, 3)

        tempo_total = round(t1_ - t0, 3)

        tempo_total = round(t1 - t0, 3)

        print(f"\nRESPOSTA LOGOUT: {json_format.MessageToJson(resp, indent=2)}")
        print(f"Tempo total LOGOUT: {tempo_total}s")

        return resp, tempo_total, tempo_envio, tempo_resposta

    except Exception as e:
        print("Erro no LOGOUT:", e)
        return None, None, None, None


def menu_operacoes(sock, token):
    tempo_resposta_geral = []
    tempo_envio_geral = []
    tempo_total_geral = []


    while True:
        print("\nDigite o número da operação desejada:")
        print("1 - ECHO")
        print("2 - SOMA")
        print("3 - STATUS")
        print("4 - HISTORICO")
        print("5 - TIMESTAMP")
        print("0 - LOGOUT e sair")
        print("-------------------------")

        # opc = input("Escolha: ").strip()
        opc = "1"

        if opc == "0":
            logout(sock, token)
            print("Saindo...")
            break
        elif opc == "1":
            mensagem = str(input("Digite a mensagem para eco: "))

            resp, tempo_total, tempo_envio, tempo_resposta = operacos_disponiveis(sock, token, "echo", parametros_mensagem=mensagem)
            print("Resposta ECHO:", resp)
            break

        elif opc == "2":
           
            # resp = operacos_disponiveis(sock, token, "SOMA", parametros=vet)
            aux = None
            numeros = []
            while aux != 'q' or aux != 'Q':
                aux = str(input("Adicione um número na lista \n ou 'q' para continuar: "))
                if aux != 'q' and aux != 'Q':
                    try:
                        num = float(aux)
                        numeros.append(str(num))
                        
                    except ValueError:
                        print("Entrada inválida. Digite um número ou 'q' para sair.")
                else:
                    break

            resp, tempo_total, tempo_envio, tempo_resposta = operacos_disponiveis(sock, token, "soma", parametros_numeros=numeros)


            print("Resposta SOMA:", resp)
            break

        elif opc == "3":
            resp, tempo_total, tempo_envio, tempo_resposta = operacos_disponiveis(sock, token, "status")
            print("STATUS:", resp)

        elif opc == "4":
            resp, tempo_total, tempo_envio, tempo_resposta = operacos_disponiveis(sock, token, "historico")
            print("HISTORICO:", resp)

        elif opc == "5":
            resp, tempo_total, tempo_envio, tempo_resposta = operacos_disponiveis(sock, token, "timestamp")
            print("TIMESTAMP:", resp)
        else:
            print("Opção inválida!")
            continue

        tempo_resposta_geral.append(tempo_resposta)
        tempo_envio_geral.append(tempo_envio)
        tempo_total_geral.append(tempo_total)
        


def main():
    print("=== Sistema de Cliente TCP com Protobuf ===")

    # matricula = input("Digite sua matrícula: ").strip()
    matricula = "509022"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print(f"Conectando a {SERVER_IP}:{SERVER_PORT}...")
        sock.connect((SERVER_IP, SERVER_PORT))
        print("Conectado!")

        enviar_info(sock, tipo="basico")
        resp, tempo_total, token = autenticar(sock, matricula)
        if not token:
            print("Falha na autenticação.")
            return

        menu_operacoes(sock, token)


if __name__ == "__main__":
    main()
