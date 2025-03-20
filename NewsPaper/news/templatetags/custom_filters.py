from django import template

register = template.Library()

CENSORED_WORD = [
    "смартфон", "интеллект"
]

@register.filter()
def censor(text):
    if isinstance(text, str):
        text = text.split()
        censored_words = []
        for word in text:
            stripped_word = word.strip(".,!?;:\"'()[]{}<>/\\|")
            if stripped_word.lower() in CENSORED_WORD:
                censored_word = stripped_word[0] + '*' * (len(stripped_word)-1)
                censored_word = word.replace(stripped_word, censored_word)
                censored_words.append(censored_word)
            else:
                censored_words.append(word)

    return ' '.join(censored_words)

        
            
        
        