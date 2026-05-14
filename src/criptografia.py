import numpy as np
import random
import string

CHAVE = np.array([[3, 3],
                  [2, 5]])

MOD = 26


def texto_para_numeros(texto):
    texto = texto.upper().replace(" ", "")
    return [ord(c) - ord('A') for c in texto if c.isalpha()]


def numeros_para_texto(numeros):
    return ''.join([chr(int(n) + ord('A')) for n in numeros])


def ajustar_texto(texto):
    texto = texto.upper().replace(" ", "")
    texto = ''.join(c for c in texto if c.isalpha())
    if len(texto) % 2 != 0:
        texto += 'X'
    return texto


def numero_para_letra(texto):
    return ''.join([chr(int(d) + 65) for d in texto if d.isdigit()])


def letra_para_numero(texto):
    return ''.join([str(ord(c) - 65) for c in texto.upper() if c.isalpha()])


def inversa_modular_matriz(matriz):
    det = int(np.round(np.linalg.det(matriz)))
    det_mod = det % MOD

    for i in range(1, MOD):
        if (det_mod * i) % MOD == 1:
            det_inv = i
            break

    adj = np.array([[matriz[1][1], -matriz[0][1]],
                    [-matriz[1][0],  matriz[0][0]]])

    return (det_inv * adj) % MOD


def criptografar_hill(texto):
    texto = ajustar_texto(texto)
    numeros = texto_para_numeros(texto)
    resultado = []

    for i in range(0, len(numeros), 2):
        bloco = np.array([[numeros[i]],
                          [numeros[i + 1]]])
        criptografado = np.dot(CHAVE, bloco) % MOD
        resultado.extend(criptografado.flatten().astype(int).tolist())

    return numeros_para_texto(resultado)


def descriptografar_hill(texto):
    numeros = texto_para_numeros(texto)
    chave_inv = inversa_modular_matriz(CHAVE)
    resultado = []

    for i in range(0, len(numeros), 2):
        bloco = np.array([[numeros[i]],
                          [numeros[i + 1]]])
        descriptografado = np.dot(chave_inv, bloco) % MOD
        resultado.extend(descriptografado.flatten().astype(int).tolist())

    return numeros_para_texto(resultado)


# CPF
# Antes da criptografia: 12345678901
# Depois da criptografia: resultado da Cifra de Hill

def criptografar_cpf(cpf):
    cpf_letras = numero_para_letra(cpf)
    return criptografar_hill(cpf_letras)


def descriptografar_cpf(cpf_criptografado):
    cpf_letras = descriptografar_hill(cpf_criptografado)
    return letra_para_numero(cpf_letras)


# Chave de Acesso
# Padrão: 2 primeiras letras do primeiro nome + 1ª letra do segundo nome + 4 dígitos aleatórios
# Exemplo original (Eleitor: André Silva): ANS4821
# Exemplo armazenado (criptografado): resultado da Cifra de Hill

def gerar_chave_acesso(nome_completo):
    partes = nome_completo.strip().upper().split()
    letra1 = partes[0][0]
    letra2 = partes[0][1]
    letra3 = partes[1][0] if len(partes) > 1 else 'X'
    digitos = ''.join(random.choices(string.digits, k=4))
    return letra1 + letra2 + letra3 + digitos


def criptografar_chave_acesso(chave):
    parte_letras = ''.join(c for c in chave if c.isalpha())
    parte_digitos = ''.join(c for c in chave if c.isdigit())
    parte_digitos_em_letras = numero_para_letra(parte_digitos)
    texto = parte_letras + parte_digitos_em_letras
    return criptografar_hill(texto)


def descriptografar_chave_acesso(chave_criptografada):
    return descriptografar_hill(chave_criptografada)


# Protocolo de Votação
# Padrão: "V" + 2 letras aleatórias + Ano (26) + Número do candidato (2 dígitos) + 5 dígitos aleatórios
# Exemplo original (voto no candidato 99): VRT269950134
# Exemplo armazenado (criptografado): resultado da Cifra de Hill

def gerar_protocolo(numero_candidato):
    letras = ''.join(random.choices(string.ascii_uppercase, k=2))
    digitos = ''.join(random.choices(string.digits, k=5))
    return f"V{letras}26{numero_candidato:02d}{digitos}"


def criptografar_protocolo(protocolo):
    parte_letras = ''.join(c for c in protocolo if c.isalpha())
    parte_digitos = ''.join(c for c in protocolo if c.isdigit())
    parte_digitos_em_letras = numero_para_letra(parte_digitos)
    texto = parte_letras + parte_digitos_em_letras
    return criptografar_hill(texto)


def descriptografar_protocolo(protocolo_criptografado):
    return descriptografar_hill(protocolo_criptografado)


if __name__ == "__main__":
    print("\n==================================================")
    print("       LAD.Py - Sistema de Votacao Digital")
    print("       Demonstracao de Criptografia - Cifra de Hill")
    print("==================================================")

    # CPF
    cpf = "12345678901"
    cpf_cripto = criptografar_cpf(cpf)
    cpf_recuperado = descriptografar_cpf(cpf_cripto)
    print(f"\n  CPF original     : {cpf}")
    print(f"  CPF criptografado: {cpf_cripto}")
    print(f"  CPF recuperado   : {cpf_recuperado[:11]}")

    # Chave de Acesso
    nome = "Andre Silva"
    chave = gerar_chave_acesso(nome)
    chave_cripto = criptografar_chave_acesso(chave)
    print(f"\n  Eleitor          : {nome}")
    print(f"  Chave original   : {chave}")
    print(f"  Chave criptograf.: {chave_cripto}")

    # Protocolo
    protocolo = gerar_protocolo(99)
    protocolo_cripto = criptografar_protocolo(protocolo)
    print(f"\n  Protocolo original   : {protocolo}")
    print(f"  Protocolo criptograf.: {protocolo_cripto}")

    print("\n==================================================\n")