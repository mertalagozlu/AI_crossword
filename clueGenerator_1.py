from nltk.corpus import wordnet
import nltk
import inflect as infe
import wikipedia as wiki
import wikipediaapi as wiki2
import helperFunctions
from nltk import pos_tag
from nltk import RegexpParser
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.tag import UnigramTagger
import requests 
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

def createNewClue(originalClue, entry, clue_log):
    print('**********************************************************')
    print('STARTING: ', entry, '\n')

    entry = entry.lower()
    # porter = PorterStemmer()
    inflect = infe.engine()

    #assuming
    entry_pos = 'n'#The determination of word type from wordnet

    plural = True
    if inflect.singular_noun(entry) is False:# Plurality of entry
        plural = False

    # entry_present_tense=None
    # entry_past_tense= None

    # entry_is_noun= True
    # foreign = False
    tokens = nltk.pos_tag([entry])
    words_spec = tokens[0]
    # noun_pos = ('NN', 'NNS', 'NNP')
    #verb_pos
    print('words_spec', words_spec)

    # if words_spec[1] == 'FW':# NYT RULE #4 CHECKING FOREIGN WORDS
    #     foreign = True
    #     # check original clue
    # elif words_spec[1] in noun_pos:# given entry must corresponds to noun as well. Rule #2 NYT "PART OF SPEECH"
    #     entry_is_noun = True
    #     #print('generating a noun clue')if t[1] == 'VBD' or t[1] == 'VBN':# NYT RULE #1 TENSES MUST BE MATCHED, so we control the tense of the entry(word)
    #     entry_past_tense=1

  
        
        
        
    possibleClues=[]
    print('Starting the search in wordnet for ' + entry + '...\n')
    try:
        syns = wordnet.synsets(entry)
        entry_pos = wordnet.synsets(entry)[0].pos()

        try:
            print('Looking up definition in Wordnet')
            wn_def = helperFunctions.clearSentence(syns[0].definition())
            print('Wordnet definition: ', wn_def)
            possibleClues.append([wn_def,'wordnet_def'])
        except Exception as e:
            print(e)
            print('Definition not found in wordnet')
        try:            
            for example in syns[0].examples():
                print('Looking up example in Wordnet')
                wn_ex = helperFunctions.clearSentence(example)
                if entry.lower() in wn_ex.lower():
                    print('Wordnet example: ', wn_ex)
                    possibleClues.append([wn_ex,'wordnet_ex'])
                    
        except Exception as e:
            print(e)
            print('Example is not found in wordnet')

    except Exception as e:
        print(e)

    print('\nContinue searching with merriam-webster dictionary...\n')
    try:
        mw_def = helperFunctions.clearSentence(helperFunctions.merriamDefinition(entry))
        print('Marriam webster definition: ', mw_def)
        possibleClues.append([mw_def, "merriam"])
    except Exception as e:
        print(e)
        print('Webster could not find, right now!')

    print('\nContinue searching with wikipedia...\n')
    try:      
        p = wiki.search(entry,results=1,suggestion=False)
        wiki_sum = None
        if len(p) != 0:
            page = wiki.page(p[0])
            title = page.title
            print('title: ', title)
            if entry.lower() in [w.lower() for w in (nltk.word_tokenize(title))]:
                wiki_sum = helperFunctions.clearSentence(wiki.summary(p[0],sentences=1))
            else:
                wiki_wiki = wiki2.Wikipedia('en')
                p = wiki_wiki.page(entry)
                if p.exists():
                    wiki_sum = helperFunctions.clearSentence(nltk.sent_tokenize(p.summary)[0])
            if wiki_sum is not None:
                print('Wikipedia definition: ', wiki_sum)
                possibleClues.append([wiki_sum,'wiki'])
                
    except Exception as e:
        print(e)
        print("Not found in wikipedia")
        
    print('\nThese Clues are found: \n')
    print(possibleClues)

    def artificialnlp(sentence):
        add_parenthesis  = False
        parenthesis_content = None
        if 'VB' in words_spec[1] and entry_pos == 'v':# Check both libraries gives the same result
            if words_spec[1] == 'VBD'or words_spec[1] == 'VBN':
                add_parenthesis=True
                parenthesis_content = ' (Past)'
