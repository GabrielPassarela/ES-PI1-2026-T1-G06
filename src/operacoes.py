import validacao
import database
import logs
import criptografia
import mysql.connector
import random
import string
from datetime import datetime


def cadastrar_eleitor():
    """
    Solicita os dados do eleitor, valida CPF e titulo de eleitor,
    gera e criptografa a chave de acesso e o CPF, e salva no banco.
 
    Args:
        nome (str): Nome completo do eleitor informado pelo usuario.
        cpf (str): CPF do eleitor, validado matematicamente antes do cadastro.
        mesario (str): Indica se o eleitor e mesario (1 para Sim, 0 para Nao).
        titulo_de_eleitor (str): Numero do titulo de eleitor, validado matematicamente.
 
    Returns:
        None
    """
    nome = input("  Digite o nome completo do eleitor: ").strip()
    cpf = input("  Digite o CPF do eleitor: ").strip()
    cpf = cpf.replace(".", "").replace("-", "")

    while not validacao.validacao(cpf):
        print("  CPF inválido! Tente novamente.")
        cpf = input("  Digite o CPF do eleitor: ").strip()
        cpf = cpf.replace(".", "").replace("-", "")

    mesario = input("  É mesário? (1 - Sim, 0 - Não): ").strip()
    titulo_de_eleitor = input("  Digite o número do título de eleitor: ").strip()

    while not validacao.validacao_titulo(titulo_de_eleitor):
        print("  Título de eleitor inválido! Tente novamente.")
        titulo_de_eleitor = input("  Digite o número do título de eleitor: ").strip()

    chave_acesso = criptografia.gerar_chave_acesso(nome)
    chave_criptografada = criptografia.criptografar_chave_acesso(chave_acesso)
    cpf_criptografado = criptografia.criptografar_cpf(cpf)

    try:
        conn = database.conectar()
        cursor = conn.cursor()

        sql = """INSERT INTO ELEITORES (nome_completo, titulo_eleitor, cpf, mesário, chave_acesso)
                VALUES (%s, %s, %s, %s, %s)"""
        valores = (nome, titulo_de_eleitor, cpf_criptografado, int(mesario), chave_criptografada)

        cursor.execute(sql, valores)
        conn.commit()
        print("\n  Eleitor cadastrado com sucesso!")
        print(f"  Chave de acesso: {chave_acesso}")

    except mysql.connector.IntegrityError:
        print("\n  Erro: CPF ou título de eleitor já cadastrado.")
    except Exception as e:
        print(f"\n  Erro ao cadastrar: {e}")
    finally:
        cursor.close()
        conn.close()




