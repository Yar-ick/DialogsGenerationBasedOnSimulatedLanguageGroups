import string

import nltk
import spacy

from enum import Enum
from pymorphy3 import MorphAnalyzer


class WordOrder(Enum):
    SubjectVerbObject = 0
    SubjectObjectVerb = 1
    VerbSubjectObject = 2
    VerbObjectSubject = 3
    ObjectVerbSubject = 4
    ObjectSubjectVerb = 5


def is_token_from_subject_phrase(token):
    morph = MorphAnalyzer()
    parsed_token = morph.parse(token.text)[0]

    # If token is subject
    if parsed_token.tag.number is not None:
        # print("Именительный падеж: ", parsed_token.inflect({parsed_token.tag.number, 'nomn'}).word)
        if (
                token.dep_ == "nsubj"
                and
                token.head.dep_ == "ROOT"
                # and
                # parsed_token.inflect({parsed_token.tag.number, 'nomn'}).word == Token.text.lower()
        ):
            return True
    # If token is subject
    if token.head.dep_ == "nsubj":
        return True

    return False


def change_text_word_order(text, word_order, print_debug_info=False):
    """
    Return a list of word tokens with changed word order

    :param text: list of work tokens
    :type text: list
    :param word_order: on of the 6 word order type
    :type word_order: WordOrder
    :param print_debug_info: for printing debug info
    :type print_debug_info: bool
    """
    svo_phrases = {}

    if word_order == WordOrder.SubjectVerbObject:
        return [text, svo_phrases]

    nlp = spacy.load("ru_core_news_lg")

    out_sentence = []
    subject_phrase_borders = []
    verb_phrase_borders = []
    object_phrase_borders = []

    sentence_parts = " ".join(text).split(',')

    for part in sentence_parts:
        subject_phrase = []
        verb_phrase = []
        object_phrase = []
        analyzed_part = nlp(part)

        for token in analyzed_part:
            # Subject phrase
            if is_token_from_subject_phrase(token):
                subject_phrase.append(token.text)
            # Verb phrase
            elif (
                    (token.dep_ == "ROOT")
                    or
                    ((token.dep_ == "xcomp" or token.dep_ == "advmod") and token.head.dep_ == "ROOT")
            ):
                verb_phrase.append(token.text)
            # Object phrase
            elif token.dep_ != "punct" and token.pos_ != "SPACE":
                object_phrase.append(token.text)

        if print_debug_info:
            print("Subject phrase: ", subject_phrase)
            print("Verb phrase: ", verb_phrase)
            print("Object phrase: ", object_phrase)

        if word_order == word_order.SubjectVerbObject:
            if subject_phrase:
                subject_phrase_borders.append((len(out_sentence) - 1 if len(out_sentence) != 0 else 0, '{'))
                out_sentence += subject_phrase
                subject_phrase_borders.append((len(out_sentence) - 1, '}'))

            if verb_phrase:
                verb_phrase_borders.append((len(out_sentence) - 1, '{'))
                out_sentence += verb_phrase
                verb_phrase_borders.append((len(out_sentence) - 1, '}'))

            if object_phrase:
                object_phrase_borders.append((len(out_sentence) - 1, '{'))
                out_sentence += object_phrase
                object_phrase_borders.append((len(out_sentence) - 1, '}'))
        elif word_order == word_order.SubjectObjectVerb:
            if subject_phrase:
                subject_phrase_borders.append((len(out_sentence) - 1 if len(out_sentence) != 0 else 0, '{'))
                out_sentence += subject_phrase
                subject_phrase_borders.append((len(out_sentence) - 1, '}'))

            if object_phrase:
                object_phrase_borders.append((len(out_sentence), '{'))
                out_sentence += object_phrase
                object_phrase_borders.append((len(out_sentence) - 1, '}'))

            if verb_phrase:
                verb_phrase_borders.append((len(out_sentence), '{'))
                out_sentence += verb_phrase
                verb_phrase_borders.append((len(out_sentence) - 1, '}'))
        elif word_order == word_order.VerbSubjectObject:
            if verb_phrase:
                verb_phrase_borders.append((len(out_sentence) - 1 if len(out_sentence) != 0 else 0, '{'))
                out_sentence += verb_phrase
                verb_phrase_borders.append((len(out_sentence) - 1, '}'))

            if subject_phrase:
                subject_phrase_borders.append((len(out_sentence), '{'))
                out_sentence += subject_phrase
                subject_phrase_borders.append((len(out_sentence) - 1, '}'))

            if object_phrase:
                object_phrase_borders.append((len(out_sentence), '{'))
                out_sentence += object_phrase
                object_phrase_borders.append((len(out_sentence) - 1, '}'))
        elif word_order == word_order.VerbObjectSubject:
            if verb_phrase:
                verb_phrase_borders.append((len(out_sentence) - 1 if len(out_sentence) != 0 else 0, '{'))
                out_sentence += verb_phrase
                verb_phrase_borders.append((len(out_sentence) - 1, '}'))

            if object_phrase:
                object_phrase_borders.append((len(out_sentence), '{'))
                out_sentence += object_phrase
                object_phrase_borders.append((len(out_sentence) - 1, '}'))

            if subject_phrase:
                subject_phrase_borders.append((len(out_sentence), '{'))
                out_sentence += subject_phrase
                subject_phrase_borders.append((len(out_sentence) - 1, '}'))
        elif word_order == word_order.ObjectVerbSubject:
            if object_phrase:
                object_phrase_borders.append((len(out_sentence) - 1 if len(out_sentence) != 0 else 0, '{'))
                out_sentence += object_phrase
                object_phrase_borders.append((len(out_sentence) - 1, '}'))

            if verb_phrase:
                verb_phrase_borders.append((len(out_sentence), '{'))
                out_sentence += verb_phrase
                verb_phrase_borders.append((len(out_sentence) - 1, '}'))

            if subject_phrase:
                subject_phrase_borders.append((len(out_sentence), '{'))
                out_sentence += subject_phrase
                subject_phrase_borders.append((len(out_sentence) - 1, '}'))
        elif word_order == word_order.ObjectSubjectVerb:
            if object_phrase:
                object_phrase_borders.append((len(out_sentence) - 1 if len(out_sentence) != 0 else 0, '{'))
                out_sentence += object_phrase
                object_phrase_borders.append((len(out_sentence) - 1, '}'))

            if subject_phrase:
                subject_phrase_borders.append((len(out_sentence), '{'))
                out_sentence += subject_phrase
                subject_phrase_borders.append((len(out_sentence) - 1, '}'))

            if verb_phrase:
                verb_phrase_borders.append((len(out_sentence), '{'))
                out_sentence += verb_phrase
                verb_phrase_borders.append((len(out_sentence) - 1, '}'))

        if part != sentence_parts[len(sentence_parts) - 1]:
            out_sentence += ','
        else:
            out_sentence += part[len(part) - 1]

        # if print_debug_info:
        #     print("\n{0:20}{1:20}{2:35}{3:20}".format("Слово", "Часть речи", "Синтаксическая связь", "Родитель"))
        #     print("==========================================================================================")
        #     for token in analyzed_part:
        #         print("{0:20}{1:20}{2:35}{3:20}".format(token.text, token.pos_, (token.dep_ + " (" + (
        #             spacy.explain(token.dep_) if isinstance(spacy.explain(token.dep_), str) else "") + ')'),
        #                                                 token.head.text))
        #     print('\n')
            # displacy.render(analyzed_part, style='dep', jupyter=True)

    svo_phrases.update({"S": subject_phrase_borders})
    svo_phrases.update({"V": verb_phrase_borders})
    svo_phrases.update({"O": object_phrase_borders})

    if print_debug_info:
        print("SVO Phrases: ", svo_phrases)

    return [out_sentence, svo_phrases]
