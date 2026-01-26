import pynooj
import json

def main():
    verbs_lst = []
    dic_path = "NooJ/Lexical Analysis/lat_verbes-flx.dic"
    print("reading verbs from NooJ dic:", dic_path)
    dics_nooj = pynooj.read_dic(dic_path)
    print(f"loaded {len(dics_nooj)} inflected forms (lines)")

    for dic_nooj in dics_nooj:
        dic_mc = {}
        try:
            dic_mc["latin"] = dic_nooj["inflected form"].replace("v", "u").replace("j", "i")
            dic_mc["lemma"] = dic_nooj["lemma"].replace("v", "u").replace("j", "i")
            dic_mc["group"] = int(dic_nooj["traits"]["GP"])
            dic_mc["mood"] = dic_nooj["traits"]["MOD"].replace("ind", "indicatif").replace("sub", "subjonctif")
            dic_mc["voice"] = dic_nooj["traits"]["VX"].replace("act", "actif").replace("pas", "passif")
            dic_mc["translation"] = dic_nooj["traits"]["TRAD"].split(";")

            # Convert to (French) human-readable tense (fut --> futur)
            match dic_nooj["traits"]["TP"]:
                case "fut":
                    dic_mc["tense"] = "futur"
                case "impf":
                    dic_mc["tense"] = "imparfait"
                case "pres":
                    dic_mc["tense"] = "présent"
                case "pft":
                    dic_mc["tense"] = "parfait"
                case "pqp":
                    dic_mc["tense"] = "plus-que-parfait"
                case "fta":
                    dic_mc["tense"] = "futur antérieur"
                case _:
                    raise ValueError("Invalid form, the tense is invalid")
            
            dic_mc["person"] = int(dic_nooj["traits"]["P"])
            if dic_mc["person"] not in range(1,4):
                raise ValueError("Invalid form, the person is invalid")
            if dic_nooj["traits"]["NB"] == "pl":
                dic_mc["person"] += 3
            verbs_lst.append(dic_mc)
        except Exception as e:
            print("Error with:", dic_nooj)
            raise e

    # Sort by lemma > mood > voice > tense > person
    verbs_lst = sorted(verbs_lst, key=lambda x: (x['lemma'], x['mood'], x['voice'], x['tense'], x['person']))

    # This list will contain only correct inflected forms and not false automatically generated forms.
    filtered_verbs = []
    for inflected_form in verbs_lst:
        if inflected_form["person"] == 2 and inflected_form["mood"] == "indicatif" and inflected_form["voice"] == "passif":
            if (inflected_form["group"] == 1 or inflected_form["group"] == 2 and inflected_form["tense"] == "futur") or (inflected_form["group"] == 3 or inflected_form["group"] == 4 and inflected_form["tense"] == "présent"):
                if inflected_form["latin"][-4:] == "iris":
                    #print(inflected_form["latin"])
                    continue
        filtered_verbs.append(inflected_form)


    json_path = "verbs_latin.json"
    print(f"writing {len(filtered_verbs)} verbs to json file:", json_path)
    with open (json_path, "w", encoding="utf-8") as f:
        json.dump(filtered_verbs, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()