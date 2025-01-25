import sqlite3
from random import choice, randint

conn = sqlite3.connect('questions.db')
cursor = conn.cursor()

def get_random_gender_with_answer():
    select_q = "SELECT * FROM noun_genders"
    cursor.execute(select_q)
    result = cursor.fetchall()

    word = choice(result)

    return word[0], word[1]


def get_random_verb_with_answer():
    select_q = "SELECT * FROM verbs"
    cursor.execute(select_q)
    result = cursor.fetchall()

    word = choice(result)

    form = randint(1, 6)

    if form == 1:
        return word[0], word[1], "ich"
    elif form == 2:
        return word[0], word[2], "du"
    elif form == 3:
        return word[0], word[3], "er"
    elif form == 4:
        return word[0], word[4], "wir"
    elif form == 5:
        return word[0], word[5], "ihr"
    elif form == 6:
        return word[0], word[6], "Sie"


def get_random_noun_with_answer():
    select_q = "SELECT * FROM noun_plurals"
    cursor.execute(select_q)
    result = cursor.fetchall()

    word = choice(result)

    return word[0], word[1]


class Editor:
    @staticmethod
    def add_gender(added_info):
        command = """
        INSERT INTO noun_genders (noun, gender) VALUES (?, ?)
        """
        try:
            cursor.executemany(command, [added_info])
            conn.commit()
            return True
        except:
            return False

    @staticmethod
    def add_noun(added_info):
        command = """
            INSERT INTO noun_plurals (singular_form, plural_form)
            VALUES (?, ?)
            """
        try:
            cursor.executemany(command, [added_info])
            conn.commit()
            return True
        except:
            return False

    @staticmethod
    def add_verb(added_info):
        command = """
            INSERT OR IGNORE INTO verbs (infinitive, ich, du, er, wir, ihr, Sie) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
        try:
            cursor.executemany(command, [added_info])
            conn.commit()
            return True
        except:
            return False