def editar_eleitor():
    """
    Busca um eleitor pelo CPF e permite a edicao dos seus dados,
    mantendo as regras de validacao e unicidade de CPF e titulo.
 
    Args:
        cpf (str): CPF do eleitor a ser editado, informado pelo usuario.
        novo_nome (str): Novo nome completo do eleitor, deixe vazio para manter o atual.
        novo_cpf (str): Novo CPF do eleitor, revalidado matematicamente, deixe vazio para manter o atual.
        novo_titulo (str): Novo titulo de eleitor, revalidado matematicamente, deixe vazio para manter o atual.
        novo_mesario (str): Novo status de mesario do eleitor, deixe vazio para manter o atual.
 
    Returns:
        None
    """
    cpf = input("Digite o CPF do eleitor a editar: ").strip()
    cpf = cpf.replace(".", "").replace("-", "")

    cpf_criptografado = criptografia.criptografar_cpf(cpf)

    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM ELEITORES WHERE cpf = %s",
            (cpf_criptografado,)
        )

        eleitor = cursor.fetchone()

        if not eleitor:
            print("Eleitor não encontrado.")
            return

        cpf_legivel = criptografia.descriptografar_cpf(eleitor['cpf'])[:11]

        print(f"\n  Eleitor encontrado: {eleitor['nome_completo']}")
        print("  Deixe em branco para manter o valor atual.")

        novo_nome = input(f"  Novo nome [{eleitor['nome_completo']}]: ").strip()

        novo_cpf = input(f"  Novo CPF [{cpf_legivel}]: ").strip()
        novo_cpf = novo_cpf.replace(".", "").replace("-", "")

        novo_titulo = input(f"  Novo título [{eleitor['titulo_eleitor']}]: ").strip()

        novo_mesario = input(
            f"  Mesário? (1-Sim, 0-Não) [{eleitor['mesário']}]: "
        ).strip()

        
        if novo_nome == "":
            novo_nome = eleitor['nome_completo']

        
        if novo_cpf == "":
            novo_cpf_criptografado = eleitor['cpf']
        else:
            while not validacao.validacao(novo_cpf):
                print("  CPF inválido! Tente novamente.")
                novo_cpf = input("  Novo CPF: ").strip()
                novo_cpf = novo_cpf.replace(".", "").replace("-", "")

            novo_cpf_criptografado = criptografia.criptografar_cpf(novo_cpf)

        
        if novo_titulo == "":
            novo_titulo = eleitor['titulo_eleitor']
        else:
            while not validacao.validacao_titulo(novo_titulo):
                print("  Título inválido! Tente novamente.")
                novo_titulo = input("  Novo título: ").strip()

       
        if novo_mesario == "":
            novo_mesario = eleitor['mesário']

        cursor.execute("""
            UPDATE ELEITORES
            SET nome_completo = %s,
                cpf = %s,
                titulo_eleitor = %s,
                mesário = %s
            WHERE cpf = %s
        """, (
            novo_nome,
            novo_cpf_criptografado,
            novo_titulo,
            int(novo_mesario),
            cpf_criptografado
        ))

        conn.commit()

        print("\n  Eleitor atualizado com sucesso!")

    except mysql.connector.IntegrityError:
        print("\n  Erro: CPF ou título já cadastrado.")

    except Exception as e:
        print(f"\n  Erro ao editar: {e}")

    finally:
        cursor.close()
        conn.close()

def remover_eleitor():

    """
    Busca um eleitor pelo CPF e o remove do banco de dados apos confirmacao.
 
    Args:
        cpf (str): CPF do eleitor a ser removido, informado pelo usuario.
        confirmacao (str): Confirmacao do usuario para prosseguir com a remocao (sim/nao).
 
    Returns:
        None
    """

    cpf = input("Digite o CPF do eleitor a remover: ").strip()
    cpf = cpf.replace(".", "").replace("-", "")

    cpf_criptografado = criptografia.criptografar_cpf(cpf)

    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM ELEITORES WHERE cpf = %s",
            (cpf_criptografado,)
        )

        eleitor = cursor.fetchone()

        if not eleitor:
            print("Eleitor não encontrado.")
            return

        print(f"\n  Eleitor encontrado: {eleitor['nome_completo']}")

        confirmacao = input(
            "  Deseja realmente remover? (sim/não): "
        ).strip().lower()

        if confirmacao != "sim":
            print("  Remoção cancelada.")
            return

        cursor.execute(
            "DELETE FROM ELEITORES WHERE cpf = %s",
            (cpf_criptografado,)
        )

        conn.commit()

        print("\n  Eleitor removido com sucesso!")

    except Exception as e:
        print(f"\n  Erro ao remover: {e}")

    finally:
        cursor.close()
        conn.close()

def listar_eleitores():
    """
    Lista todos os eleitores cadastrados no banco de dados,
    descriptografando o CPF para exibicao legivel.
 
    Args:
        Nenhum argumento externo. Os dados sao obtidos diretamente do banco.
 
    Returns:
        None
    """
    try:
        conn = database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM eleitores")
        resultados = cursor.fetchall()

        if not resultados:
            print("\n  Nenhum eleitor cadastrado.")
            return

        print("\n  --------------------------------------------------")
        for resultado in resultados:
            cpf_legivel = criptografia.descriptografar_cpf(resultado[3])[:11]
            print(f"\n  ID:      {resultado[0]}")
            print(f"  Nome:    {resultado[1]}")
            print(f"  Título:  {resultado[2]}")
            print(f"  CPF:     {cpf_legivel}")
            print(f"  Mesário: {'Sim' if resultado[4] else 'Não'}")
            print(f"  Votou:   {'Sim' if resultado[6] else 'Não'}")
            print("  --------------------------------------------------")

    except Exception as e:
        print(f"\n  Erro ao listar: {e}")
    finally:
        cursor.close()
        conn.close()


