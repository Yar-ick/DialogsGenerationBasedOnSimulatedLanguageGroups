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


class PhraseAffiliation(Enum):
    SubjectPhrase = 0
    VerbPhrase = 1
    ObjectPhrase = 2
    UnknownPhrase = 3


def detect_phrase_affiliation_of_token(token):
    # Subject phrase
    if is_token_from_subject_phrase(token):
        return PhraseAffiliation.SubjectPhrase

    # Verb phrase
    if (
        token.dep_ == "ROOT"
        or
        (
            token.head.dep_ == "ROOT"
            and
            (token.dep_ == "xcomp" or token.dep_ == "advmod")
            and
            token.dep_ != "punct"
        )
    ):
        return PhraseAffiliation.VerbPhrase

    # Object phrase
    if token.dep_ != "punct" and token.pos_ != "SPACE":
        return PhraseAffiliation.ObjectPhrase

    return PhraseAffiliation.UnknownPhrase


def is_token_from_subject_phrase(token):
    morph = MorphAnalyzer()
    parsed_token = morph.parse(token.text)[0]

    # # If token is subject
    # if parsed_token.tag.number is not None:
    #     # print("Именительный падеж: ", parsed_token.inflect({parsed_token.tag.number, 'nomn'}).word)
    #     if (
    #             token.dep_ == "nsubj"
    #             and
    #             token.head.dep_ == "ROOT"
    #             # and
    #             # parsed_token.inflect({parsed_token.tag.number, 'nomn'}).word == Token.text.lower()
    #     ):
    #         return True
    if (
            token.dep_ == "nsubj" and token.head.dep_ == "ROOT"
            or
            token.dep_ == "cc" and token.head.head is not None and token.head.head.head.dep_ == "ROOT"
    ):
        return True
    # If token is subject
    if token.head.dep_ == "nsubj":
        return True

    return False


