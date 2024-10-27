import json


# Função de login
def login():
    # Carregar dados dos logins
    with open('Cesaeland_logins.json', 'r', encoding='utf-8') as f:
        logins = json.loads(f.read())  # Carregamento dos dados

    username = input("Username: ")
    password = input("Password: ")

    for log in logins:
        if log['username'] == username and log['password'] == password:
            return log['role']
    print("Username ou Password incorretos.")
    return None

# Menu Cliente
def menu_cliente():
    while True:
        print("\nMenu do Cliente:")
        print("1. Consultar Atrações Disponíveis")
        print("2. Consultar Atrações Favoritas")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case '1':
                consultar_atracoes_disponiveis()
            case '2':
                consultar_atracoes_favoritas()
            case '3':
                print("A sair...")
                break
            case _:
                print("Opção inválida.")

# Consultar Atrações Disponíveis
def consultar_atracoes_disponiveis():
    # Carregar dados das atrações
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read())  # Carregamento dos dados

    # Tabela
    print("\nAtrações Disponíveis:")
    print(f"{'ID':<3} {'Nome':<33} {'Preço Adulto':<15} {'Preço Criança':<15} {'Duração(min:seg)':<15}")
    for atracao in atracoes:
        duracao = atracao['duracaoSegundos']
        min_seg = f"{duracao // 60}:{duracao % 60:02d}"
        print(f"{atracao['id']:<3} {atracao['atracao']:<33} €{atracao['precoAdulto']:<14} €{atracao['precoCrianca']:<14} {min_seg:<15}")

# Consultar Atrações Favoritas
def consultar_atracoes_favoritas():
    # Carregar dados das vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read()) # Carregamento dos dados

    # Carregar dados das atrações
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read()) # Carregamento dos dados

    # Dicionários para contar bilhetes vendidos
    contagem_adultos = {}
    contagem_criancas = {}

    # Contar bilhetes vendidos
    for venda in vendas:
        if 'atracao' in venda and 'tipoCliente' in venda:
            atracao_id = venda['atracao']
            tipo_cliente = venda['tipoCliente']

            if tipo_cliente == 'adulto':
                if atracao_id in contagem_adultos:
                    contagem_adultos[atracao_id] += 1
                else:
                    contagem_adultos[atracao_id] = 1

            elif tipo_cliente == 'crianca':
                if atracao_id in contagem_criancas:
                    contagem_criancas[atracao_id] += 1
                else:
                    contagem_criancas[atracao_id] = 1

    # Encontrar a Atração Favorita para os Adultos
    atracao_adulto_id = None
    max_adultos = 0
    for ID, quantidade in contagem_adultos.items():
        if quantidade > max_adultos:
            max_adultos = quantidade
            atracao_adulto_id = ID

    # Encontrar a Atração Favorita para as Crianças
    atracao_crianca_id = None
    max_criancas = 0

    for atracao_id in contagem_criancas:  # Itera sobre as chaves do dicionário
        quantidade = contagem_criancas[atracao_id]
        if quantidade > max_criancas:
            max_criancas = quantidade
            atracao_crianca_id = atracao_id

    # Adquirir nomes das atrações
    nome_atracao_adulto = []
    nome_atracao_crianca = []

    for atracao in atracoes:
        if atracao['id'] == atracao_adulto_id:
            nome_atracao_adulto = atracao['atracao']
        elif atracao['id'] == atracao_crianca_id:
            nome_atracao_crianca = atracao['atracao']

    # Mostrar resultados
    if atracao_adulto_id:
        print(
            f"\nAtração mais procurada por Adultos: ID {atracao_adulto_id}, Nome: {nome_atracao_adulto} com {max_adultos} bilhetes vendidos.")
    else:
        print("Nenhuma venda registada para Adultos.")

    if atracao_crianca_id:
        print(
            f"\nAtração mais procurada por Crianças: ID {atracao_crianca_id}, Nome: {nome_atracao_crianca} com {max_criancas} bilhetes vendidos.")
    else:
        print("Nenhuma venda registada para Crianças.")

