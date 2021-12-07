import requests
from bs4 import BeautifulSoup
import sys

languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese',
             'Romanian', 'Russian', 'Turkish']


def main():
    language_1 = sys.argv[1]
    language_2 = sys.argv[2]
    word = sys.argv[3]

    if language_1.capitalize() not in languages:
        print(f"Sorry, the program doesn't support {language_1}")
    elif language_2.capitalize() not in languages and language_2 != 'all':
        print(f"Sorry, the program doesn't support {language_2}")
    elif language_2 == 'all':
        for lang in languages:
            if lang != language_1.capitalize():
                translate(language_1.capitalize(), lang, word, 1)
    else:
        translate(language_1.capitalize(), language_2.capitalize(), word, 5)


def translate(language_1, language_2, word, how_much):
    try:
        r = requests.get(
            f'https://context.reverso.net/translation/{language_1.lower()}-{language_2.lower()}/{word.lower()}',
            headers={'User-Agent': 'Mozilla/5.0'})
        if r:
            soup = BeautifulSoup(r.content, 'html.parser')
            translations = []
            examples_1 = []
            examples_2 = []
            trans_tags = soup.find_all('a', class_='translation')
            examples_1_tags = soup.find_all('div', class_='src')
            examples_2_tags = soup.find_all('div', class_='trg')
            for trans in trans_tags:
                translations.append(trans.text.strip())
            for ex in examples_1_tags:
                examples_1.append(ex.text.strip())
            for ex in examples_2_tags:
                examples_2.append(ex.text.strip())

            file = open(f'{word.lower()}.txt', 'a', encoding='utf-8')
            file.write(f'\n{language_2} Translation:\n')
            for x in range(1, how_much + 1):
                file.write(f'{translations[x]}\n')

            file.write(f'\n{language_2} Example:\n')
            for x in range(how_much):
                file.write(f'{examples_1[x]}:\n')
                file.write(f'{examples_2[x]}\n')

            file.close()
            with open(f'{word.lower()}.txt', 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            print(f'Sorry, unable to find {word}')

    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')


main()
