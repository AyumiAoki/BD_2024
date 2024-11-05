#include "BPlusTree.h"

#include "BPlusTree.h"

// Serialização do nó
void Node::serialize(ofstream& out) const {
    out.write(reinterpret_cast<const char*>(&isLeaf), sizeof(isLeaf));
    int keysSize = keys.size();
    out.write(reinterpret_cast<const char*>(&keysSize), sizeof(keysSize));
    for (int key : keys) out.write(reinterpret_cast<const char*>(&key), sizeof(key));
    
    int childrenSize = children.size();
    out.write(reinterpret_cast<const char*>(&childrenSize), sizeof(childrenSize));
    for (int childID : children) out.write(reinterpret_cast<const char*>(&childID), sizeof(childID));

    out.write(reinterpret_cast<const char*>(&nextLeafID), sizeof(nextLeafID));
}

// Desserialização do nó
void Node::deserialize(ifstream& in) {
    in.read(reinterpret_cast<char*>(&isLeaf), sizeof(isLeaf));
    int keysSize;
    in.read(reinterpret_cast<char*>(&keysSize), sizeof(keysSize));
    keys.resize(keysSize);
    for (int& key : keys) in.read(reinterpret_cast<char*>(&key), sizeof(key));

    int childrenSize;
    in.read(reinterpret_cast<char*>(&childrenSize), sizeof(childrenSize));
    children.resize(childrenSize);
    for (int& childID : children) in.read(reinterpret_cast<char*>(&childID), sizeof(childID));

    in.read(reinterpret_cast<char*>(&nextLeafID), sizeof(nextLeafID));
}

// Construtor da B+ Tree
BPlusTree::BPlusTree() {
    loadOrCreate();
}

void BPlusTree::loadOrCreate() {
    ifstream infile(FILENAME, ios::binary);
    if (!infile.is_open()) {
        ofstream outfile(FILENAME, ios::binary);
        Node root;
        rootID = saveNode(root);  // Salva raiz vazia no arquivo
        outfile.close();
    } else {
        infile.seekg(0, ios::end);
        if (infile.tellg() == 0) {
            Node root;
            rootID = saveNode(root);
        } else {
            rootID = 0;
        }
        infile.close();
    }
    nextNodeID = 1;
}

Node BPlusTree::loadNode(int nodeID) {
    if (cache.count(nodeID)) return cache[nodeID];

    Node node;
    ifstream infile(FILENAME, ios::binary);
    infile.seekg(nodeID * sizeof(Node), ios::beg);
    node.deserialize(infile);
    infile.close();

    cache[nodeID] = node;
    return node;
}

int BPlusTree::saveNode(const Node& node) {
    int nodeID = nextNodeID++;
    ofstream outfile(FILENAME, ios::binary | ios::in | ios::out);
    outfile.seekp(nodeID * sizeof(Node), ios::beg);
    node.serialize(outfile);
    outfile.close();
    return nodeID;
}

int BPlusTree::findLeaf(int key) {
    int cursorID = rootID;
    while (true) {
        Node cursor = loadNode(cursorID);
        if (cursor.isLeaf) return cursorID;

        int i = 0;
        while (i < cursor.keys.size() && key > cursor.keys[i]) i++;
        cursorID = cursor.children[i];
    }
}

void BPlusTree::insertInternal(int key, int nodeID, int childID) {
    Node parent = loadNode(nodeID);
    int pos = 0;
    while (pos < parent.keys.size() && key > parent.keys[pos]) pos++;

    parent.keys.insert(parent.keys.begin() + pos, key);
    parent.children.insert(parent.children.begin() + pos + 1, childID);

    if (parent.keys.size() == ORDER) {
        Node newInternal(false);
        int mid = ORDER / 2;

        newInternal.keys.assign(parent.keys.begin() + mid + 1, parent.keys.end());
        parent.keys.resize(mid);

        newInternal.children.assign(parent.children.begin() + mid + 1, parent.children.end());
        parent.children.resize(mid + 1);

        if (nodeID == rootID) {
            Node newRoot(false);
            newRoot.keys.push_back(parent.keys[mid]);
            newRoot.children.push_back(nodeID);
            newRoot.children.push_back(saveNode(newInternal));
            rootID = saveNode(newRoot);
        } else {
            insertInternal(parent.keys[mid], nodeID, saveNode(newInternal));
        }
    }
    saveNode(parent);
}