# =============================================================================
#         elif plural:
#             add_parenthesis=True
#             parenthesis_content = ' (Plural)'
# =============================================================================
                
            
        
        
        print('Lets see what we can do with: \n', sentence,'\n')
        
        
        print('Generating artificial noun phrases...')
    
        trimmed = helperFunctions.trimSentence(sentence[0])
        tokenized_possible_clue = nltk.word_tokenize(trimmed)
    
        tokens_tag = nltk.pos_tag(tokenized_possible_clue)#token tags of the tokenized possible clue
        print('Tokens: \n', tokens_tag)


        # If exists just trim
        if entry.strip().lower() in trimmed.lower():#Omitting
            if clue_log['fill_blank'] == 0:#clue log 
                retx = trimmed.replace(entry, '___')
                return [retx, 'fill_blank', sentence[1]]
            else:
                return None
        # Cannot Help jazzy -> resembling jazz -> NOT ACCEPTABLE AND CANNOT USE
        else:
            for i in nltk.word_tokenize(trimmed):
                if fuzz.ratio(i.lower(), entry.strip().lower()) > 85:
                    print('RETURNING NONE!!\n')
                    print('trimmed: ', i)
                    print('entry: ', entry, '\n')
                    return None

        #Don't do anything if already short
# =============================================================================
#         if len(tokenized_possible_clue) <= 5:
#             if add_parenthesis:
#                 return [trimmed + parenthesis_content, 'nc', sentence[1]]
#             else:
#                 if plural:
#                     helperFunctions.make_plural()
#                 return [trimmed, 'nc', sentence[1]]
# =============================================================================
                        
        verb_wait = False
        noun_wait = True
        noun_close = False
        skip = False
        proper = False
        noun_phrase_element=[]
        for parse in tokens_tag:# We successfully implement a meaninggul noun phrase for noun entry
            #print(parse)
            if parse[0][0].isupper():# If the possible clue has special name, do not omit 'and' within the special name
                proper = True
            elif parse[1] != 'CC':
                proper = False
            if 'JJ' in parse[1] and skip:
                continue
            elif skip:
                skip = False
            elif parse[1] == 'DT' or parse[1] == 'RB':
                continue
            elif parse[1] == ',' or parse[1] == '.':
                break
            elif parse[1] == 'CC' and not proper:
                skip = True
            elif len(noun_phrase_element) > 5 and parse[1][0] == 'V':
                break
            else:
                noun_phrase_element.append(parse[0])        
        if plural:
            helperFunctions.make_plural(noun_phrase_element)
            
        possibleClue = helperFunctions.getTogether(noun_phrase_element)

        newClue = None
        if entry_pos == 's' and sentence[1] == 'wiki':#adjective
            newClue= 'Like ' + possibleClue
        elif add_parenthesis:
            newClue= possibleClue + parenthesis_content
        else:
            newClue= possibleClue
            
        print('Artificalnlpre: \n', newClue)
        return [newClue, 'shortened', sentence[1]]
        
    l_np=[]
    for sentence in possibleClues:
        after = artificialnlp(sentence)
        if after == None:
            continue
        elif after[0].lower() not in originalClue.lower() and originalClue.lower() not in after[0].lower():
            l_np.append(after)   

    if len(l_np) > 0:
        closest=-1
        closest_len=999
        print('Candidate clues are: ')
        print(l_np)
        print('Choosing the optimal length...')
      
        for b in range(len(l_np)):
            distance = abs(len(originalClue)-len(l_np[b][0]))#distance from 18 characters, heuristic method applied as original clue chars
# =============================================================================
# # =============================================================================
# #             if l_np[b][2] == 'merriam':
# #                 closest = b
# #                 found_merriam = True
# # =============================================================================
# =============================================================================
            if l_np[b][2] == 'wordnet_def':
                distance += 5 
                
            elif l_np[b][2] == 'wordnet_ex':
                distance += 3
                
            elif l_np[b][2] == 'wiki':
                distance += 10
            if distance < closest_len:
                closest = b
                closest_len = distance
                

        print('Choosen: ', l_np[closest][0])
        if l_np[closest][1] == 'fill_blank':#if returned fill_blanck obtained, increase clue log
            clue_log['fill_blank'] += 1
        return helperFunctions.firstCapitalize(l_np[closest][0])
     
    else:
        return helperFunctions.firstCapitalize(helperFunctions.replaceWithSynonyms(originalClue))
#print(createNewClue("fast wheels for children", "Bus"))
        
print(pos_tag(['cared']))
print(wordnet.synsets('cared')[0].pos())