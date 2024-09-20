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

# grupo
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

#produto

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


#similares
def consultarSimilares(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM similares;")
        similares = cursor.fetchall()
        
        print("Produtos similares encontrados:")
        for similar in similares:
            print(similar)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao consultar similares: {error}")
    finally:
        cursor.close()


#categoria

def consultarCategorias(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM categoria;")
        categorias = cursor.fetchall()
        
        print("Categorias encontradas:")
        for categoria in categorias:
            print(categoria)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao consultar categorias: {error}")
    finally:
        cursor.close()

#revieww

def consultarReviews(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM review;")
        reviews = cursor.fetchall()
        
        print("Reviews encontrados:")
        for review in reviews:
            print(review)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao consultar reviews: {error}")
    finally:
        cursor.close()

#usuario

def consultarUsuarios(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM \"user\";")
        usuarios = cursor.fetchall()
        
        print("Usuários encontrados:")
        for usuario in usuarios:
            print(usuario)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao consultar usuários: {error}")
    finally:
        cursor.close()

#produto categoria

def consultarProdutoCategoria(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM ProdutoCategoria;")
        produtos_categoria = cursor.fetchall()
        
        print("Relações de produtos e categorias encontradas:")
        for pc in produtos_categoria:
            print(pc)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao consultar produtos e categorias: {error}")
    finally:
        cursor.close()


def main():
    conn = conectarAoBanco()
    if conn:
        consultarGrupos(conn)
        consultarProdutos(conn)
        consultarSimilares(conn)
        consultarCategorias(conn)
        consultarReviews(conn)
        consultarUsuarios(conn)
        consultarProdutoCategoria(conn)
        conn.close()

# Ponto de entrada do script
if __name__ == '__main__':
    main()
