from munseedict import utils
import Levenshtein

dictionary = utils.get_csv("dictionary.csv")

# Clean database
# remove aliases for the Entry and only use the main version for etymological parsing
"""
Processes a string with square brackets, returning variants with and without the content inside the brackets.
ato[h] -> ato;atoh , -[w]aakan = -aakan;-waakan , alangweew -> alangweew
"""
def process_bracketed_string(input_str):
  start, end = input_str.find('['), input_str.find(']')
  if start != -1 and end != -1:
    before, inside, after = input_str[:start], input_str[start + 1:end], input_str[end + 1:]
    return f"{before}{after};{before}{inside}{after}"
  return input_str

# ato;atoh becomes ato
# -ush becomes ush
def remove_aliases(input_str):
  result = ""
  if ';' in input_str:
      result = input_str.split(';')[0]
  result = input_str.replace('-', '')
  return result

'''
# Create a new column to store the original entries
data['Original_Entry'] = data['Entry']
# Apply the process_entries function to the "Entry" column
data['Entry'] = data['Entry'].apply(process_bracketed_string)
# Now data contains both the processed entries and the original entries
# Save the DataFrame with processed entries to a new CSV file
data.to_csv('processed_dictionary.csv', index=False)
# To revert to the original entries, you can do the following:
data['Entry'] = data['Original_Entry']
# Save the DataFrame with original entries to another CSV file
data.to_csv('your_reverted_file.csv', index=False)
'''

def is_consonant(c):
  return c.isalpha() and c.lower() not in 'aeiou'

def is_vowel(c):
  return c.isalpha() and c.lower() in 'aeiou'

def trim_final_vowels(word):
  while (is_vowel(word[-1])): word = word[:-1]
  return word

def trim_initial_vowels(word):
  while (is_vowel(word[0])): word = word[1:]
  return word


def find_closest_entry(word, pos):
  # Filter entries based on POS
  pos_entries = dictionary[dictionary['POS'].str.contains(pos, na=False)]
  # Use edit distance to find the closest word
  closest_entry = min(pos_entries['Entry'], key=lambda x: Levenshtein.distance(x, word))
  return closest_entry

# Define replacements as a global variable
replacements = {
  "ch": "č",
  "sh": "š",
  "zh": "ž",
  "aa": "ā",
  "ee": "ē",
  "ii": "ī",
  "oo": "ō"
}

# munseeToEnglish
def mte(input_str):
  output_str = input_str
  for key, value in replacements.items():
    output_str = output_str.replace(key, value)
  return output_str

# englishToMunsee
def etm(input_str):
  # Create reverse replacements by swapping keys and values
  reverse_replacements = {value: key for key, value in replacements.items()}
  output_str = input_str
  for key, value in reverse_replacements.items():
    output_str = output_str.replace(key, value)
  return output_str

def find_closest_entry(word, pos):
  # Filter entries based on POS
  pos_entries = dictionary[dictionary['POS'].str.contains(pos, na=False)]
  # Use edit distance to find the closest word, applying etm function first
  closest_entry = min(pos_entries['Entry'], key=lambda x: Levenshtein.distance(etm(x.replace('*', '')), etm(word)))
  return closest_entry

def prefix_edit_distance(str1, str2):
  # Calculate the Levenshtein distance only for the prefix
  min_len = min(len(str1), len(str2))
  prefix_distance = Levenshtein.distance(str1[:min_len], str2[:min_len])
  return prefix_distance

# parts of speech that correspond to standalone words, not parts of words such as prefixes, medials, suffixes
# all parts of speech listed in O'Meara's Delaware Dictionary except pv & pn (preverb and prenoun)
noun_pos = ['na', 'ni', 'nad', 'nid']
verb_pos = ['vai', 'vai-s', 'vii', 'vii-s', 'vta', 'vti1a', 'vti1b', 'vti2', 'vti3', 'vtao', 'vaio', 'voti']
particle_pos = ['pc', 'pr']
word_pos = noun_pos + verb_pos + particle_pos

nonword_noun_pos = ["np", "nb", "nmed", "npom", "nfin"]
nonword_verb_pos = ["vp", "vinc", "vmed", "vpf", "vf", "vpos", "vts"]
nonword_pos = nonword_noun_pos + nonword_verb_pos

pos_tagset = word_pos + nonword_pos