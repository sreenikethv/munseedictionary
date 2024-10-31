from munseedict import nouns
from munseedict import verbs

def parser(word, pos):
  if pos.startswith('n'):
    return nounParser(word, pos)+'?'
  elif pos.startswith('v'):
    return verbParser(word, pos)+'?'
  return word+'?'


'''
def parse_csv():
  copy input csv1 into new csv2
  for each word in csv2 based on its pos parse the word and print parsed string into new column named parsed_outputs
  return new csv
'''

def print_test_cases():
    noun_test_cases = [
    ("na", "awehleeshoosh"),
    ("na", "amiimunzhush"),
    ("na", "ngukush"),
    ("ni", "naxkush"),
    ("na", "xuwiipambiil"),
    ("ni", "maxkasun"),
    ("ni", "maxkalaakwsiit"),
    ("ni", "miichuwaakan"),
    ("na", "pehpunawus"),
    ("na", "kiimooxkweew")]

    verb_test_cases = [
        ("vai", "muneew"),
        ("vai", "akiinsuw")
    ]

    test_cases = noun_test_cases + verb_test_cases

    for input_pos, input_str in test_cases:
        result = parser(input_str, input_pos)
        print(f"Input: {input_str}, Result: {result}")

def parse_user_input():
  while True:
      input_str = input("Enter Word: ")
      if input_str.lower() == 'quit':
          break

      input_pos = input("Enter Part of Speech: ")
      if input_pos.lower() == 'quit':
          break

      result = parser(input_str, input_pos)
      print(f"Input: {input_str}, Result: {result}")