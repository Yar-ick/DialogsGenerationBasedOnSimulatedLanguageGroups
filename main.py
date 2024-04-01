import word_order
import lexical_units
import isolation_degree
import labeled_sounds
import sv_ttk
import json
import locale
import sys
import os.path

from characterai import PyCAI
from deep_translator import GoogleTranslator
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

    result = word_order.change_text_word_order(text, word_order.WordOrder.VerbSubjectObject, False)
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

    window = Tk()
    sv_ttk.set_theme("dark")
    window.title('Диалогус')
    window.iconbitmap(default="./icons/Icon.ico")

    w = 1000
    h = 1080
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    window.geometry("%dx%d+%d+%d" % (w, h, x, y))

    saved_language_groups = []
    # selected_language_group = {}
    load_saved_language_groups(saved_language_groups)

    language_groups_for_combobox = []

    # Создание набора вкладок для разных задач
    notebook = ttk.Notebook()
    notebook.pack(expand=True, fill=BOTH)

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
        width=45,
    )

    word_order_combobox.pack(expand=False, anchor="w", ipady=5, padx=15)
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

    isolation_degree_value_label = ttk.Label(language_group_frame, text="0", font=("Arial", 10))
    isolation_degree_value_label.pack(expand=False, anchor="w", padx=210, pady=5)

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
                selected_language_group = get_language_group_from_list(saved_language_groups, language_group_choice.get())

                result = word_order.change_text_word_order(translated_text, word_order.WordOrder(selected_language_group["word_order"]), False)
                result = lexical_units.replace_lexical_units_in_text(result, selected_language_group["lexical_units"])
                result = isolation_degree.change_text_isolation_degree(result, selected_language_group["isolation_degree"])
                result = labeled_sounds.apply_labeled_sounds_to_text(result, selected_language_group["labeled_sounds"])

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
    ttk.Frame(generation_frame).pack(
        pady=7.5)  # Horizontal spacer between selected_language_group and selected_character
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

    notebook.add(language_group_frame, text="Создание языковой группы", image=language_group_logo, compound=LEFT)
    notebook.add(generation_frame, text="Генерация", image=generation_logo, compound=LEFT)

    window.mainloop()


if __name__ == '__main__':
    # start()
    launch_tkinter_app()
    # print(sys.stdout.encoding)
