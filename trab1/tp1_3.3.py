import os
import psycopg2
from psycopg2 import OperationalError

# Função para conectar ao banco de dados
def conectarAoBanco():
    try:
        # Conectar ao banco de dados PostgreSQL
        conexao = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'products_amazon'),
            user=os.getenv('DB_USER', 'ame'),
            password=os.getenv('DB_PASS', 'ame1234'),
            port="5433"
        )
        print("Conexão com o banco de dados estabelecida com sucesso.")
        return conexao
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao conectar ao banco de dados: {error}")
        return None

# Função para consultar grupos
def consultarGrupos(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM grupo;")
        grupos = cursor.fetchall()
        
        print("Grupos encontrados:")
        for grupo in grupos:
            print(grupo)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao consultar grupos: {error}")
    finally:
        cursor.close()

def consultarProdutos(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produto;")
        produtos = cursor.fetchall()
        
        print("Produtos encontrados:")
        for produto in produtos:
            print(produto)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao consultar produtos: {error}")
    finally:
        cursor.close()

def main():
    conn = conectarAoBanco()
    if conn:
        consultarGrupos(conn)
        consultarProdutos(conn)
        conn.close()

# Ponto de entrada do script
if __name__ == '__main__':
    main()
