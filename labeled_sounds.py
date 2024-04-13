import difflib


def apply_labeled_sounds_to_text(text, labeled_sounds):
    out_text = text.copy()
    changed_tokens = {}

    for key in labeled_sounds.keys():
        for index in range(len(out_text)):
            if key in text[index]:
                out_text[index] = out_text[index].replace(key, labeled_sounds[key])
                changed_symbols = []
                diff = difflib.ndiff(text[index], out_text[index])
                real_index = 0

                for i, s in enumerate(diff):
                    if s[0] == '-':
                        real_index -= 1
                    if s[0] == '+':
                        changed_symbols.append(real_index)
                    elif s[0] == ' ' and s[-1] in labeled_sounds.keys():
                        changed_symbols.append(real_index)

                    real_index += 1

                changed_tokens.update({index: changed_symbols})

    # print(changed_tokens)
    return [out_text, changed_tokens]
