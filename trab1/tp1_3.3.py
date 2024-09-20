import os
import psycopg2
from psycopg2 import OperationalError
from datetime import datetime, timedelta

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
        print("Conexão com o banco de dados estabelecida com sucesso.")
        return conexao
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao conectar ao banco de dados: {error}")
        return None

# Dicionário com consultas SQL
consultas = {
    'grupos': "SELECT * FROM grupo;",
    'produtos': "SELECT * FROM produto;",
    'similares': "SELECT * FROM similares;",
    'categorias': "SELECT * FROM categoria;",
    'reviews': "SELECT * FROM review;",
    'usuarios': "SELECT * FROM \"user\";",
    'produtos_categoria': "SELECT * FROM ProdutoCategoria;",
    'comentarios_por_produto': '''
        SELECT idUser, data, rating, votes, helpful
        FROM review
        WHERE idProduct = %s
        ORDER BY helpful DESC, rating DESC
        LIMIT 5;
    ''',
    'comentarios_por_produto_menores': '''
        SELECT idUser, data, rating, votes, helpful
        FROM review
        WHERE idProduct = %s
        ORDER BY helpful DESC, rating ASC
        LIMIT 5;
    ''',
    'produtos_similares_maiores_vendas': '''
        SELECT sp.asinSimilar, p.title, p.salesrank
        FROM similares sp
        JOIN produto p ON p.asin = sp.asinSimilar
        WHERE sp.asinPai = (SELECT asin FROM produto WHERE id = %s) AND p.salesrank < %s;
    ''',
    'evolucao_diaria_avaliacoes': '''
        SELECT data, rating
        FROM review
        WHERE idProduct = %s
        ORDER BY data;
    '''
}

def executarConsulta(conexao, chave, *args):
    try:
        cursor = conexao.cursor()
        consulta = consultas[chave]
        cursor.execute(consulta, args)
        return cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao consultar {chave}: {error}")
        return None
    finally:
        cursor.close()

def consultarEvolucaoDiariaAvaliacoes(conexao, idProduto):
    avaliacoes = executarConsulta(conexao, 'evolucao_diaria_avaliacoes', idProduto)
    
    if avaliacoes:
        medias_diarias = {}
        for data, rating in avaliacoes:
            data = data.strftime('%Y-%m-%d')
            if data not in medias_diarias:
                medias_diarias[data] = {'soma': 0, 'count': 0}
            medias_diarias[data]['soma'] += rating
            medias_diarias[data]['count'] += 1

        medias_calculadas = {data: valores['soma'] / valores['count'] for data, valores in medias_diarias.items()}
        
        print(f"Evolução diária das médias de avaliação para o produto ID {idProduto}:")
        for data, media in sorted(medias_calculadas.items()):
            print(f"Data: {data}, Média de Avaliação: {media:.2f}")

def main():
    conn = conectarAoBanco()
    if conn:
        for chave in ['grupos', 'produtos', 'similares', 'categorias', 'reviews', 'usuarios', 'produtos_categoria']:
            resultados = executarConsulta(conn, chave)
            print(f"{chave.capitalize()} encontrados:")
            for resultado in resultados:
                print(resultado)

        idProduto = 1
        melhores_comentarios = executarConsulta(conn, 'comentarios_por_produto', idProduto)
        print("5 comentários mais úteis e com maior avaliação:")
        for comentario in melhores_comentarios:
            print(comentario)

        piores_comentarios = executarConsulta(conn, 'comentarios_por_produto_menores', idProduto)
        print("\n5 comentários mais úteis e com menor avaliação:")
        for comentario in piores_comentarios:
            print(comentario)

        salesrank_produto = executarConsulta(conn, 'produtos_similares_maiores_vendas', idProduto)
        if salesrank_produto:  
            print("\nProdutos similares com maiores vendas que o produto ID {}:".format(idProduto))
            for produto in salesrank_produto:
                print(produto)
        else:
            print(f"Erro: Nenhum produto similar encontrado para o produto ID {idProduto} com rank menor que o valor especificado.")

        consultarEvolucaoDiariaAvaliacoes(conn, idProduto)
        
        conn.close()

if __name__ == '__main__':
    main()