# Menu Bilheteira
def menu_bilheteira():
    while True:
        print("\nMenu Bilheteira:")
        print("1. Adicionar nova venda")
        print("2. Sair")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case '1':
                adicionar_nova_venda()
            case '2':
                print("A sair...")
                break
            case _:
                print("Opção inválida.")

def validar_data(data, ultima_data):
    # Verificar se a nova data é posterior à última data registada
    if data >= ultima_data:
        return True
    else:
        return False

def adicionar_nova_venda():
    # Carregar dados das vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read()) # Carregamento dos dados

    # Carregar dados das atrações
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read()) # Carregamento dos dados

    # Última data registrada
    ultima_data = "00-0000"  # Valor inicial
    for venda in vendas:
        if venda['data'] > ultima_data:
            ultima_data = venda['data']

    # Perguntar qual a atração
    atracao_id = int(input("Digite o ID da atração: "))
    if not any(atracao['id'] == atracao_id for atracao in atracoes):
        print("Atração não encontrada.")
        return

    # Perguntar qual a data
    data_venda = input("Digite a data da venda (MM-AAAA): ")
    if not validar_data(data_venda, ultima_data):
        print("Data inválida. Deve ser igual ou posterior à última venda.")
        return

    # Perguntar qual a categoria
    categoria = input("Digite a categoria do cliente (criança/adulto): ").strip().lower()
    if categoria not in ['criança', 'adulto']:
        print("Categoria inválida. Deve ser 'criança' ou 'adulto'.")
        return

    # Adicionar nova venda
    nova_venda = {
        "atracao": atracao_id,
        "data": data_venda,
        "categoria": categoria
    }
    vendas.append(nova_venda)

    # Guardar dados das novas vendas
    with open('Cesaeland_vendas.json', 'w', encoding='utf-8') as f:
        json.dump(vendas, f, indent=4)

    print("Nova venda adicionada com sucesso!")

# Menu Engenheiro de Manutenção
def menu_engenheiro():
    while True:
        print("\nMenu do Engenheiro de Manutenção:")
        print("1. Consultar Próximas Revisões")
        print("2. Consultar Histórico de Revisões")
        print("3. Sair")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case '1':
                consultar_proximas_revisoes()
            case '2':
                consultar_historico_revisoes()
            case '3':
                print("A sair...")
                break
            case _:
                print("Opção inválida.")

# Consultar Próximas Revisões
def consultar_proximas_revisoes():
    # Carregar dados das vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read()) # Carregamento dos dados

    # Carregar dados das atrações
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read()) # Carregamento dos dados

    # Contar bilhetes vendidos por atração
    contagem_vendas = {}
    for venda in vendas:
        if 'atracao' in venda and 'tipoCliente' in venda:
            atracao_id = venda['atracao']
            tipo_cliente = venda['tipoCliente']

            # Verificar se o ID da atração é válido
            if atracao_id and tipo_cliente in ['adulto', 'crianca']:
                if atracao_id not in contagem_vendas:
                    contagem_vendas[atracao_id] = {'adulto': 0, 'crianca': 0}
                contagem_vendas[atracao_id][tipo_cliente] += 1

    # Tabela
    print("\nPróximas Revisões:")
    print(f"{'ID':<3} {'Nome Atração':<33} {'Nº bilhetes que faltam':<5}")
    for atracao in atracoes:
        atracao_id = atracao['id']

        # Verifica se atracao_id está em contagem_vendas
        if atracao_id in contagem_vendas:
            bilhetes_vendidos = contagem_vendas[atracao_id]
        else:
            bilhetes_vendidos = {'adulto': 0, 'crianca': 0}  # Inicializa se não existir

        total_vendidos = bilhetes_vendidos['adulto'] + bilhetes_vendidos['crianca']

        faltam = 50 - (total_vendidos % 50) if total_vendidos % 50 != 0 else 0

        if faltam > 0:
            print(f"{atracao_id:<3} {atracao['atracao']:<33} {faltam:<5}")