def cadastrar_candidato():
    """
    Cadastra um novo candidato com nome, numero de votacao e partido no banco.
 
    Args:
        Nenhum argumento externo. Os dados sao obtidos diretamente do banco.
 
    Returns:
        None
    """
    print("\n  Em desenvolvimento.")


def editar_candidato():
    """
    Edita os dados de um candidato existente, respeitando a regra de numero unico.
 
    Args:
        Nenhum argumento externo. Os dados sao obtidos diretamente do banco.
 
    Returns:
        None
    """
    print("\n  Em desenvolvimento.")


def remover_candidato():
    """
    Remove um candidato do banco de dados pelo numero de votacao.
 
    Args:
        Nenhum argumento externo. Os dados sao obtidos diretamente do banco.
 
    Returns:
        None
    """
    print("\n  Em desenvolvimento.")


def buscar_candidato():
    """
    Busca um candidato no banco de dados pelo numero de votacao.
 
    Args:
        Nenhum argumento externo. Os dados sao obtidos diretamente do banco.
 
    Returns:
        None
    """
    print("\n  Em desenvolvimento.")


def listar_candidatos():
    """
    Lista todos os candidatos cadastrados no banco de dados.
 
    Args:
        Nenhum argumento externo. Os dados sao obtidos diretamente do banco.
 
    Returns:
        None
    """
    print("\n  Em desenvolvimento.")


