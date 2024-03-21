
def apply_labeled_sounds_to_text(text, labeled_sounds):
    out_text = text

    for key in labeled_sounds.keys():
        out_text = out_text.replace(key, labeled_sounds[key])

    return out_text
