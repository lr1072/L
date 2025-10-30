import pandas as pd

df = pd.read_csv(r"D:\ITMO Python\books-en.csv", 
                sep=';', 
                encoding="cp1252")

print("Названия столбцов:", list(df.columns))

author = input("Введите имя автора: ")

books = df[(df['Book-Author'] == author) & (int(df['Price']) <= 200)]

print(f"Найдено {len(books)} книг:")
for i, row in books.iterrows():
    print(f"- {row['Book-Title']} (${row['Price']})")