# AI_crossword

The different website sources are utilized to obtain sentences that can potentially become new clues for the New York Times crossword puzzle. New clues are processed by the createNewClue function by the help of helperFunction function to properly execute the NLP by using multiple sources such as Wikipedia, Wordnet, and Merriam-Webster. After the implementation of all the rules that are presented in the ‘how to solve NYT crossword puzzle’ guideline (Amlen, 1), an artificial intelligence score based method is applied to conveniently select from the possible clues and illustrate new clues with a proper fashion in a GUI.

In this project, our task was to generate new clues for the New York Times 5x5 crossword puzzles by using answers and clues that are given by the original puzzle. For this purpose, we started to store the 5x5 crossword puzzles from the New York Times website with the Selenium library. It helped us to understand the structure of the clues while generating new ones. First of all, we benefited from the article, which is “How to Solve The New York Times Crossword” by Deb Amlen. In the light of this article, we categorized the clues in terms of their tenses, part of speech, plural or singular forms and languages. Thus, we tried to generate compatible clues with their answers. Also, we followed different paths for the clues that have cross-referenced or abbreviations in it. We also benefited from the synonyms of the words.

Briefly, we have different kinds of NLP procedures that give the optimum results. We will examine the code with some crucial method to eliminate, choose, adjust, or neglect the clues that are obtained from the various sources online. While generating the new clues, we used different types of websites as Wikipedia, Merriam Webster, Wordnet, and Google Translate (Farkiya, 1). Our algorithm searches for the most compatible clue from these websites by using the methods that we mentioned above. In this report, we briefly mention the details of our methodology when generating new clues, and our NLP strategy.

Methodology:

In this section, we described the strategies we used while generating the clues. The Implementation details are in the next section.


Tense:

We check if the entry word is whether in the present tense, or past tense. We print the tense near the new clues inside parentheses ( Amlen, 1).

Part of Speech:

According to the part of speech rule, if the entry is a noun, we generate artificial noun clues from a sentence (Amlen, 1).


Plural:

All the websites that we search for if the entry is plural they convert it into a singular form. For this reason, we check the plurality condition of the entry and if it is a plural noun, we convert our clue’s noun to plural and conjugate the next verb accordingly (Amlen, 1).


Foreign Words:

If we cannot find the entry in the dictionaries and Wikipedia. If we cannot find any clues in those, we assume that the word is foreign and try Google Translate. If the word is foreign we display the translation as a clue with source entry language in parentheses. Note that Merriam-Webster dictionary sometimes finds foreign words. (Amlen, 1).


Abbreviations:

If neither Wordnet nor Merriam-Webster gives us a result and if the entry is an abbreviation, we check Wikipedia for clues. Wikipedia is a good source for finding abbreviations (Amlen, 1).


Omission Words:

If there is the same entry or even similar entry in the sentence, we omit these words from the sentence.


Sentence Format:

We use different functions to get rid of all improper signs or even unnecessary parts of a sentence, which may disrupt the quality of the new clues such as

parentheses. We also omit some of the word types such as adverbs, pronouns in a way that we can generate a grammarly and semantically correct new clues


The Worst-Case Scenario:

If nothing can find any possible clues, we change each word in the original clue with their synonyms if parts of speech don’t change. In this way, we generate a new clue from the original clue without losing the meaning.


Clue Filter:

We implement a score-based method for picking clues from possible clue lists. This handicap based method is a heuristic implementation. Clues that are close in length to the original clue have an advantage. Also, wordnet has an advantage over Merriam webster and Merriam webster has an advantage over Wikipedia in scoring.

Procedure:

In this section, we will explain how we implemented the strategies described in the previous section.


Retrieving Definitions and Example Sentences:

We retrieved definitions and examples for the original entry to create a new clue in the clueGenerator.py module.

Wordnet with nltk library:

-Merriam Webster with BeautifulSoup library,
-Wikipedia with Wikipedia API library,
-Google Translate With Google Translate API library
are used. One definition is retrieved from each site (the first one). We add a log that keeps track of the number of fill in the blank clues to limit the number of those by a maximum of one. All gathered definitions are stored in a list of possible clues to be used in further procedures.

Getting Wordnet Definition:

For each possible clue we find in the wordnet definition, Wordnet uses synsets, which lists the semantically closer words as an array in the nltk library. However, we continue only if the entry matches the first element of the array due to the Wordnet arrangement as in ranked order (Bird, 3).


Getting Wordnet Example:

We obtain example sentences from wordnet to create fill in the blanks type of clues. We only retrieve an example if there is no other fill in the blanks clue in the log of other generated clues.


Getting Merriam Webster Definition:

Merriam Webster definitions are simply retrieved from BeautifulSoup library by the help of ‘dt-text’ named class.


Getting Wikipedia Summary:

We get the first sentence of a Wikipedia page for the entry. Page titles consisting of multiple words are accepted if one of the words match with the entry (unless there is disambiguation). This choice is made because these pages are generally suitable for generating clues in the Wikipedia API library.


