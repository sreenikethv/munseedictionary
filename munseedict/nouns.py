from munseedict import core

def check_reduplication(word, pos):
  #ex: pehpetahkuw, there is a lot of thunder
  if len(word) >= 4:
    if word[0] == word[3] and is_consonant(word[0]):
      if is_vowel(word[1]) and word[2] == 'h':
        return "reduplication:"+word
  if len(word) >= 3:
    if word[0] == word[2] and is_consonant(word[0]) and is_vowel(word[1]):
      return "reduplication:"+word
    if word.startswith("a") and word[0] == word[2]:
      return "reduplication:"+word

def check_diminutive(word, pos):
  if word.endswith("s"):
    root = find_closest_entry(trim_final_vowels(word[:-1]), pos)
    suffix = "+-us"
    word = root+suffix
    return word
  elif word.endswith("sh"):
    root = find_closest_entry(trim_final_vowels(word[:-2]), pos)
    suffix = "+-ush"
    word = root+suffix
    return word

def check_locative(word, pos):
  if word.endswith("ng"):
    root = find_closest_entry(trim_final_vowels(word[:-2]), pos)
    suffix = "+-ung"
    return root+suffix

def check_plural(word, pos):
  if word.endswith("ak") or word.endswith("al"):
    root = find_closest_entry(trim_final_vowels(word[:-2]), pos)
    suffix = "+-" + word[-2:]
    word = root+suffix
    return word

def check_prenoun(word, pos):
  prenouns = dictionary[dictionary['POS'].str.contains('np', na=False)]
  for index, row in prenouns.iterrows():
    prenoun = row['Entry']
    prefix = prenoun.replace('-', '')
    if word.startswith(prefix):
      root = find_closest_entry(word[len(prefix):], 'n')
      word = prenoun + "+" + root
      return word
    else:
      prefix = trim_final_vowels(prenoun.replace('-', ''))
      if word.startswith(prefix):
        root = find_closest_entry(word[len(prefix):], 'n')
        word = prenoun + "+" + root
        return word

def check_nfin(word, pos):
  '''
  nfins = dictionary[dictionary['POS'].str.contains('nfin', na=False)]
  for index, row in nfins.iterrows():
    noun_final = row['Entry']
    suffix = noun_final.replace('-', '')
    if word.endswith(suffix):
      root = find_closest_entry(word[len(suffix):], 'v') #verb_pos
      word = root + "+" + noun_final
      return word
    else:
      suffix = trim_initial_vowels(noun_final.replace('-', ''))
      if word.endswith(suffix):
        root = find_closest_entry(word[len(suffix):], 'v')
        word = root + "+" + noun_final
        return word
  '''
  nfins = dictionary[dictionary['POS'].str.contains('nfin', na=False)]
  best_match = None
  min_distance = float('inf')

  for index, row in nfins.iterrows():
    noun_final = row['Entry']
    suffix = noun_final.replace('-', '')

    # Calculate edit distance for the suffix
    distance = Levenshtein.distance(word[-len(suffix):], suffix)
    # If the current suffix is a better match, update the best_match
    if distance < min_distance:
      min_distance = distance
      best_match = noun_final

    # Also check with trimmed initial vowels
    suffix = trim_initial_vowels(noun_final.replace('-', ''))
    distance = Levenshtein.distance(word[-len(suffix):], suffix)
    if distance < min_distance:
      min_distance = distance
      best_match = noun_final

    if best_match:
      root = find_closest_entry(word[:-len(best_match)], 'v')
      word = root + "+" + best_match
      return word

#prenoun-root-nounsuffix
def nounParser(word, pos):
  functions_to_check = [
    check_prenoun,
    check_plural,
    check_locative,
    check_diminutive,
    check_nfin,
    check_reduplication
  ]

  word = remove_aliases(process_bracketed_string(word.replace('*', '')))

  for func in functions_to_check:
    result = func(word, pos)
    if result:
      return result

    # If none of the functions returned anything
  return None