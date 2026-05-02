import os
import csv

def extract_and_save_data():
    # Ввод данных от пользователя
    folder_path = input("Введите путь к папке с файлами: ")
    
    # Проверяем существование папки
    if not os.path.isdir(folder_path):
        print(f"Ошибка: папка '{folder_path}' не существует!")
        return
    
    base_name = input("Введите базовое название файлов (например, 'файл', программа запишет как 0_файл.txt): ")
    start_idx = int(input("Введите начальный индекс: "))
    end_idx = int(input("Введите конечный индекс: "))
    target_string = input("Введите строку, после которой нужно взять значение: ")
    output_column = int(input("Введите номер столбца для записи значений (начиная с 1): "))
    output_filename = input("Введите имя выходного CSV‑файла (с расширением например, 'результат.csv'): ")
    file_extension = input("Введите расширение файлов (например, 'txt', 'log', 'dat' и т. д., без точки): ")
    output_file = os.path.join(folder_path, output_filename)

    # Создаём пустую таблицу (список списков)
    # Теперь у нас минимум 2 столбца: индексы и значения
    num_columns = max(output_column + 1, 2)  # Гарантируем минимум 2 столбца
    max_rows = end_idx - start_idx + 1
    table = [['' for _ in range(num_columns)] for _ in range(max_rows)]

    # Обрабатываем каждый файл
    for idx in range(start_idx, end_idx + 1):
        # Формируем имя файла: индекс_название.расширение
        filename = f"{idx}_{base_name}.{file_extension}"
        file_path = os.path.join(folder_path, filename)

        # Проверяем, существует ли файл
        if not os.path.isfile(file_path):
            print(f"Предупреждение: файл '{filename}' не найден в папке '{folder_path}', пропускаем.")
            continue

        try:
            # Открываем файл как текстовый, независимо от расширения
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Ищем позицию целевой строки
            pos = content.find(target_string)
            if pos == -1:
                print(f"Строка '{target_string}' не найдена в файле '{filename}', пропускаем.")
                # Даже если строка не найдена, записываем индекс
                row_idx = idx - start_idx
                table[row_idx][0] = str(idx)
                continue

            # Находим начало значения (после целевой строки)
            start_pos = pos + len(target_string)

            # Пропускаем все пробелы после целевой строки
            while start_pos < len(content) and content[start_pos].isspace():
                start_pos += 1

            # Если после пропуска пробелов мы вышли за пределы строки
            if start_pos >= len(content):
                value = ''
            else:
                # Находим конец значения (до следующего пробела)
                end_pos = start_pos
                while end_pos < len(content) and not content[end_pos].isspace():
                    end_pos += 1
                value = content[start_pos:end_pos].strip()

            # Записываем данные в таблицу
            row_idx = idx - start_idx
            table[row_idx][0] = str(idx)  # Первый столбец — индекс файла
            table[row_idx][output_column] = value  # Указанный столбец — значение

        except Exception as e:
            print(f"Ошибка при обработке файла '{filename}': {e}")

    # Сохраняем таблицу в CSV-файл в указанной папке
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(table)
        print(f"Данные успешно сохранены в файл '{output_file}'.")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

# Запуск функции
extract_and_save_data()
