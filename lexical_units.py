from nltk import word_tokenize
from pymorphy3 import MorphAnalyzer
from pymystem3 import Mystem


def replace_lexical_units_in_text(text, lexical_units):
    mystem = Mystem()
    morph = MorphAnalyzer()
    tokenized_text = word_tokenize(text)
    # print("Токенизированный текст: ", tokenized_text)

    lemmatized_text_original = mystem.lemmatize(text)
    lemmatized_text_original_no_spaces = [token for token in lemmatized_text_original if token != ' ']
    lemmatized_text = lemmatized_text_original_no_spaces.copy()

    index = 0
    for key in lexical_units.keys():
        for token in lemmatized_text:
            if token == key:
                lemmatized_text[index] = lexical_units[key]
            index = index + 1
        index = 0

    # print("lemmatized_text_changed: ", lemmatized_text)
    # print("lemmatized_text_original: ", lemmatized_text_original_nospaces)

    index = 0
    for token in lemmatized_text_original_no_spaces:
        if token != lemmatized_text[index]:
            # print("Gonna replace ", token, " on ", lemmatized_text[index])
            parsed_word_original = morph.parse(tokenized_text[index])[0]
            parsed_word_replacing = morph.parse(lemmatized_text[index])[0]
            # print(parsed_word_original)
            # print(parsed_word_replacing)

            if parsed_word_original is not None and parsed_word_replacing is not None:
                newform_grammemes_set = set(parsed_word_original.tag.grammemes)
                grammemes_to_remove = {"masc", "femn", "neut", "Sgtm", "Pltm", "tran", "intr"}
                newform_grammemes_set.difference_update(grammemes_to_remove)

                parsed_word_replacing_newform = parsed_word_replacing.inflect(newform_grammemes_set)
                # print("parsed_word_replacing_newform: ", parsed_word_replacing_newform)

                if parsed_word_replacing_newform is not None:
                    tokenized_text[index] = parsed_word_replacing_newform.word
        index = index + 1

    out_text = " ".join(tokenized_text)

    return out_text
