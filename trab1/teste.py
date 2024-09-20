import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import psycopg2
import os

# Variável global para a conexão
conn = None

# Inicializar a aplicação Dash com o tema Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

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

# Função para realizar a consulta SQL no banco de dados
def consulta_a(id_product):
    global conn
    # Definir a consulta SQL
    sql = f'''(select 'Maiores avaliações' as tipo, iduser, data, rating, helpful
               from review
               where idproduct = {id_product}
               order by rating desc, helpful desc
               limit 5)
               union
               (select 'Menores avaliações' as tipo, iduser, data, rating, helpful
               from review
               where idproduct = {id_product}
               order by rating asc, helpful desc
               limit 5)
               order by tipo, helpful desc;'''

    try:
        # Criar cursor para executar a consulta
        cur = conn.cursor()

        # Executar a consulta
        cur.execute(sql)

        # Obter os resultados da consulta
        rows = cur.fetchall()

        # Fechar o cursor
        cur.close()

        # Mapear os resultados para um formato de dicionário
        data = [
            {
                "id_user": row[1],
                "date": row[2],
                "rating": row[3],
                "helpful": row[4]
            }
            for row in rows
        ]
        
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao realizar consulta: {error}")
        return []

# Função para exibir as estrelas de rating
def exibir_estrelas(rating):
    return html.Div([html.Span("*") for _ in range(rating)], style={"display": "inline-block"})

# Função que engloba todo o layout e a lógica da Consulta A
def consulta_a_layout():
    return dbc.Container(
        [
            # Botão para retornar ao menu principal no topo com o texto "Voltar"
            # Linha com o botão à esquerda e o título centralizado
            dbc.Row(
                [
                    # Coluna para o botão "Voltar" alinhado à esquerda
                    dbc.Col(
                        dcc.Link(dbc.Button("Voltar", color="secondary", size="sm"), href="/"),
                        width=2,  # Define a largura da coluna do botão
                        style={"textAlign": "left"}
                    ),
                    # Coluna para o título centralizado
                    dbc.Col(
                        html.H1(
                            "Consulta A - Comentários do Produto", 
                            style={"margin-bottom": "2.5rem", "margin-top": "1rem"}
                        ),
                        width=8,  # Define a largura da coluna do título
                        style={"textAlign": "center"}
                    ),
                ],
                className="mt-4 mb-4"
            ),

            # Input para inserir o ID do produto
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Input(id="input-produto-id", placeholder="Insira o ID do produto", type="number"), 
                        width=4
                    ),
                    dbc.Col(
                        dbc.Button("OK", id="submit-id", color="primary"), 
                        width=1
                    )
                ],
                justify="center",
                className="mb-4"
            ),

            # Área onde os comentários serão exibidos
            html.Div(id="comentarios")
        ]
    )

# Callback para processar o ID do produto e exibir os comentários (integração com a função de layout)
@app.callback(
    Output("comentarios", "children"),
    Input("submit-id", "n_clicks"),
    State("input-produto-id", "value")
)
def mostrar_comentarios(n_clicks, id_product):
    if n_clicks and id_product:
        comentarios = consulta_a(id_product)

        # Se a consulta não retornar resultados, exibe uma mensagem
        if not comentarios:
            return html.P(f"ID {id_product} não encontrado ou sem avaliações.", style={"textAlign": "center", "color": "red"})
        
        # Remover duplicatas (se necessário, caso não seja garantido pela consulta SQL)
        comentarios_unicos = {comentario["id_user"]: comentario for comentario in comentarios}.values()

        # Exibir os comentários formatados
        return [
            dbc.Card(
                dbc.CardBody([
                    html.Div([
                        html.Span(f"Usuário: {comentario['id_user']}")
                    ]),
                    html.P(f"Avaliado em {pd.to_datetime(comentario['date']).strftime('%d de %B de %Y')}", className="text-muted"),
                    exibir_estrelas(comentario["rating"]),  # Exibe estrelas
                    html.P(f"{comentario['helpful']} {'pessoas acharam' if comentario['helpful'] > 1 else 'pessoa achou'} isso útil")
                ]), className="mb-3"
            )
            for comentario in comentarios_unicos
        ]
    return html.P("Insira o ID do produto e clique em OK para ver os comentários.", style={"textAlign": "center"})

