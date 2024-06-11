import os
from PIL import Image

class ImageConverter:
    def __init__(self, alphabet_image, rows, cols):
        self.alphabet_image = alphabet_image  # Исходное изображение алфавита
        self.rows = rows  # Количество рядов в изображении алфавита
        self.cols = cols  # Количество колонок в изображении алфавита
        self.alphabet_dict = self._create_alphabet_dict(alphabet_image, rows, cols)  # Заполнение словаря алфавита

    def _create_alphabet_dict(self, image, rows, cols):
        width, height = image.size  # Размеры изображения
        cell_width = width // cols  # Ширина одной ячейки
        cell_height = height // rows  # Высота одной ячейки
        alphabet_dict = {}  # Словарь для хранения изображений символов

        letters = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'  # Русский алфавит
        index = 0

        for row in range(rows):
            for col in range(cols):
                if index >= len(letters):
                    break
                char = letters[index]
                left = col * cell_width  # Левая координата обрезки
                upper = row * cell_height  # Верхняя координата обрезки
                right = left + cell_width  # Правая координата обрезки
                lower = upper + cell_height  # Нижняя координата обрезки
                alphabet_dict[char] = image.crop((left, upper, right, lower))  # Нарезка и добавление изображения
                index += 1

        return alphabet_dict  # Возвращение словаря алфавита

    def text_to_image(self, text, chars_per_line=10, thumbnail_size=None):
        lines = [text[i:i + chars_per_line] for i in range(0, len(text), chars_per_line)]  # Разбиение текста на строки
        first_image = list(self.alphabet_dict.values())[0]
        char_width, char_height = first_image.size  # Размер одного символа

        img_width = chars_per_line * char_width  # Ширина итогового изображения
        img_height = len(lines) * char_height  # Высота итогового изображения
        output_image = Image.new('RGB', (img_width, img_height), (255, 255, 255))  # Создание белого фона итогового изображения

        for line_index, line in enumerate(lines):  # Перебор строк текста
            for char_index, char in enumerate(line):  # Перебор символов в строке
                if char == ' ':  # Пропуск пробела
                    continue
                if char.upper() in self.alphabet_dict:  # Проверка, что символ есть в алфавите
                    char_image = self.alphabet_dict[char.upper()]  # Получение изображения символа
                    x = char_index * char_width  # Координата X для вставки символа
                    y = line_index * char_height  # Координата Y для вставки символа
                    output_image.paste(char_image, (x, y))  # Вставка символа в итоговое изображение

        if thumbnail_size:  # Проверка на наличие размера для уменьшения изображения
            output_image.thumbnail(thumbnail_size)  # Уменьшение изображения до заданного размера

        return output_image  # Возвращение итогового изображения

    # Функция для создания экземпляра класса из файла
    def from_file(file_path, rows, cols):
        if not os.path.exists(file_path):  # Проверка существования файла
            raise FileNotFoundError(f"File not found: {file_path}")  # Исключение, если файл не найден
        image = Image.open(file_path)  # Открытие изображения
        return ImageConverter(image, rows, cols)  # Создание экземпляра класса с изображением