// Função para imprimir a árvore B+ Tree
void BPlusTree::printTree() {
    cout << "B+ Tree:" << endl;
    printNode(rootID, 0);
}

// Função para carregar dados de um CSV
void BPlusTree::loadFromCSV(const string& csvFilename) {
    ifstream csvFile(csvFilename);
    string line;

    while (getline(csvFile, line)) {
        stringstream ss(line);
        string field;
        vector<string> fields;

        // Separar cada campo pelo delimitador ";"
        while (getline(ss, field, ';')) {
            field.erase(remove(field.begin(), field.end(), '"'), field.end());
            fields.push_back(field);
        }

        if (fields.size() == 7) {
            int id = stoi(fields[0]);
            string title = fields[1];
            string year = fields[2];
            string authors = fields[3];
            string type = fields[4];
            string date = fields[5];
            string abstractText = fields[6];

            Article article(id, title);
            article.year = year;
            article.authors = authors;
            article.type = type;
            article.date = date;
            article.abstractText = abstractText;

            insert(article);
        }
    }
    csvFile.close();
}

// Função para inserir um artigo na árvore B+
void BPlusTree::insert(const Article& article) {
    int leafID = findLeaf(article.id);
    Node leaf = loadNode(leafID);

    leaf.keys.push_back(article.id);
    leaf.records.push_back(article);
    sort(leaf.keys.begin(), leaf.keys.end());

    if (leaf.keys.size() == ORDER) {
        Node newLeaf;
        int mid = ORDER / 2;

        newLeaf.keys.assign(leaf.keys.begin() + mid, leaf.keys.end());
        newLeaf.records.assign(leaf.records.begin() + mid, leaf.records.end());
        leaf.keys.resize(mid);
        leaf.records.resize(mid);

        newLeaf.nextLeafID = leaf.nextLeafID;
        leaf.nextLeafID = saveNode(newLeaf);

        if (leafID == rootID) {
            Node newRoot(false);
            newRoot.keys.push_back(newLeaf.keys[0]);
            newRoot.children.push_back(leafID);
            newRoot.children.push_back(leaf.nextLeafID);
            rootID = saveNode(newRoot);
        } else {
            insertInternal(newLeaf.keys[0], leafID, leaf.nextLeafID);
        }
    }

    saveNode(leaf);
}

// Função de busca por ID
bool BPlusTree::searchByID(int id, Article& result) {
    int leafID = findLeaf(id);
    Node leaf = loadNode(leafID);

    for (size_t i = 0; i < leaf.keys.size(); i++) {
        if (leaf.keys[i] == id) {
            result = leaf.records[i];
            return true;
        }
    }
    return false;
}

// Função de busca por título
bool BPlusTree::searchByTitle(const string& title, Article& result) {
    int cursorID = rootID;
    while (true) {
        Node cursor = loadNode(cursorID);
        if (cursor.isLeaf) {
            for (const Article& article : cursor.records) {
                if (article.title == title) {
                    result = article;
                    return true;
                }
            }
            return false;
        }

        int i = 0;
        while (i < cursor.keys.size() && title > cursor.records[i].title) i++;
        cursorID = cursor.children[i];
    }
}

void BPlusTree::printNode(int nodeID, int level) {
    Node node = loadNode(nodeID);

    cout << string(level * 4, ' ') << (node.isLeaf ? "Leaf" : "Internal") << " Node: ";
    for (int key : node.keys) cout << key << " ";
    cout << endl;

    if (node.isLeaf) {
        for (const auto& record : node.records) {
            cout << string(level * 4 + 4, ' ') << "ID: " << record.id 
                 << ", Title: " << record.title << endl;
        }
    } else {
        for (int childID : node.children) {
            printNode(childID, level + 1);
        }
    }
}
