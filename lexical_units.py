from nltk import word_tokenize
from pymorphy3 import MorphAnalyzer
from pymystem3 import Mystem


def replace_lexical_units_in_text(text, lexical_units, print_debug_info=False):
    mystem = Mystem()
    morph = MorphAnalyzer()
    tokenized_text = word_tokenize(text)

    if print_debug_info:
        print("Tokenized text: ", tokenized_text)

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

    if print_debug_info:
        print("Lemmatized text changed: ", lemmatized_text)
        print("Lemmatized text original: ", lemmatized_text_original_no_spaces)

    index = 0
    for token in lemmatized_text_original_no_spaces:
        if token != lemmatized_text[index]:
            if print_debug_info:
                print("Gonna replace ", token, " on ", lemmatized_text[index])

            # parsed_word_original_variants = morph.parse(token)
            parsed_word_original_variants = morph.parse(tokenized_text[index])
            parsed_word_replacing_variants = morph.parse(lemmatized_text[index])

            if not parsed_word_original_variants or not parsed_word_replacing_variants:
                break

            parsed_word_original = parsed_word_original_variants[0]
            parsed_word_replacing = parsed_word_replacing_variants[0]

            if print_debug_info:
                print("Parsed word original: ", parsed_word_original)
                print("Parsed word replacing: ", parsed_word_replacing)

            if parsed_word_original is not None and parsed_word_replacing is not None:
                newform_grammems_set = set(parsed_word_original.tag.grammemes)
                grammemes_to_remove = {"masc", "femn", "neut", "Sgtm", "Pltm", "tran", "intr"}
                newform_grammems_set.difference_update(grammemes_to_remove)

                parsed_word_replacing_newform = parsed_word_replacing.inflect(newform_grammems_set)

                if print_debug_info:
                    print("Parsed word replacing new form: ", parsed_word_replacing_newform, "\n")

                if parsed_word_replacing_newform is not None:
                    tokenized_text[index] = parsed_word_replacing_newform.word
        index = index + 1

    out_text = " ".join(tokenized_text)

    return out_text
