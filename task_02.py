import string
import requests
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text.lower()
    except requests.RequestException as e:
        return None

# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    return word, 1

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Виконання MapReduce
def map_reduce(text):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

# Функція для візуалізації топ-слів
def visualize_top_words(word_counts, top_n=10):
    # Сортуємо слова за частотою
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    words, counts = zip(*sorted_words[:top_n])  # Беремо топ-N слів

    # Побудова графіку
    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.gca().invert_yaxis()  # Відображаємо найчастіші слова зверху
    plt.show()

if __name__ == '__main__':
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        result = map_reduce(text)

       # print("Результат підрахунку слів:", result)

        visualize_top_words(result, top_n=10)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")