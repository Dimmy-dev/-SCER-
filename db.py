import sqlite3
from tabulate import tabulate

class Database:
    def __init__(self, db_name="especies.db"):
        self.__db_name = db_name

    def __conectar(self):
        # O encapsulamento com __ impede que a conexão seja feita diretamente de fora da classe
        return sqlite3.connect(self.__db_name)

    def criar_tabela(self):
        conn = self.__conectar()
        cursor = conn.cursor()
        # Uso de consultas seguras
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

    def adicionar_especie(self, nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes, especie_id=None):
        conn = self.__conectar()
        cursor = conn.cursor()
        
        # PREPARED STATEMENTS: Evita SQL Injection utilizando os marcadores (?)
        if especie_id:
            cursor.execute(
                "INSERT INTO especies (id, nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes) VALUES (?, ?, ?, ?, ?, ?)",
                (especie_id, nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes))
        else:
            cursor.execute(
                "INSERT INTO especies (nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes) VALUES (?, ?, ?, ?, ?)",
                (nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes))
                
        conn.commit()
        conn.close()

    def listar_especies(self):
        conn = self.__conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM especies")
        resultados = cursor.fetchall()
        conn.close()
        return resultados  

    def buscar_por_grau_risco(self, grau_ameaca):
        conn = self.__conectar()
        cursor = conn.cursor()
        # PREPARED STATEMENTS
        cursor.execute("SELECT * FROM especies WHERE LOWER(grau_ameaca) = LOWER(?)", (grau_ameaca,))
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def atualizar_especie(self, especie_id, nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes):
        conn = self.__conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE especies SET nome_cientifico=?, nome_popular=?, grau_ameaca=?, localizacao=?, observacoes=? WHERE id=?",
            (nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes, especie_id)
        )
        conn.commit()
        atualizados = cursor.rowcount
        conn.close()
        return atualizados > 0

    def get_estatisticas(self):
        conn = self.__conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT grau_ameaca, COUNT(*) FROM especies GROUP BY grau_ameaca")
        resultados = cursor.fetchall()
        conn.close()
        return dict(resultados)

    def buscar_por_id(self, especie_id):
        conn = self.__conectar()
        cursor = conn.cursor()
        # PREPARED STATEMENTS
        cursor.execute("SELECT * FROM especies WHERE id = ?", (especie_id,))
        resultados = cursor.fetchone()
        conn.close()
        return resultados

    def deletar_especie(self, especie_id):
        conn = self.__conectar()
        cursor = conn.cursor()
        # PREPARED STATEMENTS
        cursor.execute("DELETE FROM especies WHERE id = ?", (especie_id,))
        conn.commit()
        deletados = cursor.rowcount 
        conn.close()
        return deletados > 0