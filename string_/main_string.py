import socket
from datetime import datetime
import time

SERVER_IP = "3.88.99.255"
SERVER_PORT = 8080


def enviar_mensagem(sock, mensagem: str):
    """Envia mensagem STRING codificada em UTF-8 (terminada com \\n)."""
    try:
        if not mensagem.endswith("\n"):
            mensagem += "\n"
        sock.sendall(mensagem.encode("utf-8"))
    except Exception as e:
        print("Erro ao enviar mensagem:", e)
        raise


def receber_resposta(sock):
    """Recebe resposta STRING e retorna texto completo sem quebras."""
    try:
        data = sock.recv(4096)
        resposta = data.decode("utf-8").strip()
        return resposta
    except Exception as e:
        print("Erro ao receber resposta:", e)
        raise

def autenticar(sock, aluno_id, print_resposta=True):
    try:
        timestamp = datetime.now().isoformat()

        msg = f"AUTH|aluno_id={aluno_id}|timestamp={timestamp}|FIM"

        

        # tempo envio
        t0 = time.time()
        enviar_mensagem(sock, msg)
        tempo_envio = round(time.time() - t0, 3)

        # tempo resposta
        t0_r = time.time()
        resposta = receber_resposta(sock)
        tempo_resposta = round(time.time() - t0_r, 3)

        tempo_total = round(tempo_envio + tempo_resposta, 3)

        if print_resposta:
            print("\nRESPOSTA AUTH")
            print(resposta)
            print(f"Tempo total AUTH: {tempo_total}s\n")

        # extrair token (simples parse)
        token = None
        for parte in resposta.split("|"):
            if parte.startswith("token="):
                token = parte.split("=")[1]

        return resposta, token, tempo_total, tempo_envio, tempo_resposta

    except Exception as e:
        print("Erro na autenticação:", e)
        return None, None, None, None, None

def operacoes_disponiveis(sock, token, operacao, parametros=None, print_resposta=True):
    try:
        timestamp = datetime.now().isoformat()



        if parametros is not None:
            chave_parametro = next(iter(parametros))
            valor_parametro = parametros[chave_parametro]
        # chave_parametro: valor_parametro
        # Monta mensagem no formato padrão
        if operacao =='timestamp':
            msg = f"OP|token={token}|operacao={operacao}|timestamp={timestamp}|FIM"
        else:
            msg = f"OP|token={token}|operacao={operacao}|{chave_parametro}={valor_parametro} |timestamp={timestamp}|FIM"

        # tempo envio
        t0 = time.time()
        enviar_mensagem(sock, msg)
        tempo_envio = round(time.time() - t0, 3)

        # tempo resposta
        t0_r = time.time()
        resposta = receber_resposta(sock)
        tempo_resposta = round(time.time() - t0_r, 3)

        tempo_total = round(tempo_envio + tempo_resposta, 3)

        if print_resposta:
            print(f"\nRESPOSTA {operacao.upper()}:")
            # resposta = resposta.strip()
            for row in resposta.split("|"):
                print(row)
            # print(resposta)
            print(f"Tempo total {operacao.upper()}: {tempo_total}s")

        return resposta, tempo_total, tempo_envio, tempo_resposta

    except Exception as e:
        print(f"Erro na operação {operacao}:", e)
        return None, None, None, None


def logout(sock, token, print_resposta=True):
    try:
        timestamp = datetime.now().isoformat()
        msg = f"LOGOUT|token={token}|timestamp={timestamp}|FIM"

        # envio
        t0 = time.time()
        enviar_mensagem(sock, msg)
        tempo_envio = round(time.time() - t0, 3)

        # resposta
        t0_r = time.time()
        resposta = receber_resposta(sock)
        tempo_rsposta = round(time.time() - t0_r, 3)

        tempo_total = round(tempo_envio + tempo_rsposta, 3)

        if print_resposta:
            print("\nRESPOSTA LOGOUT")
            print(resposta)
            print(f"Tempo total LOGOUT: {tempo_total}s")

        return resposta, tempo_total, tempo_envio, tempo_rsposta

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

        # ECHO
        elif opc == "1":
            msg = input("Digite a mensagem para ECO: ")
            operacoes_disponiveis(sock, token, "echo", {"mensagem": msg})

        # SOMA
        elif opc == "2":
            numeros = ''
            while True:
                aux = input("Digite número ou 'q' para finalizar: ")
                if aux.lower() == 'q':
                    break
                elif not(aux.isdigit()):
                    print("Valor inválido.")
                    continue
                try:
                    
                    numeros = numeros + aux + ','
                except:
                    print("Valor inválido.")

            operacoes_disponiveis(sock, token, "soma", {"nums": numeros[:-1]}) 

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

            operacoes_disponiveis(sock, token, "status", {"detalhado": detalhado})

        elif opc == "4":
            while True:
                limite = input("Digite o valor do limite: ")
                if not limite.isdigit():
                    print("Valor inválido. Digite um número inteiro.")
                else:
                    break
            
            operacoes_disponiveis(sock, token, "historico", {"limite": limite})

        elif opc == "5":
            operacoes_disponiveis(sock, token, "timestamp")

        else:
            print("Opção inválida!")


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

        resposta_auth, token, _, _, _ = autenticar(sock, "509022")

        if not token:
            print("Falha na autenticação.")
            return

        menu_operacoes(sock, token)


if __name__ == "__main__":
    main()
