from supabase import create_client, Client
import os
from dotenv import load_dotenv
import re

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_cpf(cpf):
    return re.match(r"^\d{11}$", cpf)

def is_valid_cnpj(cnpj):
    return re.match(r"^\d{14}$", cnpj)

def not_empty(value):
    return value is not None and value != ""

def validate():
    errors = []

    # Clientes
    clientes = supabase.table("clientes").select("*").execute().data
    cliente_ids = {c["id_cliente"] for c in clientes}
    for cliente in clientes:
        cid = cliente["id_cliente"]
        if not not_empty(cliente.get("nome")):
            errors.append(f"Cliente ID {cid} sem nome.")
        if not is_valid_cpf(cliente.get("cpf", "")):
            errors.append(f"Cliente ID {cid} com CPF inválido: {cliente.get('cpf')}")
        if not is_valid_email(cliente.get("email", "")):
            errors.append(f"Cliente ID {cid} com e-mail inválido: {cliente.get('email')}")
        if not not_empty(cliente.get("telefone")):
            errors.append(f"Cliente ID {cid} sem telefone.")
        if not not_empty(cliente.get("endereco")):
            errors.append(f"Cliente ID {cid} sem endereço.")

    # Funcionários
    funcionarios = supabase.table("funcionarios").select("*").execute().data
    funcionario_ids = {f["id_funcionario"] for f in funcionarios}
    for funcionario in funcionarios:
        fid = funcionario["id_funcionario"]
        if not not_empty(funcionario.get("nome")):
            errors.append(f"Funcionário ID {fid} sem nome.")
        if not is_valid_cpf(funcionario.get("cpf", "")):
            errors.append(f"Funcionário ID {fid} com CPF inválido: {funcionario.get('cpf')}")
        if not not_empty(funcionario.get("cargo")):
            errors.append(f"Funcionário ID {fid} sem cargo.")
        if funcionario.get("salario", 0) <= 0:
            errors.append(f"Funcionário ID {fid} com salário inválido: {funcionario.get('salario')}")

    # Fornecedores
    fornecedores = supabase.table("fornecedores").select("*").execute().data
    fornecedor_ids = {f["id_fornecedor"] for f in fornecedores}
    for fornecedor in fornecedores:
        fid = fornecedor["id_fornecedor"]
        if not not_empty(fornecedor.get("nome")):
            errors.append(f"Fornecedor ID {fid} sem nome.")
        if not is_valid_cnpj(fornecedor.get("cnpj", "")):
            errors.append(f"Fornecedor ID {fid} com CNPJ inválido: {fornecedor.get('cnpj')}")
        if not is_valid_email(fornecedor.get("email", "")):
            errors.append(f"Fornecedor ID {fid} com e-mail inválido: {fornecedor.get('email')}")
        if not not_empty(fornecedor.get("telefone")):
            errors.append(f"Fornecedor ID {fid} sem telefone.")

    # Jogos
    jogos = supabase.table("jogos").select("*").execute().data
    jogo_ids = {j["id_jogo"] for j in jogos}
    for jogo in jogos:
        jid = jogo["id_jogo"]
        if not not_empty(jogo.get("nome")):
            errors.append(f"Jogo ID {jid} sem nome.")
        if not not_empty(jogo.get("genero")):
            errors.append(f"Jogo ID {jid} sem gênero.")
        if jogo.get("preco", 0) <= 0:
            errors.append(f"Jogo ID {jid} com preço inválido: {jogo.get('preco')}")
        if jogo.get("estoque", -1) < 0:
            errors.append(f"Jogo ID {jid} com estoque negativo: {jogo.get('estoque')}")

    # Consoles
    consoles = supabase.table("consoles").select("*").execute().data
    console_ids = {c["id_console"] for c in consoles}
    for console in consoles:
        cid = console["id_console"]
        if not not_empty(console.get("nome")):
            errors.append(f"Console ID {cid} sem nome.")
        if not not_empty(console.get("fabricante")):
            errors.append(f"Console ID {cid} sem fabricante.")
        if console.get("preco", 0) <= 0:
            errors.append(f"Console ID {cid} com preço inválido: {console.get('preco')}")
        if console.get("estoque", -1) < 0:
            errors.append(f"Console ID {cid} com estoque negativo: {console.get('estoque')}")

    # Vendas
    vendas = supabase.table("vendas").select("*").execute().data
    venda_ids = {v["id_venda"] for v in vendas}
    for venda in vendas:
        vid = venda["id_venda"]
        if venda.get("id_cliente") not in cliente_ids:
            errors.append(f"Venda ID {vid} refere cliente inexistente: {venda.get('id_cliente')}")
        if venda.get("id_funcionario") not in funcionario_ids:
            errors.append(f"Venda ID {vid} refere funcionário inexistente: {venda.get('id_funcionario')}")
        if not not_empty(venda.get("data_venda")):
            errors.append(f"Venda ID {vid} sem data.")
        if venda.get("total", 0) < 0:
            errors.append(f"Venda ID {vid} com total negativo: {venda.get('total')}")

    # Fornecimento de jogos (chave composta)
    fornecimento_jogos = supabase.table("fornecimento_jogos").select("*").execute().data
    for fj in fornecimento_jogos:
        fj_key = f"{fj['id_fornecedor']}-{fj['id_jogo']}"
        if fj.get("id_fornecedor") not in fornecedor_ids:
            errors.append(f"Fornecimento_jogos ({fj_key}) refere fornecedor inexistente: {fj.get('id_fornecedor')}")
        if fj.get("id_jogo") not in jogo_ids:
            errors.append(f"Fornecimento_jogos ({fj_key}) refere jogo inexistente: {fj.get('id_jogo')}")
        if not not_empty(fj.get("data_entrada")):
            errors.append(f"Fornecimento_jogos ({fj_key}) sem data_entrada.")
        if fj.get("preco_custo", 0) <= 0:
            errors.append(f"Fornecimento_jogos ({fj_key}) com preco_custo inválido: {fj.get('preco_custo')}")

    # Fornecimento de consoles
    fornecimento_consoles = supabase.table("fornecimento_consoles").select("*").execute().data
    for fc in fornecimento_consoles:
        fc_key = f"{fc['id_fornecedor']}-{fc['id_console']}"
        if fc.get("id_fornecedor") not in fornecedor_ids:
            errors.append(f"Fornecimento_consoles ({fc_key}) refere fornecedor inexistente: {fc.get('id_fornecedor')}")
        if fc.get("id_console") not in console_ids:
            errors.append(f"Fornecimento_consoles ({fc_key}) refere console inexistente: {fc.get('id_console')}")
        if not not_empty(fc.get("data_entrada")):
            errors.append(f"Fornecimento_consoles ({fc_key}) sem data_entrada.")
        if fc.get("preco_custo", 0) <= 0:
            errors.append(f"Fornecimento_consoles ({fc_key}) com preco_custo inválido: {fc.get('preco_custo')}")

    # Itens de venda - jogos
    itens_venda_jogos = supabase.table("itens_venda_jogos").select("*").execute().data
    for ivj in itens_venda_jogos:
        ivjid = ivj["id_item"]
        if ivj.get("id_venda") not in venda_ids:
            errors.append(f"Itens_venda_jogos ID {ivjid} refere venda inexistente: {ivj.get('id_venda')}")
        if ivj.get("id_jogo") not in jogo_ids:
            errors.append(f"Itens_venda_jogos ID {ivjid} refere jogo inexistente: {ivj.get('id_jogo')}")
        if ivj.get("quantidade", 0) <= 0:
            errors.append(f"Itens_venda_jogos ID {ivjid} com quantidade inválida: {ivj.get('quantidade')}")
        if ivj.get("preco_unitario", 0) <= 0:
            errors.append(f"Itens_venda_jogos ID {ivjid} com preco_unitario inválido: {ivj.get('preco_unitario')}")

    # Itens de venda - consoles
    itens_venda_consoles = supabase.table("itens_venda_consoles").select("*").execute().data
    for ivc in itens_venda_consoles:
        ivcid = ivc["id_item"]
        if ivc.get("id_venda") not in venda_ids:
            errors.append(f"Itens_venda_consoles ID {ivcid} refere venda inexistente: {ivc.get('id_venda')}")
        if ivc.get("id_console") not in console_ids:
            errors.append(f"Itens_venda_consoles ID {ivcid} refere console inexistente: {ivc.get('id_console')}")
        if ivc.get("quantidade", 0) <= 0:
            errors.append(f"Itens_venda_consoles ID {ivcid} com quantidade inválida: {ivc.get('quantidade')}")
        if ivc.get("preco_unitario", 0) <= 0:
            errors.append(f"Itens_venda_consoles ID {ivcid} com preco_unitario inválido: {ivc.get('preco_unitario')}")

    # Resultado
    if errors:
        print("Erros encontrados:")
        for e in errors:
            print("-", e)
    else:
        print("Todos os dados estão consistentes!")

if __name__ == "__main__":
    validate()