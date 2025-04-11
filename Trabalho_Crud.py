import sqlite3

conexao = sqlite3.connect('produtos.db')
cursor = conexao.cursor()

# Criação da tabela
cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL NOT NULL
    )
""")

# Criação das funções CRUD

def cadastrar_produto(nome, quantidade, preco):
    if nome == "":
        print("Você deve dar um nome ao produto")
        return

    if quantidade < 0:
        print("O produto tem que ter uma quantidade maior que zero")
        return
    
    if preco < 0:
        print("O produto deve ter um preço positivo")
        return
    try:
        cursor.execute("""
            INSERT INTO produtos (nome, quantidade, preco)
            VALUES (?, ?, ?)
        """, (nome, quantidade, preco))
        conexao.commit()
        print("Produto cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Produto já cadastrado.")
    except Exception as e:
        print(f"Erro ao cadastrar produto: {e}")

def mostrar_produtos():
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    if produtos:
        print("\nProdutos cadastrados:")
        for produto in produtos:
            print(f"ID: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[2]}, Preço: {produto[3]}")
    else:
        print("Nenhum produto cadastrado.")

def atualizar_produto(quantidade, preco, id):
    cursor.execute("""
        UPDATE produtos
        SET quantidade = ?, preco = ?
        WHERE id = ?
    """, (quantidade, preco, id))
    conexao.commit()
    if cursor.rowcount > 0:
        print("Produto atualizado com sucesso!")
    else:
        print("Erro: Produto não encontrado.")

def deletar_produto(id):
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))


# Painel de controle (Via CMD)

print("Bem-vindo ao sistema de controle de produtos!")

while True:
    print("\nEscolha uma opção:")
    print("1. Cadastrar produto")
    print("2. Mostrar produtos")
    print("3. Atualizar produto (Quantidade e Preço)")
    print("4. Deletar produto")
    print("5. Sair")

    opcao = input("\nDigite o número da opção desejada: ")

    if opcao == '1':
        nome = str(input("\nDigite o nome do produto: "))
        quantidade = int(input("Digite a quantidade do produto: "))
        preco = float(input("Digite o preço do produto: "))
        cadastrar_produto(nome, quantidade, preco)
    elif opcao == '2':
        mostrar_produtos() 
    elif opcao == '3':
        id = int(input("\nDigite o ID do produto a ser atualizado: "))
        quantidade = int(input("Digite a nova quantidade do produto: "))
        preco = float(input("Digite o novo preço do produto: "))
        atualizar_produto(quantidade, preco, id)
    elif opcao == '4':
        id = int(input("\nDigite o ID do produto a ser deletado: "))
        deletar_produto(id)
        conexao.commit()
        if cursor.rowcount > 0:
            print("\nProduto deletado com sucesso!")
        else:
            print("\nErro: Produto não encontrado.")
    elif opcao == '5':
        print("\nSaindo do sistema...")
        break


# Casos de Teste da Função Inserir

# Primeira Tentativa
#cadastrar_produto("iPhone 15", 6, 6500)

# Cadastrar Novamente
#cadastrar_produto("iPhone 15", 5, 5000)

# Cadastrar Sem Nome
#cadastrar_produto("", 5, 6000)

# Cadastrar com Quantidade Menor que Zero
#cadastrar_produto("Notebook", -1, 5000)

# Cadastrar com Preço Menor que Zero
#cadastrar_produto("Tablet", 2, -2)
