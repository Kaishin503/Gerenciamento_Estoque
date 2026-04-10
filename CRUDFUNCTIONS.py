
def Cadastro(cursor):
    while True:
        nome = input("Digite O Nome Do Produto:")
        nome = nome.lower()
        if not nome:
            print("ERRO: É Necessário Digitar Um Nome!")
            continue
        if nome.isdigit() == True:
            print("ERRO: Nome Não Pode Ser Um Número!")
        
        resultado = cursor.execute("SELECT ProductName FROM Products WHERE ProductName = ?", (nome,))
        item = resultado.fetchone()
        if item is not None:
            print("ERRO: Produto Já Cadastrado!")
            return None
        else:
            print("SISTEMA: Nome Validado!")
            break
    while True:
        nome_categoria = input("Digite A Categoria Do Produto:")
        if not nome_categoria:
            print("ERRO: É Necessário Digitar Uma Categoria!")
            continue
        nome_categoria = nome_categoria.lower()
        resultado = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(nome_categoria,))
        chave = resultado.fetchone()
        if chave is None:
            print("ERRO: Categoria Não Encontrada!")
            return None
        else:
            valor_chave = chave[0]
            print("SISTEMA: Categoria Encontrada!")
            break 
    while True:
        try:
            preco = float(input("Digite O Preço:"))
            if not preco:
                print("ERRO: É Necessário Digitar Um Preço!")
                continue
            if preco < 0:
                print("ERRO: Preço Não Pode Ser Menor Do Que Zero!")
                continue
            if preco == 0:
                print("ERRO: Preço Não Pode Ser Zero!")
                continue
            print("SISTEMA: Preço Validado!")
            break
        except ValueError:
            print("ERRO: Digite Um Caractere Válido!")
    while True:
        try:
            quantidade = int(input("Digite A Quantidade Inicial Do Produto:"))
            if not quantidade:
                print("ERRO: É Necessário Digitar Uma Quantidade!")
                continue
            if quantidade < 0:
                print("ERRO: Quantidade Não Pode Ser Menor Que Zero!")
                continue
            if quantidade == 0:
                print("ERRO: Quantidade Inicial Não Pode Ser Zero!")
                continue
            print("SISTEMA: Quantidade Validada!")
            break
        except ValueError:
            print("ERRO: Digite Um Caractere Válido!")
    cursor.execute("INSERT INTO Products (ProductName, CategoryFK, ProductPrice, ProductQuantity) VALUES (?,?,?,?)",(nome,valor_chave,preco,quantidade))
    

def Cadastro_Categoria(cursor):
        while True:
            nome_categoria = input("Digite O Nome De Registro Da Categoria:")
            if not nome_categoria:
                print("ERRO: É Necessário Digitar Um Nome!")
                continue
            nome_categoria = nome_categoria.lower()
            resultado = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(nome_categoria,))
            nome = resultado.fetchone()
            if nome is not None:
                print("ERRO: Categoria Já Existe!")
                return None
            else:
                cursor.execute("INSERT INTO ProductCategory (CategoryName) VALUES (?)",(nome_categoria,))
                print("SISTEMA: Categoria Cadastrada!")
                break

def Listagem(cursor):
    produtos = cursor.execute("SELECT * FROM Produtos")
    resultado = produtos.fetchall()
    for item in resultado:
        id,nome,categoriaFK,preco,quantidade = item
        categoria = cursor.execute("SELECT CategoryName FROM ProductCategory WHERE CategoryPK = ?",(categoriaFK,))
    resultado_categoria = categoria.fetchone()
    for item in resultado_categoria:
        nome_categoria = item
    for item in resultado:
        id,nome,categoriaFK,preco,quantidade = item
        print("ID:{}\nNome: {}\nCategoria: {}\nChave Da Categoria: {}\nPreço: R${}\nQuantidade: {} Unidades\n".format(id,nome,nome_categoria,categoriaFK,preco,quantidade))

