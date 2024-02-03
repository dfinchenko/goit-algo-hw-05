import timeit

# Реалізація алгоритму Кнута-Морріса-Прата
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено


# Реалізація алгоритму Боєра-Мура
def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1


# Реалізація алгоритму Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

# Вимірювання часу виконання
def measure_time(algorithm, text, pattern):
    start_time = timeit.default_timer()
    algorithm(text, pattern)
    end_time = timeit.default_timer()
    return end_time - start_time


if __name__ == "__main__":
    with open("text_1.txt", "r", encoding="utf-8") as file:
        text_1 = file.read()

    with open("text_2.txt", "r", encoding="utf-8") as file:
        text_2 = file.read()

    # Визначення підрядків для пошуку
    existing_pattern = "алгоритм"  # Підрядок, який існує в обох статтях
    non_existing_pattern = "неіснуючий підрядок"  # Вигаданий підрядок

    # Стаття 1
    print("Стаття 1:")
    # Існуючий підрядок
    time_kmp_existing_1 = measure_time(kmp_search, text_1, existing_pattern)
    time_bm_existing_1 = measure_time(boyer_moore_search, text_1, existing_pattern)
    time_rk_existing_1 = measure_time(rabin_karp_search, text_1, existing_pattern)
    print(f"Час Кнута-Морріса-Пратта: {time_kmp_existing_1}")
    print(f"Час Боєра-Мура: {time_bm_existing_1}")
    print(f"Час Рабіна-Карпа: {time_rk_existing_1}")

    # Вигаданий підрядок
    time_kmp_fictional_1 = measure_time(kmp_search, text_1, non_existing_pattern)
    time_bm_fictional_1 = measure_time(boyer_moore_search, text_1, non_existing_pattern)
    time_rk_fictional_1 = measure_time(rabin_karp_search, text_1, non_existing_pattern)
    print(f"Час Кнута-Морріса-Пратта (вигаданий): {time_kmp_fictional_1}")
    print(f"Час Боєра-Мура (вигаданий): {time_bm_fictional_1}")
    print(f"Час Рабіна-Карпа (вигаданий): {time_rk_fictional_1}")

    # Стаття 2
    print("\nСтаття 2:")
    # Існуючий підрядок
    time_kmp_existing_2 = measure_time(kmp_search, text_2, existing_pattern)
    time_bm_existing_2 = measure_time(boyer_moore_search, text_2, existing_pattern)
    time_rk_existing_2 = measure_time(rabin_karp_search, text_2, existing_pattern)
    print(f"Час Кнута-Морріса-Пратта: {time_kmp_existing_2}")
    print(f"Час Боєра-Мура: {time_bm_existing_2}")
    print(f"Час Рабіна-Карпа: {time_rk_existing_2}")

    # Вигаданий підрядок
    time_kmp_fictional_2 = measure_time(kmp_search, text_2, non_existing_pattern)
    time_bm_fictional_2 = measure_time(boyer_moore_search, text_2, non_existing_pattern)
    time_rk_fictional_2 = measure_time(rabin_karp_search, text_2, non_existing_pattern)
    print(f"Час Кнута-Морріса-Пратта (вигаданий): {time_kmp_fictional_2}")
    print(f"Час Боєра-Мура (вигаданий): {time_bm_fictional_2}")
    print(f"Час Рабіна-Карпа (вигаданий): {time_rk_fictional_2}")

    # Агрегація часу виконання для кожного тексту і алгоритму
    total_times_text_1 = {
        "Кнута-Морріса-Пратта": time_kmp_existing_1 + time_kmp_fictional_1,
        "Боєра-Мура": time_bm_existing_1 + time_bm_fictional_1,
        "Рабіна-Карпа": time_rk_existing_1 + time_rk_fictional_1
    }

    total_times_text_2 = {
        "Кнута-Морріса-Пратта": time_kmp_existing_2 + time_kmp_fictional_2,
        "Боєра-Мура": time_bm_existing_2 + time_bm_fictional_2,
        "Рабіна-Карпа": time_rk_existing_2 + time_rk_fictional_2
    }

    # Визначення найшвидшого алгоритму для кожного тексту
    fastest_text_1 = min(total_times_text_1, key=total_times_text_1.get)
    fastest_text_2 = min(total_times_text_2, key=total_times_text_2.get)

    # Виведення результатів
    print(f"\nНайшвидший алгоритм для Статті 1: {fastest_text_1} з часом {total_times_text_1[fastest_text_1]:.6f} сек")
    print(f"Найшвидший алгоритм для Статті 2: {fastest_text_2} з часом {total_times_text_2[fastest_text_2]:.6f} сек")

    # Підсумок
    total_times = {
        "Кнута-Морріса-Пратта": time_kmp_existing_1 + time_kmp_fictional_1 + time_kmp_existing_2 + time_kmp_fictional_2,
        "Боєра-Мура": time_bm_existing_1 + time_bm_fictional_1 + time_bm_existing_2 + time_bm_fictional_2,
        "Рабіна-Карпа": time_rk_existing_1 + time_rk_fictional_1 + time_rk_existing_2 + time_rk_fictional_2
    }

    fastest_algorithm = min(total_times, key=total_times.get)
    print(f"\nНайшвидший алгоритм в цілому: {fastest_algorithm} з часом {total_times[fastest_algorithm]}")