import re  # 导入正则表达式模块，用于模式匹配和文本搜索
import csv  # 导入CSV模块，用于读写CSV格式文件
from collections import OrderedDict  # 导入有序字典类（虽然代码中未使用，但导入以备后用）

# ==================== 任务1 ====================
def task1():  # 定义任务1的函数
    """任务1：从文本文件中提取特定模式的数据"""  # 函数文档字符串，描述函数功能
    print("=" * 50)  # 打印50个等号作为分隔线
    print("Задание 1 - Вариант 4")  # 打印任务标题和选项编号
    print("=" * 50)  # 打印50个等号作为分隔线
    print("1. Все слова, в которых есть дефис;")  # 打印任务要求1：带连字符的单词
    print("2. всю информацию в круглых скобках.")  # 打印任务要求2：圆括号中的信息
    print()  # 打印空行
    
    try:  # 尝试执行以下代码块，捕获可能出现的异常
        with open('task1-ru.txt', 'r', encoding='utf-8') as file:  # 以只读模式打开文件，指定UTF-8编码
            text = file.read()  # 读取文件的全部内容到字符串变量text中
        
        # 1. 所有包含连字符的单词
        print("1. Слова с дефисом:")  # 打印小节标题
        hyphen_words = re.findall(r'\b[А-Яа-яA-Za-z]+[-][А-Яа-яA-Za-z]+\b', text)  # 使用正则表达式查找所有包含连字符的单词
        unique_hyphen_words = sorted(set(hyphen_words))  # 将结果转换为集合去重，然后排序
        for i, word in enumerate(unique_hyphen_words, 1):  # 遍历去重后的单词列表，i从1开始计数
            print(f"  {i}. {word}")  # 打印带编号的单词
        
        print("\n" + "-" * 40)  # 打印空行和40个减号作为分隔线
        
        # 2. 所有圆括号中的信息
        print("2. Информация в круглых скобках:")  # 打印小节标题
        parentheses_content = re.findall(r'\((.*?)\)', text)  # 使用正则表达式查找所有圆括号中的内容，非贪婪匹配
        for i, content in enumerate(parentheses_content, 1):  # 遍历找到的内容，i从1开始计数
            print(f"  {i}. ({content})")  # 打印带编号的圆括号内容
            
    except FileNotFoundError:  # 捕获文件未找到异常
        print("Ошибка: Файл task1_ru.txt не найден")  # 打印错误信息

# ==================== 任务2 ====================
def task2():  # 定义任务2的函数
    """任务2：从HTML文件中提取特定模式的数据"""  # 函数文档字符串
    print("\n" + "=" * 50)  # 打印空行和50个等号
    print("Задание 2 - Вариант 4")  # 打印任务标题
    print("=" * 50)  # 打印50个等号
    print("1. Все слова, в которых есть дефис;")  # 打印任务要求1
    print("2. всю информацию в круглых скобках.")  # 打印任务要求2
    print()  # 打印空行
    
    try:  # 尝试执行代码块
        with open('task2.html', 'r', encoding='utf-8') as file:  # 打开HTML文件
            html_content = file.read()  # 读取HTML文件全部内容
        
        # 1. 所有包含连字符的单词（在HTML中）
        print("1. Слова с дефисом в HTML:")  # 打印小节标题
        html_hyphen_words = re.findall(r'\b[a-zA-Z]+[-][a-zA-Z]+\b', html_content)  # 查找HTML中的连字符单词（仅英文）
        unique_html_hyphen = sorted(set(html_hyphen_words))  # 去重并排序
        for i, word in enumerate(unique_html_hyphen, 1):  # 遍历并打印结果
            print(f"  {i}. {word}")
        
        print("\n" + "-" * 40)  # 打印分隔线
        
        # 2. 所有圆括号中的信息（在HTML中）
        print("2. Информация в круглых скобках в HTML:")  # 打印小节标题
        html_parentheses = re.findall(r'\((.*?)\)', html_content)  # 查找HTML中的圆括号内容
        for i, content in enumerate(html_parentheses, 1):  # 遍历并打印结果
            print(f"  {i}. ({content})")
            
    except FileNotFoundError:  # 捕获文件未找到异常
        print("Ошибка: Файл task2.html не найден")  # 打印错误信息

