import requests 
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
import inflect
from googletrans import Translator

def merriamSynonym(word):
    r = requests.get("https://www.merriam-webster.com/dictionary/{}".format(word))
    soup = BeautifulSoup(r.content, "html.parser")
    sth = soup.find("ul",attrs={"class":"mw-list"})
    sth = str(sth)
    new = ''
    start = 0
    for i in range(len(sth)):
        if sth[i] == '>':
            start += 1
        elif start == 3 and sth[i] == '<':
            break
        elif start == 3:
            new += sth[i]
    return new

def merriamDefinition(word):
    r = requests.get("https://www.merriam-webster.com/dictionary/{}".format(word))
    soup = BeautifulSoup(r.content, "html.parser")
    mean = soup.find("span",attrs={"class":"dtText"}).text
    
    mean = clearSentence(mean)
    return mean

def replaceWithSynonyms(sentence):
    tokenized = nltk.word_tokenize(sentence)
    pos = nltk.pos_tag(tokenized)

    result = []
    for token in tokenized:
        nt = merriamSynonym(token)
        if nt != '' and (' ' not in nt):
            result.append(nt)
        else:
            result.append(token)
    #print(result)
    #print(pos)
    pos2 = nltk.pos_tag(result)
    #print(pos2)
    newSentence = ''
    for i in range(len(pos)):
        if pos[i][1] == 'IN':
        
            if pos[i][1] == pos2[i][1]:
                newSentence += pos2[i][0] + ' '
            else:
                newSentence += pos[i][0] + ' '
        else:
            newSentence += pos2[i][0] + ' '
            
    newSentence[:-1]
    return newSentence


def clearSentence(sentence):
    print('Original:\n', sentence)
    if sentence[0] == ':':
        sentence = sentence[1:]
    sentence = sentence.strip()
    print('stripped: \n', sentence)
    paranthesesDepth = 0
    newSentence = ''
    problematic = False
    for i in range(len(sentence)):
        if problematic and sentence[i] == ' ':
            problematic = False
            continue
        if sentence[i] == '(':
            paranthesesDepth += 1
        elif sentence[i] == ')':
            paranthesesDepth -= 1
            if paranthesesDepth == 0:
                problematic = True

        elif paranthesesDepth == 0:
            if sentence[i] == ':' or sentence[i] == ';' or sentence[i] == '—' or sentence[i] == '\n':
                break
            else:
                newSentence += sentence[i]
        
        
            
    print('Result: \n', newSentence)
    return newSentence

def trimSentence(sentence):
    print('Original: \n', sentence)
    foundIndex = None
    amisare = ('am', 'is', 'are', 'was', 'were')
    dt = ('a', 'an', 'the')
    words = nltk.word_tokenize(sentence)
    pos = nltk.pos_tag(words)
    for i in range(len(pos)):
        if pos[i][0] in amisare:
            # Dangerous assumption
            if pos[i + 1][0] in dt:
                foundIndex = i + 1
            else:
                print(pos[i + 1][0])
                foundIndex = i
            break

    result = ''
    if foundIndex == None:
        if pos[0][1] == 'DT':
            foundIndex = 0
        else:
            foundIndex = -1
        
    for i in range(foundIndex + 1, len(words)):
        if words[i] == 'sense' and i + 1 < len(words) and words[i+1].isdigit():
            break
        result += words[i] + ' '
    result = result[:-1]
            
    print('trimResult: ', result)
    return result

def getTogether(words):
    result = ''
    punctuation = (',', '.')
    for word in words:
        if word in punctuation:
            result += word
        else:
            result += (' ' + word)
    return result.strip()

def firstCapitalize(sentence):
    return sentence[0].upper() + sentence[1:]

def merriamExample(word):
    r = requests.get("https://www.merriam-webster.com/dictionary/{}".format(word))
    soup = BeautifulSoup(r.content, "html.parser")
    sth = soup.find("span",attrs={"class":"ex-sent"}).text
    return sth


def make_plural(words):
   
    pos_tags = nltk.pos_tag(words)

    first_noun_index = None
    for i in range(len(words)):
        if 'NN' in pos_tags[i][1]:
            engine = inflect.engine()
            words[i] = engine.plural(words[i])
            first_noun_index = i
            break
    if first_noun_index != None:
        for i in range( first_noun_index, len(words)):
            print('yead: ', pos_tags[i][1])
            if 'VB' in pos_tags[i][1]:
                if words[i][len(words[i]) - 4:len(words[i]) - 1] == 'ies':
                    words[i] = words[i][:-3] + 'y'
                elif words[i][len(words[i]) - 5:len(words[i]) - 1] == 'sses':
                    words[i] = words[i][:-3]
                elif words[i][len(words[i]) - 1] == 's':
                    words[i] = words[i][:-1]
                break
    #if first_noun_index != None:
        

def foreign_clue( word):
    translator = Translator()
    translation_result = translator.translate(word)
    if translation_result.text != word:
        return (translation_result.text + ' (' + translation_result.src.capitalize() + ')').capitalize()
    else:
        return None