replacebale_characters = {
    "o:": "ö",
    "O:": "Ö",
    "u:": "ü",
    "U:": "Ü",
    "a:": "ä",
    "A:": "Ä",
    "ss": "ß"
}

def umlauts_and_eszett(text):
    for key in replacebale_characters:
        text = text.replace(key, replacebale_characters[key])
    return text