from pymorphy3 import MorphAnalyzer


def change_text_isolation_degree(text, isolation_degree):
    """
    Return a list of list and set:

    List[0] is a list of isolated word tokens;

    List[1] is a set with indexes of isolated tokens;

    :param text: list of work tokens
    :type text: list
    :param isolation_degree: isolation degree from 0 to 3
    :type isolation_degree: int
    """
    changed_tokens = set()

    if isolation_degree == 0:
        return [text, changed_tokens]

    morph = MorphAnalyzer()
    word_tokens = text.copy()

    index = 0

    for token in word_tokens:
        parsed_word = morph.parse(token)

        if isolation_degree == 1:
            if parsed_word[0].tag.POS == "VERB":
                word_tokens[index] = parsed_word[0].normal_form
                changed_tokens.add(index)
        elif isolation_degree == 2:
            if parsed_word[0].tag.POS == "VERB":
                word_tokens[index] = parsed_word[0].normal_form
                changed_tokens.add(index)
            if parsed_word[0].tag.POS == "NOUN" or parsed_word[0].tag.POS == "NPRO":
                word_tokens[index] = parsed_word[0].normal_form
                changed_tokens.add(index)
        elif isolation_degree == 3:
            if word_tokens[index] != parsed_word[0].normal_form:
                changed_tokens.add(index)

            word_tokens[index] = parsed_word[0].normal_form

        index += 1

    return [word_tokens, changed_tokens]
