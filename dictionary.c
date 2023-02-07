// Implements a dictionary's functionality
#include <strings.h>
#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include "dictionary.h"
#include <stdio.h>
#include <stdlib.h>

//count the size of the dict
int count = 0;
// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 10000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);
    //search through the hash with the same index;
    node *cursor = table[index];
    //searching though the whole hash table;
    while (cursor != NULL)
    {
        if (strcasecmp(cursor-> word, word) == 0) //found
        {
            return true;
        }
        else //not found
        {
            cursor = cursor-> next; //move the pointer to the next word;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    long number = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        number += tolower(word[i]);
    }
    return number % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char new_word[LENGTH + 1]; //to put data in
    //open the dictionary
    FILE *input = fopen(dictionary, "r");

    //scan a dict
    if (input == NULL)
    {
        return false;
    }
    //creating an empty values for the table
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    while (fscanf(input, "%s", new_word) != EOF)
    {
        //allocate as much place as needed for the particular word
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }
        //copy
        strcpy(n-> word, new_word);
        //hash function + fidning the index;
        int index = hash(new_word);
        //point to the linked arrays
        n-> next = table[index];
        if (table[index] == NULL)
        {
            n->next = NULL;
            table[index] = n;
        }
        else
        {
            n-> next = table[index];
            table[index] = n;
        }
        count++;
    }
    fclose(input);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor-> next;
            free(temp);
        }
        table[i] = NULL;
    }
    return true;
}
