import os
from datetime import datetime

ARQUIVO_LOG = "ocorrencias.txt"


def _timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")


def registrar_log(mensagem: str):
    """
    Registra uma mensagem no arquivo de log com timestamp.

    Args:
        mensagem (str): Texto da ocorrência a ser registrada.

    Returns:
        None
    """
    linha = f"{_timestamp()} {mensagem}\n"
    try:
        with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
            f.write(linha)
    except Exception as e:
        print(f"  [ERRO] Não foi possível registrar log: {e}")


def log_abertura():
    registrar_log("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")


def log_alerta_acesso_negado(contexto: str):
    registrar_log(f"ALERTA: Tentativa de acesso negado [{contexto}].")


def log_alerta_voto_duplo(titulo: str):
    registrar_log(f"ALERTA: Tentativa de voto duplo [título: {titulo}].")


def log_sucesso_voto(titulo: str):
    registrar_log(f"SUCESSO: Voto realizado com sucesso [título: {titulo}].")


def log_encerramento():
    registrar_log("ENCERRAMENTO: Votação finalizada com sucesso.")


def exibir_logs():
    """
    Lê e exibe no terminal todas as ocorrências registradas no arquivo de log.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n  --------------------------------------------------")
    print("           LOG DE OCORRÊNCIAS")
    print("  --------------------------------------------------")

    if not os.path.exists(ARQUIVO_LOG):
        print("  Nenhuma ocorrência registrada ainda.")
        print("\n  --------------------------------------------------")
        return

    with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    if not linhas:
        print("  Nenhuma ocorrência registrada ainda.")
    else:
        for linha in linhas:
            print(f"  {linha}", end="")

    print("\n  --------------------------------------------------")
    print(f"  Total de registros: {len(linhas)}")
    print("  --------------------------------------------------")