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

# Função para criar o esquema de tabelas
def criarEsquema(conexao):
    try:
        cursor = conexao.cursor()

        # Criar a tabela grupo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grupo (
                id SERIAL PRIMARY KEY,
                name VARCHAR(32) UNIQUE
            );
        ''')

        # Criar a tabela produto
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produto (
                id INT PRIMARY KEY,
                asin VARCHAR(10) UNIQUE NOT NULL,
                title VARCHAR(512),
                salesrank INT UNIQUE,
                idgroup INT,
                CONSTRAINT fk_group FOREIGN KEY(idgroup) REFERENCES grupo(id)
            );
        ''')

        # Criar a tabela similares
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS similares (
                asinPai VARCHAR(10),
                asinSimilar VARCHAR(10),
                PRIMARY KEY (asinPai, asinSimilar)
            );
        ''')

        # Criar a tabela category
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category (
                id INT PRIMARY KEY,
                name VARCHAR(255),
                idPai INT
            );
        ''')

        # Criar a tabela review
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS review (
                idUser VARCHAR(25),
                idProduct INT,
                data DATE,
                rating SMALLINT,
                votes INT,
                helpful INT,
                PRIMARY KEY (idUser, idProduct)
            );
        ''')

        # Criar a tabela user
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "user" (
                idUser VARCHAR(25) PRIMARY KEY
            );
        ''')

        # Criar a tabela ProductCategory
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProductCategory (
                idProduct INT,
                idCategory INT,
                PRIMARY KEY (idProduct, idCategory)
            );
        ''')

        # Commit das mudanças
        conexao.commit()
        print("Esquema de banco de dados criado com sucesso.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao criar o esquema de banco de dados: {error}")
    finally:
        if conexao:
            cursor.close()
            conexao.close()

# Função principal
def main():
    conn = conectarAoBanco()
    criarEsquema(conn)