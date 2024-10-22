import json

# Função de login
def login():
    with open('Cesaeland_logins.json', 'r', encoding='utf-8') as f:
        logins = json.loads(f.read())  # Carregamento dos dados

    username = input("Username: ")
    password = input("Password: ")

    for LOGIN in logins:
        if LOGIN['username'] == username and LOGIN['password'] == password:
            return LOGIN['role']
    print("Username ou Password incorretos.")
    return None

# Menu do Cliente
def menu_cliente():
    while True:
        print("\nMenu do Cliente:")
        print("1. Consultar Atrações Disponíveis")
        print("2. Consultar Atrações Favoritas")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            listar_atracoes()
        elif opcao == '2':
            consultar_atracoes_favoritas()
        elif opcao == '3':
            print("A sair...")
            break
        else:
            print("Opção inválida.")

# Listar Atrações
def listar_atracoes():
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read())  # Carregamento dos dados

    print("\nAtrações Disponíveis:")
    print(f"{'ID':<5} {'Nome':<30} {'Preço Adulto':<15} {'Preço Criança':<15} {'Duração (min:seg)':<15}")
    for atracao in atracoes:
        duracao = atracao['duracaoSegundos']
        min_seg = f"{duracao // 60}:{duracao % 60:02d}"
        print(
            f"{atracao['id']:<5} {atracao['atracao']:<30} {atracao['precoAdulto']:<15} {atracao['precoCrianca']:<15} {min_seg:<15}")

# Consultar Atrações Favoritas
def consultar_atracoes_favoritas():
    # Carregar dados das vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read())

    # Carregar dados das atrações
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read())

    # Dicionários para contar bilhetes vendidos
    contagem_adultos = {}
    contagem_criancas = {}

    # Contar bilhetes vendidos
    for venda in vendas:
        atracao_id = venda['atracao']
        tipo_cliente = venda['tipoCliente']

        if tipo_cliente == 'adulto':
            contagem_adultos[atracao_id] = contagem_adultos.get(atracao_id, 0) + 1
        elif tipo_cliente == 'crianca':
            contagem_criancas[atracao_id] = contagem_criancas.get(atracao_id, 0) + 1

    # Encontrar a Atração Favorita para adultos
    atracao_adulto_id = None
    max_adultos = 0
    for ID, quantidade in contagem_adultos.items():
        if quantidade > max_adultos:
            max_adultos = quantidade
            atracao_adulto_id = ID

    # Encontrar a Atração Favorita para crianças
    atracao_crianca_id = None
    max_criancas = 0
    for ID, quantidade in contagem_criancas.items():
        if quantidade > max_criancas:
            max_criancas = quantidade
            atracao_crianca_id = ID

    # Obter nomes das atrações
    nome_atracao_adulto = ""
    nome_atracao_crianca = ""

    for atracao in atracoes:
        if atracao['id'] == atracao_adulto_id:
            nome_atracao_adulto = atracao['atracao']
        if atracao['id'] == atracao_crianca_id:
            nome_atracao_crianca = atracao['atracao']

    # Mostrar resultados
    print("\nAtrações Favoritas:")
    if nome_atracao_adulto:
        print(f"Atração mais procurada por adultos: ID: {atracao_adulto_id}, Nome: {nome_atracao_adulto} com {contagem_adultos[atracao_adulto_id]} bilhetes vendidos.")
    else:
        print("Nenhuma venda registada para adultos.")

    if nome_atracao_crianca:
        print(f"Atração mais procurada por crianças: ID: {atracao_crianca_id}, Nome: {nome_atracao_crianca} com {contagem_criancas[atracao_crianca_id]} bilhetes vendidos.")
    else:
        print("Nenhuma venda registada para crianças.")

# Menu do Engenheiro de Manutenção
def menu_engenheiro():
    while True:
        print("\nMenu do Engenheiro de Manutenção:")
        print("1. Consultar Próximas Revisões")
        print("2. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            consultar_proximas_revisoes()
        elif opcao == '2':
            print("A sair...")
            break
        else:
            print("Opção inválida.")

# Consultar Próximas Revisões
def consultar_proximas_revisoes():
    # Ler vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read())

    # Ler atrações
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read())

    # Contar bilhetes vendidos por atração
    contagem_vendas = {}
    for venda in vendas:
        atracao_id = venda['atracao']
        if atracao_id in contagem_vendas:
            contagem_vendas[atracao_id] += 1
        else:
            contagem_vendas[atracao_id] = 1

    print("\nPróximas Revisões:")
    for atracao in atracoes:
        atracao_id = atracao['id']
        bilhetes_vendidos = contagem_vendas.get(atracao_id, 0)
        faltam = 50 - (bilhetes_vendidos % 50) if bilhetes_vendidos % 50 != 0 else 0

        if faltam > 0:
            print(f"Atração ID: {atracao_id}, Nome: {atracao['atracao']}, Faltam {faltam} bilhetes para a próxima revisão.")

