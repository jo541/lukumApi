import sys
import time

try:
    from nltk import wordpunct_tokenize
    from nltk.corpus import stopwords
except ImportError:
    print
    '[!] You need to install nltk (http://nltk.org/index.html)'


def calculate_languages_ratios(text):
    languages_ratios = {}
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements)  # language "score"

    return languages_ratios


def detect_language(text):
    ratios = calculate_languages_ratios(text)
    most_rated_language = max(ratios, key=ratios.get)
    return most_rated_language


def load_bad_words(language):
    if language.upper() in ['ENGLISH', 'FRENCH', 'SPANISH', 'GERMAN']:
        try:
            badwords_list = []
            lang_file = open('datasets/' + language.lower() + '.csv', 'rb')
            for word in lang_file:
                badwords_list.append(word.lower().strip('\n'))
            return badwords_list
        except:
            return False
        finally:
            lang_file.close()
    else:
        return False


def load_file(filename):
    file = open(filename, 'rb')
    return file
