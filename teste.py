import sqlite3
import json
import zipfile
import os

def export_tables_to_json_and_zip(database_file, tables, zip_file_name):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Crie um dicionário para armazenar os dados de todas as tabelas
    data = {}

    # Itere sobre as tabelas e obtenha os dados
    for table_name in tables:
        # Consultar todas as linhas da tabela
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Lista para armazenar as linhas da tabela
        table_data = []

        # Percorra as linhas e adicione ao dicionário da tabela
        for row in rows:
            # Crie um dicionário com os dados da linha
            row_data = {}
            for i, column_name in enumerate(cursor.description):
                row_data[column_name[0]] = row[i]
            
            # Adicione a linha à lista de dados da tabela
            table_data.append(row_data)

        # Adicione os dados da tabela ao dicionário principal
        data[table_name] = table_data

    # Feche a conexão com o banco de dados SQLite
    cursor.close()
    conn.close()

    # Salve os dados em arquivos JSON
    for table_name, table_data in data.items():
        # Crie o nome do arquivo com base no nome da tabela
        filename = f"{table_name}.json"

        # Escreva os dados da tabela no arquivo JSON
        with open(filename, 'w') as json_file:
            json.dump(table_data, json_file)

    # Crie um arquivo ZIP e adicione todos os arquivos JSON a ele
    with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
        for table_name in tables:
            filename = f"{table_name}.json"
            zip_file.write(filename)

            # Remova o arquivo JSON após adicioná-lo ao arquivo ZIP
            os.remove(filename)

    print("Exportação concluída com sucesso!")

# Exemplo de uso da função
export_tables_to_json_and_zip('Banco_de_dados', ['FAVORITAS', 'LOGERROS', 'MARKETANTIG', 'MARKETATUAL'], 'export.zip')