Clear Sentence:

Some definitions contain parentheses. After the definitions are retrieved, if there are any, we remove the parentheses (and inside of them) to make the clues more concise and less obvious by using the clearSentence method in the helperFunctions.py. Also, we cut the clue string after characters ‘;’, ‘-’ etc.


Manipulating The Definition:

After retrieving a sentence and clearing it, we put the sentence to a list of candidateClues and manipulate each of them via artificialnlp function (to make it shorter and more difficult).

Trim Sentence:

Some definitions (especially most of Wikipedia definitions) are in the following format.

‘clue’ is definition

Therefore we use the trimSentence function inside artificialnlp to get rid of the ‘clue’ part and to obtain the part which will be used to generate the clue. This function also removes any determiners at the beginning of the sentence because original clue nouns don’t have determiners.


Clue Difficulty Verification:

Whether a clue candidate has the entry inside it or not is checked because if the clue has the answer in it, it would be an easy clue. If the answer is in the clue, the answer is replaced with ‘ ’ and we have a fill in the blank type of clue. Note that if there was another fill in the blank clue in the clue log, the clue is discarded to avoid having multiple fills in the blanks clues.

Moreover, we checked whether any word in the new clue is very similar to the answer by using the fuzzywuzzy library’s similarity ratio function. If there is a word with more than 85 percent similarity to the answer in the clue, the clue is discarded.


Parts of Speech Tagging:

We start checking each word's plurality condition. Then, divide into its word types by using the nltk library with the pos_tag method. The method pos_tag pinpoints each word’s types for example, whether a noun, adjective, or a verb (Bird, 2).


Step by Step Procedure of NLP in a Nutshell:

After the search process is gathered with the various online sources, we have a possible clue array, which is candidate clues. While obtaining sentences, we also make records of where the program obtains sentences as logs. Then, we continue with the artificialnlp named function. First, we check the tense of the entry to indicate the tense at the end of the new clues. Then, we used an artificial intelligent NLP

procedure which generates new candidate clues with the general noun phrase format as [‘DT’, ‘JJ’, ‘NN’, ‘IN’]. ‘DT’ is for determiner, ‘JJ’ is for adjectives, ‘NN’ is for noun words, and last but not least ‘IN’ is for prepositions. By arranging this condition in order, we can generate a meaningful noun phrase that is grammarly correct by using the nltk library (Farkiya, 1).

While subtracting these types of words, we check for whether the sentence is long enough to avoid the semantic shift because often if the candidate clue has not enough elements, a semantic shift cannot be avoided. While we try to create a grammarly correct noun phrase, we also look for additional parts of the sentence that we can alter. We cut the following word of the candidate clues if there is a ‘or’ before the noun in the sentence. However, to cut without losing the meaning of the candidate clue, we check whether the following word of ‘or’ has a verb or not. In simple terms, we find the ‘or’ and cut the following noun, which has a key as ‘CC’ in the nltk library. In addition to these, we also cut before the words ‘is’, ‘are’, ‘was’, ‘were’ and ‘am’ to introduce more difficulty without losing the semantic meaning. Some other deductions are made such that adverbs and pronouns are deducted without semantic shift as well. Pronouns are omitted if the length of the sentence is higher than 5 characters. The reason behind this is that we generally do not have enough words to make sensible clues that have a pronoun if the length of the sentence is lower than 5 characters. In this way, we can eliminate extra explanations of the entries and can make difficult clues because clues generally have to be tricky and hard to solve for addiction purposes (game theory). Then, as stated in the methods, if the entry is plural, we make the plural of the word with make_plural function with finding the proper word in the candidate clue. Since we cannot make all nouns (if there is) plural (this may generate semantic shift and incorrect grammar), we find the most appropriate word and change its condition of plurality by adding ‘s’, ‘es’, or even ‘ies’. For the depiction of the condition of tenses, we simply indicate the type of the tense near the new clues within parenthesis such as (Past) or (Present).

Artificial Intelligent Score Based Clue Selection:

For the score based elimination artificial intelligence system, we aim for the optimal new clue. This can be achieved by a heuristic application. We create a heuristic named distance from the original clue (the clues that are gathered from the NYT website). We iterate and learn that the accuracy and the quality of the clues are better if we pick closer distant clues from the original clue. This is beneficial for not only the depiction of the clues in the GUI but also beneficial for the precise new clue generation. While picking the least distant ones, we rank the quality of our external sources, for instance, Wikipedia has slight disadvantages from the Wordnet. This disadvantage is introduced by increasing the distance from the original clue. In this case, the candidate clues obtained from Wikipedia have increased distances by adding an extra clue length (Jha, Mitra, Choudhury, 3). In the end, If nothing can find anything, we assume the entry is a foreign word. First, we check the entry in Merriam-Webster Dictionary due to the possibility of finding foreign words and then we search it in Google Translate for an exact resolution.




![1](https://user-images.githubusercontent.com/59175450/158487801-738df9fd-9ea2-4fba-95ba-541aca17f9ae.png)


