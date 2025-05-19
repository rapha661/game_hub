-- TABELA DE CLIENTES
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    endereco TEXT
);

-- TABELA DE FUNCIONÁRIOS
CREATE TABLE funcionarios (
    id_funcionario SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    cargo VARCHAR(50),
    salario NUMERIC(10,2)
);

-- TABELA DE FORNECEDORES
CREATE TABLE fornecedores (
    id_fornecedor SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cnpj VARCHAR(14) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100)
);

-- TABELA DE JOGOS
CREATE TABLE jogos (
    id_jogo SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    genero VARCHAR(50),
    preco NUMERIC(10,2),
    estoque INT DEFAULT 0
);

-- TABELA DE CONSOLES
CREATE TABLE consoles (
    id_console SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    fabricante VARCHAR(50),
    preco NUMERIC(10,2),
    estoque INT DEFAULT 0
);

-- TABELA DE RELACIONAMENTO FORNECEDOR - JOGOS
CREATE TABLE fornecimento_jogos (
    id_fornecedor INT REFERENCES fornecedores(id_fornecedor),
    id_jogo INT REFERENCES jogos(id_jogo),
    data_entrada DATE NOT NULL,
    preco_custo NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (id_fornecedor, id_jogo)
);

-- TABELA DE RELACIONAMENTO FORNECEDOR - CONSOLES
CREATE TABLE fornecimento_consoles (
    id_fornecedor INT REFERENCES fornecedores(id_fornecedor),
    id_console INT REFERENCES consoles(id_console),
    data_entrada DATE NOT NULL,
    preco_custo NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (id_fornecedor, id_console)
);

-- TABELA DE VENDAS
CREATE TABLE vendas (
    id_venda SERIAL PRIMARY KEY,
    data_venda DATE NOT NULL,
    id_cliente INT REFERENCES clientes(id_cliente),
    id_funcionario INT REFERENCES funcionarios(id_funcionario),
    total NUMERIC(10,2)
);

-- TABELA DE ITENS DE VENDA - JOGOS
CREATE TABLE itens_venda_jogos (
    id_item SERIAL PRIMARY KEY,
    id_venda INT REFERENCES vendas(id_venda),
    id_jogo INT REFERENCES jogos(id_jogo),
    quantidade INT NOT NULL,
    preco_unitario NUMERIC(10,2) NOT NULL
);

-- TABELA DE ITENS DE VENDA - CONSOLES
CREATE TABLE itens_venda_consoles (
    id_item SERIAL PRIMARY KEY,
    id_venda INT REFERENCES vendas(id_venda),
    id_console INT REFERENCES consoles(id_console),
    quantidade INT NOT NULL,
    preco_unitario NUMERIC(10,2) NOT NULL
);
