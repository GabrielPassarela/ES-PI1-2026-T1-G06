import validacao
import database
import logs
import mysql.connector
import random
import string
from datetime import datetime

def gerar_chave():
        caracteres = string.ascii_uppercase + string.digits
        return ''.join(random.choices(caracteres, k=7))


def cadastrar_eleitor():
        nome = input("Digite o nome completo do eleitor: ").strip()
        cpf = input("Digite o CPF do eleitor: ").strip()
        cpf = cpf.replace(".", "").replace("-", "")
        
        while not validacao.validacao(cpf):
            print("CPF inválido! Tente novamente.")
            cpf = input("Digite o CPF do eleitor: ").strip()
        
        mesario = input("Você é mesário? (1 - Sim, 0 - Não): ").strip()
        titulo_de_eleitor = input("Digite o número do título de eleitor: ").strip()

        while not validacao.validacao_titulo(titulo_de_eleitor):
            print("Título de eleitor inválido! Tente novamente.")
            titulo_de_eleitor = input("Digite o número do título de eleitor: ").strip()
        
        chave_acesso = gerar_chave()

        try:
            conn = database.conectar()
            cursor = conn.cursor()

            sql = """INSERT INTO ELEITORES (nome_completo, titulo_eleitor, cpf, mesário, chave_acesso)
                    VALUES (%s, %s, %s, %s, %s)"""
            valores = (nome, titulo_de_eleitor, cpf, int(mesario), chave_acesso)

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


def buscar_eleitor():
        cpf = input("Digite o CPF do eleitor a buscar: ").strip()

        try:
            conn = database.conectar()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM ELEITORES WHERE cpf = %s", (cpf,))
            eleitor = cursor.fetchone()

            if eleitor:
                print("\n  --- Eleitor encontrado ---")
                print(f"  Nome:    {eleitor['nome_completo']}")
                print(f"  CPF:     {eleitor['cpf']}")
                print(f"  Título:  {eleitor['titulo_eleitor']}")
                print(f"  Mesário: {'Sim' if eleitor['mesário'] else 'Não'}")
                print(f"  Votou:   {'Sim' if eleitor['votou'] else 'Não'}")
            else:
                print("\n  Eleitor não encontrado.")

        except Exception as e:
            print(f"\n  Erro ao buscar: {e}")
        finally:
            cursor.close()
            conn.close()


def editar_eleitor():
        print("\n  Em desenvolvimento.")

def remover_eleitor():
        print("\n  Em desenvolvimento.")

def listar_eleitores():
        conn = database.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM eleitores")
        resultados = cursor.fetchall()

        for resultado in resultados:
            print(f"\nID: {resultado[0]}")
            print(f"Nome: {resultado[1]}")
            print(f"Título: {resultado[2]}")
            print(f"CPF: {resultado[3]}")
            print(f"Mesário: {'Sim' if resultado[4] else 'Não'}")
            print(f"Votou: {'Sim' if resultado[6] else 'Não'}")
            print("--------------------------------------------------")

        cursor.close()
        conn.close()

def cadastrar_candidato():
        print("\n  Em desenvolvimento.")

def editar_candidato():
        print("\n  Em desenvolvimento.")

def remover_candidato():
        print("\n  Em desenvolvimento.")

def buscar_candidato():
        print("\n  Em desenvolvimento.")

def listar_candidatos():
        print("\n  Em desenvolvimento.")

def autenticar_mesario():
        titulo_eleitor = input("digite seu titulo de eleitor: ")
        cpf = input("digite os 4 primeiros dígitos do seu cpf: ")
        chave = input("digite a chave de acesso: ")
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM eleitores WHERE titulo_eleitor = %s AND cpf LIKE %s AND chave_acesso = %s AND mesário = 1", (titulo_eleitor, f"{cpf}%", chave))
            eleitor = cursor.fetchone()
            if eleitor:
                print("Autenticação bem-sucedida! Bem-vindo, mesário.")
                cursor.execute("DELETE FROM VOTOS")
                cursor.execute("UPDATE eleitores SET votou = 0")
                conn.commit()
                cursor.execute("SELECT * FROM CANDIDATOS")
                resultados = cursor.fetchall()
                for candidato in resultados:
                    print(f"Candidato: {candidato['nome']} - Votos: 0")
                logs.log_abertura()
            else:
                print("Dados inválidos ou usuário não é mesário.")
                logs.log_alerta_acesso_negado("abertura de urna")
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            cursor.close()
            conn.close()


