# TODO
from cs50 import get_string

# Get string from user
text = get_string("Text: ")
characters = len(text)
letters = sentences = 0
# Set word count to 1 to cater for the last word of the text
words = 1

# Loop through every character of the user's input checking if it is alphabetical or punctuation
for i in text:
    if i.isalpha():
        letters += 1
    # If it is space increment number of words
    elif i == " ":
        words += 1
    # If it is "." or "!" or "?" increment number of sentences
    elif i == "." or i == "!" or i == "?":
        sentences += 1

# Calculate grade and round it up
grade = round(0.0588 * ((letters / words) * 100) - 0.296 * ((sentences / words) * 100) - 15.8)

# Print grade level
if grade >= 16:
    print("Grade 16+")
elif grade < 1:
    print("Before Grade 1")
else:
    print(f"Grade, {int(grade)}")
