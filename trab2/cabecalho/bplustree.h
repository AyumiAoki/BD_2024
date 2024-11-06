#ifndef BPLUSTREE_H
#define BPLUSTREE_H

#include <vector>
#include <iostream>
#include <algorithm>

using namespace std;

struct BPlusTreeNode {
    bool isLeaf;
    vector<int> keys;
    vector<int> values;  
    vector<BPlusTreeNode*> children;

    BPlusTreeNode(bool isLeaf = false) : isLeaf(isLeaf) {}
};

class BPlusTree {
private:
    BPlusTreeNode* root;
    int order;
    int totalBlocks; // Total de blocos
    int blocksRead;  // Blocos lidos durante a busca

public:
    BPlusTree(int order) : order(order), totalBlocks(1), blocksRead(0) {
        root = new BPlusTreeNode(true);  
    }

    void insert(int key, int value) {
        BPlusTreeNode* leaf = findLeafNode(root, key);
        //cout << "Attempting to insert key: " << key << " at position in leaf node.\n";
        insertInLeaf(leaf, key, value);
    }

    BPlusTreeNode* findLeafNode(BPlusTreeNode* node, int key) {
        blocksRead++;  // Incrementa o contador de blocos lidos
        if (node->isLeaf) {
            return node;
        }
        for (size_t i = 0; i < node->keys.size(); ++i) {
            if (key < node->keys[i]) {
                return findLeafNode(node->children[i], key);
            }
        }
        return findLeafNode(node->children.back(), key);
    }

    void insertInLeaf(BPlusTreeNode* leaf, int key, int value) {
        auto it = lower_bound(leaf->keys.begin(), leaf->keys.end(), key);
        if (it == leaf->keys.end() || *it != key) {
            int position = it - leaf->keys.begin();
            //cout << "Inserting key: " << key << " at position " << position << endl;
            leaf->keys.insert(it, key);
            leaf->values.insert(leaf->values.begin() + position, value);
        } else {
            //cout << "Key " << key << " already exists in the leaf node. Skipping insertion.\n";
        }

        // Simulação de divisão do nó (split), incrementa total de blocos se houver divisão.
        if (leaf->keys.size() > order) {
            totalBlocks++; // Simula o incremento do total de blocos ao dividir o nó
        }
    }

    int search(int key) {
        blocksRead = 0; // Reseta o contador antes da busca
        BPlusTreeNode* leaf = findLeafNode(root, key);
        auto it = lower_bound(leaf->keys.begin(), leaf->keys.end(), key);
        if (it != leaf->keys.end() && *it == key) {
            return leaf->values[it - leaf->keys.begin()];
        }
        return -1;
    }

    int getBlocksRead() const { return blocksRead; }
    int getTotalBlocks() const { return totalBlocks; }
};

#endif // BPLUSTREE_H
