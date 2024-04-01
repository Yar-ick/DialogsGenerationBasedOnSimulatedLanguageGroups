from pymorphy3 import MorphAnalyzer
from nltk.tokenize import word_tokenize


def change_text_isolation_degree(text, isolation_degree):
    if isolation_degree == 0:
        return text

    morph = MorphAnalyzer()
    word_tokens = word_tokenize(text)
    index = 0

    for token in word_tokens:
        parsed_word = morph.parse(token)
        if isolation_degree == 1:
            if parsed_word[0].tag.POS == "VERB":
                word_tokens[index] = parsed_word[0].normal_form
        elif isolation_degree == 2:
            if parsed_word[0].tag.POS == "VERB":
                word_tokens[index] = parsed_word[0].normal_form
            if parsed_word[0].tag.POS == "NOUN" or parsed_word[0].tag.POS == "NPRO":
                word_tokens[index] = parsed_word[0].normal_form
        elif isolation_degree == 3:
            word_tokens[index] = parsed_word[0].normal_form

        index += 1

    out_text = ""
    out_text += " ".join(word_tokens)

    return out_text
