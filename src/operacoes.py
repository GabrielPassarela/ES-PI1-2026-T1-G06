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
    Solicita os dados do eleitor, valida CPF e título de eleitor,
    gera e criptografa a chave de acesso e o CPF, e salva no banco.

    Args:
        Nenhum.

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
    Edita os dados de um eleitor existente no banco de dados.

    Args:
        Nenhum.

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
    Remove um eleitor do banco de dados.

    Args:
        Nenhum.

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
    Lista todos os eleitores cadastrados, descriptografando o CPF para exibição.

    Args:
        Nenhum.

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
    Cadastra um novo candidato no banco de dados.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n  Em desenvolvimento.")


def editar_candidato():
    """
    Edita os dados de um candidato existente no banco de dados.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n  Em desenvolvimento.")


def remover_candidato():
    """
    Remove um candidato do banco de dados.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n  Em desenvolvimento.")


def buscar_candidato():
    """
    Busca um candidato pelo número de votação.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n  Em desenvolvimento.")


def listar_candidatos():
    """
    Lista todos os candidatos cadastrados no banco de dados.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n  Em desenvolvimento.")


def autenticar_mesario():
    """
    Autentica o mesário pelo título, 4 primeiros dígitos do CPF e chave de acesso.
    Realiza a zerézima após autenticação bem-sucedida.

    Args:
        Nenhum.

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
    Autentica o eleitor, exibe o candidato escolhido, confirma o voto
    e registra no banco com protocolo criptografado.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n  --------------------------------------------------")
    print("               REGISTRAR VOTO")
    print("  --------------------------------------------------")

    titulo_eleitor = input("  Digite seu título de eleitor: ").strip()
    cpf = input("  Digite os 4 primeiros dígitos do seu CPF: ").strip()
    chave = input("  Digite sua chave de acesso: ").strip().upper()

    chave_criptografada = criptografia.criptografar_chave_acesso(chave)

    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM eleitores 
            WHERE titulo_eleitor = %s 
            AND chave_acesso = %s
        """, (titulo_eleitor, chave_criptografada))

        eleitor = cursor.fetchone()

        if not eleitor:
            print("\n  Dados inválidos: título de eleitor ou chave de acesso incorretos.")
            logs.log_alerta_acesso_negado("tentativa de voto inválida")
            return

        cpf_banco = criptografia.descriptografar_cpf(eleitor['cpf'])
        if not cpf_banco.startswith(cpf):
            print("\n  Dados inválidos: CPF incorreto.")
            logs.log_alerta_acesso_negado("tentativa de voto inválida")
            return

        if eleitor['votou']:
            print("\n  Este eleitor já votou.")
            logs.log_alerta_voto_duplo(titulo_eleitor)
            return

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
        cursor.close()
        conn.close()


def encerrar_votacao():
    """
    Encerra a votação após autenticação do mesário com dupla confirmação da chave.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n  --------------------------------------------------")
    print("         ENCERRAMENTO DO SISTEMA DE VOTAÇÃO")
    print("  --------------------------------------------------")

    titulo_eleitor = input("  Digite seu título de eleitor: ").strip()
    cpf = input("  Digite os 4 primeiros dígitos do seu CPF: ").strip()
    chave = input("  Digite sua chave de acesso: ").strip().upper()

    chave_criptografada = criptografia.criptografar_chave_acesso(chave)

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
            return

        cpf_banco = criptografia.descriptografar_cpf(eleitor['cpf'])
        if not cpf_banco.startswith(cpf):
            print("\n  Dados inválidos ou usuário não é mesário.")
            logs.log_alerta_acesso_negado("encerramento de urna")
            return

        confirmacao = input("\n  Deseja realmente encerrar a votação? (Sim/Não): ").strip().lower()

        if confirmacao != "sim":
            print("\n  Encerramento cancelado.")
            return

        chave_confirmacao = input("  Digite sua chave de acesso novamente: ").strip()

        if chave_confirmacao != chave:
            print("\n  Chave de acesso incorreta. Encerramento não autorizado.")
            logs.log_alerta_acesso_negado("confirmação de chave no encerramento")
            return

        print("\n  Votação encerrada com sucesso!")
        logs.log_encerramento()

    except Exception as e:
        print(f"\n  Erro: {e}")
    finally:
        cursor.close()
        conn.close()


def exibir_logs():
    """
    Exibe o arquivo de log de ocorrências no terminal.

    Args:
        Nenhum.

    Returns:
        None
    """
    logs.exibir_logs()


def exibir_protocolos():
    """
    Exibe todos os protocolos de votação armazenados, descriptografando-os para exibição.

    Args:
        Nenhum.

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
    Exibe o boletim de urna com os votos de cada candidato em ordem alfabética
    e declara o vencedor da eleição.

    Args:
        Nenhum.

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
    Exibe a quantidade de eleitores que votaram e o percentual
    em relação ao total de eleitores cadastrados.

    Args:
        Nenhum.

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
    Exibe a somatória de votos recebidos por cada partido, com percentual.

    Args:
        Nenhum.

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
    Compara o total de votos registrados na urna com a quantidade de eleitores
    marcados como 'já votou' para verificar a integridade da eleição.

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