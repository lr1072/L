import csv
import os

def read_csv(filename):
    """
    读取 CSV 文件（自动尝试 UTF-8 和 CP1251 编码）
    """
    for encoding in ['utf-8', 'cp1251']:
        try:
            with open(filename, encoding=encoding) as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if rows:
                    return rows
        except Exception:
            continue
    raise ValueError("❌ Не удалось прочитать CSV файл. Проверьте кодировку или путь.")

def count_long_titles(data):
    """
    统计标题 (Title / Название) 长度 > 30 的记录数量
    """
    if not data:
        return 0

    header = data[0].keys()
    possible_names = ['Title', 'Название', 'Name', 'Book title']
    title_field = None
    for name in possible_names:
        if name in header:
            title_field = name
            break

    if not title_field:
        print("⚠️ В файле не найдено поле 'Title' или 'Название'.")
        print("Найденные поля:", list(header))
        return 0

    count = 0
    for row in data:
        title = str(row.get(title_field, '')).strip()
        if len(title) > 30:
            count += 1
    return count


if __name__ == "__main__":
    # === 修改成你的文件完整路径 ===
    filename = r"D:\ITMO Python\books-en.csv"

    if not os.path.exists(filename):
        print(f"❌ Файл не найден по пути: {filename}")
    else:
        print(f"📘 Открывается файл: {filename}")
        data = read_csv(filename)
        result = count_long_titles(data)
        print(f"📊 Количество записей, где название длиннее 30 символов: {result}")