def verificar_mesario_para_abrir_votacao():
    """
    Verifica se o eleitor informado possui perfil de mesario antes de
    liberar o acesso ao submenu de votacao.
 
    Args:
        titulo_eleitor (str): Numero do titulo de eleitor informado pelo usuario.
        cpf (str): CPF completo do eleitor informado pelo usuario.
 
    Returns:
        bool: True se o eleitor for mesario e os dados forem validos, False caso contrario.
    """
    print("\n  --------------------------------------------------")
    print("       VERIFICAÇÃO PARA ABRIR SISTEMA DE VOTAÇÃO")
    print("  --------------------------------------------------")

    titulo_eleitor = input("  Digite seu título de eleitor: ").strip()
    cpf = input("  Digite seu CPF: ").strip()
    cpf = cpf.replace(".", "").replace("-", "")

    conn = None
    cursor = None

    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM eleitores
            WHERE titulo_eleitor = %s
        """, (titulo_eleitor,))

        eleitor = cursor.fetchone()

        if not eleitor or not eleitor['mesário']:
            print("\n  Acesso negado. Apenas mesários podem abrir o sistema de votação.")
            logs.log_alerta_acesso_negado("abertura do sistema de votação por não mesário")
            return False

        cpf_banco = criptografia.descriptografar_cpf(eleitor['cpf'])[:11]
        if cpf_banco != cpf and eleitor['cpf'] != cpf:
            print("\n  Acesso negado. CPF ou título de eleitor incorreto.")
            logs.log_alerta_acesso_negado("abertura do sistema de votação com dados inválidos")
            return False

        print("\n  Mesário confirmado. Sistema de votação liberado.")
        return True

    except Exception as e:
        print(f"\n  Erro ao verificar mesário: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def autenticar_mesario():
    """
    Autentica o mesario pelo titulo de eleitor, primeiros 4 digitos do CPF
    e chave de acesso criptografada. Apos autenticacao, executa a Zerezima,
    apagando votos anteriores e exibindo todos os candidatos com zero votos.
 
    Args:
        titulo_eleitor (str): Numero do titulo de eleitor do mesario.
        cpf (str): Primeiros 4 digitos do CPF do mesario.
        chave (str): Chave de acesso do mesario.
 
    Returns:
        None
    """
    print("\n  --------------------------------------------------")
    print("         AUTENTICAÇÃO DO MESÁRIO / ZERÉZIMA")
    print("  --------------------------------------------------")

    titulo_eleitor = input("  Digite seu título de eleitor: ").strip()
    cpf = input("  Digite os 4 primeiros dígitos do seu CPF: ").strip()
    chave = input("  Digite sua chave de acesso: ").strip().upper()

    chave_criptografada = criptografia.criptografar_chave_acesso(chave)

    conn = None
    cursor = None

    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM eleitores 
            WHERE titulo_eleitor = %s AND chave_acesso = %s AND mesário = 1
        """, (titulo_eleitor, chave_criptografada))

        eleitor = cursor.fetchone()

        if not eleitor:
            print("\n  Dados inválidos ou usuário não é mesário.")
            logs.log_alerta_acesso_negado("abertura de urna")
            return

        cpf_banco = criptografia.descriptografar_cpf(eleitor['cpf'])
        if not cpf_banco.startswith(cpf):
            print("\n  Dados inválidos ou usuário não é mesário.")
            logs.log_alerta_acesso_negado("abertura de urna")
            return

        print("\n  Autenticação bem-sucedida! Bem-vindo, mesário.")
        print("\n  Realizando Zerézima...")

        cursor.execute("DELETE FROM VOTOS")
        cursor.execute("UPDATE eleitores SET votou = 0")
        conn.commit()

        cursor.execute("SELECT nome, numerodevotacao FROM CANDIDATOS ORDER BY nome ASC")
        candidatos = cursor.fetchall()

        print("\n  --------------------------------------------------")
        print("  CANDIDATOS - TOTAL DE VOTOS: ZERO")
        print("  --------------------------------------------------")
        for c in candidatos:
            print(f"  {c['nome']} (Nº {c['numerodevotacao']}): 0 voto(s)")
        print("  --------------------------------------------------")

        logs.log_abertura()

    except Exception as e:
        print(f"\n  Erro: {e}")
    finally:
        cursor.close()
        conn.close()


