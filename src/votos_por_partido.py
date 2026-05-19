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