from munseedict import verbs

# approximate the underlying form of a verb given its lemma form and POS
# maxkeew -> maxk
def findVerbStem(verb, pos):
  root = verb

  if(pos == "vta"):
    root = verb[:-3] # remove eew from 3rd person inflected form

  match pos:
    # vai
    case "vai" if(root.endswith("suw")): # /-usii/  What about "wiisuw" which is /-ii/ not /-usii/
      return root[:-3]
    case "vai" if(root.endswith("uw")): # /-ii/ unstable
      return root[:-2]
    case "vai" if(root.endswith("ul")): # /-ul/
      return root[:-2]
    case "vai" if(root.endswith("iil")):  # /-ul/
      return root[:-1]
    case "vai" if(root.endswith("xiin")): # /-iin/
      return root[:-3]
    case "vai" if(root.endswith("aam")): # /-aam/ 'sleep'
      return root
    case "vai" if(root.endswith("hl")): # /-hl/ 'motion'
      return root
    case "vai" if(root.endswith("keew")): # /-kaa/ or /-kee/ 'dance'
      return root[:-1]
    case "vai" if(root.endswith("pahtoow")): # /-pahtoo/ 'hurry, run'
      return root[:-1]
    case "vai" if(root.endswith("eew")): # /-ee/ or /-aa/ unstable
      return root[:-3]
    case "vai":
      print(f"{verb!r} has an unrecognized {pos!r} final")

    case "vai-s" if(root.endswith("iiw")): # /-ii/ stable
      return root[:-3]
    case "vai-s" if(root.endswith("aaw")): # /-aa/ stable
      return root[:-3]
    case "vai-s":
      print(f"{verb!r} has and unrecognized {pos!r} final")

    # vii
    case "vii" if(root.endswith("eew")):
      return root[:-3]
    case "vii" if(root.endswith("aaw")):
      return root[:-3]
    case "vii" if(root.endswith("iiw")):
      return root[:-3]
    case "vii" if(root.endswith("at")):
      return root[:-2]
    case "vii" if(root.endwith("uw")):
      return root[:-2]
    case "vii" if(root.endswith("an")):
      return root[:-2]
    case "vii" if(root.endswith("un")):
      return root[:-2]
    case "vii" if(root.endswith("unool")): # /-un-/ + /-al/
      return root[:-5]
    case "vii" if(root.endswith("ut")):
      return root[:-2]
    case "vii" if(root.endswith("tool")):
      return root[:-4]
    case "vii":
      print(f"{verb!r} has an unrecognized {pos!r} final")

    # vta
    case "vta" if(root.endswith("aw")):
      return root[:-2]
    case "vta" if(root.endswith("w")):
      return root[:-1]
    case "vta" if(root.endswith("l")):
      return root[:-1]
    case "vta":
      return root

    # vti
    case "vti1a" if(root.endswith("am")):
      return root[:-2]
    case "vti1a":
      print(f"{verb!r} has an unrecognized {pos!r} final")
    case "vti1b" if(root.endswith("um")):
      return root[:-2]
    case "vti1b":
      print(f"{verb!r} has an unrecognized {pos!r} final")
    case "vti2" if(root.endswith("toow")):
      return root[:-4]
    case "vti2":
      print(f"{verb!r} has an unrecognized {pos!r} final")
    case "vti3" if(root.endswith("nd")): # wund, piind, pumutaachiind
      return root[:-1]
    case "vti3" if(root.endswith("m")): # neem, kutaam, mulaam
      return root[:-1]
    case "vti3" if(root == "miichuw"): # miichii
      return root
    case "vti3":
      print(f"{verb!r} has an unrecognized {pos!r} final")

    # vaio
    case "vaio":
      print(f"{verb!r} has an unrecognized {pos!r} final")
    case "vtao":
      print(f"{verb!r} has an unrecognized {pos!r} final")

    # voti
    case "voti1a":
      print(f"{verb!r} has an unrecognized {pos!r} final")
    case "voti1b":
      print(f"{verb!r} has an unrecognized {pos!r} final")
    case "voti2":
      print(f"{verb!r} has an unrecognized {pos!r} final")

    # error
    case _:
      print(f"{pos!r} is not a valid verb type for {verb!r}")
  return 0

def verbParser(word, pos):
  stem = findVerbStem(word, pos)
  #check for prefixes
  #check for suffixes
  #check for medials
  return word