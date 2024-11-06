/*
 * Autores: Ayumi, Erllison, Maria Luiza
 * Descrição: Este programa pesquisa um registro através do arquivo de índice primário (B+Tree)
 * com base no ID fornecido, retornando os campos do registro e informações sobre os blocos lidos.
 */

#include <iostream>
#include <fstream>
#include <string>
#include "cabecalho/bplustree.h"
#include "cabecalho/record.h"


using namespace std;

void loadCSV(const string& filename, vector<Record>& records, BPlusTree& btree) {
    ifstream file(filename);
    string line;
    int id, ano, citacoes;
    string titulo, autores, atualizacao, snippet;

    while (getline(file, line)) {
        stringstream ss(line);
        string temp;

        getline(ss, temp, ';');
        removeQuotes(temp);
        if (!isInteger(temp)) {
            while (getline(ss, temp, ';')) {
                removeQuotes(temp);
                if (isInteger(temp)) break;
            }
        }
        id = stoi(temp);

        getline(ss, titulo, ';');
        removeQuotes(titulo);

        getline(ss, temp, ';');
        removeQuotes(temp);
        if (!isInteger(temp)) {
            while (getline(ss, temp, ';')) {
                removeQuotes(temp);
                if (isInteger(temp)) break;
            }
        }
        ano = stoi(temp);

        getline(ss, autores, ';');
        removeQuotes(autores);

        getline(ss, temp, ';');
        removeQuotes(temp);
        if (!isInteger(temp)) {
            while (getline(ss, temp, ';')) {
                removeQuotes(temp);
                if (isInteger(temp)) break;
            }
        }
        citacoes = stoi(temp);

        getline(ss, atualizacao, ';');
        removeQuotes(atualizacao);

        getline(ss, snippet);
        removeQuotes(snippet);

        Record record(id, titulo, ano, autores, citacoes, atualizacao, snippet);
        records.push_back(record);
        btree.insert(id, records.size() - 1);
    }
}

void searchById(int searchId, const vector<Record>& records, BPlusTree& btree) {
    int recordIndex = btree.search(searchId);
    int blocksRead = btree.getBlocksRead();
    int totalBlocks = btree.getTotalBlocks();

    if (recordIndex == -1) {
        cout << "Registro com ID " << searchId << " não encontrado." << endl;
        cout << "Blocos lidos para busca: " << blocksRead << endl;
        cout << "Total de blocos no índice primário: " << totalBlocks << endl;
        return;
    }

    const Record& record = records[recordIndex];
    cout << "Registro encontrado: " << endl;
    cout << "ID: " << record.id << endl;
    cout << "Título: " << record.titulo << endl;
    cout << "Ano: " << record.ano << endl;
    cout << "Autores: " << record.autores << endl;
    cout << "Citações: " << record.citacoes << endl;
    cout << "Atualização: " << record.atualizacao << endl;
    cout << "Snippet: " << record.snippet << endl;
    cout << "Blocos lidos para busca: " << blocksRead << endl;
    cout << "Total de blocos no índice primário: " << totalBlocks << endl;
}

/**
 * Função que busca um registro pelo índice primário (B+Tree) baseado no ID informado.
 * 
 * Implementação da busca usando o índice primário (B+Tree).
 * 
 * @param ID Identificador do registro a ser buscado
 */
void seek1(int ID) {
    string filename = "artigo_menor.csv";
    vector<Record> records;
    BPlusTree btree(3);

    loadCSV(filename, records, btree);

    searchById(ID, records, btree);

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
