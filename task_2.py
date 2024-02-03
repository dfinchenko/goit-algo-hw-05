def binary_search_with_iterations(arr, x):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (high + low) // 2

        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            upper_bound = arr[mid]  # Знайдено точний елемент
            break
    if upper_bound is None:  # Якщо елемент не знайдений, шукаємо верхню межу
        if low < len(arr):
            upper_bound = arr[low]
        else:
            upper_bound = None  # Верхньої межі немає, якщо всі елементи менші за x

    return (iterations, upper_bound)

# Приклад використання функції:
arr = [1.5, 2.3, 3.4, 5.6, 7.8]
x = 5.6

result = binary_search_with_iterations(arr, x)
print(f"Кількість ітерацій: {result[0]}, Верхня межа: {result[1]}")