def registrar_voto():
        print("\n  --------------------------------------------------")
        print("               REGISTRAR VOTO")
        print("  --------------------------------------------------")

        # Autenticar eleitor
        titulo_eleitor = input("  Digite seu título de eleitor: ").strip()
        cpf = input("  Digite os 4 primeiros dígitos do seu CPF: ").strip()
        chave = input("  Digite sua chave de acesso: ").strip()

        try:
            conn = database.conectar()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM eleitores 
                WHERE titulo_eleitor = %s 
                AND cpf LIKE %s 
                AND chave_acesso = %s 
                AND mesário = 0
            """, (titulo_eleitor, f"{cpf}%", chave))

            eleitor = cursor.fetchone()

            if not eleitor:
                print("\n  Dados inválidos ou eleitor não encontrado.")
                logs.log_alerta_acesso_negado("tentativa de voto inválida")
                return

            if eleitor['votou']:
                print("\n  Este eleitor já votou.")
                logs.log_alerta_voto_duplo()
                return

            while True:
                print("\n  --------------------------------------------------")
                numero_votacao = input("  Digite o número do candidato: ").strip()

                cursor.execute("""
                    SELECT * FROM CANDIDATOS WHERE numerodevotacao = %s
                """, (numero_votacao,))
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

                elif confirmacao in ('N', 'NAO', 'NÃO'):

                    continue
                else:
                    print("  Opção inválida. Digite S ou N.")
                    continue


            letras = ''.join(random.choices(string.ascii_uppercase, k=2))
            ano = "26"
            num_candidato = candidato['numerodevotacao'][-2:].zfill(2) if candidato else "00"
            digitos = ''.join(random.choices(string.digits, k=5))
            protocolo = f"V{letras}{ano}{num_candidato}{digitos}"


            candidato_id = candidato['id'] if candidato else None

            cursor.execute("""
                INSERT INTO VOTOS (candidato_id, data_hora, protocolo) 
                VALUES (%s, NOW(), %s)
            """, (candidato_id, protocolo))

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
    
        print("\n  --------------------------------------------------")
        print("         ENCERRAMENTO DO SISTEMA DE VOTAÇÃO")
        print("  --------------------------------------------------")
    
    
        titulo_eleitor = input("digite seu titulo de eleitor: ")
        cpf = input("digite os 4 primeiros digitos do seu cpf: ")
        chave = input("digite a chave de acesso: ")
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM eleitores WHERE titulo_eleitor = %s AND cpf LIKE %s AND chave_acesso = %s AND mesário = 1", (titulo_eleitor, f"{cpf}%", chave))
            eleitor = cursor.fetchone()
            if eleitor:
                confirmacao = input("Deseja realmente encerrar a votacao? (Sim/Nao): ")
                confirmacao2 = confirmacao.lower()
                if confirmacao2 != "sim":
                    print("Encerramento cancelado.")
                else:
                    chave_confirmacao = input("Digite sua chave de acesso novamente: ")
                    if chave_confirmacao != chave:
                        print("Chave de acesso incorreta. Encerramento nao autorizado.")
                        logs.log_alerta_acesso_negado("confirmação de chave no encerramento")
                    else:
                        print("Votacao encerrada com sucesso!")
                        logs.log_encerramento()
            else:
                print("Dados invalidos ou usuario nao e mesário.")
                logs.log_alerta_acesso_negado("encerramento de urna")
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            cursor.close()
            conn.close()

def exibir_logs():
        logs.exibir_logs()

def exibir_protocolos():
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
                    print(f"  {i:>3}. {row[0]}  |  {row[1]}")
            print("  --------------------------------------------------")
            print(f"  Total: {len(protocolos)} protocolo(s).")
            print("  --------------------------------------------------")
        except Exception as e:
            print(f"\n  Erro ao exibir protocolos: {e}")
        finally:
            cursor.close()
            conn.close()
def boletim_urna():
    print("\n  --------------------------------------------------")
    print("               BOLETIM DE URNA")
    print("  --------------------------------------------------")

    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT CANDIDATOS.nome, CANDIDATOS.numerodevotacao, CANDIDATOS.partido, COUNT(VOTOS.id) as total_votos
            FROM CANDIDATOS
            LEFT JOIN VOTOS ON VOTOS.candidato_id = CANDIDATOS.id
            GROUP BY CANDIDATOS.id, CANDIDATOS.nome, CANDIDATOS.numerodevotacao, CANDIDATOS.partido
            ORDER BY CANDIDATOS.nome ASC
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
            print(f"  Total que compareceram:           {total_votaram}")
            print(f"  Percentual de comparecimento:   {percentual:.2f}%")
            print("  --------------------------------------------------")

        except Exception as e:
            print(f"\n  Erro ao exibir comparecimento: {e}")
        finally:
            cursor.close()
            conn.close()

def votos_por_partido():
    print("\n  --------------------------------------------------")
    print("              VOTOS POR PARTIDO")
    print("  --------------------------------------------------")
 
    try:
        conn = database.conectar()
        cursor = conn.cursor(dictionary=True)
 
        cursor.execute("""
            SELECT
                c.partido,
                c.sigla_partido,
                COUNT(v.id) AS total_votos
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
 
        # Total geral de votos para calcular percentual
        total_geral = sum(p['total_votos'] for p in partidos)
 
        print(f"  {'Partido':<30} {'Sigla':<10} {'Votos':>6}  {'%':>6}")
        print(f"  {'-'*30} {'-'*10} {'-'*6}  {'-'*6}")
 
        for p in partidos:
            percentual = (p['total_votos'] / total_geral * 100) if total_geral > 0 else 0.0
            print(f"  {p['partido']:<30} {p['sigla_partido']:<10} {p['total_votos']:>6}  {percentual:>5.1f}%")
 
        print("  --------------------------------------------------")
        print(f"  Total de votos computados: {total_geral}")
        print("  --------------------------------------------------")
 
        if total_geral == 0:
            print("  Nenhum voto registrado até o momento.")
            print("  --------------------------------------------------")
 
    except Exception as e:
        print(f"\n  Erro ao exibir votos por partido: {e}")
    finally:
        cursor.close()
        conn.close()

def validacao_integridade():
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
