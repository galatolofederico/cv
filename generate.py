import json

mejson = json.load(open("me.json/me.json", "r"))
template = open("template.tex", "r").read()


placeholders = {
    "@firstname": mejson["anagraphic"]["fullname"]["first"]+" "+mejson["anagraphic"]["fullname"]["middle"][0]+". ",
    "@lastname": mejson["anagraphic"]["fullname"]["last"],
    "@qualification": mejson["anagraphic"]["qualifications"][1],
    "@city": mejson["anagraphic"]["address"]["city"]+" "+mejson["anagraphic"]["address"]["cap"],
    "@street": mejson["anagraphic"]["address"]["street"],
    "@building": mejson["anagraphic"]["address"]["building"]
}

for key, value in placeholders.items():
    template = template.replace(key, value)


open("cv.tex", "w").write(template)