# Consultar Histórico de Revisões
def consultar_historico_revisoes():
    # Carregar dados das vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read()) # Carregamento dos dados

    # Carregar dados das atrações
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read()) # Carregamento dos dados

        # Contagem dos bilhetes vendidos
        contagem_vendas = {}
        for venda in vendas:
            if 'tipoCliente' in venda and 'atracao' in venda:  # Verificar se as keys existem
                atracao_id = venda['atracao']
                tipo_cliente = venda['tipoCliente']

                # Iniciar o dicionário para o ID da atração
                if atracao_id not in contagem_vendas:
                    contagem_vendas[atracao_id] = {"adulto": 0, "crianca": 0}

                if tipo_cliente in ['adulto', 'crianca']:
                    contagem_vendas[atracao_id][tipo_cliente] += 1

        # Criar nova lista com o Mês e Ano
        vendas_com_data = []
        for venda in vendas:
            data = venda['data']
            if data:  # Verificar se a data existe
                partes = data.split('/')  # Dividir a data em partes
                if len(partes) == 2:  # Verificar se temos o mês e ano
                    mes = partes[0].zfill(2)  # Formata o mês
                    ano = partes[1]  # Ano
                    formato_data = f"{mes}/{ano}"  # Cria uma string com o formato Mês/Ano
                    vendas_com_data.append((formato_data, venda))  # Adicionar à lista

        # Ordenar a lista por data em ordem decrescente
        for i in range(len(vendas_com_data)):
            for j in range(len(vendas_com_data) - 1):
                if vendas_com_data[j][1]['data'] < vendas_com_data[j + 1][1]['data']:
                    # Trocar as vendas
                    vendas_com_data[j], vendas_com_data[j + 1] = vendas_com_data[j + 1], vendas_com_data[j]

        # Obter as 3 últimas revisões
        ultimas_revisoes = vendas_com_data[:3]

        # Mostrar as 3 últimas revisões
        for formato_data, revisao in ultimas_revisoes:
            atracao_id = revisao['atracao']
            nome_atracao = next((a['atracao'] for a in atracoes if a['id'] == atracao_id), "Desconhecida")
            num_bilhetes_vendidos = contagem_vendas[atracao_id]['adulto'] + contagem_vendas[atracao_id]['crianca']

            print(f"\nID: {atracao_id}, Nome: {nome_atracao}, Bilhetes Vendidos desde {formato_data}: {num_bilhetes_vendidos}")

# Menu do Administrador
def menu_administrador():
    while True:
        print("\nMenu do Administrador:")
        print("1. Consultar Total de Vendas")
        print("2. Consultar Total de Lucro")
        print("3. Consultar o total de vendas e lucro por mês")
        print("4. Consultar a atração com melhor relação preço/tempo")
        print("5. Consultar Atração Mais Procurada")
        print("6. Consultar Atração Mais Procurada por Adultos")
        print("7. Consultar Atração Mais Procurada por Crianças")
        print("8. Consultar Atração Mais Lucrativa")
        print("9. Consultar Atração Menos Lucrativa")
        print("10. Adicionar Nova Atração")
        print("11. Adicionar Novo Login")
        print("12. Sair")

        opcao = input("Escolha uma opção: ")

        match opcao:
            case '1':
                consultar_vendas()
            case '2':
                consultar_lucro()
            case '3':
                consultar_total_vendas_lucro_mes()
            case '4':
                atracao_melhor_relacao_preco_tempo()
            case '5':
                consultar_atracao_mais_procurada()
            case '6':
                consultar_atracao_procurada('maior')
            case '7':
                consultar_atracao_procurada('menor')
            case '8':
                consultar_atracao_lucrativa('mais')
            case '9':
                consultar_atracao_lucrativa('menos')
            case '10':
                adicionar_nova_atracao()
            case '11':
                adicionar_novo_login()
            case '12':
                print("A sair...")
                break
            case _:
                print("Opção inválida.")