def add_phrases_to_sentence(dict_with_parameters):
    word_order_to_phrases = {
        WordOrder.SubjectVerbObject: [
            [dict_with_parameters["SubjectPhrase"], dict_with_parameters["SubjectPhraseIndexes"]],
            [dict_with_parameters["VerbPhrase"], dict_with_parameters["VerbPhraseIndexes"]],
            [dict_with_parameters["ObjectPhrase"], dict_with_parameters["ObjectPhraseIndexes"]],
        ],
        WordOrder.SubjectObjectVerb: [
            [dict_with_parameters["SubjectPhrase"], dict_with_parameters["SubjectPhraseIndexes"]],
            [dict_with_parameters["ObjectPhrase"], dict_with_parameters["ObjectPhraseIndexes"]],
            [dict_with_parameters["VerbPhrase"], dict_with_parameters["VerbPhraseIndexes"]]
        ],
        WordOrder.VerbSubjectObject: [
            [dict_with_parameters["VerbPhrase"], dict_with_parameters["VerbPhraseIndexes"]],
            [dict_with_parameters["SubjectPhrase"], dict_with_parameters["SubjectPhraseIndexes"]],
            [dict_with_parameters["ObjectPhrase"], dict_with_parameters["ObjectPhraseIndexes"]]
        ],
        WordOrder.VerbObjectSubject: [
            [dict_with_parameters["VerbPhrase"], dict_with_parameters["VerbPhraseIndexes"]],
            [dict_with_parameters["ObjectPhrase"], dict_with_parameters["ObjectPhraseIndexes"]],
            [dict_with_parameters["SubjectPhrase"], dict_with_parameters["SubjectPhraseIndexes"]]
        ],
        WordOrder.ObjectVerbSubject: [
            [dict_with_parameters["ObjectPhrase"], dict_with_parameters["ObjectPhraseIndexes"]],
            [dict_with_parameters["VerbPhrase"], dict_with_parameters["VerbPhraseIndexes"]],
            [dict_with_parameters["SubjectPhrase"], dict_with_parameters["SubjectPhraseIndexes"]]
        ],
        WordOrder.ObjectSubjectVerb: [
            [dict_with_parameters["ObjectPhrase"], dict_with_parameters["ObjectPhraseIndexes"]],
            [dict_with_parameters["SubjectPhrase"], dict_with_parameters["SubjectPhraseIndexes"]],
            [dict_with_parameters["VerbPhrase"], dict_with_parameters["VerbPhraseIndexes"]]
        ]
    }

    in_sentence = dict_with_parameters["Sentence"]
    first_phrase = word_order_to_phrases[dict_with_parameters["WordOrder"]][0][0]
    second_phrase = word_order_to_phrases[dict_with_parameters["WordOrder"]][1][0]
    third_phrase = word_order_to_phrases[dict_with_parameters["WordOrder"]][2][0]
    first_phrase_indexes = word_order_to_phrases[dict_with_parameters["WordOrder"]][0][1]
    second_phrase_indexes = word_order_to_phrases[dict_with_parameters["WordOrder"]][1][1]
    third_phrase_indexes = word_order_to_phrases[dict_with_parameters["WordOrder"]][2][1]

    if first_phrase:
        sentence_len_before_append = len(in_sentence) - 1 if len(in_sentence) != 0 else 0
        in_sentence += first_phrase
        first_phrase_indexes += [index for index in range(sentence_len_before_append, len(in_sentence))]

    if second_phrase:
        sentence_len_before_append = len(in_sentence)
        in_sentence += second_phrase
        second_phrase_indexes += [index for index in range(sentence_len_before_append, len(in_sentence))]

    if third_phrase:
        sentence_len_before_append = len(in_sentence)
        in_sentence += third_phrase
        third_phrase_indexes += [index for index in range(sentence_len_before_append, len(in_sentence))]

    word_order_to_phrase_indexes = {
        WordOrder.SubjectVerbObject: [first_phrase_indexes, second_phrase_indexes, third_phrase_indexes],
        WordOrder.SubjectObjectVerb: [first_phrase_indexes, third_phrase_indexes, second_phrase_indexes],
        WordOrder.VerbSubjectObject: [second_phrase_indexes, first_phrase_indexes, third_phrase_indexes],
        WordOrder.VerbObjectSubject: [third_phrase_indexes, first_phrase_indexes, second_phrase_indexes],
        WordOrder.ObjectVerbSubject: [third_phrase_indexes, second_phrase_indexes, first_phrase_indexes],
        WordOrder.ObjectSubjectVerb: [second_phrase_indexes, third_phrase_indexes, first_phrase_indexes]
    }

    out_phrase_indexes = word_order_to_phrase_indexes[dict_with_parameters["WordOrder"]]

    # print("Sentence with added phrases: ", in_sentence)
    # print("Subject phrase indexes: ", out_phrase_indexes[0])
    # print("Verb phrase indexes: ", out_phrase_indexes[1])
    # print("Object phrase indexes: ", out_phrase_indexes[2])

    return [in_sentence, out_phrase_indexes[0], out_phrase_indexes[1], out_phrase_indexes[2]]


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

    spacy_russian_model = spacy.load("ru_core_news_lg")

    out_sentence = []
    subject_phrase_indexes = []
    verb_phrase_indexes = []
    object_phrase_indexes = []

    sentence_parts = " ".join(text).split(',')

    if print_debug_info:
        print("Sentence parts:")

    # sentence_text = " ".join(text)
    # sentence_parts = [sentence_text]

    part_index = 0
    for part in sentence_parts:
        print("Part ", part_index, ": ", part)
        part_index += 1

        subject_phrase = []
        verb_phrase = []
        object_phrase = []
        analyzed_part = spacy_russian_model(part)

        # Detect phrase affiliation of all tokens
        for token in analyzed_part:
            token_phrase_affiliation = detect_phrase_affiliation_of_token(token)

            if token_phrase_affiliation is PhraseAffiliation.UnknownPhrase:
                continue
            elif token_phrase_affiliation is PhraseAffiliation.SubjectPhrase:
                subject_phrase.append(token.text)
            elif token_phrase_affiliation is PhraseAffiliation.VerbPhrase:
                verb_phrase.append(token.text)
            elif token_phrase_affiliation is PhraseAffiliation.ObjectPhrase:
                object_phrase.append(token.text)

        if print_debug_info:
            print("Subject phrase: ", subject_phrase)
            print("Verb phrase: ", verb_phrase)
            print("Object phrase: ", object_phrase)

        result_list = add_phrases_to_sentence({
            "WordOrder": word_order,
            "SubjectPhrase": subject_phrase,
            "VerbPhrase": verb_phrase,
            "ObjectPhrase": object_phrase,
            "SubjectPhraseIndexes": subject_phrase_indexes,
            "VerbPhraseIndexes": verb_phrase_indexes,
            "ObjectPhraseIndexes": object_phrase_indexes,
            "Sentence": out_sentence
        })

        out_sentence = result_list[0]
        subject_phrase_indexes = result_list[1]
        verb_phrase_indexes = result_list[2]
        object_phrase_indexes = result_list[3]

        if part != sentence_parts[len(sentence_parts) - 1]:
            out_sentence += ','
        else:
            out_sentence += part[len(part) - 1]

        if print_debug_info:
            print("\n{0:20}{1:20}{2:35}{3:20}".format("Слово", "Часть речи", "Синтаксическая связь", "Родитель"))
            print("==========================================================================================")

            for token in analyzed_part:
                print("{0:20}{1:20}{2:35}{3:20}".format(token.text, token.pos_, (token.dep_ + " (" + (
                    spacy.explain(token.dep_) if isinstance(spacy.explain(token.dep_), str) else "") + ')'),
                                                        token.head.text))

            print('\n')

    svo_phrases.update({"S": subject_phrase_indexes})
    svo_phrases.update({"V": verb_phrase_indexes})
    svo_phrases.update({"O": object_phrase_indexes})

    if print_debug_info:
        print("SVO Phrases: ", svo_phrases)

    return [out_sentence, svo_phrases]
