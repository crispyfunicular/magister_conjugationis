import pynooj
import json

def main():
    verbs_lst = []
    dic_path = "NooJ/la/Lexical Analysis/lat_verbes-flx.dic"
    print("reading verbs from NooJ dic:", dic_path)
    dics_nooj = pynooj.read_dic(dic_path)
    print(f"loaded {len(dics_nooj)} inflected forms (lines)")

    for dic_nooj in dics_nooj:
        dic_mc = {}
        try:
            dic_mc["latin"] = dic_nooj["inflected form"].replace("v", "u").replace("j", "i")
            dic_mc["lemma"] = dic_nooj["lemma"].replace("v", "u").replace("j", "i")
            dic_mc["group"] = dic_nooj["traits"]["GP"]
            dic_mc["mod"] = dic_nooj["traits"]["MOD"]
            dic_mc["voice"] = dic_nooj["traits"]["VX"]

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


    json_path = "verbs_latin.json"
    print("writing verbs to json file:", json_path)
    with open (json_path, "w", encoding="utf-8") as f:
        json.dump(verbs_lst, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()