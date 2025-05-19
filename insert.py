from supabase import create_client, Client
import os
from dotenv import load_dotenv
import random

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Inserção de clientes
clientes = [
    {"nome": "João Silva", "cpf": "12345678901", "email": "joao@gmail.com", "telefone": "11999990001", "endereco": "Rua A, 100"},
    {"nome": "Maria Souza", "cpf": "23456789012", "email": "maria@gmail.com", "telefone": "11999990002", "endereco": "Rua B, 200"},
    {"nome": "Carlos Lima", "cpf": "34567890123", "email": "carlos@gmail.com", "telefone": "11999990003", "endereco": "Rua C, 300"},
    {"nome": "Ana Pereira", "cpf": "45678901234", "email": "ana@gmail.com", "telefone": "11999990004", "endereco": "Rua D, 400"},
    {"nome": "Lucas Alves", "cpf": "56789012345", "email": "lucas@gmail.com", "telefone": "11999990005", "endereco": "Rua E, 500"},
]

for cliente in clientes:
    supabase.table("clientes").insert(cliente).execute()

# Funcionários
funcionarios = [
    {"nome": "Fernanda Costa", "cpf": "98765432100", "cargo": "Atendente", "salario": 2500.00},
    {"nome": "Ricardo Martins", "cpf": "87654321099", "cargo": "Gerente", "salario": 4500.00},
    {"nome": "Patrícia Rocha", "cpf": "76543210988", "cargo": "Caixa", "salario": 2300.00},
    {"nome": "Mariana Borges", "cpf": "65432109877", "cargo": "Estoquista", "salario": 2700.00},
    {"nome": "Eduardo Vasconcelos", "cpf": "54321098766", "cargo": "Vendedor", "salario": 2800.00},
]

for funcionario in funcionarios:
    supabase.table("funcionarios").insert(funcionario).execute()

# Fornecedores
fornecedores = [
    {"nome": "GameDistribuidora", "cnpj": "11222333000199", "telefone": "1144440001", "email": "contato@gamedist.com"},
    {"nome": "TechForGames", "cnpj": "22333444000188", "telefone": "1144440002", "email": "vendas@techforgames.com"},
    {"nome": "MegaConsoles", "cnpj": "33444555000177", "telefone": "1144440003", "email": "suporte@megaconsoles.com"}
]

for fornecedor in fornecedores:
    supabase.table("fornecedores").insert(fornecedor).execute()

# Jogos
jogos = [
    {"nome": "God of War Ragnarok", "genero": "Ação", "preco": 199.90, "estoque": 20},
    {"nome": "FIFA 23", "genero": "Esporte", "preco": 249.90, "estoque": 15},
    {"nome": "The Last of Us Part II", "genero": "Aventura", "preco": 159.90, "estoque": 10},
    {"nome": "Horizon Forbidden West", "genero": "RPG", "preco": 229.90, "estoque": 12},
    {"nome": "Spider-Man Miles Morales", "genero": "Ação", "preco": 179.90, "estoque": 8},
    {"nome": "Elden Ring", "genero": "RPG", "preco": 299.90, "estoque": 9},
    {"nome": "Gran Turismo 7", "genero": "Corrida", "preco": 259.90, "estoque": 11},
    {"nome": "NBA 2K23", "genero": "Esporte", "preco": 219.90, "estoque": 7}
]

for jogo in jogos:
    supabase.table("jogos").insert(jogo).execute()

# Consoles
consoles = [
    {"nome": "PlayStation 5", "fabricante": "Sony", "preco": 3999.90, "estoque": 5},
    {"nome": "Xbox Series X", "fabricante": "Microsoft", "preco": 3899.90, "estoque": 7},
    {"nome": "Nintendo Switch", "fabricante": "Nintendo", "preco": 2999.90, "estoque": 6},
    {"nome": "PlayStation 4", "fabricante": "Sony", "preco": 1999.90, "estoque": 4},
    {"nome": "Xbox Series S", "fabricante": "Microsoft", "preco": 2799.90, "estoque": 5},
    {"nome": "Nintendo Switch OLED", "fabricante": "Nintendo", "preco": 3299.90, "estoque": 4}
]

for console in consoles:
    supabase.table("consoles").insert(console).execute()

# Inserção de vendas
vendas = [
    {"data_venda": "2025-05-01", "id_cliente": 1, "id_funcionario": 1, "total": 4199.80},
    {"data_venda": "2025-05-02", "id_cliente": 2, "id_funcionario": 2, "total": 229.90},
    {"data_venda": "2025-05-03", "id_cliente": 3, "id_funcionario": 1, "total": 199.90},
    {"data_venda": "2025-05-04", "id_cliente": 4, "id_funcionario": 3, "total": 5899.80},
    {"data_venda": "2025-05-05", "id_cliente": 5, "id_funcionario": 2, "total": 159.90},
    {"data_venda": "2025-05-06", "id_cliente": 1, "id_funcionario": 3, "total": 299.90},
    {"data_venda": "2025-05-07", "id_cliente": 2, "id_funcionario": 4, "total": 2999.90}
]

for venda in vendas:
    supabase.table("vendas").insert(venda).execute()

# Fornecimento de jogos
for id_fornecedor in range(1, 4):
    for id_jogo in range(1, 9):
        fornecimento = {
            "id_fornecedor": id_fornecedor,
            "id_jogo": id_jogo,
            "data_entrada": f"2025-04-{random.randint(1,28):02}",
            "preco_custo": round(random.uniform(120, 200), 2)
        }
        supabase.table("fornecimento_jogos").insert(fornecimento).execute()

# Fornecimento de consoles
for id_fornecedor in range(1, 4):
    for id_console in range(1, 7):
        fornecimento = {
            "id_fornecedor": id_fornecedor,
            "id_console": id_console,
            "data_entrada": f"2025-04-{random.randint(1,28):02}",
            "preco_custo": round(random.uniform(1800, 3500), 2)
        }
        supabase.table("fornecimento_consoles").insert(fornecimento).execute()

# Itens de venda - jogos
for id_venda in range(1, 8):
    item = {
        "id_venda": id_venda,   
        "id_jogo": random.randint(1, 8),
        "quantidade": random.randint(1, 3),
        "preco_unitario": round(random.choice([199.90, 249.90, 159.90, 229.90, 179.90, 299.90, 259.90, 219.90]), 2)
    }
    supabase.table("itens_venda_jogos").insert(item).execute()

# Itens de venda - consoles
for id_venda in range(1, 8):
    item = {
        "id_venda": id_venda,
        "id_console": random.randint(1, 6),
        "quantidade": 1,
        "preco_unitario": round(random.choice([3999.90, 3899.90, 2999.90, 1999.90, 2799.90, 3299.90]), 2)
    }
    supabase.table("itens_venda_consoles").insert(item).execute()
