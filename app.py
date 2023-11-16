# Importa as bibliotecas necessárias
from flask import Flask, jsonify, request
import pandas as pd

# Cria a aplicação Flask
app = Flask(__name__)

# Tenta criar o arquivo Text.csv caso ele não exista e escreve o cabeçalho
try:
    open('Text.csv', 'x')
    with open("Text.csv", "w") as arquivo:
         arquivo.write("ID,TAREFA\n") 
except:
    pass

# Define a rota para listar as tarefas
@app.route("/list", methods=['GET'])
def listarTarefas():    
    # Lê o arquivo Text.csv e converte para um dicionário
    tarefas = pd.read_csv('Text.csv')
    tarefas = tarefas.to_dict('records')    
    # Retorna as tarefas em formato JSON
    return jsonify(tarefas)

# Define a rota para adicionar uma tarefa
@app.route("/add", methods=['POST'])
def addTarefas():
    # Obtém a tarefa enviada pelo cliente
    item = request.json  
    # Lê o arquivo Text.csv e converte para um dicionário
    tarefas = pd.read_csv('Text.csv')
    tarefas = tarefas.to_dict('records') 
    # Define o ID da nova tarefa
    id = len(tarefas) + 1
    # Adiciona a nova tarefa ao arquivo Text.csv
    with open("Text.csv", "a") as arquivo:
         arquivo.write(f"{id},{item['Tarefa']}\n")    
    # Lê o arquivo Text.csv e converte para um dicionário
    tarefas = pd.read_csv('Text.csv')
    tarefas = tarefas.to_dict('records')        
    # Retorna as tarefas em formato JSON
    return jsonify(tarefas)

# Define a rota para deletar uma tarefa
@app.route("/delete/<int:id>", methods=['DELETE'])
def deleteTarefa(id):
    tarefas = pd.read_csv('Text.csv')
    if id not in tarefas['ID'].values:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    tarefas = tarefas.drop(tarefas[tarefas['ID'] == id].index)
    
    # Reajusta os IDs após a exclusão
    tarefas['ID'] = range(1, len(tarefas) + 1)
    
    tarefas.to_csv('Text.csv', index=False)
    return jsonify(tarefas.to_dict('records'))
    

@app.route("/update/<int:id>", methods=["PUT"])
def update_task(id):
    item = request.json
    tarefas = pd.read_csv('Text.csv')
    if id not in tarefas['ID'].values:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    tarefas.loc[tarefas['ID'] == id, 'TAREFA'] = item['Tarefa']
    tarefas.to_csv('Text.csv', index=False)
    return jsonify(tarefas.to_dict('records'))


# Inicia a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

