import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def convert_pos(pos_tb):
    """
    Converts the treebank pos tag found by nltk.pos_tag and converts it to wordnet pos tag
    useable by Wordnet lemmatizer
    :param pos_tb:
    :return:
    """
    if pos_tb.startswith('J'):
        return wordnet.ADJ
    elif pos_tb.startswith('V'):
        return wordnet.VERB
    elif pos_tb.startswith('N'):
        return wordnet.NOUN
    elif pos_tb.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def get_lemma(word, infer_pos=True):
    lemmatizer = WordNetLemmatizer()
    """
    Finds the lemma for a given word if any
    :param word: The word for which a lemma is required
    :return: The lemma found for that word
    """
    nWord = nltk.word_tokenize(word)
    tag = nltk.pos_tag(nWord)
    pos = convert_pos(tag[0][1])
    try:
        r = lemmatizer.lemmatize(word,pos)
    except:
        r=word
    return r

def lemmatize_string(strin):
    words = strin.split()
    words = [get_lemma(x) for x in words]
    n_strin = " ".join(words)
    return n_strin