# Menu do Administrador
def menu_administrador():
    while True:
        print("\nMenu do Administrador:")
        print("1. Consultar Total de Vendas")
        print("2. Consultar Total de Lucro")
        print("3. Consultar Atração Mais Procurada por Adultos")
        print("4. Consultar Atração Mais Procurada por Crianças")
        print("5. Consultar Atração Mais Lucrativa")
        print("6. Consultar Atração Menos Lucrativa")
        print("7. Adicionar Novo Login")
        print("8. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            consultar_vendas()
        elif opcao == '2':
            consultar_lucro()
        elif opcao == '3':
            consultar_atracoes_favoritas()
        elif opcao == '4':
            consultar_atracoes_favoritas()
        elif opcao == '5':
            consultar_atracao_lucrativa()
        elif opcao == '6':
            consultar_atracao_lucrativa()
        elif opcao == '7':
            adicionar_novo_login()
        elif opcao == '8':
            print("A sair...")
            break
        else:
            print("Opção inválida.")

# Consultar Vendas
def consultar_vendas():
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read())

    total_vendas = len(vendas)
    print(f"\nTotal de Vendas: {total_vendas:.2f}€")

# Consultar Lucro
def consultar_lucro():
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read())

    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read())

    total_lucro = 0
    for venda in vendas:
        atracao_id = venda['atracao']
        tipo_cliente = venda['tipoCliente']

        for atracao in atracoes:
            if atracao['id'] == atracao_id:
                if tipo_cliente == 'adulto':
                    total_lucro += atracao['precoAdulto']
                elif tipo_cliente == 'crianca':
                    total_lucro += atracao['precoCrianca']

    print(f"\nTotal de Lucro: {total_lucro:.2f}€")

# Consultar Atração Mais e Menos Lucrativa
def consultar_atracao_lucrativa():
    # Carregar Vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read())

    # Carregar Atrações
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read())

    # Iniciar os lucros para cada Atração
    lucros = {}
    for atracao in atracoes:
        lucros[atracao['id']] = 0  # Começar com lucro zero

    # Calcular lucros baseados nas vendas
    for venda in vendas:
        atracao_id = venda['atracao']
        tipo_cliente = venda['tipoCliente']

        # Encontrar o preço da Atração
        for atracao in atracoes:
            if atracao['id'] == atracao_id:
                if tipo_cliente == 'adulto':
                    lucros[atracao_id] += atracao['precoAdulto']
                elif tipo_cliente == 'crianca':
                    lucros[atracao_id] += atracao['precoCrianca']
                break  # Sair do loop mal encontre o preço da Atração

    # Determinar a Atração Mais e Menos Lucrativa
    atracao_mais_lucrativa = None
    atracao_menos_lucrativa = None
    max_lucro = 0
    min_lucro = float('inf')  # Um valor inicial muito alto

    for atracao_id, lucro in lucros.items():
        if lucro > max_lucro:
            max_lucro = lucro
            atracao_mais_lucrativa = atracao_id

        # Ignorar lucros zero
        if 0 < lucro < min_lucro:
            min_lucro = lucro
            atracao_menos_lucrativa = atracao_id

    # Resultados
    print("\nAtração Mais Lucrativa:")
    if atracao_mais_lucrativa:
        print(f"Atração com o ID: {atracao_mais_lucrativa}, Lucro: {lucros[atracao_mais_lucrativa]:.2f}€")
    else:
        print("Nenhuma venda registrada.")

    print("\nAtração Menos Lucrativa:")
    if atracao_menos_lucrativa:
        print(f"Atração com o ID: {atracao_menos_lucrativa}, Lucro: {lucros[atracao_menos_lucrativa]:.2f}€")
    else:
        print("Nenhuma venda registrada.")


def adicionar_novo_login():
    # Abrir o ficheiro de logins para leitura
    with open('Cesaeland_logins.json', 'r', encoding='utf-8') as f:
        logins = json.loads(f.read())

        novo_username = input("Novo Utilizador: ")
        nova_password = input("Nova Password: ")
        tipo_acesso = input("Tipo de Acesso (ADMIN/ENG): ").strip().upper()

        # Verificar se o tipo de acesso é válido
        if not tipo_acesso in ["ADMIN", "ENG"]:
            print("Tipo de acesso inválido. Deve ser ADMIN ou ENG.")
            return

        # Verificar se o username já existe
        for LOGIN in logins:
            if LOGIN['username'] == novo_username:
                print("Este utilizador já existe. Tente outro nome de utilizador.")
                return

        # Adicionar novo login
        logins.append({
            "role": tipo_acesso,
            "username": novo_username,
            "password": nova_password
        })

        # Reescrever o arquivo
        with open('Cesaeland_logins.json', 'w', encoding='utf-8') as f:
            json.dump(logins, f, ensure_ascii=False, indent=4)

        print("Novo login adicionado com sucesso!")

# Execução do programa
while True:
    print("\nEscolha o tipo de acesso:")
    print("\n1. Administrador")
    print("2. Engenheiro de Manutenção")
    print("3. Cliente")
    print("4. Sair")

    escolha = input("\nEscolha uma opção: ")

    if escolha == '1':
        if login() == "ADMIN":
            print("Administrador.")
            # Menu do Administrador
            menu_administrador()
        else:
            print("Acesso negado.")
    elif escolha == '2':
        if login() == "ENG":
            print("Engenheiro de Manutenção.")
            # Menu do Engenheiro
            menu_engenheiro()
        else:
            print("Acesso negado.")
    elif escolha == '3':
        menu_cliente()
    elif escolha == '4':
        print("A sair...")
        break
    else:
        print("Opção inválida.")