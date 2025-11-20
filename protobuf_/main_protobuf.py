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
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import protobuf_.sd_protocol_pb2 as sd_protocol_pb2
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

def autenticar(sock, aluno_id, print_resposta=True):

    try:
        req = sd_protocol_pb2.Requisicao()
        req.auth.aluno_id = aluno_id
        req.auth.timestamp_cliente = datetime.now().isoformat()

        t0 = time.time()
        enviar_protobuf(sock, req)
        t1 = time.time()
        tempo_envio = round(t1 - t0, 3)

        t0_ = time.time()
        resposta = receber_protobuf(sock, sd_protocol_pb2.Resposta)
        t1_ = time.time()
        tempo_resposta = round(t1_ - t0_, 3)

        tempo_total = round(t1_ - t0, 3)
        
        if print_resposta:
            print("\nRESPOSTA AUTH:")
            print(json_format.MessageToJson(resposta, indent=2))
            print(f"Tempo total AUTH: {tempo_total}s")

        if resposta.HasField("ok"):
            token = resposta.ok.dados.get("token", "")
            return resposta, token, tempo_total, tempo_envio, tempo_resposta
        else:
            return resposta, None, tempo_total, tempo_envio, tempo_resposta

    except Exception as e:
        print("Erro na autenticação:", e)
        return None, None, None, None, None

def operacoes_disponiveis(sock, token, operacao, parametros=None, print_resposta=True):

    try:
        req = sd_protocol_pb2.Requisicao()
        req.operacao.token = token
        req.operacao.operacao = operacao

        if parametros is not None:
            chave_parametro = next(iter(parametros))
            valor_parametro = parametros[chave_parametro]

      
            req.operacao.parametros[chave_parametro] = valor_parametro

        

        t0 = time.time()
        enviar_protobuf(sock, req)
        t1 = time.time()
        tempo_envio = round(t1 - t0, 3)

        t0_ = time.time()
        resposta = receber_protobuf(sock, sd_protocol_pb2.Resposta)
        t1_ = time.time()
        tempo_resposta = round(t1_ - t0_, 3)

        tempo_total = round(t1_ - t0, 3)

        if print_resposta:
           print(f"\nRESPOSTA {operacao.upper()}:")
           print(json_format.MessageToJson(resposta, indent=2))
           print(f"Tempo total {operacao.upper()}: {tempo_total}s")

        return resposta, tempo_total, tempo_envio, tempo_resposta
    except Exception as e:
        print(f"Erro na operação {operacao}:", e)
        return None, None, None, None

def enviar_info(sock, tipo, print_resposta=True):

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

        if print_resposta:
            print(f"\nRESPOSTA INFO: {json_format.MessageToJson(resp, indent=2)}")
            print(f"Tempo total INFO: {tempo_total}s")

        return resp, tempo_total, tempo_envio, tempo_resposta

    except Exception as e:
        print("Erro ao enviar INFO:", e)
        return None, None, None, None

def logout(sock, token, print_resposta=True):

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

        if print_resposta:
            print(f"\nRESPOSTA LOGOUT: {json_format.MessageToJson(resp, indent=2)}")
            print(f"Tempo total LOGOUT: {tempo_total}s")

        return resp, tempo_total, tempo_envio, tempo_resposta

    except Exception as e:
        print("Erro no LOGOUT:", e)
        return None, None, None, None


def menu_operacoes(sock, token):

    while True:
        print("\nDigite o número da operação desejada:")
        print("1 - ECHO")
        print("2 - SOMA")
        print("3 - STATUS")
        print("4 - HISTORICO")
        print("5 - TIMESTAMP")
        print("0 - LOGOUT e sair")
        print("-------------------------")

        opc = input("Escolha: ").strip()
        # opc = "1"

        if opc == "0":
            logout(sock, token)
            print("Saindo...")
            break
        elif opc == "1":
            mensagem = str(input("Digite a mensagem para eco: "))

            resp, _, _, _ = operacoes_disponiveis(sock, token, "echo", parametros={"mensagem": mensagem})
            print("Resposta ECHO:", resp)
   

        elif opc == "2":
           
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
                
            resp ,_ ,_ ,_ = operacoes_disponiveis(sock, token, "soma", parametros={"numeros": ",".join(numeros)})


            print("Resposta SOMA:", resp)
            

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
            resp , _, _, _ = operacoes_disponiveis(sock, token, "status", parametros={"detalhado": str(detalhado)})
            print("STATUS:", resp)

        elif opc == "4":
            while True:
                limite = input("Digite o valor do limite: ")
                if limite.isdigit():
                    break
                else:
                    print("Valor inválido. Digite um número inteiro.")
            resp, _, _, _ =  operacoes_disponiveis(sock, token, "historico", parametros={"limite": limite})
            
            print("HISTORICO:", resp)

        elif opc == "5":
            resp, _, _, _ = operacoes_disponiveis(sock, token, "timestamp")
            print("TIMESTAMP:", resp)
        else:
            print("Opção inválida!")
            continue




def main():
    print("=== Sistema de Cliente TCP com Protobuf ===")

    # matricula = input("Digite sua matrícula: ").strip()
    matricula = "509022"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print(f"Conectando a {SERVER_IP}:{SERVER_PORT}...")
        sock.connect((SERVER_IP, SERVER_PORT))
        print("Conectado!")

        enviar_info(sock, tipo="basico")
        esp, token, tempo_total, tempo_envio, tempo_resposta = autenticar(sock, matricula)
        if not token:
            print("Falha na autenticação.")
            return

        menu_operacoes(sock, token)


if __name__ == "__main__":
    main()
