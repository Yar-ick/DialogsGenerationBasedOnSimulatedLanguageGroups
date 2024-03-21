import nltk
import spacy

from enum import Enum
from pymorphy3 import MorphAnalyzer


class WordOrder(Enum):
    SubjectVerbObject = 1
    SubjectObjectVerb = 2
    VerbSubjectObject = 3
    VerbObjectSubject = 4
    ObjectVerbSubject = 5
    ObjectSubjectVerb = 6


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


def change_text_word_order(text, word_order, print_help_info=False):
    nlp = spacy.load("ru_core_news_lg")
    out_text = ""
    sentence_tokens = nltk.sent_tokenize(text)

    for sentence in sentence_tokens:
        out_sentence = list("")

        analyzed_sentence = nlp(sentence)
        sentence_parts = sentence.split(',')

        for part in sentence_parts:
            subject_phrase = list("")
            verb_phrase = list("")
            object_phrase = list("")
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

            if print_help_info:
                print("Subject phrase: ", subject_phrase)
                print("Verb phrase: ", verb_phrase)
                print("Object phrase: ", object_phrase)

            if word_order == word_order.SubjectVerbObject:
                out_sentence.append(" ".join(subject_phrase))
                out_sentence.append(" ".join(verb_phrase))
                out_sentence.append(" ".join(object_phrase))
            elif word_order == word_order.SubjectObjectVerb:
                out_sentence.append(" ".join(subject_phrase))
                out_sentence.append(" ".join(object_phrase))
                out_sentence.append(" ".join(verb_phrase))
            elif word_order == word_order.VerbSubjectObject:
                out_sentence.append(" ".join(verb_phrase))
                out_sentence.append(" ".join(subject_phrase))
                out_sentence.append(" ".join(object_phrase))
            elif word_order == word_order.VerbObjectSubject:
                out_sentence.append(" ".join(verb_phrase))
                out_sentence.append(" ".join(object_phrase))
                out_sentence.append(" ".join(subject_phrase))
            elif word_order == word_order.ObjectVerbSubject:
                out_sentence.append(" ".join(object_phrase))
                out_sentence.append(" ".join(verb_phrase))
                out_sentence.append(" ".join(subject_phrase))
            elif word_order == word_order.ObjectSubjectVerb:
                out_sentence.append(" ".join(object_phrase))
                out_sentence.append(" ".join(subject_phrase))
                out_sentence.append(" ".join(verb_phrase))

            if part != sentence_parts[len(sentence_parts) - 1]:
                out_sentence.append(',')
            else:
                out_sentence.append(sentence[len(sentence) - 1])

            if print_help_info:
                print("\n{0:20}{1:20}{2:35}{3:20}".format("Слово", "Часть речи", "Синтаксическая связь", "Родитель"))
                print("==========================================================================================")
                for token in analyzed_part:
                    print("{0:20}{1:20}{2:35}{3:20}".format(token.text, token.pos_, (token.dep_ + " (" + (
                        spacy.explain(token.dep_) if isinstance(spacy.explain(token.dep_), str) else "") + ')'),
                                                            token.head.text))
                print('\n')
                # displacy.render(analyzed_part, style='dep', jupyter=True)

        out_text += " ".join(out_sentence)

    return out_text
