import collections, operator


class CaesarError(Exception):

    def __init__(self, message=None):
        super().__init__(message)
        self.message: str = message if message else "Неправильный ввод!"

    def __str__(self):
        return self.message


class Caesar:

    # Инициализация
    def __init__(self):
        self.brute_flag = False
        self.settings = {  # Параметры шифрования/дешифрования
            "режим работы": "не выбран",
            "язык сообщения": "не выбран",
            "шаг шифрования": "не выбран",
        }

    # Выбор режима работы
    def choose_operating_mode(self, operating_mode):

        if operating_mode not in [
            "шифрование",
            "дешифрование",
            "полный перебор",
            "частотный анализ",
        ]:
            raise CaesarError(
                "Некорректный ввод! Введите один из " "вариантов режима работы.\n"
            )

        if operating_mode not in ["шифрование", "дешифрование"]:
            self.step = "нет"
            self.settings["шаг шифрования"] = "нет"

        if operating_mode == "шифрование":
            self.func = operator.add
        else:
            self.func = operator.sub

        self.settings["режим работы"] = operating_mode
        self.operating_mode = operating_mode
        return operating_mode

    # Выбор языка
    def choose_language(
        self, language, add_letter=False
    ):  # add_letter - флаг для буквы ё
        if language not in ["русский", "английский"]:
            raise CaesarError("Некоррректный ввод! Введите один из вариантов выше.\n")

        self.language = language
        first_letter, last_letter = (  # Первая и последняя буква в выбранном языке
            ["А", "Я"] if language == "русский" else ["A", "Z"]
        )

        upper_chars = [  # Заглавные буквы
            chr(i) for i in range(ord(first_letter), ord(last_letter) + 1)
        ]

        lower_chars = [  # Строчные буквы
            chr(i)
            for i in range(ord(first_letter.lower()), ord(last_letter.lower()) + 1)
        ]

        if add_letter and language == "русский":
            alphabet_length = 33
            upper_chars.insert(6, "Ё")  # Добавление буквы Ё
            lower_chars.insert(6, "ё")  # Добавление буквы ё
        elif language == "русский":
            alphabet_length = 32
        else:
            alphabet_length = 26

        self.upper_chars = upper_chars  # Заглавные буквы
        self.lower_chars = lower_chars  # Строчные буквы
        self.alphabet_length = alphabet_length  # Длина алфавита

        self.settings["язык сообщения"] = language
        return language, alphabet_length

    # Выбор шага шифрования/дешифрования
    def choose_step(self, step):
        max_step = self.alphabet_length - 1

        if (step != "по длине слова") and (step not in range(1, max_step + 1)):
            raise CaesarError(
                f"Некорректный ввод, введите шаг от 1 до "
                f"{max_step} или вариант 'по длине слова':\n"
            )

        self.step = step
        self.settings["шаг шифрования"] = step
        return step

    # Ввод текста
    def text_input(self, text):
        if text.isspace() or text == "":
            raise CaesarError(
                "Ошибка! Вы ничего не ввели\n"
                "Введите текст на выбранном вами языке:\n"
            )

        self.text = text
        return text

    # Шифрование по фиксированному шагу
    def cryption_by_step(self, step=None, text=None) -> str:
        if step is not None:
            self.step = step
        if text is not None:
            self.text = text

        result = ""
        for char in self.text:
            if char.isalpha():

                if char in self.upper_chars:
                    try:
                        ind = (
                            self.func(self.upper_chars.index(char), self.step)
                            % self.alphabet_length
                        )
                    except ValueError:
                        print("Ошибка!")
                        exit()

                    result += self.upper_chars[ind]
                else:
                    try:
                        ind = (
                            self.func(self.lower_chars.index(char), self.step)
                            % self.alphabet_length
                        )
                    except ValueError:
                        print("Ошибка!")
                        exit()

                    result += self.lower_chars[ind]

            else:
                result += char

        self.result = result
        return result

    # Шифрование по длине слова
    def cryption_by_len_word(self, text=None) -> str:
        if text is not None:
            self.text = text

        result = []  # Список для зашифрованных слов
        words = (  # Список слов исходного текста, если их больше 1, иначе список из одного элемента
            self.text.split() if self.text.count(" ") > 0 else [self.text]
        )
        for word in words:
            rspec, lspec = "", ""
            new_word = ""

            while not word[0].isalpha() or not word[-1].isalpha():

                if not word[0].isalpha() and word != "":
                    lspec += word[0]
                    word = word.replace(word[0], "", 1)

                elif not word[-1].isalpha() and word != "":
                    rspec += word[-1]
                    word = word[:-1]
            rspec = rspec[::-1]

            step = len(word)
            new_word = self.cryption_by_step(step, word)

            new_word = lspec + new_word + rspec
            result.append(new_word)

        return " ".join(result)  # Зашифрованный текст

    # Полный перебор
    def brute_force(self, text=None) -> str:
        if text is not None:
            self.text = text

        self.brute_flag = True
        all_variants = []

        for step in range(1, self.alphabet_length):
            all_variants.append(
                f"{step}) {self.cryption_by_step(step)} " f"(шаг: {step})\n"
            )
        all_variants.append(
            f"{self.alphabet_length}) "
            f"{self.cryption_by_len_word()} "
            "(шаг: по длине слова)"
        )

        return "\n".join(all_variants)

    # Частотный анализ
    def frequency_analysis(self, text=None) -> str:
        if text is not None:
            self.text = text

        if len(self.text) < 15:
            raise CaesarError(
                "Объём текста слишком мал для использования " "частотного анализа."
            )

        variants = []  # Варианты расшифровки
        frequency_chars = (
            "оеаи"  # "оеаинтсрвлкмдпуяыьгзбчйхжшюцщэфъ"
            if self.language == "русский"
            else "etao"  # "etaoinshrdlcumwfgypbvkjxqz"
        )
        
        # frequency_chars += "ё" if self.alphabet_length == 33 else ""

        most_frequent_char = collections.Counter(
            self.text.replace(" ", "").lower()
        ).most_common(1)[0][0]

        for i, char in enumerate(frequency_chars, start=1):
            step = (
                self.func(
                    self.lower_chars.index(most_frequent_char),
                    self.lower_chars.index(char),
                ) % self.alphabet_length
            )

            result = self.cryption_by_step(step)
            variants.append(f"{i}) {result} (шаг шифрования: {step})\n")

        return "\n".join(variants)


