import pandas as pd
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from  string_.main_string import operacoes_disponiveis, autenticar, logout
import socket

def teste_performance(sock, token, repeticoes=3):
    """
    Executa múltiplos testes de desempenho e retorna um DataFrame com os tempos.
    """

    resultados = []

    for i in range(repeticoes):
        print(f"\n=== Rodada {i+1}/{repeticoes} ===")

        # ECHO
        msg = "teste de desempenho"
        
        _, tempo_total, tempo_envio, tempo_resposta =  operacoes_disponiveis(sock, token, "echo", {"mensagem": msg}, print_resposta=False) 
            
        # resp, tempo_total, tempo_envio, tempo_resposta = operacos_disponiveis(sock, token, "echo", parametros_mensagem=mensagem)


        resultados.append({
            "operacao": "echo",
            "tempo_envio": tempo_envio,
            "tempo_resposta": tempo_resposta, # seu protocolo não separa envio/recebimento
            "tempo_total": tempo_total
        })

        # SOMA
        numeros = '1,2,3,4'
        
        _, tempo_total, tempo_envio, tempo_resposta =  operacoes_disponiveis(sock, token, "soma", {"nums": numeros}, print_resposta=False)
        
        resultados.append({
            "operacao": "soma",
            "tempo_envio": tempo_envio,
            "tempo_resposta": tempo_resposta,
            "tempo_total": tempo_total
        })

        # STATUS
        
        _, tempo_total, tempo_envio, tempo_resposta =  operacoes_disponiveis(sock, token, "status", {"detalhado": True}, print_resposta=False)
        
        resultados.append({
            "operacao": "status",
            "tempo_envio": tempo_envio,
            "tempo_resposta": tempo_resposta,
            "tempo_total": tempo_total
        })

        # HISTORICO
        
        _, tempo_total, tempo_envio, tempo_resposta =  operacoes_disponiveis(sock, token, "historico", {"limite": 3}, print_resposta=False)

        
        resultados.append({
            "operacao": "historico",
            "tempo_envio": tempo_envio,
            "tempo_resposta": tempo_resposta,
            "tempo_total": tempo_total
        })

        # TIMESTAMP
        
        _, tempo_total, tempo_envio, tempo_resposta =  operacoes_disponiveis(sock, token, "timestamp", print_resposta=False)
        
        resultados.append({
            "operacao": "timestamp",
            "tempo_envio": tempo_envio,
            "tempo_resposta": tempo_resposta,
            "tempo_total": tempo_total
        })

    df = pd.DataFrame(resultados)
    print("\nResultado da análise temporal:")
    print(df)

    return df

SERVER_IP = "3.88.99.255"   # exemplo local — altere para o IP público AWS
SERVER_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

res, token, _,_,_ = autenticar(sock, "509022")
df = teste_performance(sock, token, repeticoes=10)
df.to_csv("./data_analytics/resultados_tempo_jstring.csv", index=False)
logout(sock, token)
print("\nArquivo salvo: resultados_teste.csv")
