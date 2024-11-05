/*
 * Autores: Ayumi, Erllison, Maria Luiza
 * Descrição: Este programa pesquisa um registro através do arquivo de índice primário (B+Tree)
 * com base no ID fornecido, retornando os campos do registro e informações sobre os blocos lidos.
 */

#include <iostream>
#include <fstream>
#include <string>
#include "cabecalho/bplustree.h"

using namespace std;

/**
 * Função que busca um registro pelo índice primário (B+Tree) baseado no ID informado.
 * 
 * Implementação da busca usando o índice primário (B+Tree).
 * 
 * @param ID Identificador do registro a ser buscado
 */
void seek1(int ID) {
    cout << "Buscando registro no índice primário com ID: " << ID << endl;

    BPlusTree tree;

    tree.loadFromCSV("bplustree.dat");
    // Realizar busca por ID
    Article result;
    int searchID = 1;
    if (tree.searchByID(ID, result)) {
        cout << "Encontrado ID " << ID << ": " << result.title << endl;
    } else {
        cout << "ID " << ID << " não encontrado." << endl;
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Uso: seek1 <ID>" << endl;
        return 1;
    }
    int ID = stoi(argv[1]);
    seek1(ID);
    return 0;
}