# ==================== 任务3 ====================
def task3():  # 定义任务3的函数
    """任务3：整理混乱的数据表"""  # 函数文档字符串
    print("\n" + "=" * 50)  # 打印空行和分隔线
    print("Задание 3")  # 打印任务标题
    print("=" * 50)  # 打印分隔线
    print("Сортировка базы данных в нормальный вид.")  # 打印任务描述
    
    try:  # 尝试执行代码块
        with open('task3.txt', 'r', encoding='utf-8') as file:  # 打开数据文件
            content = file.read()  # 读取文件内容
        
        # 使用正则表达式提取各种类型的数据
        ids = re.findall(r'\b(?:ID:?\s*)?(\d{1,3})\b', content)  # 提取ID：1-3位数字，可选前缀"ID:"
        surnames = re.findall(r'\b(?:[А-Я][а-я]+|[A-Z][a-z]+)\b', content)  # 提取姓氏：首字母大写，其余小写（支持俄英）
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)  # 提取邮箱地址
        dates = re.findall(r'\b\d{4}-\d{2}-\d{2}\b', content)  # 提取日期：YYYY-MM-DD格式
        websites = re.findall(r'(?:https?://)?(?:www\.)?[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', content)  # 提取网站URL
        
        # 清理数据（移除不符合要求的项）
        # 从surnames中移除可能被错误识别的单词
        cleaned_surnames = []  # 创建空列表存储清理后的姓氏
        surname_pattern = re.compile(r'^[A-Z][a-z]+$')  # 编译正则模式：英文姓氏（首字母大写）
        for surname in surnames:  # 遍历所有提取的姓氏
            if surname_pattern.match(surname) and len(surname) > 2:  # 如果符合模式且长度大于2
                # 检查是否不是常见的HTML标签或其他词汇
                common_exclusions = ['html', 'head', 'body', 'style', 'title', 'meta', 'div', 'span', 
                                   'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'a', 'href', 'src']  # 常见排除词列表
                if surname.lower() not in common_exclusions:  # 如果小写的姓氏不在排除列表中
                    cleaned_surnames.append(surname)  # 添加到清理后的列表
        
        # 限制每个列表为100个元素（根据数据量）
        ids = ids[:100]  # 截取前100个ID
        cleaned_surnames = cleaned_surnames[:100]  # 截取前100个清理后的姓氏
        emails = emails[:100]  # 截取前100个邮箱
        dates = dates[:100]  # 截取前100个日期
        websites = websites[:100]  # 截取前100个网站
        
        # 创建CSV文件
        with open('sorted_database.csv', 'w', newline='', encoding='utf-8') as csvfile:  # 打开CSV文件用于写入
            csvwriter = csv.writer(csvfile)  # 创建CSV写入器对象
            # 写入标题行
            csvwriter.writerow(['ID', 'Фамилия', 'Email', 'Дата регистрации', 'Сайт'])  # 写入列标题
            
            # 写入数据行
            min_length = min(len(ids), len(cleaned_surnames), len(emails), len(dates), len(websites))  # 获取最小列表长度
            for i in range(min_length):  # 遍历所有列表的共同长度范围
                csvwriter.writerow([ids[i], cleaned_surnames[i], emails[i], dates[i], websites[i]])  # 写入一行数据
        
        print(f"✓ Создан файл sorted_database.csv с {min_length} записями")  # 打印成功信息
        print("Первые 5 записей:")  # 打印提示信息
        print("-" * 80)  # 打印分隔线
        print(f"{'ID':<5} {'Фамилия':<15} {'Email':<25} {'Дата':<12} {'Сайт'}")  # 打印表头（格式化对齐）
        print("-" * 80)  # 打印分隔线
        for i in range(min(5, min_length)):  # 遍历前5条记录（或更少）
            print(f"{ids[i]:<5} {cleaned_surnames[i]:<15} {emails[i]:<25} {dates[i]:<12} {websites[i]}")  # 打印格式化数据
            
    except FileNotFoundError:  # 捕获文件未找到异常
        print("Ошибка: Файл task3.txt не найден")  # 打印错误信息

# ==================== 额外任务 ====================
def additional_task():  # 定义额外任务的函数
    """额外任务：从随机字符中提取有用信息"""  # 函数文档字符串
    print("\n" + "=" * 50)  # 打印空行和分隔线
    print("Дополнительное задание")  # 打印任务标题
    print("=" * 50)  # 打印分隔线
    print("Поиск дат, email-адресов и веб-сайтов в файле task_add.txt")  # 打印任务描述
    
    try:  # 尝试执行代码块
        with open('task_add.txt', 'r', encoding='utf-8') as file:  # 打开额外任务文件
            content = file.read()  # 读取文件内容
        
        # 1. 查找日期（支持不同格式）
        print("\n1. Даты:")  # 打印小节标题
        date_patterns = [  # 定义日期模式列表
            r'\b\d{4}[/.-]\d{2}[/.-]\d{2}\b',  # 模式1：2023/12/25, 2023-12-25, 2023.12.25
            r'\b\d{2}[/.-]\d{2}[/.-]\d{4}\b',  # 模式2：25/12/2023, 25-12-2023, 25.12.2023
            r'\b\d{1,2}\s+[а-яА-Я]+\s+\d{4}\b'  # 模式3：25 декабря 2023（俄语月份）
        ]
        
        all_dates = []  # 创建空列表存储所有找到的日期
        for pattern in date_patterns:  # 遍历所有日期模式
            dates_found = re.findall(pattern, content)  # 使用当前模式查找日期
            all_dates.extend(dates_found)  # 将找到的日期添加到总列表
        
        # 显示前5个日期
        for i, date in enumerate(all_dates[:5], 1):  # 遍历前5个日期
            print(f"  {i}. {date}")  # 打印带编号的日期
        
        # 2. 查找电子邮件地址
        print("\n2. Email-адреса:")  # 打印小节标题
        emails = re.findall(r'\s[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)  # 查找邮箱（前面有空格）
        for i, email in enumerate(emails[:5], 1):  # 遍历前5个邮箱
            print(f"  {i}. {email.strip()}")  # 打印去除空格的邮箱
        
        # 3. 查找网站地址
        print("\n3. Веб-сайты:")  # 打印小节标题
        websites = re.findall(r'\s(?:https?://)?(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)  # 查找网站（前面有空格）
        for i, website in enumerate(websites[:5], 1):  # 遍历前5个网站
            print(f"  {i}. {website.strip()}")  # 打印去除空格的网站
        
        print(f"\nИтого найдено: {len(all_dates)} дат, {len(emails)} email-адресов, {len(websites)} веб-сайтов")  # 打印统计信息
        
    except FileNotFoundError:  # 捕获文件未找到异常
        print("Ошибка: Файл task_add.txt не найден")  # 打印错误信息

# ==================== 主程序 ====================
def main():  # 定义主函数
    print("Лабораторная работа №5")  # 打印作业标题
    print("Работа с регулярными выражениями")  # 打印作业主题
    print("Вариант 4")  # 打印选项编号
    print()  # 打印空行
    
    # 执行所有任务
    task1()  # 调用任务1函数
    task2()  # 调用任务2函数
    task3()  # 调用任务3函数
    additional_task()  # 调用额外任务函数
    
    print("\n" + "=" * 50)  # 打印空行和分隔线
    print("Задание выполнено успешно!")  # 打印成功信息
    print("=" * 50)  # 打印分隔线

if __name__ == "__main__":  # 如果当前脚本作为主程序运行
    main()  # 调用主函数