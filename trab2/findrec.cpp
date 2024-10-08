/*
 * Autores: Ayumi, Erllison, Maria Luiza
 * Descrição: Este programa busca diretamente no arquivo de dados por um registro com o ID informado,
 * retornando os campos do registro, a quantidade de blocos lidos e a quantidade total de blocos do arquivo.
 */

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

/**
 * Função que busca diretamente no arquivo de dados um registro com o ID informado.
 * 
 * Implementação da busca direta no arquivo de dados por hashing.
 * 
 * @param ID Identificador do registro a ser buscado
 */
void findrec(int ID) {
    cout << "Buscando registro com ID: " << ID << endl;

    // Simulação da busca e saída dos resultados.
    // Aqui vai a lógica de leitura do arquivo de dados e contagem de blocos lidos.
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Uso: findrec <ID>" << endl;
        return 1;
    }
    int ID = stoi(argv[1]);
    findrec(ID);
    return 0;
}