# Consultar Vendas
def consultar_vendas():
    # Carregar dados das vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read()) # Carregamento dos dados

    total_vendas = len(vendas)
    print(f"\nTotal de Vendas: {total_vendas:.2f}€")

# Consultar Lucro
def consultar_lucro():
    # Carregar dados das vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read())

    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read())

    total_lucro = 0
    for venda in vendas:
        # Verifica se as chaves necessárias estão presentes
        if 'atracao' in venda and 'tipoCliente' in venda:
            atracao_id = venda['atracao']
            tipo_cliente = venda['tipoCliente']

            # Encontra a atração correspondente
            for atracao in atracoes:
                if atracao['id'] == atracao_id:
                    if tipo_cliente == 'adulto':
                        total_lucro += atracao['precoAdulto']
                    elif tipo_cliente == 'crianca':
                        total_lucro += atracao['precoCrianca']

    print(f"\nTotal de Lucro: {total_lucro:.2f}€")

def consultar_total_vendas_lucro_mes():
    # Carregar dados das vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read()) # Carregamento dos dados

    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read()) # Carregamento dos dados

    relatorio = {}
    for venda in vendas:
        # Verificar se as keys (data, tipoCliente e atracao) estão presentes
        if 'data' in venda and 'tipoCliente' in venda and 'atracao' in venda:
            mes = venda['data'][:7]  # Formato Mês e Ano
            tipo_cliente = venda['tipoCliente']
            atracao_id = venda['atracao']

            # Iniciar o mês no relatório, caso não exista
            if mes not in relatorio:
                relatorio[mes] = {'total_vendas': 0, 'total_lucro': 0}

            relatorio[mes]['total_vendas'] += 1

            # Encontrar a atração e atualizar o lucro
            for atracao in atracoes:
                if atracao['id'] == atracao_id:
                    if tipo_cliente == 'adulto':
                        relatorio[mes]['total_lucro'] += atracao['precoAdulto']
                    elif tipo_cliente == 'crianca':
                        relatorio[mes]['total_lucro'] += atracao['precoCrianca']
                    break

    # Tabela
    print("\nVendas e Lucro por Mês:")
    print(f"{'Mês':<10} {'Total de Vendas':<15} {'Total de Lucro':<20}")
    for mes, dados in relatorio.items():
        print(f"{mes:<10} {dados['total_vendas']:<15} €{dados['total_lucro']:.2f}")

# Consultar a atração com melhor relação preço/tempo
def atracao_melhor_relacao_preco_tempo():
    # Carregar dados das atrações
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read()) # Carregamento dos dados

    melhor_atracao = 0
    melhor_relacao = 9999999999  # Um valor inicial muito alto

    for atracao in atracoes:
        custo = (atracao['precoAdulto'] + atracao['precoCrianca']) / 2  # Custo médio
        tempo = atracao['duracaoSegundos']

        if tempo > 0:
            relacao = custo / tempo
            if relacao < melhor_relacao:
                melhor_relacao = relacao
                melhor_atracao = atracao  # Agora guarda o objeto da atração

    if melhor_atracao != 0:  # Verifica se uma atração foi encontrada
        print(f"\nAtração com melhor relação preço/tempo: {melhor_atracao['atracao']} (Custo por segundo: {melhor_relacao:.2f}€)")

# Consultar Atração Mais Procurada
def consultar_atracao_mais_procurada():
    # Carregar dados das vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read()) # Carregamento dos dados

    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read()) # Carregamento dos dados

    contagem_vendas = {}
    for venda in vendas:
        atracao_id = venda['atracao']
        # Verificar se o ID da atração já se encontra no dicionário e acrescenta
        if atracao_id in contagem_vendas:
            contagem_vendas[atracao_id] += 1
        else:
            contagem_vendas[atracao_id] = 1  # Iniciar a contagem

    # Encontra a atração mais vendida sem usar None
    atracao_procurada = ''
    max_vendas = -1

    for atracao_id, total in contagem_vendas.items():
        if total > max_vendas:
            max_vendas = total
            atracao_procurada = atracao_id

    # Como atracao_procurada será uma string válida, não haverá problema
    total_vendidos = contagem_vendas[atracao_procurada]

    nome_atracao = None
    for atracao in atracoes:
        if atracao['id'] == atracao_procurada:
            nome_atracao = atracao['atracao']
            break

    print(f"\nAtração mais procurada: ID: {atracao_procurada}, Nome: {nome_atracao} com {total_vendidos} bilhetes vendidos.")

