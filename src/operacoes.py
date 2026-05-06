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

            # Verifica se o eleitor existe, não é mesário e ainda não votou
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
                logs.log_alerta_acesso_negado("tentativa de voto duplicado")
                return

            # Exibir candidatos disponíveis
            cursor.execute("SELECT id, nome FROM CANDIDATOS")
            candidatos = cursor.fetchall()

            if not candidatos:
                print("\n  Nenhum candidato cadastrado.")
                return

            print("\n  --- Candidatos disponíveis ---")
            for c in candidatos:
                print(f"  [{c['id']}] {c['nome']}")

            candidato_id = int(input("\n  Digite o ID do candidato: ").strip())

            # Verifica se o ID informado existe
            ids_validos = [c['id'] for c in candidatos]
            if candidato_id not in ids_validos:
                print("\n  Candidato inválido.")
                return

            # Gerar protocolo e registrar voto
            protocolo = f"PROT-{random.randint(100000, 999999)}"

            cursor.execute("""
                INSERT INTO VOTOS (candidato_id, data_hora, protocolo) 
                VALUES (%s, NOW(), %s)
            """, (candidato_id, protocolo))

            # Marcar eleitor como votou
            cursor.execute("""
                UPDATE eleitores SET votou = 1 
                WHERE titulo_eleitor = %s
            """, (titulo_eleitor,))

            conn.commit()

            print("\n  Voto registrado com sucesso!")
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
                if confirmacao != "sim":
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
        print("\n  Em desenvolvimento.")

def estatistica_comparecimento():
        print("\n  Em desenvolvimento.")

def votos_por_partido():
        print("\n  Em desenvolvimento.")

def validacao_integridade():
        print("\n  Em desenvolvimento.")