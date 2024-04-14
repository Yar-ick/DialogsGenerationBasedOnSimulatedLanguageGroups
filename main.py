import string

import word_order
import lexical_units
import isolation_degree
import labeled_sounds
import sv_ttk
import json
import os.path
import nltk
import difflib

from characterai import PyCAI
from deep_translator import GoogleTranslator
from tkinter import *
from tkinter import ttk
# from tktooltip import ToolTip
from pymorphy3 import MorphAnalyzer


def launch_nltk_installer():
    import nltk
    nltk.download()


def pymorphy_test():
    morph = MorphAnalyzer()
    parsed_word_variants = morph.parse("правда")

    for word in parsed_word_variants:
        print(word)


def ndiff_test():
    # diff = difflib.ndiff("что", "шо")
    # print('\n'.join(diff))
    print('\n'.join(difflib.Differ().compare("сущего", "сусчеггггго")))


def launch_tkinter_app():
    def on_notebook_tab_selected(event):
        event.widget.selection_clear()

    def on_combobox_selected(event):
        event.widget.selection_clear()

    def load_saved_language_groups(in_list):
        if os.path.isfile("./LanguageGroups.json"):
            with open("LanguageGroups.json", 'r', encoding="utf-8") as infile:
                language_groups_from_json = json.load(infile)

                for language_group in language_groups_from_json:
                    in_list.append(language_group)

    def refill_language_groups_for_combobox(in_language_groups_for_combobox, in_saved_language_groups):
        in_language_groups_for_combobox.clear()

        for language_group in in_saved_language_groups:
            in_language_groups_for_combobox.append(language_group["language_group_name"])

    def get_language_group_from_list(in_language_groups, in_language_group_name):
        for language_group in in_language_groups:
            # print(language_group)
            # print(type(language_group))
            if language_group["language_group_name"] == in_language_group_name:
                return language_group

    def has_index_in_tuple(in_index, in_list_of_dicts):
        result_list = []

        for key in in_list_of_dicts.keys():
            list_from_key = in_list_of_dicts[key]

            for tuple_from_list in list_from_key:
                if tuple_from_list[0] == in_index:
                    result_list.append((True, tuple_from_list[0], tuple_from_list[1], key))

        return result_list if result_list else [(False, None, None, None), (False, None, None, None)]

    def get_tag_from_symbol(in_symbol):
        if in_symbol == "S":
            return "word_order_subject"
        elif in_symbol == "V":
            return "word_order_verb"
        elif in_symbol == "O":
            return "word_order_object"

    window = Tk()
    sv_ttk.set_theme("dark")
    window.title('Диалогус')
    window.iconbitmap(default="./icons/Icon.ico")

    w = 1500
    h = 1080
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    window.geometry("%dx%d+%d+%d" % (w, h, x, y))

    saved_language_groups = []
    load_saved_language_groups(saved_language_groups)

    language_groups_for_combobox = []

    notebook = ttk.Notebook()
    notebook.pack(expand=True, fill=BOTH)
    notebook.bind("<<NotebookTabChanged>>", on_notebook_tab_selected)

    # region LanguageGroupFrame
    """------------------------------LANGUAGE GROUP FRAME SECTION------------------------------"""

    language_group_frame = ttk.Frame(notebook)

    # language_group_scrollbar = ttk.Scrollbar(language_group_frame, orient="vertical")
    # language_group_scrollbar.config(command=language_group_frame.yview)
    # language_group_scrollbar.pack(expand=True, anchor="e", side="right", fill="y")

    # region WordOrder
    """------------------------------WORD ORDER SECTION------------------------------"""

    word_order_label = ttk.Label(
        language_group_frame,
        text="Порядок слов:",
        font=("Segoe UI", 14, "bold"),
        background="#000000"
    )
    word_order_label.pack(expand=False, fill=X, anchor="w", ipady=5, padx=15, pady=15)

    word_orders = [
        "Подлежащее 🠊 сказуемое 🠊 дополнение",
        "Подлежащее 🠊 дополнение 🠊 сказуемое",
        "Сказуемое 🠊 подлежащее 🠊 дополнение",
        "Сказуемое 🠊 дополнение 🠊 подлежащее",
        "Дополнение 🠊 сказуемое 🠊 подлежащее",
        "Дополнение 🠊 подлежащее 🠊 сказуемое"
    ]
    default_word_order_choice = StringVar(value=word_orders[0])

    word_order_combobox = ttk.Combobox(
        language_group_frame,
        textvariable=default_word_order_choice,
        values=word_orders,
        state='readonly',
        width=45,
    )

    word_order_combobox.pack(expand=False, anchor="w", ipady=1, padx=15)
    word_order_combobox.bind("<<ComboboxSelected>>", on_combobox_selected)

    """------------------------------WORD ORDER SECTION END------------------------------"""
    # endregion

    # region LexicalUnits
    """------------------------------LEXICAL UNITS SECTION------------------------------"""

    lexical_unit_label = ttk.Label(
        language_group_frame,
        text="Замена лексических единиц:",
        font=("Segoe UI", 14, "bold"),
        background="#000000"
    )
    lexical_unit_label.pack(expand=False, fill=X, anchor="w", ipady=5, padx=15, pady=15)

    lexical_units_frame = ttk.Frame(language_group_frame)

    ttk.Frame(lexical_units_frame).pack(side="left", padx=7.5)  # Spacer before lexical units table

    lexical_unit_columns = ("Word1", "Word2")
    lexical_units_table = ttk.Treeview(lexical_units_frame, columns=lexical_unit_columns, show="headings")
    lexical_units_table.pack(expand=False, anchor="w", side="left")
    lexical_units_table.heading("Word1", text="Заменяемое слово")
    lexical_units_table.heading("Word2", text="Заменяющее слово")
    lexical_unit_table_scrollbar = ttk.Scrollbar(
        lexical_units_frame,
        orient="vertical",
        command=lexical_units_table.yview
    )
    lexical_units_table.configure(yscroll=lexical_unit_table_scrollbar.set)
    lexical_unit_table_scrollbar.pack(side="left", fill="y")

    lexical_unit_couples = [("терпение", "халтура"), ("наблюдательность", "безолаберность")]

    for lexical_unit in lexical_unit_couples:
        lexical_units_table.insert("", END, values=lexical_unit)

    ttk.Frame(lexical_units_frame).pack(side="left", padx=7.5)  # Spacer after lexical units table

    def on_add_lexical_unit_button_clicked():
        lexical_units_table.insert("", END, values=(first_word_entry.get(), second_word_entry.get()))

    lexical_unit_table_buttons_frame = ttk.Frame(lexical_units_frame)

    add_lexical_unit_button = ttk.Button(
        lexical_unit_table_buttons_frame,
        text="Добавить",
        command=on_add_lexical_unit_button_clicked
    )
    add_lexical_unit_button.pack(anchor="e", side="left")

    def on_remove_lexical_unit_button_clicked():
        for selected_item in lexical_units_table.selection():
            lexical_units_table.delete(selected_item)

    remove_lexical_unit_button = ttk.Button(
        lexical_unit_table_buttons_frame,
        text="Удалить",
        command=on_remove_lexical_unit_button_clicked
    )

    remove_lexical_unit_button.pack(anchor="e", side="left", padx=15)
    lexical_unit_table_buttons_frame.pack(expand=False, anchor="nw")

    lexical_unit_table_input_fields_frame = ttk.Frame(lexical_units_frame)

    first_word_entry = ttk.Entry(lexical_unit_table_input_fields_frame)
    first_word_entry.insert(0, "Заменяемое слово")
    first_word_entry.pack(anchor="e", side="left")

    switch_on_lexical_unit_label = ttk.Label(
        lexical_unit_table_input_fields_frame,
        text="Заменить на:",
        font=("Segoe UI", 12)
    )
    switch_on_lexical_unit_label.pack(expand=False, anchor="w", side="left", padx=15)

    second_word_entry = ttk.Entry(lexical_unit_table_input_fields_frame)
    second_word_entry.insert(0, "Заменяющее слово")
    second_word_entry.pack(anchor="e", side="left")

    lexical_unit_table_input_fields_frame.pack(expand=False, anchor="w", pady=15)
    lexical_units_frame.pack(expand=False, anchor="w")

    """------------------------------LEXICAL UNITS SECTION END------------------------------"""
    # endregion

    # region IsolationDegree
    """------------------------------ISOLATION DEGREE SECTION------------------------------"""

    isolation_degree_label = ttk.Label(
        language_group_frame,
        text="Степень изолированности:",
        font=("Segoe UI", 14, "bold"),
        background="#000000"
    )
    isolation_degree_label.pack(expand=False, fill=X, anchor="w", ipady=5, padx=15, pady=15)

    isolation_degree_value_label = ttk.Label(language_group_frame, text="0", font=("Segoe UI", 12))
    isolation_degree_value_label.pack(expand=False, anchor="w", padx=210)

    def isolation_degree_horizontal_scale_changed(new_value):
        float_value = float(new_value)
        int_value = round(float_value)
        isolation_degree_value_label["text"] = int_value

    isolation_degree_value = IntVar(value=0)
    isolation_degree_horizontal_scale = ttk.Scale(
        language_group_frame,
        orient=HORIZONTAL,
        length=410,
        from_=0.0,
        to=3.0,
        value=0,
        variable=isolation_degree_value,
        command=isolation_degree_horizontal_scale_changed
    )
    isolation_degree_horizontal_scale.pack(expand=False, anchor="w", padx=15)
    # tooltip = ToolTip(
    #     isolation_degree_horizontal_scale,
    #     msg="Чем выше степень изолированности, тем больше слов будет поставлено в нормальную форму",
    #     follow=True,
    #     refresh=60
    # )

    """------------------------------ISOLATION DEGREE SECTION END------------------------------"""
    # endregion

    # region LabeledSounds
    """------------------------------LABELED SOUNDS SECTION------------------------------"""

    labeled_sounds_label = ttk.Label(
        language_group_frame,
        text="Маркированные звуки:",
        font=("Segoe UI", 14, "bold"),
        background="#000000"
    )
    labeled_sounds_label.pack(expand=False, fill=X, anchor="w", ipady=5, padx=15, pady=15)

    labeled_sounds_frame = ttk.Frame(language_group_frame)

    ttk.Frame(labeled_sounds_frame).pack(side="left", padx=7.5)  # Spacer before labeled sound table

    labeled_sound_columns = ("Sound1", "Sound2")
    labeled_sounds_table = ttk.Treeview(labeled_sounds_frame, columns=labeled_sound_columns, show="headings")
    labeled_sounds_table.pack(expand=False, anchor="w", side="left")
    labeled_sounds_table.heading("Sound1", text="Заменяемый звук")
    labeled_sounds_table.heading("Sound2", text="Заменяющий звук")
    labeled_sounds_table_scrollbar = ttk.Scrollbar(
        labeled_sounds_frame,
        orient="vertical",
        command=labeled_sounds_table.yview
    )
    labeled_sounds_table.configure(yscroll=labeled_sounds_table_scrollbar.set)
    labeled_sounds_table_scrollbar.pack(side="left", fill="y")

    ttk.Frame(labeled_sounds_frame).pack(side="left", padx=7.5)  # Spacer after labeled sound table

    def on_add_labeled_sound_button_clicked():
        labeled_sounds_table.insert(
            "",
            END,
            values=(first_labeled_sound_combobox.get(), second_labeled_sound_combobox.get())
        )

    labeled_sound_table_buttons_frame = ttk.Frame(labeled_sounds_frame)

    add_labeled_sound_button = ttk.Button(
        labeled_sound_table_buttons_frame,
        text="Добавить",
        command=on_add_labeled_sound_button_clicked
    )
    add_labeled_sound_button.pack(anchor="e", side="left")

    def on_remove_labeled_sound_button_clicked():
        for selected_item in labeled_sounds_table.selection():
            labeled_sounds_table.delete(selected_item)

    remove_labeled_sound_button = ttk.Button(
        labeled_sound_table_buttons_frame,
        text="Удалить",
        command=on_remove_labeled_sound_button_clicked
    )
    remove_labeled_sound_button.pack(anchor="e", side="left", padx=15)
    labeled_sound_table_buttons_frame.pack(expand=False, anchor="nw")

    labeled_sound_table_input_fields_frame = ttk.Frame(labeled_sounds_frame)

    russian_labeled_sounds = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р',
                              'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    english_labeled_sounds = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                              's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    kazakh_labeled_sounds = ['а', 'ә', 'б', 'в', 'г', 'ғ', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'қ', 'л', 'м', 'н',
                             'ң', 'о', 'ө', 'п', 'р', 'с', 'т', 'у', 'ұ', 'ү', 'ф', 'х', 'һ', 'ц', 'ч', 'ш', 'щ', 'ъ',
                             'ы', 'і', 'ь', 'э', 'ю', 'я']

    default_first_labeled_sound = StringVar(value=russian_labeled_sounds[0])

    first_labeled_sound_combobox = ttk.Combobox(
        labeled_sound_table_input_fields_frame,
        textvariable=default_first_labeled_sound,
        values=russian_labeled_sounds,
        width=2
    )
    first_labeled_sound_combobox.pack(anchor="e", side="left")
    first_labeled_sound_combobox.bind("<<ComboboxSelected>>", on_combobox_selected)

    switch_on_labeled_sound_label = ttk.Label(
        labeled_sound_table_input_fields_frame,
        text="Заменить на:",
        font=("Segoe UI", 12)
    )
    switch_on_labeled_sound_label.pack(expand=False, anchor="w", side="left", padx=15)

    def on_labeled_sound_language_combobox_selected(event):
        selection = labeled_sound_language_combobox.get()

        if selection == "Русский звук":
            second_labeled_sound_combobox.configure(values=russian_labeled_sounds)
            second_labeled_sound_combobox.set(russian_labeled_sounds[0])
        elif selection == "Английский звук":
            second_labeled_sound_combobox.configure(values=english_labeled_sounds)
            second_labeled_sound_combobox.set(english_labeled_sounds[0])
        elif selection == "Казахский звук":
            second_labeled_sound_combobox.configure(values=kazakh_labeled_sounds)
            second_labeled_sound_combobox.set(kazakh_labeled_sounds[0])

        labeled_sound_language_combobox.selection_clear()

    second_labeled_sounds_language = ["Русский звук", "Английский звук", "Казахский звук", "Греческий звук"]

    default_second_labeled_sounds_language = StringVar(value=second_labeled_sounds_language[0])

    labeled_sound_language_combobox = ttk.Combobox(
        labeled_sound_table_input_fields_frame,
        textvariable=default_second_labeled_sounds_language,
        values=second_labeled_sounds_language,
        state='readonly'
    )
    labeled_sound_language_combobox.pack(anchor="e", side="left")
    labeled_sound_language_combobox.bind("<<ComboboxSelected>>", on_labeled_sound_language_combobox_selected)

    spacer_after_labeled_sound_language_combobox = ttk.Frame(labeled_sound_table_input_fields_frame)
    spacer_after_labeled_sound_language_combobox.pack(side="left", padx=7.5)

    default_second_labeled_sound = StringVar(value=russian_labeled_sounds[0])

    second_labeled_sound_combobox = ttk.Combobox(
        labeled_sound_table_input_fields_frame,
        textvariable=default_second_labeled_sound,
        values=russian_labeled_sounds,
        width=2
    )
    second_labeled_sound_combobox.pack(anchor="e", side="left")
    second_labeled_sound_combobox.bind("<<ComboboxSelected>>", on_combobox_selected)

    labeled_sound_table_input_fields_frame.pack(expand=False, anchor="w", pady=15)
    labeled_sounds_frame.pack(expand=False, anchor="w")

    """------------------------------LABELED SOUNDS SECTION END------------------------------"""
    # endregion

    # region Saving
    """------------------------------SAVING SECTION------------------------------"""

    save_label = ttk.Label(
        language_group_frame,
        text="Сохранение:",
        font=("Segoe UI", 14, "bold"),
        background="#000000"
    )
    save_label.pack(expand=False, fill=X, anchor="w", ipady=5, padx=15, pady=15)

    save_input_frame = ttk.Frame(language_group_frame)

    # language_group_label = ttk.Label(
    #     save_input_frame,
    #     text="Имя моделируемой языковой группы:",
    #     font=("Segoe UI", 12)
    # )
    # language_group_label.pack(expand=False, side="left")

    language_group_name_entry = ttk.Entry(save_input_frame, width=32)
    language_group_name_entry.insert(0, "Имя моделируемой языковой группы")
    language_group_name_entry.pack(side="left")

    def on_save_button_clicked():
        saved_language_groups.clear()
        lexical_units_to_write = {}
        labeled_sounds_to_write = {}

        for child in lexical_units_table.get_children(""):
            lexical_units_to_write.update({lexical_units_table.set(child, 0): lexical_units_table.set(child, 1)})

        for child in labeled_sounds_table.get_children(""):
            labeled_sounds_to_write.update({labeled_sounds_table.set(child, 0): labeled_sounds_table.set(child, 1)})

        save_dictionary = {
            "language_group_name": language_group_name_entry.get(),
            "word_order": word_order_combobox.current(),
            "lexical_units": lexical_units_to_write,
            "isolation_degree": isolation_degree_value.get(),
            "labeled_sounds": labeled_sounds_to_write
        }
        saved_language_groups.append(save_dictionary)

        load_saved_language_groups(saved_language_groups)
        refill_language_groups_for_combobox(language_groups_for_combobox, saved_language_groups)
        selected_language_group_combobox.configure(values=language_groups_for_combobox)

        json_save = json.dumps(saved_language_groups, indent=4, ensure_ascii=False)
        # json_save = json_save.encode("utf-8").decode("utf-8")

        with open("LanguageGroups.json", "w", encoding="utf-8") as outfile:
            outfile.write(json_save)

    save_button = ttk.Button(
        save_input_frame,
        text="Сохранить языковую группу",
        command=on_save_button_clicked
    )
    save_button.pack(fill=BOTH, side="left", padx=15)

    save_input_frame.pack(anchor="w", padx=15)

    """------------------------------SAVING SECTION END------------------------------"""
    # endregion

    language_group_frame.pack(fill=BOTH, expand=True)

    """------------------------------LANGUAGE GROUP FRAME SECTION END------------------------------"""
    # endregion

    # region TextTransformationFrame
    """------------------------------TEXT TRANSFORMATION FRAME SECTION------------------------------"""

    text_transformation_frame = ttk.Frame(notebook)

    # region FastSettings
    """------------------------------FAST SETTINGS SECTION------------------------------"""

    fast_settings_frame = ttk.Frame(text_transformation_frame)

    selected_language_group_fast_frame = ttk.Frame(fast_settings_frame)

    selected_language_group_fast_label = ttk.Label(
        selected_language_group_fast_frame,
        text="Исходная языковая группа:",
        font=("Segoe UI", 12)
    )

    refill_language_groups_for_combobox(language_groups_for_combobox, saved_language_groups)

    language_group_fast_choice = StringVar(value=language_groups_for_combobox[0])

    def on_selected_language_group_fast_combobox_selected(event):
        event.widget.selection_clear()

        selected_language_group = get_language_group_from_list(
            saved_language_groups,
            language_group_fast_choice.get()
        )

        word_order_fast_combobox.set(word_orders[selected_language_group["word_order"]])
        lexical_units_fast_table.delete(*lexical_units_fast_table.get_children())
        for item in selected_language_group["lexical_units"]:
            lexical_units_fast_table.insert("", END, values=(item, selected_language_group["lexical_units"][item]))
        isolation_degree_horizontal_fast_scale.set(selected_language_group["isolation_degree"])
        labeled_sounds_fast_table.delete(*labeled_sounds_fast_table.get_children())
        for item in selected_language_group["labeled_sounds"]:
            labeled_sounds_fast_table.insert("", END, values=(item, selected_language_group["labeled_sounds"][item]))

    selected_language_group_fast_combobox = ttk.Combobox(
        selected_language_group_fast_frame,
        textvariable=language_group_fast_choice,
        values=language_groups_for_combobox,
        state='readonly',
        width=19,
    )

    selected_language_group_fast_combobox.bind("<<ComboboxSelected>>",
                                               on_selected_language_group_fast_combobox_selected)

    word_order_fast_label = ttk.Label(
        fast_settings_frame,
        text="Порядок слов:",
        font=("Segoe UI", 14, "bold"),
        background="#000000"
    )

    word_order_fast_choice = StringVar(value=word_orders[0])

    word_order_fast_combobox = ttk.Combobox(
        fast_settings_frame,
        textvariable=word_order_fast_choice,
        values=word_orders,
        state='readonly',
        width=45,
    )
    word_order_fast_combobox.bind("<<ComboboxSelected>>", on_combobox_selected)

    lexical_units_fast_label = ttk.Label(
        fast_settings_frame,
        text="Замена лексических единиц:",
        font=("Segoe UI", 14, "bold"),
        background="#000000"
    )

    lexical_units_fast_table_frame = ttk.Frame(fast_settings_frame)
    lexical_units_fast_table_buttons_frame = ttk.Frame(lexical_units_fast_table_frame)
    lexical_units_fast_table_other_frame = ttk.Frame(lexical_units_fast_table_frame)

    def on_add_lexical_unit_fast_button_clicked():
        lexical_units_fast_table.insert("", END, values=('-', '-'))

    def on_remove_lexical_unit_fast_button_clicked():
        for selected_item in lexical_units_fast_table.selection():
            lexical_units_fast_table.delete(selected_item)

    add_lexical_unit_fast_button = ttk.Button(
        lexical_units_fast_table_buttons_frame,
        text="+",
        command=on_add_lexical_unit_fast_button_clicked
    )

    remove_lexical_unit_fast_button = ttk.Button(
        lexical_units_fast_table_buttons_frame,
        text="-",
        command=on_remove_lexical_unit_fast_button_clicked
    )

    def on_lexical_units_fast_table_item_selected(event):
        if not event.widget.focus():
            return

        w = 500
        h = 110
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        lexical_units_fast_table_edit_row_window = Tk()
        lexical_units_fast_table_edit_row_window.resizable(False, False)
        sv_ttk.set_theme("dark", lexical_units_fast_table_edit_row_window)
        lexical_units_fast_table_edit_row_window.title("Редактирование строки")
        lexical_units_fast_table_edit_row_window.geometry("%dx%d+%d+%d" % (w, h, x, y))

        lexical_units_fast_table_edit_row_input_frame = ttk.Frame(lexical_units_fast_table_edit_row_window)

        first_word_fast_entry = ttk.Entry(lexical_units_fast_table_edit_row_input_frame)
        first_word_fast_entry.insert(0, lexical_units_fast_table.set(lexical_units_fast_table.focus(), 0))

        switch_on_lexical_unit_fast_label = ttk.Label(
            lexical_units_fast_table_edit_row_input_frame,
            text="Заменить на:",
            font=("Segoe UI", 12)
        )

        second_word_fast_entry = ttk.Entry(lexical_units_fast_table_edit_row_input_frame)
        second_word_fast_entry.insert(0, lexical_units_fast_table.set(lexical_units_fast_table.focus(), 1))

        lexical_units_fast_table_edit_row_buttons_frame = ttk.Frame(lexical_units_fast_table_edit_row_window)

        def on_confirm_lexical_unit_fast_edit_row_button_clicked():
            selected_item = lexical_units_fast_table.focus()
            lexical_units_fast_table.item(
                selected_item,
                text="",
                values=(first_word_fast_entry.get(), second_word_fast_entry.get())
            )
            lexical_units_fast_table_edit_row_window.destroy()

        def on_cancel_lexical_unit_fast_edit_row_button_clicked():
            lexical_units_fast_table_edit_row_window.destroy()

        confirm_lexical_unit_fast_edit_row_button = ttk.Button(
            lexical_units_fast_table_edit_row_buttons_frame,
            text="Изменить",
            command=on_confirm_lexical_unit_fast_edit_row_button_clicked
        )

        cancel_lexical_unit_fast_edit_row_button = ttk.Button(
            lexical_units_fast_table_edit_row_buttons_frame,
            text="Отмена",
            command=on_cancel_lexical_unit_fast_edit_row_button_clicked
        )

        first_word_fast_entry.pack(anchor="e", side="left")
        switch_on_lexical_unit_fast_label.pack(expand=False, anchor="w", side="left", padx=15)
        second_word_fast_entry.pack(anchor="e", side="left")
        lexical_units_fast_table_edit_row_input_frame.pack(anchor="nw", padx=15, pady=15)

        confirm_lexical_unit_fast_edit_row_button.pack(fill=X, expand=True, anchor="e", side="left")
        ttk.Frame(lexical_units_fast_table_edit_row_buttons_frame).pack(side="left", padx=2.5)  # Vertical spacer
        cancel_lexical_unit_fast_edit_row_button.pack(fill=X, expand=True, anchor="e", side="left")
        lexical_units_fast_table_edit_row_buttons_frame.pack(fill=X, anchor="w", padx=15)

    lexical_units_fast_table = ttk.Treeview(
        lexical_units_fast_table_other_frame,
        columns=lexical_unit_columns,
        show="headings",
        height=9
    )
    lexical_units_fast_table.heading("Word1", text="Заменяемое слово")
    lexical_units_fast_table.heading("Word2", text="Заменяющее слово")
    lexical_unit_fast_table_scrollbar = ttk.Scrollbar(
        lexical_units_fast_table_other_frame,
        orient="vertical",
        command=lexical_units_fast_table.yview
    )
    lexical_units_fast_table.configure(yscroll=lexical_unit_fast_table_scrollbar.set)
    lexical_units_fast_table.bind("<Double-Button-1>", on_lexical_units_fast_table_item_selected)

    isolation_degree_fast_label = ttk.Label(
        fast_settings_frame,
        text="Степень изолированности:",
        font=("Segoe UI", 14, "bold"),
        background="#000000"
    )

    isolation_degree_fast_frame = ttk.Frame(fast_settings_frame)

    isolation_degree_value_fast_label = ttk.Label(isolation_degree_fast_frame, text="0", font=("Segoe UI", 12))

    def isolation_degree_horizontal_fast_scale_changed(new_value):
        float_value = float(new_value)
        int_value = round(float_value)
        isolation_degree_value_fast_label["text"] = int_value
        isolation_degree_fast_value.set(int_value)

    isolation_degree_fast_value = IntVar(value=0)
    isolation_degree_horizontal_fast_scale = ttk.Scale(
        isolation_degree_fast_frame,
        orient=HORIZONTAL,
        length=410,
        from_=0.0,
        to=3.0,
        value=0,
        variable=isolation_degree_fast_value,
        command=isolation_degree_horizontal_fast_scale_changed
    )

    labeled_sounds_fast_label = ttk.Label(
        fast_settings_frame,
        text="Маркированные звуки:",
        font=("Segoe UI", 14, "bold"),
        background="#000000"
    )

    labeled_sounds_fast_table_frame = ttk.Frame(fast_settings_frame)
    labeled_sounds_fast_table_buttons_frame = ttk.Frame(labeled_sounds_fast_table_frame)
    labeled_sounds_fast_table_other_frame = ttk.Frame(labeled_sounds_fast_table_frame)

    def on_add_labeled_sound_fast_button_clicked():
        labeled_sounds_fast_table.insert("", END, values=('-', '-'))

    def on_remove_labeled_sound_fast_button_clicked():
        for selected_item in labeled_sounds_fast_table.selection():
            labeled_sounds_fast_table.delete(selected_item)

    add_labeled_sound_fast_button = ttk.Button(
        labeled_sounds_fast_table_buttons_frame,
        text="+",
        command=on_add_labeled_sound_fast_button_clicked
    )

    remove_labeled_sound_fast_button = ttk.Button(
        labeled_sounds_fast_table_buttons_frame,
        text="-",
        command=on_remove_labeled_sound_fast_button_clicked
    )

    def on_labeled_sounds_fast_table_item_selected(event):
        if not event.widget.focus():
            return

        w = 500
        h = 110
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        labeled_sounds_fast_table_edit_row_window = Tk()
        labeled_sounds_fast_table_edit_row_window.resizable(False, False)
        sv_ttk.set_theme("dark", labeled_sounds_fast_table_edit_row_window)
        labeled_sounds_fast_table_edit_row_window.title("Редактирование строки")
        labeled_sounds_fast_table_edit_row_window.geometry("%dx%d+%d+%d" % (w, h, x, y))

        lexical_units_fast_table_edit_row_input_frame = ttk.Frame(labeled_sounds_fast_table_edit_row_window)

        first_word_fast_entry = ttk.Entry(lexical_units_fast_table_edit_row_input_frame)
        first_word_fast_entry.insert(0, labeled_sounds_fast_table.set(labeled_sounds_fast_table.focus(), 0))

        switch_on_lexical_unit_fast_label = ttk.Label(
            lexical_units_fast_table_edit_row_input_frame,
            text="Заменить на:",
            font=("Segoe UI", 12)
        )

        second_word_fast_entry = ttk.Entry(lexical_units_fast_table_edit_row_input_frame)
        second_word_fast_entry.insert(0, labeled_sounds_fast_table.set(labeled_sounds_fast_table.focus(), 1))

        labeled_sounds_fast_table_edit_row_buttons_frame = ttk.Frame(labeled_sounds_fast_table_edit_row_window)

        def on_confirm_labeled_sound_fast_edit_row_button_clicked():
            selected_item = labeled_sounds_fast_table.focus()
            labeled_sounds_fast_table.item(
                selected_item,
                text="",
                values=(first_word_fast_entry.get(), second_word_fast_entry.get())
            )
            labeled_sounds_fast_table_edit_row_window.destroy()

        def on_cancel_labeled_sound_fast_edit_row_button_clicked():
            labeled_sounds_fast_table_edit_row_window.destroy()

        confirm_labeled_sound_fast_edit_row_button = ttk.Button(
            labeled_sounds_fast_table_edit_row_buttons_frame,
            text="Изменить",
            command=on_confirm_labeled_sound_fast_edit_row_button_clicked
        )

        cancel_labeled_sound_fast_edit_row_button = ttk.Button(
            labeled_sounds_fast_table_edit_row_buttons_frame,
            text="Отмена",
            command=on_cancel_labeled_sound_fast_edit_row_button_clicked
        )

        first_word_fast_entry.pack(anchor="e", side="left")
        switch_on_lexical_unit_fast_label.pack(expand=False, anchor="w", side="left", padx=15)
        second_word_fast_entry.pack(anchor="e", side="left")
        lexical_units_fast_table_edit_row_input_frame.pack(anchor="nw", padx=15, pady=15)

        confirm_labeled_sound_fast_edit_row_button.pack(fill=X, expand=True, anchor="e", side="left")
        ttk.Frame(labeled_sounds_fast_table_edit_row_buttons_frame).pack(side="left", padx=2.5)  # Vertical spacer
        cancel_labeled_sound_fast_edit_row_button.pack(fill=X, expand=True, anchor="e", side="left")
        labeled_sounds_fast_table_edit_row_buttons_frame.pack(fill=X, anchor="w", padx=15)

    labeled_sounds_fast_table = ttk.Treeview(
        labeled_sounds_fast_table_other_frame,
        columns=labeled_sound_columns,
        show="headings",
        height=9
    )
    labeled_sounds_fast_table.heading("Sound1", text="Заменяемый звук")
    labeled_sounds_fast_table.heading("Sound2", text="Заменяющий звук")
    labeled_sound_fast_table_scrollbar = ttk.Scrollbar(
        labeled_sounds_fast_table_other_frame,
        orient="vertical",
        command=labeled_sounds_fast_table.yview
    )
    labeled_sounds_fast_table.configure(yscroll=labeled_sound_fast_table_scrollbar.set)
    labeled_sounds_fast_table.bind("<Double-Button-1>", on_labeled_sounds_fast_table_item_selected)

    """------------------------------FAST SETTINGS SECTION END------------------------------"""
    # endregion

    # region TextTransformation
    """------------------------------TEXT TRANSFORMATION SECTION------------------------------"""

    transformation_field_frame = ttk.Frame(text_transformation_frame)

    transformation_legend_frame = ttk.Frame(transformation_field_frame)

    word_order_legend_frame = ttk.Frame(transformation_legend_frame)

    word_order_subject_legend_frame = ttk.Frame(word_order_legend_frame)

    word_order_subject_legend_label = ttk.Label(
        word_order_subject_legend_frame,
        text="{ }",
        font=("Segoe UI", 16),
        foreground="red"
    )

    word_order_subject_description_legend_label = ttk.Label(
        word_order_subject_legend_frame,
        text=" - подлежащее",
        font=("Segoe UI", 12)
    )

    word_order_verb_legend_frame = ttk.Frame(word_order_legend_frame)

    word_order_verb_legend_label = ttk.Label(
        word_order_verb_legend_frame,
        text="{ }",
        font=("Segoe UI", 16),
        foreground="green"
    )

    word_order_verb_description_legend_label = ttk.Label(
        word_order_verb_legend_frame,
        text=" - сказуемое",
        font=("Segoe UI", 12)
    )

    word_order_object_legend_frame = ttk.Frame(word_order_legend_frame)

    word_order_object_legend_label = ttk.Label(
        word_order_object_legend_frame,
        text="{ }",
        font=("Segoe UI", 16),
        foreground="blue"
    )

    word_order_object_description_legend_label = ttk.Label(
        word_order_object_legend_frame,
        text=" - дополнение",
        font=("Segoe UI", 12)
    )

    lexical_units_legend_frame = ttk.Frame(transformation_legend_frame)

    lexical_units_legend_label = ttk.Label(
        lexical_units_legend_frame,
        text="( )",
        font=("Segoe UI", 16),
        foreground="yellow"
    )

    lexical_units_description_legend_label = ttk.Label(
        lexical_units_legend_frame,
        text=" - заменённая лексическая единица",
        font=("Segoe UI", 12)
    )

    isolation_degree_legend_frame = ttk.Frame(transformation_legend_frame)

    isolation_degree_legend_label = ttk.Label(
        isolation_degree_legend_frame,
        text="А",
        font=("Segoe UI", 16),
        foreground="red"
    )

    isolation_degree_description_legend_label = ttk.Label(
        isolation_degree_legend_frame,
        text=" - изолированное слово",
        font=("Segoe UI", 12)
    )

    labeled_sound_legend_frame = ttk.Frame(transformation_legend_frame)

    labeled_sound_legend_label = ttk.Label(
        labeled_sound_legend_frame,
        text="   ",
        font=("Segoe UI", 16),
        background="#3A58CF"
    )

    labeled_sound_description_legend_label = ttk.Label(
        labeled_sound_legend_frame,
        text=" - маркированный звук",
        font=("Segoe UI", 12)
    )

    transformed_text_widget_frame = ttk.Frame(transformation_field_frame)

    transformed_text_widget = Text(transformed_text_widget_frame, height=25, font=("Segoe UI", 12), wrap="word")
    transformed_text_widget_scrollbar = ttk.Scrollbar(
        transformed_text_widget_frame,
        orient="vertical",
        command=transformed_text_widget.yview
    )
    transformed_text_widget["yscrollcommand"] = transformed_text_widget_scrollbar.set
    transformed_text_widget.tag_configure("just_bold_segoe", font=("Segoe UI", 12, "bold"))
    transformed_text_widget.tag_configure("word_order_subject", foreground="red", font=("Segoe UI", 16, "bold"))
    transformed_text_widget.tag_configure("word_order_verb", foreground="green", font=("Segoe UI", 16, "bold"))
    transformed_text_widget.tag_configure("word_order_object", foreground="blue", font=("Segoe UI", 16, "bold"))
    transformed_text_widget.tag_configure("replaced_lexical_unit", foreground="yellow", font=("Segoe UI", 12, "bold"))
    transformed_text_widget.tag_configure("isolated_word", foreground="red", font=("Segoe UI", 12))
    transformed_text_widget.tag_configure("labeled_sound", background="#3A58CF", font=("Segoe UI", 12))
    transformed_text_widget.tag_configure(
        "labeled_sound_in_isolated_word",
        foreground="red",
        background="#3A58CF",
        font=("Segoe UI", 12)
    )

    input_text_widget_frame = ttk.Frame(transformation_field_frame)

    input_text_widget = Text(input_text_widget_frame, height=10, font=("Segoe UI", 12), wrap="word")
    input_text_widget_scrollbar = ttk.Scrollbar(
        input_text_widget_frame,
        orient="vertical",
        command=input_text_widget.yview
    )
    input_text_widget["yscrollcommand"] = input_text_widget_scrollbar.set

    text_image = PhotoImage(file="./icons/Text.png")
    text_image = text_image.subsample(15, 15)
    gear_image = PhotoImage(file="./icons/Gear.png")
    gear_image = gear_image.subsample(12, 12)

    def on_transform_text_button_clicked():
        def try_to_print_open_bracket(in_is_index_in_svo_phrase):
            for result_tuple in in_is_index_in_svo_phrase:
                if result_tuple[0] and result_tuple[2] == '{':
                    transformed_text_widget.insert(
                        END,
                        '{',
                        get_tag_from_symbol(result_tuple[3])
                    )

        def try_to_print_close_bracket(in_is_index_in_svo_phrase):
            for result_tuple in in_is_index_in_svo_phrase:
                if result_tuple[0] and result_tuple[2] == '}':
                    transformed_text_widget.insert(
                        END,
                        '}',
                        get_tag_from_symbol(result_tuple[3])
                    )

        input_text = input_text_widget.get("1.0", END)

        if not input_text:
            return

        fast_lexical_units = {}
        fast_labeled_sounds = {}

        for child in lexical_units_fast_table.get_children(""):
            fast_lexical_units.update({lexical_units_fast_table.set(child, 0): lexical_units_fast_table.set(child, 1)})

        for child in labeled_sounds_fast_table.get_children(""):
            fast_labeled_sounds.update(
                {labeled_sounds_fast_table.set(child, 0): labeled_sounds_fast_table.set(child, 1)})

        fast_language_group = {
            "word_order": word_order_fast_combobox.current(),
            "lexical_units": fast_lexical_units,
            "isolation_degree": isolation_degree_fast_value.get(),
            "labeled_sounds": fast_labeled_sounds
        }

        input_text_widget.delete("1.0", END)

        transformed_text_widget.image_create(END, image=text_image)
        transformed_text_widget.insert(END, " Исходный текст:\n", "just_bold_segoe")
        transformed_text_widget.insert(END, input_text + "\n\n")

        transformed_text_widget.image_create(END, image=gear_image)
        transformed_text_widget.insert(END, " Преобразованный текст:\n", "just_bold_segoe")

        # Input string split like this because nltk.tokenize does not take into account \n symbol
        paragraphs = [p for p in input_text.split('\n') if p]

        for paragraph in paragraphs:
            sentence_tokens = nltk.sent_tokenize(paragraph)

            for sentence_token in sentence_tokens:
                word_tokens = nltk.word_tokenize(sentence_token)

                word_order_result = word_order.change_text_word_order(
                    word_tokens,
                    word_order.WordOrder(fast_language_group["word_order"]),
                    False
                )

                lexical_units_result = lexical_units.replace_lexical_units_in_text(
                    word_order_result[0],
                    fast_language_group["lexical_units"],
                    False
                )

                isolation_degree_result = isolation_degree.change_text_isolation_degree_list(
                    lexical_units_result[0],
                    fast_language_group["isolation_degree"]
                )

                labeled_sounds_result = labeled_sounds.apply_labeled_sounds_to_text(
                    isolation_degree_result[0],
                    fast_language_group["labeled_sounds"]
                )

                final_result = labeled_sounds_result[0]

                for i in range(len(final_result)):
                    final_result[i] = final_result[i].lower()

                final_result[0] = final_result[0].capitalize()

                token_was_replaced = False
                # print("Final Result: ", final_result)

                for i in range(len(final_result)):
                    if final_result[i] == ' ':
                        continue

                    is_index_in_svo_phrase = has_index_in_tuple(i, word_order_result[1])

                    try_to_print_open_bracket(is_index_in_svo_phrase)

                    # print("Is index ", i, " in SVO Phrase: ", is_index_in_svo_phrase)

                    if i in lexical_units_result[1]:
                        token_was_replaced = True
                        transformed_text_widget.insert(END, '(', "replaced_lexical_unit")

                    if i in isolation_degree_result[1]:
                        if i in labeled_sounds_result[1].keys():
                            for j in range(len(final_result[i])):
                                if j in labeled_sounds_result[1][i]:
                                    transformed_text_widget.insert(
                                        END,
                                        final_result[i][j],
                                        "labeled_sound_in_isolated_word"
                                    )
                                else:
                                    transformed_text_widget.insert(END, final_result[i][j], "isolated_word")

                            if token_was_replaced:
                                transformed_text_widget.insert(END, ')', "replaced_lexical_unit")

                            try_to_print_close_bracket(is_index_in_svo_phrase)

                            transformed_text_widget.insert(
                                END,
                                ' ' if i + 1 <= len(final_result) - 1 and final_result[
                                    i + 1] not in string.punctuation else ''
                            )
                        else:
                            transformed_text_widget.insert(END, final_result[i], "isolated_word")

                            if token_was_replaced:
                                transformed_text_widget.insert(END, ')', "replaced_lexical_unit")

                            try_to_print_close_bracket(is_index_in_svo_phrase)

                            transformed_text_widget.insert(
                                END,
                                (' ' if i + 1 <= len(final_result) - 1 and final_result[
                                    i + 1] not in string.punctuation else '')
                            )
                    else:
                        if i in labeled_sounds_result[1].keys():
                            for j in range(len(final_result[i])):
                                if j in labeled_sounds_result[1][i]:
                                    transformed_text_widget.insert(END, final_result[i][j], "labeled_sound")
                                else:
                                    transformed_text_widget.insert(END, final_result[i][j])

                            if token_was_replaced:
                                transformed_text_widget.insert(END, ')', "replaced_lexical_unit")

                            try_to_print_close_bracket(is_index_in_svo_phrase)

                            transformed_text_widget.insert(
                                END,
                                ' ' if i + 1 <= len(final_result) - 1 and final_result[
                                    i + 1] not in string.punctuation else ''
                            )
                        else:
                            transformed_text_widget.insert(END, final_result[i])

                            if token_was_replaced:
                                transformed_text_widget.insert(END, ')', "replaced_lexical_unit")

                            try_to_print_close_bracket(is_index_in_svo_phrase)

                            transformed_text_widget.insert(
                                END,
                                (' ' if i + 1 <= len(final_result) - 1 and final_result[
                                    i + 1] not in string.punctuation else '')
                            )

                    token_was_replaced = False

                print('\n')

                transformed_text_widget.insert(END, ' ')

            transformed_text_widget.insert(END, "\n\n")

    transform_text_button = ttk.Button(
        transformation_field_frame,
        text="Преобразовать текст",
        command=on_transform_text_button_clicked
    )

    """------------------------------TEXT TRANSFORMATION SECTION END------------------------------"""
    # endregion

    # For start autofill
    selected_language_group_fast_combobox.event_generate("<<ComboboxSelected>>")

    # region Packing
    ttk.Frame(fast_settings_frame).pack(pady=7.5)  # Horizontal spacer before all

    selected_language_group_fast_label.pack(expand=False, anchor="w", side="left")
    selected_language_group_fast_combobox.pack(expand=False, anchor="w", side="left", ipady=1, padx=15)
    selected_language_group_fast_frame.pack(anchor="w")

    ttk.Frame(fast_settings_frame).pack(pady=7.5)  # Horizontal spacer

    word_order_fast_label.pack(expand=False, fill=X, anchor="w", ipady=5)

    ttk.Frame(fast_settings_frame).pack(pady=7.5)  # Horizontal spacer

    word_order_fast_combobox.pack(expand=False, anchor="w", ipady=1)

    ttk.Frame(fast_settings_frame).pack(pady=7.5)  # Horizontal spacer

    lexical_units_fast_label.pack(expand=False, fill=X, anchor="w", ipady=5)

    ttk.Frame(fast_settings_frame).pack(pady=7.5)  # Horizontal spacer

    add_lexical_unit_fast_button.pack(fill=BOTH, expand=True, side="left")
    ttk.Frame(lexical_units_fast_table_buttons_frame).pack(side="left", padx=2.5)  # Vertical spacer
    remove_lexical_unit_fast_button.pack(fill=BOTH, expand=True, side="left")
    ttk.Frame(lexical_units_fast_table_buttons_frame).pack(side="left", padx=12)  # Vertical spacer
    lexical_units_fast_table_buttons_frame.pack(fill=X, expand=True, anchor="w")
    ttk.Frame(lexical_units_fast_table_frame).pack(pady=2.5)  # Horizontal spacer
    lexical_units_fast_table.pack(expand=False, side="left")
    lexical_unit_fast_table_scrollbar.pack(side="left", fill=Y)
    lexical_units_fast_table_other_frame.pack(anchor="w")
    lexical_units_fast_table_frame.pack(anchor="w")

    ttk.Frame(fast_settings_frame).pack(pady=7.5)  # Horizontal spacer

    isolation_degree_fast_label.pack(expand=False, fill=X, anchor="w", ipady=5)
    ttk.Frame(fast_settings_frame).pack(pady=7.5)  # Horizontal spacer
    isolation_degree_value_fast_label.pack(expand=False, side="top")
    isolation_degree_horizontal_fast_scale.pack(expand=False, side="bottom")
    isolation_degree_fast_frame.pack(anchor="w")

    ttk.Frame(fast_settings_frame).pack(pady=7.5)  # Horizontal spacer

    labeled_sounds_fast_label.pack(expand=False, fill=X, anchor="w", ipady=5)

    ttk.Frame(fast_settings_frame).pack(pady=7.5)  # Horizontal spacer

    add_labeled_sound_fast_button.pack(fill=BOTH, expand=True, side="left")
    ttk.Frame(labeled_sounds_fast_table_buttons_frame).pack(side="left", padx=2.5)  # Vertical spacer
    remove_labeled_sound_fast_button.pack(fill=BOTH, expand=True, side="left")
    ttk.Frame(labeled_sounds_fast_table_buttons_frame).pack(side="left", padx=12)  # Vertical spacer
    labeled_sounds_fast_table_buttons_frame.pack(fill=X, expand=True, anchor="w")
    ttk.Frame(labeled_sounds_fast_table_frame).pack(pady=2.5)  # Horizontal spacer
    labeled_sounds_fast_table.pack(expand=False, side="left")
    labeled_sound_fast_table_scrollbar.pack(side="left", fill=Y)
    labeled_sounds_fast_table_other_frame.pack(anchor="w")
    labeled_sounds_fast_table_frame.pack(anchor="w")

    ttk.Frame(text_transformation_frame).pack(side="left", padx=7.5)  # Vertical spacer

    fast_settings_frame.pack(fill=BOTH, anchor="n", side="left")

    ttk.Frame(transformation_field_frame).pack(pady=7.5)  # Horizontal spacer

    word_order_subject_legend_label.pack(side="left")
    word_order_subject_description_legend_label.pack(side="left")
    word_order_verb_legend_label.pack(side="left")
    word_order_verb_description_legend_label.pack(side="left")
    word_order_object_legend_label.pack(side="left")
    word_order_object_description_legend_label.pack(side="left")
    word_order_subject_legend_frame.pack(anchor="w")
    word_order_verb_legend_frame.pack(anchor="w")
    word_order_object_legend_frame.pack(anchor="w")
    word_order_legend_frame.pack(side="left", fill=X, expand=True)

    ttk.Frame(transformation_legend_frame).pack(side="left", padx=7.5)  # Vertical spacer

    lexical_units_legend_label.pack(side="left", anchor="w")
    lexical_units_description_legend_label.pack(side="left", anchor="w")
    lexical_units_legend_frame.pack(side="left", fill=X, expand=True)

    ttk.Frame(transformation_legend_frame).pack(side="left", padx=7.5)  # Vertical spacer

    isolation_degree_legend_label.pack(side="left", anchor="w")
    isolation_degree_description_legend_label.pack(side="left", anchor="w")
    isolation_degree_legend_frame.pack(side="left", fill=X, expand=True)

    ttk.Frame(transformation_legend_frame).pack(side="left", padx=7.5)  # Vertical spacer

    labeled_sound_legend_label.pack(side="left", anchor="w")
    labeled_sound_description_legend_label.pack(side="left", anchor="w")
    labeled_sound_legend_frame.pack(side="left", fill=X, expand=True, anchor="e")

    transformation_legend_frame.pack(fill=X, padx=15)

    ttk.Frame(transformation_field_frame).pack(pady=3.75)  # Horizontal spacer

    transformed_text_widget.pack(fill=X, expand=True, side="left")
    transformed_text_widget_scrollbar.pack(side="left", fill=Y)
    transformed_text_widget_frame.pack(fill=X, expand=False, padx=15)

    ttk.Frame(transformation_field_frame).pack(pady=7.5)  # Horizontal spacer

    input_text_widget.pack(expand=True, side="left", fill=X)
    input_text_widget_scrollbar.pack(side="left", fill=Y)
    input_text_widget_frame.pack(fill=X, padx=15)

    transform_text_button.pack(anchor="n", fill=X, padx=15, pady=15)

    transformation_field_frame.pack(fill=BOTH, expand=True, side="left")

    text_transformation_frame.pack(fill=BOTH, expand=True)

    # endregion

    """------------------------------TEXT TRANSFORMATION FRAME SECTION END------------------------------"""
    # endregion

    # region GenerationFrame
    """------------------------------GENERATION FRAME------------------------------"""

    generation_frame = ttk.Frame(notebook)

    selected_language_group_frame = ttk.Frame(generation_frame)

    selected_language_group_label = ttk.Label(
        selected_language_group_frame,
        text="Моделируемая языковая группа:",
        font=("Segoe UI", 12)
    )
    selected_language_group_label.pack(expand=False, anchor="w", side="left")

    refill_language_groups_for_combobox(language_groups_for_combobox, saved_language_groups)

    language_group_choice = StringVar(value=language_groups_for_combobox[0])

    selected_language_group_combobox = ttk.Combobox(
        selected_language_group_frame,
        textvariable=language_group_choice,
        values=language_groups_for_combobox,
        state='readonly',
        width=41,
    )

    selected_language_group_combobox.pack(expand=False, anchor="w", ipady=1, padx=15)
    selected_language_group_combobox.bind("<<ComboboxSelected>>", on_combobox_selected)

    selected_character_frame = ttk.Frame(generation_frame)

    selected_character_label = ttk.Label(
        selected_character_frame,
        text="Токен персонажа CharacterAI:",
        font=("Segoe UI", 12)
    )
    selected_character_label.pack(expand=False, anchor="w", side="left")

    character_token_entry = ttk.Entry(selected_character_frame, width=45)
    character_token_entry.insert(0, "BfIwQWZcLBjFI4f7pzE3a24pmKM0DrTTkb75KatQC8w")  # Default character token
    character_token_entry.pack(anchor="e", side="left", padx=37)

    chat_text = Text(generation_frame, height=20, font=("Segoe UI", 12), wrap="word")

    send_prompt_image = PhotoImage(file="./icons/SendPrompt.png")
    send_prompt_image = send_prompt_image.subsample(3, 3)

    def on_start_conversation_button_clicked():
        client = PyCAI("42f1d0ea1d29f9a116c4b9d7ce75748f757a949a")
        chat = client.chat.get_chat(character_token_entry.get())

        participants = chat['participants']

        if not participants[0]['is_human']:
            tgt = participants[0]['user']['username']
        else:
            tgt = participants[1]['user']['username']

        start_conversation_button.destroy()
        prompt_frame = ttk.Frame(generation_frame)

        prompt_entry = ttk.Entry(prompt_frame)
        prompt_entry.pack(expand=True, fill=X, ipady=2, side="left")
        ttk.Frame(prompt_frame).pack(side="left", padx=7.5)  # Vertical spacer before send prompt button

        def on_send_prompt_button_clicked():
            if prompt_entry.get():
                chat_text.insert(END, "Вы: " + prompt_entry.get() + "\n\n")

                data = client.chat.send_message(
                    chat['external_id'], tgt, prompt_entry.get()
                )

                prompt_entry.delete(0, END)

                character_name = data['src_char']['participant']['name']
                text = data['replies'][0]['text']
                translated_text = GoogleTranslator(source='en', target='ru').translate(text)
                selected_language_group = get_language_group_from_list(saved_language_groups,
                                                                       language_group_choice.get())

                result = word_order.change_text_word_order(
                    translated_text,
                    word_order.WordOrder(selected_language_group["word_order"]),
                    False
                )
                result = lexical_units.replace_lexical_units_in_text(
                    result,
                    selected_language_group["lexical_units"]
                )
                result = isolation_degree.change_text_isolation_degree(
                    result,
                    selected_language_group["isolation_degree"]
                )
                result = labeled_sounds.apply_labeled_sounds_to_text(
                    result,
                    selected_language_group["labeled_sounds"]
                )

                result_for_print = result.split(".")

                chat_text.insert(END, character_name + ": " + result + "\n\n")

        send_prompt_button = ttk.Button(
            prompt_frame,
            width=10,
            image=send_prompt_image,
            command=on_send_prompt_button_clicked
        )
        send_prompt_button.pack(side="left")

        prompt_frame.pack(fill=X, anchor="w", padx=15)

    start_conversation_button = ttk.Button(
        generation_frame,
        text="Начать общение",
        command=on_start_conversation_button_clicked
    )

    ttk.Frame(generation_frame).pack(pady=7.5)  # Horizontal spacer before all
    selected_language_group_frame.pack(anchor="w", padx=15)
    ttk.Frame(generation_frame).pack(pady=7.5)  # Horizontal spacer
    selected_character_frame.pack(anchor="w", padx=15)
    chat_text.pack(anchor="w", fill=X, padx=15, pady=15)
    start_conversation_button.pack(expand=True, fill=X, side="left", anchor="n", padx=15)
    generation_frame.pack(fill=BOTH, expand=True)

    """------------------------------GENERATION FRAME SECTION END------------------------------"""
    # endregion

    language_group_logo = PhotoImage(file="./icons/LanguageGroup.png")
    language_group_logo = language_group_logo.subsample(20, 20)
    generation_logo = PhotoImage(file="./icons/Generation.png")
    generation_logo = generation_logo.subsample(20, 20)
    transformation_logo = PhotoImage(file="./icons/Transformation.png")
    transformation_logo = transformation_logo.subsample(20, 20)

    notebook.add(language_group_frame, text="Создание языковой группы", image=language_group_logo, compound=LEFT)
    notebook.add(text_transformation_frame, text="Преобразовние текста", image=transformation_logo, compound=LEFT)
    notebook.add(generation_frame, text="Общение с персонажем", image=generation_logo, compound=LEFT)

    window.mainloop()


if __name__ == '__main__':
    launch_tkinter_app()
    # pymorphy_test()
    # ndiff_test()