def consultar_atracao_procurada(tipo):
    # Carregar dados das vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read()) # Carregamento dos dados
    # Carregar dados das atrações
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read()) # Carregamento dos dados

        # Dicionários para contar bilhetes vendidos
        contagem_adultos = {}
        contagem_criancas = {}

        # Contar bilhetes vendidos
        for venda in vendas:
            atracao_id = venda['atracao']

            # Verificar 'tipoCliente' está presente
            if 'tipoCliente' in venda:
                tipo_cliente = venda['tipoCliente']

                # Contagem de adultos
                if tipo_cliente == 'adulto':
                    if atracao_id in contagem_adultos:
                        contagem_adultos[atracao_id] += 1
                    else:
                        contagem_adultos[atracao_id] = 1  # Iniciar contagem

                # Contagem de crianças
                elif tipo_cliente == 'crianca':
                    if atracao_id in contagem_criancas:
                        contagem_criancas[atracao_id] += 1
                    else:
                        contagem_criancas[atracao_id] = 1  # Iniciar contagem

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
        if tipo == 'maior':
            if nome_atracao_adulto:
                print(f"\nAtração mais procurada por Adultos: {nome_atracao_adulto} com {contagem_adultos[atracao_adulto_id]} bilhetes vendidos.")

        if tipo == 'menor':
            if nome_atracao_crianca:
                print(f"\nAtração mais procurada por Crianças: {nome_atracao_crianca} com {contagem_criancas[atracao_crianca_id]} bilhetes vendidos.")

# Consultar Atração Mais e Menos Lucrativa
def consultar_atracao_lucrativa(classe):
    # Carregar dados das vendas
    with open('Cesaeland_vendas.json', 'r', encoding='utf-8') as f:
        vendas = json.loads(f.read()) # Carregamento dos dados

    # Carregar dados das atrações
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read()) # Carregamento dos dados

    # Iniciar os lucros para cada Atração
    lucros = {}
    for venda in vendas:
        atracao_id = venda['atracao']

        # Verificar 'tipoCliente' está presente
        if 'tipoCliente' in venda:
            tipo_cliente = venda['tipoCliente']

            # Iniciar o lucro para a atração, se este ainda não existir
            if atracao_id not in lucros:
                lucros[atracao_id] = 0  # Iniciar contagem

            # Encontrar o preço da atração
            for atracao in atracoes:
                if atracao['id'] == atracao_id:
                    if tipo_cliente == 'adulto':
                        lucros[atracao_id] += atracao['precoAdulto']
                    elif tipo_cliente == 'crianca':
                        lucros[atracao_id] += atracao['precoCrianca']
                    break

    # Saber qual a Atração Mais e Menos Lucrativa
    atracao_mais_lucrativa = None
    atracao_menos_lucrativa = None
    lucro_max = 0
    lucro_min = 9999999999  # Um valor inicial muito alto

    for atracao_id, lucro in lucros.items():
        if lucro > lucro_max:
            lucro_max = lucro
            atracao_mais_lucrativa = atracao_id

        # Ignorar lucros zero
        if 0 < lucro < lucro_min:
            lucro_min = lucro
            atracao_menos_lucrativa = atracao_id

    nome_atracao_mais = None
    for atracao in atracoes:
        if atracao['id'] == atracao_mais_lucrativa:
            nome_atracao_mais = atracao['atracao']
            break

    nome_atracao_menos = None
    for atracao in atracoes:
        if atracao['id'] == atracao_menos_lucrativa:
            nome_atracao_menos = atracao['atracao']
            break

    # Resultados com base no lucro
    if classe == 'mais':
        if atracao_mais_lucrativa:
            print(f"\nAtração Mais Lucrativa: ID: {atracao_mais_lucrativa}, Nome: {nome_atracao_mais}, Lucro: {lucros[atracao_mais_lucrativa]:.2f}€")

    if classe == 'menos':
        if atracao_menos_lucrativa:
            print(f"\nAtração Menos Lucrativa: ID: {atracao_menos_lucrativa}, Nome: {nome_atracao_menos}, Lucro: {lucros[atracao_menos_lucrativa]:.2f}€")