# Função para realizar a consulta SQL no banco de dados para a Consulta B
def consulta_b(id_product):
    global conn
    try:
        # Consulta para obter o nome e salesrank do produto principal
        sql_produto = f'''select title, salesrank from produto where id = {id_product};'''
        cur = conn.cursor()

        cur.execute(sql_produto)
        produto_info = cur.fetchone()

        if produto_info is None:
            return {"produto_nao_encontrado": True}, []

        # Extrai o título e salesrank do produto principal
        nome_produto, salesrank_produto = produto_info

        # Consulta para obter os produtos similares com mais vendas (salesrank menor)
        sql_similares = f'''
            select produto.id, produto.title, produto.salesrank
            from produto
            join similares on produto.asin = similares.asinsimilar
            where similares.asinpai = (select asin from produto where id = {id_product})
            and produto.salesrank > {salesrank_produto}
            order by produto.salesrank asc;
        '''

        cur.execute(sql_similares)
        similares = cur.fetchall()
        cur.close()

        return {"produto_nao_encontrado": False, "nome_produto": nome_produto, "salesrank_produto": salesrank_produto}, similares

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao realizar consulta: {error}")
        return {"produto_nao_encontrado": True}, []


# Função que engloba todo o layout e a lógica da Consulta B
def consulta_b_layout():
    return dbc.Container(
        [
            # Linha com o botão à esquerda e o título centralizado
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Link(dbc.Button("Voltar", color="secondary", size="sm"), href="/"),
                        width=2,
                        style={"textAlign": "left"}
                    ),
                    dbc.Col(
                        html.H1(
                            "Consulta B - Produtos Similares com Mais Vendas", 
                            style={"margin-bottom": "2rem", "margin-top": "1rem"}
                        ),
                        width=8,
                        style={"textAlign": "center"}
                    ),
                ],
                className="mt-4 mb-4"
            ),

            # Input para inserir o ID do produto
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Input(id="input-produto-id-b", placeholder="Insira o ID do produto", type="number"), 
                        width=4
                    ),
                    dbc.Col(
                        dbc.Button("OK", id="submit-id-b", color="primary"), 
                        width=1
                    )
                ],
                justify="center",
                className="mb-4"
            ),

            # Área onde a mensagem e a tabela serão exibidas
            html.Div(id="resultado-b")
        ]
    )


# Callback para processar o ID do produto e exibir os produtos similares com mais vendas
@app.callback(
    Output("resultado-b", "children"),
    Input("submit-id-b", "n_clicks"),
    State("input-produto-id-b", "value")
)
def mostrar_similares(n_clicks, id_product):
    if n_clicks and id_product:
        info_produto, similares = consulta_b(id_product)

        # Se o produto não for encontrado
        if info_produto["produto_nao_encontrado"]:
            return html.P(f"ID {id_product} não encontrado ou sem produtos similares.", style={"textAlign": "center", "color": "red"})

        # Se não houver produtos similares com mais vendas
        if not similares:
            return html.P([
                "O produto ",
                html.Span(f"{info_produto['nome_produto']}", style={"color": "blue"}),
                " com classificação ",
                html.Span(f"{info_produto['salesrank_produto']}", style={"color": "blue"}),
                " não possui produtos similares com mais vendas."
            ], style={"textAlign": "center"}), 

        # Tabela com os resultados dos produtos similares
        tabela = dbc.Table(
            [
                html.Thead(
                    html.Tr([html.Th("ID do Produto"), html.Th("Nome do Produto"), html.Th("Classificação")])
                ),
                html.Tbody([
                    html.Tr([html.Td(similar[0]), html.Td(similar[1]), html.Td(similar[2])]) for similar in similares
                ])
            ],
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
        )

        # Mensagem e tabela
        return html.Div([
            html.P([
                "O produto ",
                html.Span(f"{info_produto['nome_produto']}", style={"color": "blue"}),
                " com classificação ",
                html.Span(f"{info_produto['salesrank_produto']}", style={"color": "blue"}),
                " tem os seguintes produtos similares com mais vendas:"
            ]),            
            tabela
        ])
    
    return html.P("Insira o ID do produto e clique em OK para ver os produtos similares.", style={"textAlign": "center"})

