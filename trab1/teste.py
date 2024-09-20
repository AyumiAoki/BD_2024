import os
import psycopg2

from tabulate import tabulate

# Função para conectar ao banco de dados
def conectarAoBanco():
    try:
        conexao = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'products_amazon'),
            user=os.getenv('DB_USER', 'ame'),
            password=os.getenv('DB_PASS', 'ame1234'),
            port="5433"
        )
        return conexao
    except psycopg2.DatabaseError as error:
        print(f"Erro ao conectar ao banco de dados: {error}")
        return None

# Função para executar consultas
def query(conexao, consulta, *args):
    try:
        cursor = conexao.cursor()
        cursor.execute(consulta, args)
        resultado = cursor.fetchall()
        cursor.close()
        conexao.commit()
        return resultado
    except psycopg2.DatabaseError as error:
        print(f"Erro ao executar a consulta: {error}")
        return None

# Dicionário com consultas SQL
dashboard_queries = {
    'a': """
        (
            SELECT 'MAIOR' AS classe, idUser, data, rating, votes, helpful
            FROM review
            WHERE idProduct = %s
            ORDER BY helpful DESC, rating DESC
            LIMIT 5
        )
        UNION
        (
            SELECT 'MENOR' AS classe, idUser, data, rating, votes, helpful
            FROM review
            WHERE idProduct = %s
            ORDER BY helpful DESC, rating ASC
            LIMIT 5
        )
        ORDER BY classe;
    """,
    'b': """
        SELECT sp.asinSimilar, p.title, p.salesrank
        FROM similares sp
        JOIN produto p ON p.asin = sp.asinSimilar
        WHERE sp.asinPai = (SELECT asin FROM produto WHERE id = %s) AND p.salesrank < %s;
    """,
    'c': """
        SELECT data, AVG(rating)
        FROM review
        WHERE idProduct = %s
        GROUP BY data
        ORDER BY data;
    """
}

# Função principal para rodar as consultas
def main():
    conexao = conectarAoBanco()
    if conexao:
        idProduto = 1

        print("\n a - Listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação.\n")
        result = query(conexao, dashboard_queries['a'], idProduto, idProduto)
        print(tabulate(result, headers=['Classe', 'ID Usuário', 'Data', 'Nota', 'Votos', 'Útil']))

        print("\n b - Listar produtos similares com maiores vendas.\n")
        result = query(conexao, dashboard_queries['b'], idProduto, 1000)
        print(tabulate(result, headers=['ASIN Similar', 'Título', 'Salesrank']))

        print("\n c - Mostrar evolução diária das médias de avaliação.\n")
        result = query(conexao, dashboard_queries['c'], idProduto)
        print(tabulate(result, headers=['Data', 'Média de Avaliações']))

        conexao.close()

if __name__ == "__main__":
    main()
