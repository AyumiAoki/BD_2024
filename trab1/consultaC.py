import psycopg2
import os

# Variáveis Globais
mensagemVoltar = 'Digite (v) para voltar e (x) para sair: '
conn = None
dashboard_query = {
    'a': """
            (
                SELECT 'MAIOR' as tipo,
                * FROM review
                WHERE idproduct = %s
                ORDER BY helpful DESC, rating DESC
                LIMIT 5
            )
            UNION ALL
            (
                SELECT 'MENOR' as tipo,
                * FROM review
                WHERE idproduct = %s
                ORDER BY helpful DESC, rating ASC
                LIMIT 5
            )
            ORDER BY tipo, helpful desc;
        """,
    'b': """
                SELECT similares .*
                FROM produto p
                JOIN similares ps ON ps.productasin = p.asin
                JOIN produto similares ON similares.asin = ps.similarproductasin
                WHERE similares.salesrank < p.salesrank AND p.asin = %s;
             """,
    'c': """
            SELECT rating, data FROM review
            WHERE idProduct = %s
            ORDER BY data;
        """,
    # outras consultas...
}

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

# Função para executar as consultas SQL
def query(sql, params=None):
    global conn
    try:
        cur = conn.cursor()
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.commit()
        return result

    except psycopg2.DatabaseError as error:
        print("** Erro ao executar a consulta:", error)
        return None

# Função para limpar o terminal
def clearTerminal():
    os.system('clear')
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para formatar o resultado da consulta C
def formatarResultadoC(resultado):
    """Formata o resultado da consulta C."""
    print("-----------Evolução das médias de avaliação--------------\n")
    for row in resultado:
        rating, data = row
        print(f"Avaliação: {rating}, Data: {data.strftime('%d de %B de %Y')}")

# Função para executar a consulta C
def consultaC():
    print("\n------------------------------------------------------------------------------------\n")
    print('Mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada;')
    print("\n------------------------------------------------------------------------------------\n")
    
    idProduct = input('Digite o id do produto: ')
    print("\n------------------------------------------------------------------------------------\n")

    # Executar a consulta 'c' (evolução diária)
    resultadoC = query(dashboard_query['c'], (idProduct,))

    if resultadoC:
        # Formatar e exibir os resultados da consulta 'c'
        formatarResultadoC(resultadoC)
    else:
        print("Nenhum resultado encontrado para o produto " + idProduct + ".")

# Executar Opções
def executarConsulta(opcao):
    funcaoOpcao = None

    if opcao == 'a':
        funcaoOpcao = consultaA
    elif opcao == 'b':
        funcaoOpcao = consultaB
    elif opcao == 'c':
        funcaoOpcao = consultaC
    elif opcao == 'd':
        funcaoOpcao = consultaD
    elif opcao == 'e':
        funcaoOpcao = consultaE
    elif opcao == 'f':
        funcaoOpcao = consultaF
    elif opcao == 'g':
        funcaoOpcao = consultaG
    elif opcao == 'x':
        exit()

    clearTerminal()
    funcaoOpcao()

    loopOpcao = input(mensagemVoltar)
    while loopOpcao != 'v':
        if loopOpcao == 'v':
            break 
        elif loopOpcao == 'x':
            exit()
        else:
            loopOpcao = input('Opção inválida, digite novamente: ')

# Função para verificar opções válidas
def opcaoValida(opcao):
    return (opcao in dashboard_query.keys() or opcao == 'x')

# Função principal
def main():
    global conn
    conn = conectarAoBanco()

    if conn is None:
        return

    try:
        while True:
            print("\n------------------------------------------------------------------------------------\n")
            print("Bem-vindo ao Dashboard :)")
            print("\n------------------------------------------------------------------------------------\n")
            print('Escolha uma das opções abaixo:')
            print('''a) Listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação;''')
            print('''b) Listar os produtos similares com maiores vendas do que ele;''')
            print('''c) Mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada;''')
            print('''d) Listar os 10 produtos líderes de venda em cada grupo de produtos;''')
            print('''e) Listar os 10 produtos com a maior média de avaliações úteis positivas por produto;''')
            print('''f) Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto;''')
            print('''g) Listar os 10 clientes que mais fizeram comentários por grupo de produto.''')
            print('''x) Sair do programa.''')

            opcao = input('Digite a opção desejada: ')

            while not opcaoValida(opcao):
                opcao = input('Opção inválida, digite novamente: ')

            if opcao == 'x':
                break
            else:
                executarConsulta(opcao)

    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados encerrada.")

if __name__ == '__main__':
    main()