def registrar_voto():
    """
    Autentica o eleitor pelo titulo, primeiros 4 digitos do CPF e chave de acesso,
    exibe o candidato escolhido pelo numero de votacao, solicita confirmacao
    e registra o voto no banco com protocolo criptografado.
 
    Args:
        titulo_eleitor (str): Numero do titulo de eleitor do eleitor.
        cpf (str): Primeiros 4 digitos do CPF do eleitor.
        chave (str): Chave de acesso do eleitor.
        numero_votacao (str): Numero do candidato escolhido pelo eleitor.
 
    Returns:
        None
    """
    print("\n  --------------------------------------------------")
    print("               REGISTRAR VOTO")
    print("  --------------------------------------------------")

    conn = None
    cursor = None

    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)

        while True:
            titulo_eleitor = input("  Digite seu título de eleitor: ").strip()
            cpf = input("  Digite os 4 primeiros dígitos do seu CPF: ").strip()
            chave = input("  Digite sua chave de acesso: ").strip().upper()

            chave_criptografada = criptografia.criptografar_chave_acesso(chave)

            cursor.execute("""
                SELECT * FROM eleitores
                WHERE titulo_eleitor = %s
                AND chave_acesso = %s
            """, (titulo_eleitor, chave_criptografada))

            eleitor = cursor.fetchone()

            if not eleitor:
                print("\n  Dados inválidos: título de eleitor ou chave de acesso incorretos.")
                logs.log_alerta_acesso_negado("tentativa de voto inválida")
                print("  Digite os dados novamente.\n")
                continue

            cpf_banco = criptografia.descriptografar_cpf(eleitor['cpf'])
            if not cpf_banco.startswith(cpf):
                print("\n  Dados inválidos: CPF incorreto.")
                logs.log_alerta_acesso_negado("tentativa de voto inválida")
                print("  Digite os dados novamente.\n")
                continue

            if eleitor['votou']:
                print("\n  Este eleitor já votou.")
                logs.log_alerta_voto_duplo(titulo_eleitor)
                return

            break

        candidato = None

        while True:
            print("\n  --------------------------------------------------")
            numero_votacao = input("  Digite o número do candidato: ").strip()

            cursor.execute("SELECT * FROM CANDIDATOS WHERE numerodevotacao = %s", (numero_votacao,))
            candidato = cursor.fetchone()

            if candidato:
                print("\n  --------------------------------------------------")
                print(f"  Nome:    {candidato['nome']}")
                print(f"  Número:  {candidato['numerodevotacao']}")
                print(f"  Partido: {candidato['partido']} ({candidato['sigla_partido']})")
                print("  --------------------------------------------------")
            else:
                print("\n  --------------------------------------------------")
                print("  Número não encontrado.")
                print("  Se confirmar, o voto será registrado como NULO.")
                print("  --------------------------------------------------")

            confirmacao = input("  Confirmar voto? (S/SIM = Confirmar / N/NAO = Redigitar): ").strip().upper()

            if confirmacao in ('S', 'SIM'):
                break
            elif confirmacao in ('N', 'NAO', 'NÃO'):
                continue
            else:
                print("  Opção inválida. Digite S ou N.")
                continue

        # Gera e criptografa o protocolo
        num_candidato = int(candidato['numerodevotacao'][-2:]) if candidato else 0
        protocolo = criptografia.gerar_protocolo(num_candidato)
        protocolo_criptografado = criptografia.criptografar_protocolo(protocolo)

        candidato_id = candidato['id'] if candidato else None

        cursor.execute("""
            INSERT INTO VOTOS (candidato_id, data_hora, protocolo) 
            VALUES (%s, NOW(), %s)
        """, (candidato_id, protocolo_criptografado))

        cursor.execute("""
            UPDATE eleitores SET votou = 1 
            WHERE titulo_eleitor = %s
        """, (titulo_eleitor,))

        conn.commit()

        logs.log_sucesso_voto(titulo_eleitor)

        print("\n  Voto registrado com sucesso!")
        if not candidato:
            print("  (Voto registrado como NULO)")
        print(f"  Protocolo: {protocolo}")
        print("  --------------------------------------------------")

    except Exception as e:
        print(f"\n  Erro ao registrar voto: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def encerrar_votacao():
    """
    Encerra a votacao apos autenticacao do mesario com dupla confirmacao da chave.
    Registra o encerramento no arquivo de log.
 
    Args:
        titulo_eleitor (str): Numero do titulo de eleitor do mesario.
        cpf (str): Primeiros 4 digitos do CPF do mesario.
        chave (str): Chave de acesso do mesario.
        confirmacao (str): Confirmacao do mesario para encerrar (Sim/Nao).
        chave_confirmacao (str): Segunda insercao da chave para dupla confirmacao.
 
    Returns:
        bool: Retorna True se o encerramento foi realizado com sucesso, False caso contrario.
    """
    print("\n  --------------------------------------------------")
    print("         ENCERRAMENTO DO SISTEMA DE VOTAÇÃO")
    print("  --------------------------------------------------")

    titulo_eleitor = input("  Digite seu título de eleitor: ").strip()
    cpf = input("  Digite os 4 primeiros dígitos do seu CPF: ").strip()
    chave = input("  Digite sua chave de acesso: ").strip().upper()

    chave_criptografada = criptografia.criptografar_chave_acesso(chave)

    conn = None
    cursor = None

    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM eleitores 
            WHERE titulo_eleitor = %s AND chave_acesso = %s AND mesário = 1
        """, (titulo_eleitor, chave_criptografada))

        eleitor = cursor.fetchone()

        if not eleitor:
            print("\n  Dados inválidos ou usuário não é mesário.")
            logs.log_alerta_acesso_negado("encerramento de urna")
            return False

        cpf_banco = criptografia.descriptografar_cpf(eleitor['cpf'])
        if not cpf_banco.startswith(cpf):
            print("\n  Dados inválidos ou usuário não é mesário.")
            logs.log_alerta_acesso_negado("encerramento de urna")
            return False

        confirmacao = input("\n  Deseja realmente encerrar a votação? (Sim/Não): ").strip().lower()

        if confirmacao != "sim":
            print("\n  Encerramento cancelado.")
            return False

        chave_confirmacao = input("  Digite sua chave de acesso novamente: ").strip()

        if chave_confirmacao != chave:
            print("\n  Chave de acesso incorreta. Encerramento não autorizado.")
            logs.log_alerta_acesso_negado("confirmação de chave no encerramento")
            return False

        print("\n  Votação encerrada com sucesso!")
        logs.log_encerramento()
        return True

    except Exception as e:
        print(f"\n  Erro: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def exibir_logs():
    """
    Le e exibe no terminal o conteudo do arquivo de log de ocorrencias.
 
    Args:
        Nenhum argumento externo. Os dados sao lidos do arquivo de log.
 
    Returns:
        None
    """
    logs.exibir_logs()


def exibir_protocolos():
    """
    Lista todos os protocolos de votacao armazenados no banco de dados,
    descriptografando-os antes da exibicao, em ordem alfabetica.
 
    Args:
        Nenhum argumento externo. Os dados sao obtidos diretamente do banco.
 
    Returns:
        None
    """
    print("\n  --------------------------------------------------")
    print("           PROTOCOLOS DE VOTAÇÃO")
    print("  --------------------------------------------------")
    try:
        conn = database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT protocolo, data_hora FROM VOTOS ORDER BY protocolo ASC")
        protocolos = cursor.fetchall()

        if not protocolos:
            print("  Nenhum protocolo registrado.")
        else:
            for i, row in enumerate(protocolos, start=1):
                protocolo_legivel = criptografia.descriptografar_protocolo(row[0])
                print(f"  {i:>3}. {protocolo_legivel}  |  {row[1]}")

        print("  --------------------------------------------------")
        print(f"  Total: {len(protocolos)} protocolo(s).")
        print("  --------------------------------------------------")

    except Exception as e:
        print(f"\n  Erro ao exibir protocolos: {e}")
    finally:
        cursor.close()
        conn.close()


def boletim_urna():
    """
    Exibe o boletim de urna com os votos consolidados por candidato
    em ordem alfabetica e declara o vencedor da eleicao.
 
    Args:
        Nenhum argumento externo. Os dados sao obtidos diretamente do banco.
 
    Returns:
        None
    """
    print("\n  --------------------------------------------------")
    print("               BOLETIM DE URNA")
    print("  --------------------------------------------------")

    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT c.nome, c.numerodevotacao, c.partido, COUNT(v.id) AS total_votos
            FROM CANDIDATOS c
            LEFT JOIN VOTOS v ON v.candidato_id = c.id
            GROUP BY c.id, c.nome, c.numerodevotacao, c.partido
            ORDER BY c.nome ASC
        """)

        candidatos = cursor.fetchall()

        if not candidatos:
            print("  Nenhum candidato cadastrado.")
            return

        for c in candidatos:
            print(f"  {c['nome']} (Nº {c['numerodevotacao']} - {c['partido']}): {c['total_votos']} voto(s)")

        vencedor = max(candidatos, key=lambda c: c['total_votos'])

        print("\n  --------------------------------------------------")
        print("                   VENCEDOR")
        print("  --------------------------------------------------")
        print(f"  Nome:        {vencedor['nome']}")
        print(f"  Número:      {vencedor['numerodevotacao']}")
        print(f"  Partido:     {vencedor['partido']}")
        print(f"  Total votos: {vencedor['total_votos']}")
        print("  --------------------------------------------------")

    except Exception as e:
        print(f"\n  Erro ao exibir boletim: {e}")
    finally:
        cursor.close()
        conn.close()


