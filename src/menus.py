def ler_opcao():
    while True:
        try:
            return int(input("  Escolha uma opção: "))
        except ValueError:
            print("\n  [ERRO] Digite apenas números.")


def exibir_menu_principal():
    
    print("\n==================================================")
    print("       LAD.Py - Sistema de Votação Digital")
    print("==================================================")
    print("  1 - Gerenciamento")
    print("  2 - Votação")
    print("  0 - Sair")
    print("==================================================")

    opcao = ler_opcao()
    return opcao


def exibir_menu_gerenciamento():
    
    print("\n--------------------------------------------------")
    print("           MÓDULO GERENCIAMENTO")
    print("--------------------------------------------------")
    print("  1 - Eleitores")
    print("  2 - Candidatos")
    print("--------------------------------------------------")

    opcao = ler_opcao()
    return opcao


def exibir_menu_eleitores():
    
    print("\n--------------------------------------------------")
    print("                 ELEITORES")
    print("--------------------------------------------------")
    print("  1 - Cadastrar eleitor")
    print("  2 - Editar eleitor")
    print("  3 - Remover eleitor")
    print("  4 - Buscar eleitor")
    print("  5 - Listar todos os eleitores")
    print("--------------------------------------------------")

    opcao = ler_opcao()
    return opcao


def exibir_menu_candidatos():
   
    print("\n--------------------------------------------------")
    print("                CANDIDATOS")
    print("--------------------------------------------------")
    print("  1 - Cadastrar candidato")
    print("  2 - Editar candidato")
    print("  3 - Remover candidato")
    print("  4 - Buscar candidato")
    print("  5 - Listar todos os candidatos")
    print("  0 - Voltar")
    print("--------------------------------------------------")

    opcao = ler_opcao()
    return opcao


def exibir_menu_votacao():
    
    print("\n--------------------------------------------------")
    print("              MÓDULO VOTAÇÃO")
    print("--------------------------------------------------")
    print("  1 - Abrir Sistema de Votação")
    print("  2 - Auditoria")
    print("  3 - Resultados da Votação")
    print("  0 - Voltar")
    print("--------------------------------------------------")

    opcao = ler_opcao()
    return opcao


def exibir_menu_abrir_votacao():
    
    print("\n--------------------------------------------------")
    print("         ABERTURA DO SISTEMA DE VOTAÇÃO")
    print("--------------------------------------------------")
    print("  1 - Autenticar Mesário / Zerézima")
    print("  2 - Votar")
    print("  3 - Encerrar Votação")
    print("--------------------------------------------------")

    opcao = ler_opcao()
    return opcao


def exibir_menu_auditoria():
   
    print("\n--------------------------------------------------")
    print("                 AUDITORIA")
    print("--------------------------------------------------")
    print("  1 - Exibir Logs de Ocorrências")
    print("  2 - Exibir Protocolos de Votação")
    print("  0 - Voltar")
    print("--------------------------------------------------")

    opcao = ler_opcao()
    return opcao


def exibir_menu_resultados():
   
    print("\n--------------------------------------------------")
    print("            RESULTADOS DA VOTAÇÃO")
    print("--------------------------------------------------")
    print("  1 - Boletim de Urna")
    print("  2 - Estatística de Comparecimento")
    print("  3 - Votos por Partido")
    print("  4 - Validação de Integridade")
    print("  0 - Voltar")
    print("--------------------------------------------------")

    opcao = ler_opcao()
    return opcao