def Busca(cursor):
    print("Digite 1 Para Busca Por ID, 2 Para Busca Por Nome:")
    while True:
        try:
            opcao = int(input("Digite A Opção Desejada:"))
            if not opcao:
                print("ERRO: É Necessário Digitar Uma Opção!")
                continue
            if opcao not in [1,2]:
                print("ERRO: Digite Uma Opção Válida!")
                continue
            break
        except ValueError:
            print("ERRO: Digite Um Caractere Válido!")
    if opcao == 1:
        entrada = input("Digite O ID:")
        busca = cursor.execute("SELECT * FROM Products WHERE ProductPK = ?",(entrada,))
        resultado = busca.fetchall()
        for item in resultado:
            id,nome,categoriaFK,preco,quantidade = item
        categoria = cursor.execute("SELECT CategoryName FROM ProductCategory WHERE CategoryPK = ?",(categoriaFK,))
        resultado2 = categoria.fetchone()
        for item in resultado2:
            nome_categoria = item
        print("ID:{}\nNome: {}\nCategoria: {}\nChave Da Categoria: {}\nPreço: R${}\nQuantidade: {} Unidades\n".format(id,nome,nome_categoria,categoriaFK,preco,quantidade))
        return None
    elif opcao == 2:
        entrada = input("Digite O Nome:")
        busca = cursor.execute("SELECT * FROM Products WHERE ProductName = ?",(entrada,))
        resultado = busca.fetchall()
        for item in resultado:
            id,nome,categoriaFK,preco,quantidade = item
        categoria = cursor.execute("SELECT CategoryName FROM ProductCategory WHERE CategoryPK = ?",(categoriaFK,))
        resultado2 = categoria.fetchone()
        for item in resultado2:
            nome_categoria = item
        print("ID:{}\nNome: {}\nCategoria: {}\nChave Da Categoria: {}\nPreço: R${}\nQuantidade: {} Unidades\n".format(id,nome,nome_categoria,categoriaFK,preco,quantidade))
        return None
    
