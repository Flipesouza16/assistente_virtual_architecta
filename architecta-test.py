import unittest
from architecta import *

valid_audio = 'audio_valid.wav'
invalid_audio = 'invalid.wav'

text_pt = 'arquiteta o que é quis'
text_eng = 'arquiteta o que é kiss'

class TestArchitecta(unittest.TestCase):
  def test_valid_last_word(self):
        self.assertTrue(is_valid_last_word("MVC"))
        self.assertTrue(is_valid_last_word("KISS"))
        self.assertTrue(is_valid_last_word("YAGNI"))
        self.assertTrue(is_valid_last_word("DRY"))
        self.assertTrue(is_valid_last_word("SOLID"))

  def test_invalid_last_word(self):
      self.assertFalse(is_valid_last_word("programador"))
      self.assertFalse(is_valid_last_word("Construtor"))
      self.assertFalse(is_valid_last_word("Engenheira"))

  def test_is_invalid_keyword(self):
      valid_keyword = is_valid_keyword('quis', 'kiss')
      self.assertNotEqual(valid_keyword, '')

  def test_is_valid_keyword(self):
      valid_keyword = is_valid_keyword('quis', 'kiss')
      self.assertEqual(valid_keyword, 'kiss')

  def test_is_invalid_prefix(self):
    is_valid = is_valid_prefix('o que é solid?')
    self.assertFalse(is_valid)

  def test_is_valid_prefix(self):
    is_valid = is_valid_prefix('arquiteta o que é solid')
    self.assertTrue(is_valid)

  def test_invalidate_keywords_and_get_formatted_text(self):
    formatted_text = validate_keywords_and_get_formatted_text(text_pt, text_eng)
    self.assertNotEqual(formatted_text, 'arquiteta o que é quis')

  def test_validate_keywords_and_get_formatted_text(self):
    formatted_text = validate_keywords_and_get_formatted_text(text_pt, text_eng)
    self.assertEqual(formatted_text, 'arquiteta o que é kiss')

  def test_remove_assistent_name(self):
    formatted_text = remove_assistent_name('arquiteta o que é MVC?')
    self.assertEqual(formatted_text, 'o que é MVC?')

  def test_valid_listen_microfone(self):
    audio = listen_microfone(valid_audio)
    self.assertTrue(audio)

  def test_valid_recognize_audio_google(self):
    audio_file = listen_microfone(valid_audio)
    text_pt = recognize_audio_google(audio_file, 'pt-BR')
    expected_text = 'arquiteta o que é mvc'
    self.assertEqual(text_pt.lower(), expected_text.lower())

  def test_invalid_recognize_audio_google(self):
    audio_file = listen_microfone(invalid_audio)
    text_pt = recognize_audio_google(audio_file, 'pt-BR')
    expected_text = 'arquiteta o que é mvc'
    self.assertNotEqual(text_pt.lower(), expected_text.lower())

if __name__ == '__main__':
    unittest.main()
