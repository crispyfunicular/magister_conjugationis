from project import get_verbs
from pynooj import read_dic

verbs_CSV = get_verbs("verbs_latin.csv")
print("Nombre de verbes latins CSV :", len(verbs_CSV))

# Parse a NooJ dictionary file
verbs_NooJ = read_dic("NooJ/la/Lexical Analysis/lat_verbes-flx.dic")
print("Nombre de verbes latins NooJ :", len(verbs_NooJ))

for verb_NooJ in verbs_NooJ:
    #print(verb_NooJ)    
    inflected_form = verb_NooJ["inflected form"]
    mod = verb_NooJ.get("traits", {}).get("MOD")
    if not mod:
        print("MOD not found")
        print(verb_NooJ)
        continue
    if mod == "sub":
        continue
    #print(inflected_form)
    
    found = False
    for verb_CSV in verbs_CSV:
        #print(verb_CSV)
        latin_form = verb_CSV["latin"]
        #print(latin_form)
        
        if inflected_form == latin_form:
            found = True
            break
    
    if not found:
        print(f"{inflected_form} not found")