# Função para realizar a consulta SQL no banco de dados para a Consulta C
def consulta_c(id_product):
    global conn
    try:
        # Consulta SQL para calcular a média diária e acumulada das avaliações
        sql = f'''
            select data, count(*) as quantidade_de_reviews, 
            round(avg(rating), 4) as media_avaliacao_dia,
            round(AVG(AVG(rating)) OVER (ORDER BY data), 4) AS media_acumulada
            from review
            where idproduct = {id_product}
            group by data
            order by data;
        '''
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()

        # Retornar os dados como lista de dicionários
        data = [
            {
                "date": row[0],
                "quantidade_de_reviews": row[1],
                "media_avaliacao_dia": row[2],
                "media_acumulada": row[3]
            }
            for row in result
        ]
        return data

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao realizar consulta: {error}")
        return []

# Função que engloba todo o layout e a lógica da Consulta C
def consulta_c_layout():
    return dbc.Container(
        [
            # Linha com o botão à esquerda e o título centralizado
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Link(dbc.Button("Voltar", color="secondary", size="sm"), href="/"),
                        width=2,
                        style={"textAlign": "left"}
                    ),
                    dbc.Col(
                        html.H1(
                            "Consulta C - Evolução Diária das Avaliações", 
                            style={"margin-bottom": "2rem", "margin-top": "1rem"}
                        ),
                        width=8,
                        style={"textAlign": "center"}
                    ),
                ],
                className="mt-4 mb-4"
            ),

            # Input para inserir o ID do produto
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Input(id="input-produto-id-c", placeholder="Insira o ID do produto", type="number"), 
                        width=4
                    ),
                    dbc.Col(
                        dbc.Button("OK", id="submit-id-c", color="primary"), 
                        width=1
                    )
                ],
                justify="center",
                className="mb-4"
            ),

            # Área onde o gráfico será exibido (inicialmente oculto)
            dcc.Graph(id="grafico-c", style={"display": "none"}),

            # Área onde as mensagens de erro serão exibidas
            html.Div(id="mensagem-erro-c", style={"textAlign": "center", "color": "red"})
        ]
    )

@app.callback(
    [Output("grafico-c", "figure"), Output("grafico-c", "style"), Output("mensagem-erro-c", "children")],
    Input("submit-id-c", "n_clicks"),
    State("input-produto-id-c", "value")
)
def mostrar_evolucao_avaliacoes(n_clicks, id_product):
    if n_clicks and id_product:
        dados = consulta_c(id_product)

        # Se não houver dados para o produto, mostrar mensagem de erro e ocultar o gráfico
        if not dados:
            return {}, {"display": "none"}, f"ID {id_product} não encontrado ou sem avaliações."

        # Criar DataFrame a partir dos dados
        df = pd.DataFrame(dados)

        # Definir a quantidade de avaliações e ajustar o singular/plural
        num_avaliacoes = len(df)
        avaliacao_plural = "avaliação" if num_avaliacoes == 1 else "avaliações"

        # Criar o gráfico de linha para mostrar a média diária e acumulada
        fig = {
            "data": [
                {"x": df["date"], "y": df["media_avaliacao_dia"], "type": "line", "name": "Média Diária"},
                {"x": df["date"], "y": df["media_acumulada"], "type": "line", "name": "Média Acumulada"}
            ],
            "layout": {
                "title": f"Evolução das Avaliações do Produto {id_product} que possui {num_avaliacoes} {avaliacao_plural}",
                "xaxis": {"title": "Data"},
                "yaxis": {"title": "Média de Avaliações"}
            }
        }

        # Se há dados, exibir o gráfico e limpar qualquer mensagem de erro
        return fig, {"display": "block"}, ""

    # Caso não tenha sido clicado ainda, ocultar o gráfico
    return {}, {"display": "none"}, "Insira o ID do produto e clique em OK para ver a evolução das avaliações."


