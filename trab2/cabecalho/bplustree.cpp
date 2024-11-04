#include "BPlusTree.h"

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

// Função para imprimir a árvore
void BPlusTree::printTree() {
    cout << "B+ Tree:" << endl;
    printNode(rootID, 0);
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