def estatistica_comparecimento():
    """
    Exibe a quantidade absoluta de eleitores que votaram e o percentual
    de comparecimento em relacao ao total de eleitores cadastrados.
 
    Args:
        Nenhum argumento externo. Os dados sao obtidos diretamente do banco.
 
    Returns:
        None
    """
    print("\n  --------------------------------------------------")
    print("          ESTATÍSTICA DE COMPARECIMENTO")
    print("  --------------------------------------------------")

    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total FROM ELEITORES")
        total_eleitores = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS votaram FROM ELEITORES WHERE votou = 1")
        total_votaram = cursor.fetchone()['votaram']

        if total_eleitores == 0:
            print("  Nenhum eleitor cadastrado.")
            return

        percentual = (total_votaram / total_eleitores) * 100

        print(f"  Total de eleitores cadastrados: {total_eleitores}")
        print(f"  Total que compareceram:         {total_votaram}")
        print(f"  Percentual de comparecimento:   {percentual:.2f}%")
        print("  --------------------------------------------------")

    except Exception as e:
        print(f"\n  Erro ao exibir comparecimento: {e}")
    finally:
        cursor.close()
        conn.close()


def votos_por_partido():
    """
    Exibe a somatoria de votos recebidos por cada partido com percentual
    em relacao ao total geral de votos computados.
 
    Args:
        Nenhum argumento externo. Os dados sao obtidos diretamente do banco.
 
    Returns:
        None
    """
    print("\n  --------------------------------------------------")
    print("              VOTOS POR PARTIDO")
    print("  --------------------------------------------------")

    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT c.partido, c.sigla_partido, COUNT(v.id) AS total_votos
            FROM CANDIDATOS c
            LEFT JOIN VOTOS v ON v.candidato_id = c.id
            GROUP BY c.partido, c.sigla_partido
            ORDER BY total_votos DESC
        """)

        partidos = cursor.fetchall()

        if not partidos:
            print("  Nenhum dado encontrado.")
            print("  --------------------------------------------------")
            return

        total_geral = sum(p['total_votos'] for p in partidos)

        print(f"  {'Partido':<30} {'Sigla':<10} {'Votos':>6}  {'%':>6}")
        print(f"  {'-'*30} {'-'*10} {'-'*6}  {'-'*6}")

        for p in partidos:
            percentual = (p['total_votos'] / total_geral * 100) if total_geral > 0 else 0.0
            print(f"  {p['partido']:<30} {p['sigla_partido']:<10} {p['total_votos']:>6}  {percentual:>5.1f}%")

        print("  --------------------------------------------------")
        print(f"  Total de votos computados: {total_geral}")
        print("  --------------------------------------------------")

    except Exception as e:
        print(f"\n  Erro ao exibir votos por partido: {e}")
    finally:
        cursor.close()
        conn.close()


def validacao_integridade():
    """
    Compara o total de votos registrados na tabela VOTOS com a quantidade
    de eleitores marcados como votou = 1, verificando a integridade da eleicao.
 
    Args:
        Nenhum.
 
    Returns:
        None
    """
    print("\n  --------------------------------------------------")
    print("           VALIDAÇÃO DE INTEGRIDADE")
    print("  --------------------------------------------------")

    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total FROM VOTOS")
        total_votos = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM ELEITORES WHERE votou = 1")
        total_votaram = cursor.fetchone()['total']

        print(f"  Votos registrados na urna:      {total_votos}")
        print(f"  Eleitores marcados como votou:  {total_votaram}")
        print("  --------------------------------------------------")

        if total_votos == total_votaram:
            print("  RESULTADO: Eleição ÍNTEGRA. Nenhuma inconsistência encontrada.")
        else:
            print("  RESULTADO: INCONSISTÊNCIA DETECTADA! Os números não coincidem.")

        print("  --------------------------------------------------")

    except Exception as e:
        print(f"\n  Erro ao validar integridade: {e}")
    finally:
        cursor.close()
        conn.close()