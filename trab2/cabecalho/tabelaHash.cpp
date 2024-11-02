#include <string>
#include <iostream>

// Definição da estrutura TableRow para armazenar informações de uma linha da tabela
struct TableRow {
    int id;
    char titulo[300];
    int ano;
    char autores[150];
    int citacoes;
    char atualizacao[20];
    std::string snippet;
};

// Constantes usadas para o tamanho máximo de bloco, número de buckets e número de blocos
constexpr int MAX_BLOCK_SIZE = 4096;
constexpr int NUM_BUCKETS = 12101;
constexpr int NUM_BLOCKS = 23;

// Nome do arquivo onde a tabela hash será armazenada
const std::string nameFileHash = "hash_table.dat";

// Função para imprimir os detalhes de um TableRow
void printTableRow(const TableRow &row) {
    std::cout << "ID: " << row.id << std::endl;
    std::cout << "Título: " << row.titulo << std::endl;
    std::cout << "Ano: " << row.ano << std::endl;
    std::cout << "Autores: " << row.autores << std::endl;
    std::cout << "Citações: " << row.citacoes << std::endl;
    std::cout << "Atualização: " << row.atualizacao << std::endl;
    std::cout << "Snippet: " << row.snippet << std::endl;
}

// Função para calcular o hash de um número, retornando um índice para a tabela hash
int calcularHash(int numero) {
    return (numero % NUM_BUCKETS);
}
