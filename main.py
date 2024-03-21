import tkinter
import word_order
import lexical_units
import isolation_degree
import labeled_sounds


# from characterai import PyCAI


def start():
    text = ("Чтобы успешно охотиться, важно обладать терпением и наблюдательностью. Обратите внимание на существ, "
            "на которых вы охотитесь, изучите их повадки и поведение. Изучив их, спланируйте атаку и нанесите "
            "решающую и смертоносную силу. Будьте бдительны и осторожны, ведь небольшие ошибки могут привести к "
            "плачевным результатам. Никогда не недооценивайте добычу, поскольку даже самое маленькое существо может "
            "причинить вам вред, если вы не будете полностью задействованы.")

    lexical_unit_couples = {
        'терпение': 'халтура',
        'наблюдательность': 'безолаберность',
        'поведение': 'запах',
        'сила': 'мощь',
        'быть': 'являться',
        'спланировать': 'набросать',
        'недооценивать': 'унижать'
    }

    labeled_sound_couples = {
        'г': 'ғ',
        'е': 'ε'
    }

    base_text = text.split(".")

    # result = word_order.change_text_word_order(text, word_order.WordOrder.VerbSubjectObject, False)
    result = lexical_units.replace_lexical_units_in_text(text, lexical_unit_couples)
    result = isolation_degree.change_text_isolation_degree(result, 2)
    result = labeled_sounds.apply_labeled_sounds_to_text(result, labeled_sound_couples)

    result_for_print = result.split(".")

    print("\nИсходный текст ответа: ")
    for sentence in base_text:
        if sentence != " ":
            print(sentence, ".")

    print("\n")

    print("Преобразованный ответ: ")
    for sentence in result_for_print:
        print(sentence, ".")


def launch_nltk_installer():
    import nltk
    nltk.download()


if __name__ == '__main__':
    # start()

    root = tkinter.Tk()
    root.title('My App')
    root.mainloop()