def adicionar_nova_atracao():
    # Carregar dados das atrações
    with open('Cesaeland_atracoes.json', 'r', encoding='utf-8') as f:
        atracoes = json.loads(f.read()) # Carregamento dos dados

        novo_id = len(atracoes) + 1  # ID automático
        nome = input("Nome da Atração: ")
        preco_adulto = float(input("Preço do Bilhete para Adultos: "))
        preco_crianca = float(input("Preço do Bilhete para Crianças: "))
        duracao = int(input("Duração (em segundos): "))

        custo_manutencao_fixo = float(input("Custo de Manutenção Fixo por Mês: "))
        custo_manutencao_por_bilhete = float(input("Custo de Manutenção por Bilhete: "))

        # Adicionar nova atração
        atracoes.append({
            "id": novo_id,
            "atracao": nome,
            "precoAdulto": preco_adulto,
            "precoCrianca": preco_crianca,
            "duracaoSegundos": duracao,
            "custoManutencaoFixo": custo_manutencao_fixo,
            "custoManutencaoPorBilhete": custo_manutencao_por_bilhete
        })

        # Guardar dados das novas atrações
        with open('Cesaeland_atracoes.json', 'w', encoding='utf-8') as f:
            json.dump(atracoes, f, indent=4)

        print("\nNova atração adicionada com sucesso!")

def adicionar_novo_login():
    # Carregar dados dos logins
    with open('Cesaeland_logins.json', 'r', encoding='utf-8') as f:
        logins = json.loads(f.read()) # Carregamento dos dados

        novo_username = input("\nNovo Utilizador: ")
        nova_password = input("Nova Password: ")
        tipo_acesso = input("Tipo de Acesso (ADMIN/ENG): ").strip().upper()

        # Verificar se o tipo de acesso é válido
        if not tipo_acesso in ["ADMIN", "ENG"]:
            print("\nTipo de acesso inválido. Deve ser ADMIN ou ENG.")
            return

        # Verificar se o username já existe
        for LOGIN in logins:
            if LOGIN['username'] == novo_username:
                print("\nEste Utilizador já existe. Tente outro nome de Utilizador.")
                return

        # Adicionar novo login
        logins.append({
            "role": tipo_acesso,
            "username": novo_username,
            "password": nova_password
        })

        # Guardar dados dos novos logins
        with open('Cesaeland_logins.json', 'w', encoding='utf-8') as f:
            json.dump(logins, f, indent=4)

        print("\nNovo login adicionado com sucesso!")

# Execução do programa
while True:
    print("\nBem-vindo ao Parque Temático CESAELand ©")
    print("\nEscolha o tipo de acesso:")
    print("\n1. Cliente")
    print("2. Bilheteira")
    print("3. Engenheiro de Manutenção")
    print("4. Administrador")
    print("5. Sair")

    escolha = input("\nEscolha uma opção: ")

    match escolha:
        case '1':
            menu_cliente()
        case '2':
            menu_bilheteira()
        case '3':
            if login() == "ENG":
                print("Engenheiro de Manutenção.")
                menu_engenheiro()
            else:
                print("Acesso negado.")
        case '4':
            if login() == "ADMIN":
                print("Administrador.")
                menu_administrador()
            else:
                print("Acesso negado.")
        case '5':
            print("A sair...")
            break
        case _:
            print("Opção inválida.")