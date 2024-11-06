/*
 * Autores: Ayumi, Erllison, Maria Luiza
 * Descrição: Este programa pesquisa um registro através do arquivo de índice secundário (B+Tree)
 * com base no Título fornecido, retornando os dados do registro e informações sobre os blocos lidos.
 */

#include <iostream>
#include <fstream>
#include <string>
#include "bplustree.h"

using namespace std;

/**
 * Função que busca um registro pelo índice secundário (B+Tree) com base no Título informado.
 * 
 * Implementação da busca usando o índice secundário (B+Tree).
 * 
 * @param Titulo Título do registro a ser buscado
 */
void seek2(const string& Titulo) {
    
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Uso: seek2 <Titulo>" << endl;
        return 1;
    }
    string Titulo = argv[1];
    seek2(Titulo);
    return 0;
}
