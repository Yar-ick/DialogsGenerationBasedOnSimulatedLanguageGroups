import word_order
import lexical_units
import isolation_degree
import labeled_sounds
import sv_ttk

# from characterai import PyCAI
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk


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


def launch_tkinter_app():
    window = Tk()
    # window = ThemedTk(theme="black")
    sv_ttk.set_theme("dark")
    window.title('Диалогус')
    window.iconbitmap(default="Icon.ico")
    window.geometry("1000x900")

    # Создание набора вкладок для разных задач
    notebook = ttk.Notebook()
    notebook.pack(expand=True, fill=BOTH)

    # region LanguageGroupFrame
    """------------------------------LANGUAGE GROUP FRAME------------------------------"""

    language_group_frame = ttk.Frame(notebook)

    word_order_label = ttk.Label(language_group_frame, text="Порядок слов:", font=("Segoe UI", 14, "bold"), background="#000000")
    word_order_label.pack(expand=False, fill=X, anchor="w", ipady=5, padx=15, pady=15)

    word_orders = [
        "Подлежащее -> сказуемое  -> дополнение",
        "Подлежащее -> дополнение -> сказуемое",
        "Сказуемое  -> подлежащее -> дополнение",
        "Сказуемое  -> дополнение -> подлежащее",
        "Дополнение -> сказуемое  -> подлежащее",
        "Дополнение -> подлежащее -> сказуемое"
    ]
    default_word_order_choice = StringVar(value=word_orders[0])

    word_order_combobox = ttk.Combobox(
        language_group_frame,
        textvariable=default_word_order_choice,
        values=word_orders,
        state='readonly',
        width=40,
    )

    # word_order_combobox.grid(row=0, column=0, ipady=4, padx=15, pady=15, sticky="w")
    word_order_combobox.pack(expand=False, anchor="w", ipady=5, padx=15)
    word_order_combobox.bind("<<ComboboxSelected>>", lambda e: language_group_frame.focus())

    lexical_unit_label = ttk.Label(language_group_frame, text="Замена лексических единиц:", font=("Segoe UI", 14, "bold"), background="#000000")
    lexical_unit_label.pack(expand=False, fill=X, anchor="w", ipady=5, padx=15, pady=15)

    lexical_unit_columns = ("Word1", "Word2")
    lexical_unit_table = ttk.Treeview(language_group_frame, columns=lexical_unit_columns, show="headings")
    # lexical_unit_table.grid(row=1, column=0, padx=15)
    lexical_unit_table.pack(expand=False, anchor="w", padx=15)
    lexical_unit_table.heading("Word1", text="Заменяемое слово")
    lexical_unit_table.heading("Word2", text="Заменяющее слово")

    lexical_unit_couples = [("терпение", "халтура"), ("наблюдательность", "безолаберность")]

    for lexical_unit in lexical_unit_couples:
        lexical_unit_table.insert("", END, values=lexical_unit)

    isolation_degree_label = ttk.Label(language_group_frame, text="Степень изолированности:", font=("Segoe UI", 14, "bold"), background="#000000")
    isolation_degree_label.pack(expand=False, fill=X, anchor="w", ipady=5, padx=15, pady=15)

    isolation_degree_value_label = ttk.Label(language_group_frame, text="0", font=("Arial", 10))
    # isolation_degree_label.grid(row=2, column=0, padx=100, sticky="w")
    isolation_degree_value_label.pack(expand=False, anchor="w", padx=125, pady=5)

    def isolation_degree_horizontal_scale_changed(new_value):
        float_value = float(new_value)
        int_value = round(float_value)
        isolation_degree_value_label["text"] = int_value

    isolation_degree_value = IntVar(value=0)
    isolation_degree_horizontal_scale = ttk.Scale(
        language_group_frame,
        orient=HORIZONTAL,
        length=250,
        from_=0.0,
        to=3.0,
        value=0,
        variable=isolation_degree_value,
        command=isolation_degree_horizontal_scale_changed
    )
    # isolation_degree_horizontal_scale.grid(row=3, column=0, ipady=4, padx=15, pady=15, sticky="w")
    isolation_degree_horizontal_scale.pack(expand=False, anchor="w", padx=15)

    labeled_sounds_label = ttk.Label(language_group_frame, text="Маркированные звуки:", font=("Segoe UI", 14, "bold"), background="#000000")
    labeled_sounds_label.pack(expand=False, fill=X, anchor="w", ipady=5, padx=15, pady=15)

    labeled_sound_columns = ("Sound1", "Sound2")
    labeled_sounds_table = ttk.Treeview(language_group_frame, columns=labeled_sound_columns, show="headings")
    # lexical_unit_table.grid(row=1, column=0, padx=15)
    labeled_sounds_table.pack(expand=False, anchor="w", padx=15)
    labeled_sounds_table.heading("Sound1", text="Заменяемый звук")
    labeled_sounds_table.heading("Sound2", text="Заменяющий звук")

    language_group_frame.pack(fill=BOTH, expand=True)

    """------------------------------LANGUAGE GROUP FRAME------------------------------"""
    # endregion

    # region GenerationFrame
    """------------------------------GENERATION FRAME------------------------------"""

    generation_frame = ttk.Frame(notebook)

    generation_frame.pack(fill=BOTH, expand=True)

    """------------------------------GENERATION FRAME------------------------------"""
    # endregion

    language_group_logo = PhotoImage(file="./LanguageGroup.png")
    language_group_logo = language_group_logo.subsample(20, 20)
    generation_logo = PhotoImage(file="./Generation.png")
    generation_logo = generation_logo.subsample(20, 20)

    notebook.add(language_group_frame, text="Создание языковой группы", image=language_group_logo, compound=LEFT)
    notebook.add(generation_frame, text="Генерация", image=generation_logo, compound=LEFT)

    window.mainloop()


if __name__ == '__main__':
    # start()
    launch_tkinter_app()
