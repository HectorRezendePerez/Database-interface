import mysql.connector
import random

class db:
    def query(ID, ano_ini, ano_fin, cor, chassi, placa, fk_Produto_Id_produto, Id_produto, modelo, marca, preco):
        # Estabelecer conexão com o banco de dados MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='bd_concessionaria_v3'
        )
        if ID == '':
            ID = '%'
        if ano_ini == '':
            ano_ini = '%'
        if ano_fin == '':
            ano_fin == '%'
        if cor == '':
            cor = '%'
        if chassi == '':
            chassi= '%'
        if placa == '':
            placa = '%'
        if fk_Produto_Id_produto == '':
            fk_Produto_Id_produto = '%'
        if Id_produto == '':
            Id_produto= '%'
        if modelo == '':
            modelo = '%'
        if marca == '':
            marca= '%'
        if preco == '':
            preco = '%'
        
        # Criar um cursor para executar consultas SQL
        cursor = connection.cursor()
        query = "SELECT * FROM veiculos WHERE ID LIKE %s AND cor LIKE %s AND chassi LIKE %s AND placa LIKE %s AND fk_Produto_Id_produto LIKE %s"
        if ano_ini != '%' and ano_ini != '':
            query += f"AND ano >= {ano_ini} "
        if ano_fin != '%' and ano_fin != '':
            query += f"AND ano <= {ano_fin} "
        query += ';'
        cursor.execute(query, (ID, cor, chassi, placa, fk_Produto_Id_produto))

        # Obter os resultados da consulta
        results = []
        veiculos = cursor.fetchall()

        query = "SELECT * FROM produto WHERE Id_produto LIKE %s AND modelo LIKE %s AND marca LIKE %s AND preco LIKE %s;"
        cursor.execute(query, (Id_produto, modelo, marca, preco))

        produtos = cursor.fetchall()
        for row in veiculos:
            for prd in produtos:
                if row[5] == prd[0]:   
                    car = {
                        'id': row[0],  # substitua pelo índice correto das colunas no seu banco de dados
                        'year': row[1],
                        'model': prd[1],
                        'brand': prd[2],
                        'price': prd[3],
                        'color': row[2],
                        'plate': row[4],
                    }
                    results.append(car)




        # Fechar o cursor e a conexão com o banco de dados
        cursor.close()
        connection.close()

        return results