# Função para criar um card (aqui fica o layout dos cards)
def criarCard(title, subtitle, text, link1, href_link):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="card-title"),
            html.H6(subtitle, className="card-subtitle mb-2 text-body-secondary"),
            html.P(text, className="card-text"),
            html.A(link1, href=href_link, className="card-link"),
        ]),
        style={"height": "12rem"}  # Definir altura padrão para todos os cards
    )

# Página principal (dashboard com cards)
def layout_principal():
    return dbc.Container(
        [
            html.H1(
                "Dashboard de Consultas Produtos Amazon", 
                style={"textAlign": "center", "margin-bottom": "2.5rem", "margin-top": "1rem"}
            ),

            dbc.Row(
                [
                    dbc.Col(criarCard("Consulta A", "Produto", "5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação", "Consultar", "/consulta-a"), xs=12, sm=6, md=4, lg=3, className="mb-4"),
                    dbc.Col(criarCard("Consulta B", "Produto", "Produtos similares com maiores vendas do que o produto fornecido", "Consultar", "/consulta-b"), xs=12, sm=6, md=4, lg=3, className="mb-4"),
                    dbc.Col(criarCard("Consulta C", "Produto", "Evolução diária das médias de avaliação ao longo do intervalo de tempo do arquivo de entrada", "Consultar", "/consulta-c"), xs=12, sm=6, md=4, lg=3, className="mb-4"),
                    dbc.Col(criarCard("Consulta D", "Listagem", "10 produtos líderes de venda em cada grupo de produtos", "Consultar", "/consulta-d"), xs=12, sm=6, md=4, lg=3, className="mb-4"),
                ],
                className="g-4",
            ),
            dbc.Row(
                [
                    dbc.Col(criarCard("Consulta E", "Listagem", "10 produtos com a maior média de avaliações úteis positivas por produto", "Consultar", "/consulta-e"), xs=12, sm=6, md=4, lg=3, className="mb-4"),
                    dbc.Col(criarCard("Consulta F", "Listagem", "5 categorias de produto com a maior média de avaliações úteis positivas por produto", "Consultar", "/consulta-f"), xs=12, sm=6, md=4, lg=3, className="mb-4"),
                    dbc.Col(criarCard("Consulta G", "Listagem", "10 clientes que mais fizeram comentários por grupo de produto", "Consultar", "/consulta-g"), xs=12, sm=6, md=4, lg=3, className="mb-4"),
                ],
                className="g-4",
            ),
        ],
        fluid=True 
    )

# Callback para alternar entre as páginas
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)

def display_page(pathname):
    if pathname == '/consulta-a':
        return consulta_a_layout()
    elif pathname == '/consulta-b':
        return consulta_b_layout()
    elif pathname == '/consulta-c':
        return consulta_c_layout()
    else:
        return layout_principal()

# Layout da aplicação com controle de navegação
app.layout = dbc.Container(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ],
    fluid=True
)

# Função principal
def main():
    global conn
    conn = conectarAoBanco()
    if conn:
        # Crie o esquema e processe o arquivo se necessário
        print("Banco de dados pronto para consultas.")
    else:
        print("Falha ao conectar ao banco.")

# Rodar a aplicação
if __name__ == '__main__':
    main()
    app.run_server(debug=True)
