import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 1. Jogos mais vendidos
def query_1_jogos_mais_vendidos():
    itens = supabase.table("itens_venda_jogos").select("id_jogo, quantidade").execute().data
    jogos = supabase.table("jogos").select("id_jogo, nome").execute().data
    vendas = {}
    for item in itens:
        vendas[item["id_jogo"]] = vendas.get(item["id_jogo"], 0) + item["quantidade"]
    jogos_vendidos = [
        {"nome": next(j["nome"] for j in jogos if j["id_jogo"] == jid), "total_vendido": total}
        for jid, total in vendas.items()
    ]
    return sorted(jogos_vendidos, key=lambda x: x["total_vendido"], reverse=True)[:5]

# 2. Consoles mais vendidos
def query_2_consoles_mais_vendidos():
    itens = supabase.table("itens_venda_consoles").select("id_console, quantidade").execute().data
    consoles = supabase.table("consoles").select("id_console, nome").execute().data
    vendas = {}
    for item in itens:
        vendas[item["id_console"]] = vendas.get(item["id_console"], 0) + item["quantidade"]
    consoles_vendidos = [
        {"nome": next(c["nome"] for c in consoles if c["id_console"] == cid), "total_vendido": total}
        for cid, total in vendas.items()
    ]
    return sorted(consoles_vendidos, key=lambda x: x["total_vendido"], reverse=True)[:5]

# 3. Clientes que mais compraram
def query_3_clientes_top():
    vendas = supabase.table("vendas").select("id_cliente, total").execute().data
    clientes = supabase.table("clientes").select("id_cliente, nome").execute().data
    gastos = {}
    for v in vendas:
        gastos[v["id_cliente"]] = gastos.get(v["id_cliente"], 0) + (v["total"] or 0)
    clientes_gastos = [
        {"nome": next(c["nome"] for c in clientes if c["id_cliente"] == cid), "total_gasto": total}
        for cid, total in gastos.items()
    ]
    return sorted(clientes_gastos, key=lambda x: x["total_gasto"], reverse=True)[:5]

# 4. Funcionários que mais venderam
def query_4_funcionarios_top():
    vendas = supabase.table("vendas").select("id_funcionario, total").execute().data
    funcionarios = supabase.table("funcionarios").select("id_funcionario, nome").execute().data
    totais = {}
    for v in vendas:
        totais[v["id_funcionario"]] = totais.get(v["id_funcionario"], 0) + (v["total"] or 0)
    funcionarios_vendas = [
        {"nome": next(f["nome"] for f in funcionarios if f["id_funcionario"] == fid), "total_vendas": total}
        for fid, total in totais.items()
    ]
    return sorted(funcionarios_vendas, key=lambda x: x["total_vendas"], reverse=True)[:5]

# 5. Jogos nunca vendidos
def query_5_jogos_nunca_vendidos():
    jogos = supabase.table("jogos").select("id_jogo, nome").execute().data
    itens = supabase.table("itens_venda_jogos").select("id_jogo").execute().data
    vendidos = set(item["id_jogo"] for item in itens)
    return [{"nome": j["nome"]} for j in jogos if j["id_jogo"] not in vendidos]

# 6. Consoles nunca vendidos
def query_6_consoles_nunca_vendidos():
    consoles = supabase.table("consoles").select("id_console, nome").execute().data
    itens = supabase.table("itens_venda_consoles").select("id_console").execute().data
    vendidos = set(item["id_console"] for item in itens)
    return [{"nome": c["nome"]} for c in consoles if c["id_console"] not in vendidos]

# 7. Fornecedores que mais forneceram jogos
def query_7_fornecedores_top_jogos():
    fornecimentos = supabase.table("fornecimento_jogos").select("id_fornecedor").execute().data
    fornecedores = supabase.table("fornecedores").select("id_fornecedor, nome").execute().data
    contagem = {}
    for f in fornecimentos:
        contagem[f["id_fornecedor"]] = contagem.get(f["id_fornecedor"], 0) + 1
    fornecedores_top = [
        {"nome": next(forn["nome"] for forn in fornecedores if forn["id_fornecedor"] == fid), "fornecimentos": total}
        for fid, total in contagem.items()
    ]
    return sorted(fornecedores_top, key=lambda x: x["fornecimentos"], reverse=True)[:3]

# 8. Maior venda já realizada
def query_8_maior_venda():
    vendas = supabase.table("vendas").select("id_venda, total, data_venda, id_cliente").execute().data
    clientes = supabase.table("clientes").select("id_cliente, nome").execute().data
    if not vendas:
        return []
    maior = max(vendas, key=lambda v: v["total"] or 0)
    cliente_nome = next((c["nome"] for c in clientes if c["id_cliente"] == maior["id_cliente"]), "Desconhecido")
    return [{
        "id_venda": maior["id_venda"],
        "cliente": cliente_nome,
        "data_venda": maior["data_venda"],
        "total": maior["total"]
    }]

# 9. Jogos por gênero
def query_9_jogos_por_genero():
    jogos = supabase.table("jogos").select("genero").execute().data
    from collections import Counter
    contagem = Counter(j["genero"] for j in jogos if j["genero"])
    return [{"genero": genero, "quantidade": qtd} for genero, qtd in contagem.most_common()]

# 10. Clientes que compraram mais de um console
def query_10_clientes_multiplos_consoles():
    vendas = supabase.table("vendas").select("id_venda, id_cliente").execute().data
    itens = supabase.table("itens_venda_consoles").select("id_venda, id_console").execute().data
    clientes = supabase.table("clientes").select("id_cliente, nome").execute().data
    from collections import defaultdict
    cliente_consoles = defaultdict(set)
    venda_cliente = {v["id_venda"]: v["id_cliente"] for v in vendas}
    for item in itens:
        id_cliente = venda_cliente.get(item["id_venda"])
        if id_cliente:
            cliente_consoles[id_cliente].add(item["id_console"])
    result = []
    for cid, consoles in cliente_consoles.items():
        if len(consoles) > 1:
            nome = next(c["nome"] for c in clientes if c["id_cliente"] == cid)
            result.append({"nome": nome, "consoles_comprados": len(consoles)})
    return sorted(result, key=lambda x: x["consoles_comprados"], reverse=True)

def main():
    queries = [
        ("1. Jogos mais vendidos", query_1_jogos_mais_vendidos()),
        ("2. Consoles mais vendidos", query_2_consoles_mais_vendidos()),
        ("3. Clientes que mais compraram", query_3_clientes_top()),
        ("4. Funcionários que mais venderam", query_4_funcionarios_top()),
        ("5. Jogos nunca vendidos", query_5_jogos_nunca_vendidos()),
        ("6. Consoles nunca vendidos", query_6_consoles_nunca_vendidos()),
        ("7. Fornecedores que mais forneceram jogos", query_7_fornecedores_top_jogos()),
        ("8. Maior venda já realizada", query_8_maior_venda()),
        ("9. Jogos por gênero", query_9_jogos_por_genero()),
        ("10. Clientes que compraram mais de um console", query_10_clientes_multiplos_consoles()),
    ]
    for title, data in queries:
        print(f"\n==== {title} ====")
        if data:
            for row in data:
                print(row)
        else:
            print("Nenhum resultado.")

if __name__ == "__main__":
    main()