import sqlite3

from tabulate import tabulate

def conectar():
    return sqlite3.connect("especies.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS especies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cientifico TEXT,
    nome_popular TEXT,
    grau_ameaca TEXT,
    localizacao TEXT,
    observacoes TEXT);""")
    cursor.execute("SELECT COUNT(*) FROM especies")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""INSERT INTO especies (id, nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes) VALUES
        (1,'Priodontes maximus', 'Tatu-canastra', 'Vulnerável', 'Pantanal', 'Maior espécie de tatu do mundo'),
        (2,'Leontopithecus rosalia', 'Mico-leão-dourado', 'Em perigo', 'Mata Atlântica', 'Símbolo da conservação no Brasil'),
        (3,'Alouatta belzebul', 'Guariba-de-mãos-ruivas', 'Vulnerável', 'Amazônia Oriental', 'Afetado pela perda de habitat'),
        (4,'Amazona vinacea', 'Papagaio-de-peito-roxo', 'Criticamente em perigo', 'Sul do Brasil', 'Captura ilegal e desmatamento'),
        (5,'Brachyteles arachnoides', 'Muriqui-do-sul', 'Em perigo', 'Mata Atlântica', 'Maior primata das Américas'),
        (6,'Podocnemis expansa', 'Tartaruga-da-amazônia', 'Vulnerável', 'Rios da Amazônia', 'Caça de ovos e carne'),
        (7,'Dendrobates tinctorius', 'Rã-tintureira', 'Quase ameaçado', 'Floresta Amazônica', 'Afetada por tráfico de animais'),
        (8,'Harpyhaliaetus coronatus', 'Águia-cinzenta', 'Vulnerável', 'Cerrado e Pantanal', 'Caça e perda de habitat'),
        (9,'Euterpe edulis', 'Palmito-juçara', 'Criticamente em perigo', 'Mata Atlântica', 'Exploração predatória'),
        (10,'Scinax alcatraz', 'Perereca-de-Alcatrazes', 'Criticamente em perigo', 'Ilha de Alcatrazes - SP', 'Espécie endêmica da ilha');""")               
    conn.commit()
    conn.close()

def Adicionar_especie():
    print("1 - Adicionar com ID\n2 - Adicionar automaticamente")
    escolha_tipo = int(input("Escolha: "))

    conn = conectar()
    cursor = conn.cursor()

    if escolha_tipo == 1:
        ID = int(input("ID: "))
        nome_cientifico = input("Nome Científico: ")
        nome_popular = input("Nome Popular: ")
        grau_ameaca = input("Grau ameaça: ")
        localizacao = input("Localização: ")
        observacoes = input("Observações: ")

        cursor.execute(
            "INSERT INTO especies (id, nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes) VALUES (?, ?, ?, ?, ?, ?)",
            (ID, nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes))
        
    elif escolha_tipo == 2:
        nome_cientifico = input("Nome Científico: ")
        nome_popular = input("Nome Popular: ")
        grau_ameaca = input("Grau ameaça: ")
        localizacao = input("Localização: ")
        observacoes = input("Observações: ")

        cursor.execute(
            "INSERT INTO especies (nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes) VALUES (?, ?, ?, ?, ?)",
            (nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes))

    else:
        print("Opção inválida. Tente novamente.")
        conn.close()
        return

    conn.commit()
    conn.close()
    print("Espécie adicionada com sucesso!")


def listar_especies():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM especies")
    resultados = cursor.fetchall()
    conn.close()
    return resultados  

def mostrar_especies():
    especies = listar_especies()
    print(tabulate(especies, headers=["ID", "Nome Científico", "Nome Popular", "Grau de Ameaça", "Localização", "Observações"], tablefmt="github"))

def grau_de_risco():
    opcoes = {
    "1": "Vulnerável",
    "2": "Quase ameaçado",
    "3": "Em perigo",
    "4": "Criticamente em perigo"}
    print("GRAUS DE AMEAÇA:\n")
    escolha = input("Qual grau de ameaça?\nVulnerável - 1\nQuase ameaçado - 2\nEm perigo - 3\nCriticamente em perigo - 4\n")
    grau_ameaca = opcoes.get(escolha)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome_popular, grau_ameaca FROM especies WHERE grau_ameaca = ?", (grau_ameaca,))
    resultados = cursor.fetchall()
    conn.close()
    print(tabulate(resultados,headers = ["Nome Popular", "Grau de ameaça"], tablefmt = "github"))
    return resultados

def buscar_por_id ():
    escolha_id = input("ID: ")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM especies WHERE id = ?", (escolha_id,))
    resultados = cursor.fetchone()
    conn.close()
    if resultados:
        print(tabulate([resultados],headers = ["ID", "Nome Científico", "Nome Popular", "Grau de Ameaça", "Localização", "Observações"], tablefmt="github"))
    else:
        print("Não foi encontada uma espécie com esse ID.")
    return resultados

def delet_usuario():
    escolha_id_delete = input("ID: ")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM especies WHERE id = ?", (escolha_id_delete,))
    conn.commit()
    deletados = cursor.rowcount 
    conn.close()

    if deletados > 0:
        print("A espécie foi deletada com sucesso.")
    else:
        print("Não foi encontrada uma espécie com esse ID.")