from flask import Flask, request, jsonify, send_from_directory
import os
from db import Database

app = Flask(__name__, static_folder='imagens')
db = Database()

# Inicializa as tabelas no banco de dados se não existirem
db.criar_tabela()

def row_to_dict(row):
    """Converte a tupla do sqlite3 em um dicionário para a API"""
    if not row:
        return None
    return {
        "id": row[0],
        "nome_cientifico": row[1],
        "nome_popular": row[2],
        "grau_ameaca": row[3],
        "localizacao": row[4],
        "observacoes": row[5]
    }

# Rota principal para servir a página HTML
@app.route('/')
def index():
    # Retorna o arquivo index.html que está no mesmo diretório
    return send_from_directory('.', 'index.html')

# Rota para servir as imagens (usada no src do HTML)
@app.route('/imagens/<path:filename>')
def serve_image(filename):
    return send_from_directory('imagens', filename)

# ====== API ENDPOINTS ======

@app.route('/api/especies', methods=['GET'])
def get_especies():
    """Retorna todas as espécies cadastradas"""
    resultados = db.listar_especies()
    return jsonify([row_to_dict(row) for row in resultados])

import unicodedata
import re

def formatar_nome_imagem(nome):
    nome = unicodedata.normalize('NFD', nome.lower())
    nome = nome.encode('ascii', 'ignore').decode('utf8')
    nome = re.sub(r'\s+', '-', nome)
    return nome + ".jpg"

@app.route('/api/especies', methods=['POST'])
def add_especie():
    """Adiciona uma nova espécie ao banco de dados"""
    # Suporta JSON e FormData
    if request.is_json:
        dados = request.json
    else:
        dados = request.form
    
    nome_cientifico = dados.get('nome_cientifico')
    nome_popular = dados.get('nome_popular')
    grau_ameaca = dados.get('grau_ameaca')
    localizacao = dados.get('localizacao')
    observacoes = dados.get('observacoes')
    especie_id = dados.get('id')  # opcional
    
    if not (nome_cientifico and nome_popular and grau_ameaca):
        return jsonify({"erro": "Dados insuficientes."}), 400
        
    # Tratamento da imagem
    if 'imagem' in request.files:
        imagem = request.files['imagem']
        if imagem.filename != '':
            nome_arquivo = formatar_nome_imagem(nome_popular)
            caminho_salvar = os.path.join('imagens', nome_arquivo)
            os.makedirs('imagens', exist_ok=True)
            imagem.save(caminho_salvar)
            
    try:
        db.adicionar_especie(nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes, especie_id)
        return jsonify({"mensagem": "Espécie adicionada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/especies/<int:especie_id>', methods=['GET'])
def get_especie_by_id(especie_id):
    """Busca uma espécie específica pelo ID"""
    resultado = db.buscar_por_id(especie_id)
    if resultado:
        return jsonify(row_to_dict(resultado))
    return jsonify({"erro": "Espécie não encontrada."}), 404

@app.route('/api/especies/<int:especie_id>', methods=['PUT'])
def update_especie(especie_id):
    """Atualiza uma espécie existente"""
    if request.is_json:
        dados = request.json
    else:
        dados = request.form
        
    nome_cientifico = dados.get('nome_cientifico')
    nome_popular = dados.get('nome_popular')
    grau_ameaca = dados.get('grau_ameaca')
    localizacao = dados.get('localizacao')
    observacoes = dados.get('observacoes')
    
    if not (nome_cientifico and nome_popular and grau_ameaca):
        return jsonify({"erro": "Dados insuficientes."}), 400

    # Se for enviada uma nova imagem, vamos salvá-la
    if 'imagem' in request.files:
        imagem = request.files['imagem']
        if imagem.filename != '':
            nome_arquivo = formatar_nome_imagem(nome_popular)
            caminho_salvar = os.path.join('imagens', nome_arquivo)
            os.makedirs('imagens', exist_ok=True)
            imagem.save(caminho_salvar)
            
    try:
        sucesso = db.atualizar_especie(especie_id, nome_cientifico, nome_popular, grau_ameaca, localizacao, observacoes)
        if sucesso:
            return jsonify({"mensagem": "Espécie atualizada com sucesso!"}), 200
        else:
            return jsonify({"erro": "Espécie não encontrada."}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/especies/<int:especie_id>', methods=['DELETE'])
def delete_especie(especie_id):
    """Deleta uma espécie pelo ID"""
    sucesso = db.deletar_especie(especie_id)
    if sucesso:
        return jsonify({"mensagem": "Espécie deletada com sucesso."}), 200
    return jsonify({"erro": "Espécie não encontrada para deletar."}), 404

@app.route('/api/especies/grau/<grau>', methods=['GET'])
def get_especies_by_grau(grau):
    """Retorna espécies por grau de ameaça"""
    resultados = db.buscar_por_grau_risco(grau)
    return jsonify([row_to_dict(row) for row in resultados])

@app.route('/api/especies/estatisticas', methods=['GET'])
def get_estatisticas():
    """Retorna as contagens de espécies por grau de ameaça"""
    return jsonify(db.get_estatisticas())

if __name__ == '__main__':
    print("Iniciando Servidor Web do Sistema de Espécies em Risco...")
    print("Acesse http://127.0.0.1:5000 no seu navegador.")
    # Rodar o Flask no modo de debug
    app.run(debug=True, port=5000)