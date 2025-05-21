# Game Hub

## Integrantes do Grupo

- **Raphael Garavati Erbert** – RA: *[22.123.014-7]*
- **Nathan Gabriel da Fonseca Leite** – RA: *[22.123.028-7]*
- **Ana Carolina Lazzuri** – RA: *[22.123.001-4]*

---

## Descrição do Projeto

O Game Hub é um projeto desenvolvido para centralizar e gerenciar informações sobre jogos, usuários e interações dentro de uma plataforma de games. O sistema permite cadastrar jogos, registrar usuários, acompanhar estatísticas de uso e criar uma infraestrutura básica para uma comunidade gamer.

As principais funcionalidades do sistema incluem:

- Cadastro e consulta de jogos
- Registro de usuários e seus perfis
- Avaliação e comentários de jogos
- Gerenciamento de conquistas e estatísticas dos jogadores
- Integração com plataformas externas (opcional)

O banco de dados foi modelado com base em requisitos realistas e implementado utilizando PostgreSQL.

---

## Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/rapha661/game_hub
cd game_hub
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` com o seguinte conteúdo:
```
SUPABASE_URL = "SEU LINK DO SUPABASE"
SUPABASE_KEY = "SUA CHAVE DO SUPABASE"
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute os scripts do projeto

#### Crie as tabelas no banco de dados

Execute o script DDL do projeto para criar as tabelas necessárias. 

#### Popule o banco de dados com dados de exemplo

```bash
python insert.py
```

#### Verifique a consistência dos dados inseridos

```bash
python validate.py
```

#### Execute as queries de teste

```bash
python test_query.py
```

> Os arquivos estão organizados da seguinte forma:
> - `create_table.sql`: script de criação das tabelas
> - `insert.py`: insere dados fictícios nas tabelas
> - `validate.py`: realiza verificações de consistência no banco
> - `test_query.py`: executa queries de teste e exemplos

---

## Modelo Relacional (MR)

![MR](https://github.com/user-attachments/assets/969fbce2-2c04-4355-b068-d3d5ac8c290d)

---

## Modelo Entidade-Relacionamento (MER)

![image](https://github.com/user-attachments/assets/bb665254-fd37-45a1-b142-cede1b214bd6)