def Atualizar(cursor):
    while True:
        try:
            busca = int(input("Digite O ID Do Produto:"))
            if not busca:
                print("ERRO: É Necessário Digitar Um ID!")
                continue
            if busca < 1:
                print("ERRO: ID Inválido, Valor Inicial a partir de 1.")
                continue
            break
        except ValueError:
            print("ERRO: Digite Um Caractere Válido!")
    select1 = cursor.execute("SELECT * FROM Products WHERE ProductPK = ?",(busca,))
    resultado1 = select1.fetchone()
    if resultado1 is None:
        print("ERRO: Produto Não Encontrado!")
        return None
    id,nome,categoriaFK,preco,quantidade = resultado1
    select2 = cursor.execute("SELECT CategoryName FROM ProductCategory WHERE CategoryPK = ?",(categoriaFK,))
    resultado2 = select2.fetchone()
    for item in resultado2:
        nome_categoria = item
    print("Produto Selecionado:")
    print("ID:{}\nNome: {}\nCategoria: {}\nChave Da Categoria: {}\nPreço: R${}\nQuantidade: {} Unidades\n".format(id,nome,nome_categoria,categoriaFK,preco,quantidade))
    print("1 - Nome | 2 - Categoria | 3 - Preço ")
    while True:
        try:
            opcao = int(input("Digite A Opção:"))
            if not opcao:
                print("ERRO: É Necessário Digitar Uma Opção!")
                continue
            if opcao not in [1,2,3]:
                print("ERRO: Digite Uma Opção Válida!")
                continue
            break
        except ValueError:
            print("ERRO: Digite Um Caractere Válido!")
    if opcao == 1:
        while True:
            novo_nome = input("Digite O Novo Nome:")
            novo_nome = novo_nome.lower()
            if not novo_nome:
                print("ERRO: É Necessário Digitar Um Nome!")
                continue
            if novo_nome.isdigit():
                print("ERRO: Nome Não Pode Ser Um Número!")
                continue
            if novo_nome == nome:
                print("ERRO: Novo Nome Não Pode Ser O Nome Atual!")
                continue
            break
        cursor.execute("UPDATE Products SET ProductName = ? WHERE ProductPK = ?",(novo_nome,busca))
        print("Nome Atualizado Com Sucesso!")
    if opcao == 2:
        while True:
            nova_categoria = input("Digite A Nova Categoria:")
            nova_categoria = nova_categoria.lower()
            if not nova_categoria:
                print("ERRO: É Necessário Digitar Uma Categoria!")
                continue
            if nova_categoria.isdigit():
                print("ERRO: Categoria Não Pode Ser Um Número!")
                continue
            if nova_categoria == nome_categoria:
                print("ERRO: Nova Categoria Não Pode Ser A Categoria Atual!")
                continue
            break
        select3 = cursor.execute("SELECT CategoryPK FROM ProductCategory WHERE CategoryName = ?",(nova_categoria,))
        resultado3 = select3.fetchone()
        for categoriapk in resultado3:
            pass
        if resultado3 is None:
            print("ERRO: Categoria Não Existe!")
            return None
        cursor.execute("UPDATE Products SET CategoryFK = ? WHERE ProductPK = ?",(categoriapk,busca))
        print("Categoria Atualizada Com Sucesso!")
    if opcao == 3:
         while True:
            try:
                novo_preco = float(input("Digite O Novo Preço:"))
                if not novo_preco:
                    print("ERRO: É Necessário Digitar Um Preço!")
                    continue
                if novo_preco <= 0:
                    print("ERRO: Novo Nome Não Pode Ser Menor Ou Igual A Zero!")
                    continue
                if novo_preco == preco:
                    print("ERRO: Novo Preço Não Pode Ser O Mesmo Que O Atual!")
                    continue
                break
            except ValueError:
                print("ERRO: Digite Um Caractere Válido!")
            cursor.execute("UPDATE Products SET ProductPrice = ? WHERE ProductPK = ?",(novo_preco,busca))
            print("Preço Atualizado Com Sucesso!")

def Deletar(cursor):
    while True:
        try:
            busca = int(input("Digite O ID Do Produto:"))
            if not busca:
                print("ERRO: É Necessário Digitar Um ID!")
                continue
            if busca < 1: 
                print("ERRO: ID Sequencial, Valor Inicial a partir de 1.")
                continue
            break
        except:
            print("ERRO: Digite Um Caractere Válido!")
    select1 = cursor.execute("SELECT * FROM Products WHERE ProductPK = ?",(busca,))
    resultado = select1.fetchone()
    if resultado is None:
        print("ERRO: Produto Não Encontrado!")
        return None
    id,nome,categoriafk,preco,quantidade = resultado
    select2 = cursor.execute("SELECT CategoryName FROM ProductCategory WHERE CategoryPK = ?",(categoriafk,))
    resultado = select2.fetchone()
    for categoria in resultado:
        print(categoria)
    print("Produto Selecionado:")
    print("ID: {}\nNome: {}\n Categoria: {}\nChave Da Categoria: {}\nPreço: {}\nQuantidade: {}\n".format(id,nome,categoria,categoriafk,preco,quantidade))
    while True:
        confirmacao = input("Confirmar Deleção? (Y/N):")
        confirmacao = confirmacao.lower()
        if not confirmacao:
            print("ERRO: É Necessário Digitar Uma Opção!")
            continue
        if confirmacao not in ['y','n']:
            print("ERRO: Opção Inválida!")
            continue
        break
    if confirmacao == 'y':
        cursor.execute("DELETE FROM Products WHERE ProductPK = ?",(busca,))
        print("Produto Deletado Com Sucesso!")
    
