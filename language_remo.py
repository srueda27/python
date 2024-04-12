import re
from langdetect import detect
from string import punctuation # The module 'string' is imported

def process_text(text):
    # It verifies that the text contains at least 50 characters.
    if len(text) < 50:
        print("Warning! The text must be at least 50 characters long.")
        return

    # The text is transformed to lowercase.
    text = text.lower()

    # Include the punctuation in the characters' count.
    num_characters = len(text)
       
    # Punctuation is removed from the text.
    text = ''.join([char for char in text if char not in punctuation])

    # Count words after removing the punctuation
    words = text.split()
    num_words = len(words)

    if ("  " in text):
        print("Warning! Double blanks have been detected. Please correct the text.")
        return

    repeated_words = []

    for match in re.finditer(r'\b(\w+)\s+\1\b', text):
        repeated_words.append(match.group(1))

    if repeated_words:
        print("Warning! Consecutive repeated words have been detected. Please correct the text.")
        print(set(repeated_words))
        return

    print("Number of characters:", num_characters)
    print("Number of words:", num_words)

    detected_language = detect(text)

    print("Language detected:", detected_language)

    words_counter = {}

    for word in words:
        words_counter[word] = words_counter.get(word, 0) + 1

    top_words = sorted(words_counter.items(), key=lambda x: x[1], reverse=True)[:5]

    print("\nTop 5 most repeated words:")

    for i, (word, frequency) in enumerate(top_words, start=1):
        print(f"{i}) '{word}': {frequency} times")

# Here is a test case for the process_text function.
example_text = "Hello, my name is John and hello. I am working on hello a Python function. The truth is that Python is a IS language that I love and I am very happy to master it."
process_text(example_text)