#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
#get data from the website, synonymer.se
def get_data(word):
    url = "https://www.synonymer.se/sv-syn/"
    url = url + word
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup
 

def get_synonyms(soup):
    synonyms = []
    for synonym in soup.select('p[class*="synonymer-li-underline"]'):
        synonyms.append(synonym.text)
    return synonyms

def convert_to_string(synonyms):
    synonym_string = []
    
    # Check if synonyms is None
    if synonyms is None:
        return synonym_string  # Return an empty list if synonyms is None
    
    # Check if synonyms is a list
    if isinstance(synonyms, list):
        for synonym_list in synonyms:
            synonyms_split = synonym_list.split(",")
            for synonym in synonyms_split:
                synonym_string.append(synonym.strip())  # Remove leading/trailing spaces
    else:
        # If synonyms is a single string, split it directly
        synonyms_split = synonyms.split(",")
        for synonym in synonyms_split:
            synonym_string.append(synonym.strip())  # Remove leading/trailing spaces
    
    return synonym_string


def get_first(numberOfSynonyms, synonyms):
    #print(synonyms)
    counter = 0
    first_synonyms = []
    for synonym in synonyms:
        counter += 1
        if counter <= numberOfSynonyms:
            if("\n" in synonym):
                synonym = synonym.replace("\n", "")
            first_synonyms.append(synonym)
        else:
            break

    return first_synonyms

def read_inputfile():
    input_words = []
    with open("input.txt", "r") as file:
        for line in file:
            if(line == "\n"):
                continue
            input_words.append(line.strip())

    return input_words

#Kollar om det finns liknande ord.
def exsists_simillary_words(word):
    soup = get_data(word)
    for synonym in soup.find_all('h2'):
        if synonym.text == "Du kanske menade:":
            #Kallar på hämta liknande ord.

            for synonym in soup.find_all('a', class_="underline", limit=1):
                new_synonym = synonym.text
            soup =  get_data(new_synonym)

        return str(new_synonym)
        
def print_tofile(word, first_synonyms):
    with open("output.txt", "a") as file:
        file.write(word + ": " + str(first_synonyms) + "\n")       

def main():
    with open("output.txt", "w") as file:
        file.write("")
    file.close()
    #Läs in data från text fil.
    input_words = read_inputfile()
    for word in input_words:
        try:
            #Hämta data för ordet.    
            soup = get_data(word)
            #Hämta synonymer för ordet.
            synonyms = get_synonyms(soup)
            if synonyms is None:
                print("The word does not exsist")
                continue
            #Om det inte finns några synonymer, kolla om det finns liknande ord.
            if(len(synonyms) == 0):
                new_synonym = exsists_simillary_words(word)
                new_soup = get_data(new_synonym)
                synonyms = get_synonyms(new_soup)
    
            synonym_string = convert_to_string(synonyms)
            first_synonyms = get_first(3, synonym_string)
            print(word + ": " + str(first_synonyms))
            print_tofile(word, first_synonyms)
        except:
            print(word + ": The word does not exsist")
    #Catch execption if the word does not exsist
    

if __name__ == "__main__":
    main()