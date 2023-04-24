import speech_recognition as sr
import pyaudio
import json
import wikipedia

speech_rec = sr.Recognizer()

with open('config.json', mode='r', encoding="utf-8") as configFile:
    config = json.load(configFile)

prefix = f'{config["name"]}, {config["prefix"]}'
architecta_key_words = config['keywords']

def init_architecta():
    try:
        print('Estou ouvindo...')
        audio = listen_microfone()

        text_pt = recognize_audio_google(audio, 'pt-BR')
        text_en = recognize_audio_google(audio, "en-US")

        text_formatted = validate_keywords_and_get_formatted_text(
            text_pt, text_en)

        if (text_formatted == False):
            return print(f'ATENÇÃO, as perguntas devem ser relacionadas a alguma dessas palavras chaves: {", ".join(architecta_key_words)}')

        if is_valid_prefix(text_pt):
            print('Busca: ' + text_formatted + '?')
            search_content(text_formatted)
    except sr.UnknownValueError:
        print("Não entendi o que você disse")


def recognize_audio_google(audio, language):
    return speech_rec.recognize_google(audio, language=language)


def listen_microfone(audio=None):
    if audio:
        with sr.AudioFile(audio) as source:
            audio = speech_rec.listen(source)
            return audio
    else:
        with sr.Microphone() as source:
            speech_rec.adjust_for_ambient_noise(source)
            audio = speech_rec.listen(source, timeout=5)
            return audio


def validate_keywords_and_get_formatted_text(text_pt, text_en):
    words_pt = text_pt.split()
    last_word_pt = words_pt[-1]

    words_eng = text_en.split()
    last_word_eng = words_eng[-1]

    valid_last_word = is_valid_keyword(last_word_pt, last_word_eng)
    words_pt.pop()

    if (valid_last_word == ''):
        return False

    words_pt.append(valid_last_word)
    text_formatted = ' '.join(words_pt)
    return text_formatted


def is_valid_prefix(text):
    is_valid = text.lower().startswith(prefix.lower().replace(',', ''))

    if (is_valid == False):
        return print(
            f'ATENÇÃO, Lembre-se de dizer "{prefix}", antes de fazer uma pergunta')
    return True


def is_valid_keyword(last_word_pt, last_word_eng: str):
    if is_valid_last_word(last_word_pt):
        return last_word_pt

    if is_valid_last_word(last_word_eng):
        return last_word_eng

    return ''


def is_valid_last_word(last_word):
    for keyword in architecta_key_words:
        if keyword.lower() == last_word.lower():
            return True
    return False


def search_content(text):
    try:
        text_withoud_assistent_name = remove_assistent_name(text)
        wikipedia.set_lang("pt")
        content = wikipedia.summary(text_withoud_assistent_name, sentences=2)
        print(content)
        return content
    except Exception as e:
        print("Erro ao buscar conteúdo: " + str(e))


def remove_assistent_name(text):
    words = text.split()
    del words[0]
    return ' '.join(words)


if __name__ == '__main__':
    init_architecta()
