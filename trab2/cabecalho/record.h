#ifndef RECORD_H
#define RECORD_H

#include <string>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <iostream>
#include <fstream>
#include <sstream>
#include "bplustree.h"

using namespace std;

struct Record {
    int id;
    string titulo;
    int ano;
    string autores;
    int citacoes;
    string atualizacao;
    string snippet;

    Record(int id, const string& titulo, int ano, const string& autores, int citacoes, const string& atualizacao, const string& snippet)
        : id(id), titulo(titulo), ano(ano), autores(autores), citacoes(citacoes), atualizacao(atualizacao), snippet(snippet) {}
};

// Função para remover aspas de uma string
void removeQuotes(string& str) {
    str.erase(remove(str.begin(), str.end(), '\"'), str.end());
}

// Verifica se uma string pode ser convertida para inteiro
bool isInteger(const string& str) {
    for (char const &c : str) {
        if (!isdigit(c)) {
            return false;
        }
    }
    return true;
}

// Função para carregar dados CSV
void loadCSV(const string& filename, vector<Record>& records, BPlusTree& btree);

#endif // RECORD_H