if __name__ == "__main__":
    caesar = Caesar()
    text = "Все счастливые семьи похожи друг на друга, каждая несчастливая семья несчастлива по-своему. Всё смешалось в доме Облонских. Жена узнала, что муж был в связи с бывшею в их доме француженкою-гувернанткой, и объявила мужу, что не может жить с ним в одном доме. Положение это продолжалось уже третий день и мучительно чувствовалось и самими супругами, и всеми членами семьи, и домочадцами. Все члены семьи и домочадцы чувствовали, что нет смысла в их сожительстве и что на каждом постоялом дворе случайно сошедшиеся люди более связаны между собой, чем они, члены семьи и домочадцы Облонских. Жена не выходила из своих комнат, мужа третий день не было дома. Дети бегали по всему дому, как потерянные; англичанка поссорилась с экономкой и написала записку приятельнице, прося приискать ей новое место; повар ушёл вчера со двора, во время самого обеда; чёрная кухарка и кучер просили расчета. На третий день после ссоры князь Степан Аркадьич Облонский — Стива, как его звали в свете, — в обычный час, то есть в восемь часов утра, проснулся не в спальне жены, а в своем кабинете, на сафьянном диване. Он повернул свое полное, выхоленное тело на пружинах дивана, как бы желая опять заснуть надолго, с другой стороны крепко обнял подушку и прижался к ней щекой; но вдруг вскочил, сел на диван и открыл глаза."
    caesar.choose_operating_mode("шифрование")
    caesar.choose_language("русский", "ё" in text)
    crypted = caesar.cryption_by_step(15, text)
    caesar.func = operator.sub
    print(caesar.frequency_analysis(crypted))
