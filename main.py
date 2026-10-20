import os, time
import caesar


clear = 'cls' if os.name == 'nt' else 'clear'

# Вывод настроек
def print_settings(settings):
    print('Программа "Шифр Цезаря"\n')
    

    print(f"Режим работы: {settings['режим работы']}\n"
          f"Язык сообщения: {settings['язык сообщения']}\n"
          f"Шаг шифрования: {settings['шаг шифрования']}\n")

    print()


# Выбор режима работы
def select_operating_mode(instance):
    print("Какой режим работы Вас интересует? Введите режим и нажмите Enter\n")
    print("1) шифрование\n"
          "2) дешифрование\n"
          "3) полный перебор\n"
          "4) частотный анализ (рекомендуется для длинных текстов)\n")
        #   "Если Вы не знаете шаг дешифрования, то введите '+' для "
        #   "полного перебора всех ключей\n")
        #   "или хотите увидеть зашифрованный текст с различным шагом"
    
    modes = {"1": "шифрование",
             "2": "дешифрование",
             "3": "полный перебор",
             "4": "частотный анализ"
            }

    option = input()
    while True:
        try:
            instance.choose_operating_mode(modes.get(option, ''))
            break
        except caesar.CaesarError as e:
            print(f"{e}\n")
            option = input()

    os.system(clear)
    print_settings(instance.settings)
    return option


# Выбор языка
def select_language(instance):
#    alphabet = []
    print("Введите язык сообщения.\n")
    print("1) русский\n"
          "2) английский\n")
    
    languages = {"1": "русский", "2": "английский"}
    
    option = input()
    while True:
        try:
            instance.choose_language(languages.get(option, ''))
            break
        except caesar.CaesarError as e:
            print(f"{e}\n")
            option = input()
    
    if option == '1':
        print("\nЕсть ли в сообщении буква ё? "
              "Введите 'да' или 'нет'")
        add_char = input().lower()

        while add_char not in ['да', 'нет']:
            print("Некорректный ввод! Введите да или нет:\n\n")
            add_char = input().lower()
        
        if add_char == 'да':
            instance.choose_language(languages.get(option), add_letter=True)

    os.system(clear)
    print_settings(instance.settings)
    return option


# Выбор шага шифрования/дешифрования
def select_step(instance):
    tmp = 'шифрования' if instance.operating_mode == 'шифрование' \
                                                else 'дешифрования'
    
    limitation = instance.alphabet_length - 1
    tmp1 = dict(русский='русского', английский='английского')
    
    print(f"Введите шаг {tmp}, либо вариант 'по длине слова' для "
                                        "шифрования по длине слова\n"
          f"Максимальный шаг для {tmp1[instance.language]} языка - "
                            f"{limitation}. Минимальный шаг равен 1\n")
    
    step = input().lower()
    while True:
        try:
            if step.isdigit(): step = int(step)
            instance.choose_step(step)
            break
        except caesar.CaesarError as e:
            print(f"{e}\n")
            step = input().lower()

    del tmp, limitation, tmp1

    os.system(clear)
    print_settings(instance.settings)
    return step


# Ввод текста
def input_text(instance):
    if instance.operating_mode == 'шифрование':
        print("Введите текст для шифрования:\n")
    else:
        print("Введите зашифрованный текст:\n")

    text = input()
    while True:
        try:
            instance.text_input(text)
            break
        except caesar.CaesarError as e:
            print(f"{e}\n")
            text = input()

    os.system(clear)
    print_settings(instance.settings)
    return text

# Главная функция
def main():
    os.system(clear)
    time.sleep(0.5)
    print('Добро пожаловать в программу "Шифр Цезаря"!')
    time.sleep(2)
    os.system(clear)
    
    while True:
        os.system(clear)
        caesar_cipher = caesar.Caesar()
    
        print_settings(caesar_cipher.settings)
        for i in range(3):
            if i == 0:
                select_operating_mode(caesar_cipher)
            elif i == 1:
                select_language(caesar_cipher)
            elif caesar_cipher.operating_mode not in ['полный перебор',
                                                    'частотный анализ']:
                select_step(caesar_cipher)
    
        input_text(caesar_cipher)
        
        if caesar_cipher.operating_mode == 'полный перебор':
            result = caesar_cipher.brute_force()
        elif caesar_cipher.operating_mode == 'частотный анализ':
            try:
                result = caesar_cipher.frequency_analysis()
            except caesar.CaesarError as e:
                print(f"{e}\n")
                break
        elif caesar_cipher.step == 'по длине слова':
            result = caesar_cipher.cryption_by_len_word()
        else:
            result = caesar_cipher.cryption_by_step()
    
        time.sleep(1)
        match caesar_cipher.operating_mode:
            case 'шифрование':
                print("Ваш зашифрованный текст:\n") 
            case 'дешифрование':
                print("Ваш расшифрованный текст:\n")
            case 'полный перебор':
                print("Все варианты расшифровок сообщения:\n")
            case 'частотный анализ':
                print("3 наиболее возможные расшифровки для этого текста:\n")
        
        print(result)
        print("\nХотите ли Вы зашифровать/дешифровать ещё один текст? (да/нет)")
    
        answer = input().lower()
        while answer not in ['да', 'нет']:
            print("Некорректный ввод! Введите да или нет:")
            answer = input().lower()
    
        if answer == 'нет':
            print("\nВозвращайтесь в следующий раз :)\n\n")
            time.sleep(1)
            break
        
        del caesar_cipher

    return 0


if __name__ == "__main__":
    main()
