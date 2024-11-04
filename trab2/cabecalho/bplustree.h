#ifndef BPLUSTREE_H
#define BPLUSTREE_H

#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <string>
#include <sstream>

using namespace std;

const int ORDER = 4;
const string FILENAME = "bplustree.dat";

struct Article {
    int id;
    string title;
    string year;
    string authors;
    string type;
    string date;
    string abstractText;

    Article(int id = 0, string title = "") : id(id), title(title) {}
};

struct Node {
    bool isLeaf;
    vector<int> keys;  // IDs como chave principal
    vector<int> children;
    int nextLeafID;

    vector<Article> records; // Registros com dados completos para folhas

    Node(bool leaf = true) : isLeaf(leaf), nextLeafID(-1) {}

    void serialize(ofstream& out) const;
    void deserialize(ifstream& in);
};

class BPlusTree {
public:
    BPlusTree();
    void insert(const Article& article);
    bool searchByID(int id, Article& result);
    bool searchByTitle(const string& title, Article& result);
    void loadFromCSV(const string& csvFilename);
    void printTree();

private:
    int rootID;
    unordered_map<int, Node> cache;
    int nextNodeID;

    void loadOrCreate();
    Node loadNode(int nodeID);
    int saveNode(const Node& node);
    int findLeaf(int key);
    void insertInternal(int key, int nodeID, int childID);
    void printNode(int nodeID, int level);
};

#endif
