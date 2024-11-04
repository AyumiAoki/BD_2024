/*
 * Autores: Ayumi, Erllison, Maria Luiza
 * Descrição: Este programa busca diretamente no arquivo de dados por um registro com o ID informado,
 * retornando os campos do registro, a quantidade de blocos lidos e a quantidade total de blocos do arquivo.
 */

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstring>
#include "./cabecalho/tabelaHash.cpp"

int posBlocks[NUM_BUCKETS] = {0};
int numRowBucket[NUM_BUCKETS] = {0};
int tamListBlocks[NUM_BUCKETS] = {0};


using namespace std;

/**
 * Função que busca diretamente no arquivo de dados um registro com o ID informado.
 * 
 * Implementação da busca direta no arquivo de dados por hashing.
 * 
 * @param ID Identificador do registro a ser buscado
 */
void findrec(const std::string &nomeArquivo, int ID) {

    std::ifstream arquivo(nomeArquivo, std::ios::binary);
    if (!arquivo.is_open()) {
        std::cerr << "Erro ao abrir o arquivo " << nomeArquivo << "." << std::endl;
        return;
    }

    int bucket = calcularHash(ID);

    arquivo.seekg(bucket * NUM_BLOCKS * MAX_BLOCK_SIZE);

    char block[4096];

    int numLinhas = 0;
    arquivo.read(reinterpret_cast<char *>(block), 4096);
    std::memcpy(&numLinhas, block, sizeof(int));
    arquivo.seekg(bucket * NUM_BLOCKS * MAX_BLOCK_SIZE);

    int linhasLidas = 0;
    int blocosLidos = 0;

    while (arquivo.read(reinterpret_cast<char *>(block), 4096) && linhasLidas < numLinhas) {
    blocosLidos++;
        int posBloco = blocosLidos == 1 ? sizeof(int) : 0;

        do {

            if (posBloco >= 4096 || linhasLidas > numLinhas) {
                break;
            }
            TableRow entrada;
            linhasLidas++;
            std::memcpy(&entrada.id, block + posBloco, sizeof(entrada.id));
            posBloco += sizeof(entrada.id);

            if (entrada.id == -1) { break; }

            std::memcpy(&entrada.titulo, block + posBloco, sizeof(entrada.titulo));
            posBloco += sizeof(entrada.titulo);
            std::memcpy(&entrada.ano, block + posBloco, sizeof(entrada.ano));
            posBloco += sizeof(entrada.ano);
            std::memcpy(&entrada.autores, block + posBloco, sizeof(entrada.autores));
            posBloco += sizeof(entrada.autores);
            std::memcpy(&entrada.citacoes, block + posBloco, sizeof(entrada.citacoes));
            posBloco += sizeof(entrada.citacoes);
            std::memcpy(&entrada.atualizacao, block + posBloco, sizeof(entrada.atualizacao));
            posBloco += sizeof(entrada.atualizacao);
            int tamSnippet;
            std::memcpy(&tamSnippet, block + posBloco, sizeof(tamSnippet));
            posBloco += sizeof(tamSnippet);
            entrada.snippet = std::string(block + posBloco, tamSnippet);
            posBloco += sizeof(char) * tamSnippet;

            if (ID == entrada.id) {
                printTableRow(entrada);
                std::cout << "------------------------------------" << std::endl;
                std::cout << "Bloco lido: " << blocosLidos << std::endl;
                std::cout << "Blocos totais: " << MAX_BLOCK_SIZE * NUM_BLOCKS << std::endl;
                return;
            }
        } while (true);
    }
    int posBloco = 0;
    while (linhasLidas <= numLinhas)
    {
        if (posBloco >= 4096)
        {
            break;
        }
        TableRow entrada;
        linhasLidas++;
        std::memcpy(&entrada.id, block + posBloco, sizeof(entrada.id));
        posBloco += sizeof(entrada.id);

        if (entrada.id == -1)
        {
            break;
        }
        std::memcpy(&entrada.titulo, block + posBloco, sizeof(entrada.titulo));
        posBloco += sizeof(entrada.titulo);
        std::memcpy(&entrada.ano, block + posBloco, sizeof(entrada.ano));
        posBloco += sizeof(entrada.ano);
        std::memcpy(&entrada.autores, block + posBloco, sizeof(entrada.autores));
        posBloco += sizeof(entrada.autores);
        std::memcpy(&entrada.citacoes, block + posBloco, sizeof(entrada.citacoes));
        posBloco += sizeof(entrada.citacoes);
        std::memcpy(&entrada.atualizacao, block + posBloco, sizeof(entrada.atualizacao));
        posBloco += sizeof(entrada.atualizacao);
        int tamSnippet;
        std::memcpy(&tamSnippet, block + posBloco, sizeof(tamSnippet));
        posBloco += sizeof(tamSnippet);
        entrada.snippet = std::string(block + posBloco, tamSnippet);
        posBloco += sizeof(char) * tamSnippet;

        if (ID == entrada.id)
        {
            printTableRow(entrada);
            std::cout << "------------------------------------" << std::endl;
            std::cout << "Bloco lido: " << blocosLidos << std::endl;
            std::cout << "Blocos totais: " << MAX_BLOCK_SIZE * NUM_BLOCKS << std::endl;
            return;
        }
    }
    std::cout << numLinhas << std::endl;
    std::cout << linhasLidas << std::endl;

    std::cout << "Registro não encontrado" << std::endl;
    arquivo.close();
}


int main(int argc, char* argv[]) {
     if (argc != 2) {
        std::cerr << "Uso: " << argv[0] << " <nome_do_arquivo.csv>" << std::endl;
        return 1;
    }

    int ID = stoi(argv[1]);
    findrec(nameFileHash, ID);
    return 0;
}
