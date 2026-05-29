
import menus

import operacoes

opc_principal = -1

while opc_principal != 0:
  

    opc_principal = menus.exibir_menu_principal()
    

   
    match opc_principal: 

        case 1:  # Gerenciamento
            opc_gerenciamento = -1

            while opc_gerenciamento != 0:

                opc_gerenciamento = menus.exibir_menu_gerenciamento()

                match opc_gerenciamento:

                    case 1:  # Eleitores
                        opc_eleitores = -1

                        while opc_eleitores != 0:

                            opc_eleitores = menus.exibir_menu_eleitores()

                            match opc_eleitores:
                                case 1:
                                    operacoes.cadastrar_eleitor()
                                case 2:
                                    operacoes.editar_eleitor()
                                case 3:
                                    operacoes.remover_eleitor()
                                case 4:
                                    operacoes.buscar_eleitor()
                                case 5:
                                    operacoes.listar_eleitores()
                                case 0:
                                    pass
                                case _:
                                    print("\n  [ERRO] Opção inválida.")

                    case 2:  # Candidatos
                        opc_candidatos = -1

                        while opc_candidatos != 0:

                            opc_candidatos = menus.exibir_menu_candidatos()

                            match opc_candidatos:
                                case 1:
                                    operacoes.cadastrar_candidato()
                                case 2:
                                    operacoes.editar_candidato()
                                case 3:
                                    operacoes.remover_candidato()
                                case 4:
                                    operacoes.buscar_candidato()
                                case 5:
                                    operacoes.listar_candidatos()
                                case 0:
                                    pass
                                case _:
                                    print("\n  [ERRO] Opção inválida.")

                    case 0:
                        pass
                    case _:
                        print("\n  [ERRO] Opção inválida.")

        case 2:  # Votação
            opc_votacao = -1

            while opc_votacao != 0:

                opc_votacao = menus.exibir_menu_votacao()

                match opc_votacao:

                    case 1:  # Abrir Votação
                        if not operacoes.verificar_mesario_para_abrir_votacao():
                            continue

                        while True:

                            opc_abrir = menus.exibir_menu_abrir_votacao()

                            match opc_abrir:
                                case 1:
                                    operacoes.autenticar_mesario()
                                case 2:
                                    operacoes.registrar_voto()
                                case 3:
                                    if operacoes.encerrar_votacao():
                                        break
                                case _:
                                    print("\n  [ERRO] Opção inválida.")

                    case 2:  # Auditoria
                        opc_auditoria = -1

                        while opc_auditoria != 0:

                            opc_auditoria = menus.exibir_menu_auditoria()

                            match opc_auditoria:
                                case 1:
                                    operacoes.exibir_logs()
                                case 2:
                                    operacoes.exibir_protocolos()
                                case 0:
                                    pass
                                case _:
                                    print("\n  [ERRO] Opção inválida.")

                    case 3:  # Resultados
                        opc_resultados = -1

                        while opc_resultados != 0:

                            opc_resultados = menus.exibir_menu_resultados()

                            match opc_resultados:
                                case 1:
                                    operacoes.boletim_urna()
                                case 2:
                                    operacoes.estatistica_comparecimento()
                                case 3:
                                    operacoes.votos_por_partido()
                                case 4:
                                    operacoes.validacao_integridade()
                                case 0:
                                    pass
                                case _:
                                    print("\n  [ERRO] Opção inválida.")

                    case 0:
                        pass
                    case _:
                        print("\n  [ERRO] Opção inválida.")

        case 0:
            print("\n  Encerrando o sistema.\n")

        case _:
            print("\n  [ERRO] Opção inválida.")
