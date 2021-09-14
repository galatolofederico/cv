import json
import re
import os
import argparse

def getPlatform(mejson, name, raw=False):
    for profile in mejson["digitalidentity"]["profiles"]:
        if profile["platform"] == name:
            if raw:
                return profile["link"]
            else:
                return profile["link"].split("/")[-1]
    return "Not Found"


def getpubBibTeX(pub):
    keywords = ";".join(pub["keywords"])
    authors = pub["authors"].replace(",", " and ")
    container = "under-review" if pub["container"] == "preprint" else pub["container"] 
    if pub["type"] == "conference":
        return """
@inproceedings{%s,
  AUTHOR = {%s},
  TITLE = {{%s}},
  BOOKTITLE = {{%s}},
  VOLUME = {%s},
  PAGES = {%s},
  YEAR = {%s},
  MONTH = {%s},
  KEYWORDS = {%s},
  DOI = {%s},
  URL = {%s},
  ISBN = {%s}
}
""" % (pub["name"], authors, pub["title"], 
        container, pub["volume"], pub["pages"], 
        pub["date"]["year"], pub["date"]["month"], 
        keywords, pub["doi"], pub["link"], pub["isbn"])

    if pub["type"] == "journal":
        return """
@article{%s,
  AUTHOR = {%s},
  TITLE = {{%s}},
  JOURNAL = {{%s}},
  VOLUME = {%s},
  PAGES = {%s},
  YEAR = {%s},
  MONTH = {%s},
  KEYWORDS = {%s},
  DOI = {%s},
  URL = {%s},
  ISBN = {%s}
}
""" % (pub["name"], authors, pub["title"], 
        container, pub["volume"], pub["pages"], 
        pub["date"]["year"], pub["date"]["month"], 
        keywords, pub["doi"], pub["link"], pub["isbn"])



def getProjectBibTex(proj):
    return """
@misc{%s,
  TITLE = {{%s}},
  KEYWORDS = {project},
  NOTE = {{%s}},
  YEAR = {%s},
  MONTH = {%s},
  DAY = {%s},
  URL = {%s}
}
""" % (proj["name"], proj["title"], proj["description"],
       proj["date"]["year"], proj["date"]["month"], proj["date"]["day"],
       proj["link"])


def getLectureBibTex(lecture):
    note = lecture["container"]+" ("+lecture["position"]+")"
    url = "https://galatolo.me/lecture/"+lecture["name"]
    return """
@misc{%s,
  TITLE = {{%s}},
  KEYWORDS = {lecture},
  NOTE = {{%s}},
  YEAR = {%s},
  MONTH = {%s},
  DAY = {%s},
  URL = {%s}
}
""" % (lecture["name"], lecture["title"], note,
       lecture["date"]["year"], lecture["date"]["month"], lecture["date"]["day"],
       url) 

thesis_id = 0
def getThesisBibTex(thesis):
    global thesis_id
    thesis_id += 1
    name = "thesis_"+str(thesis_id)
    return """
@misc{%s,
  TITLE = {{%s}},
  AUTHOR = {%s},
  KEYWORDS = {thesis},
  NOTE = {{%s}},
  YEAR = {%s},
  MONTH = {%s},
  DAY = {%s},
}
""" % (name, thesis["title"], thesis["author"], thesis["type"],
      thesis["date"]["year"], thesis["date"]["month"], thesis["date"]["day"],)

journal_role_count = 0
def getJorunalRoleBibTex(role):
    global journal_role_count
    journal_role_count += 1
    return """
@misc{journalrole-%s,
  TITLE = {{%s - %s}},
  AUTHOR = {%s},
  KEYWORDS = {journalrole},
  URL = {%s}
}
""" % (journal_role_count, role["journal"], role["publisher"], role["role"], role["link"]) 


conference_role_count = 0
def getConferenceRoleBibTex(role):
    global conference_role_count
    conference_role_count += 1
    return """
@misc{conferencerole-%s,
  TITLE = {{%s}},
  AUTHOR = {%s},
  KEYWORDS = {conferencerole},
  URL = {%s}
}
""" % (conference_role_count, role["conference"], role["role"], role["link"]) 

mejson_file = os.getenv("MEJSON") if os.getenv("MEJSON") is not None else "./me.json/me.json"
mejson = json.load(open(mejson_file, "r"))

placeholders = {
    "@firstname": mejson["anagraphic"]["fullname"]["first"]+" "+mejson["anagraphic"]["fullname"]["middle"][0]+". ",
    "@lastname": mejson["anagraphic"]["fullname"]["last"],
    "@qualification": mejson["anagraphic"]["qualifications"][1],
    "@city": mejson["anagraphic"]["address"]["city"]+" ("+mejson["anagraphic"]["address"]["cap"]+")",
    "@street": mejson["anagraphic"]["address"]["street"],
    "@building": mejson["anagraphic"]["address"]["building"],
    "@website": mejson["digitalidentity"]["website"].split("://")[1],
    "@url_website": mejson["digitalidentity"]["website"],
    "@phone": mejson["digitalidentity"]["telephone"],
    "@url_phone": "tel:"+mejson["digitalidentity"]["telephone"],
    "@email": mejson["digitalidentity"]["email"].replace("@", " @"),
    "@url_email": "mailto:"+mejson["digitalidentity"]["email"].replace("@", " @"),
    "@telegram": getPlatform(mejson, "Telegram"),
    "@url_telegram": getPlatform(mejson, "Telegram", True),
    "@github": getPlatform(mejson, "GitHub"),
    "@url_github": getPlatform(mejson, "GitHub", True),
}

placeholders["@signature_file"] = os.getenv("SIGNATURE_FILE") if os.getenv("SIGNATURE_FILE") is not None else "./pictures/signature.png"

legalnotice = 'Consapevole delle sanzioni penali, nel caso di dichiarazioni non veritiere, di formazione o uso atti falsi richiamate dall’art. 76 del D.P.R. 445 del 28 dicembre 2000, nonché della sanzione ulteriore prevista dall’art. 75 del citato D.P.R. 445 del 28 dicembre 2000, consistente nella decadenza dai benefici eventualmente conseguenti al provvedimento emanato sulla base della dichiarazione non veritiera. Autorizzo il trattamento dei miei dati personali presenti nel cv ai sensi del Decreto Legislativo 30 giugno 2003, n. 196 "Codice in materia di protezione dei dati personali" e del GDPR (Regolamento UE 2016/679).'

parser = argparse.ArgumentParser()

parser.add_argument("--template", type=str, default="template.tex")
parser.add_argument("--tex-output", type=str, default="cv.tex")
parser.add_argument("--bibliography-output", type=str, default="bibliography.bib")
parser.add_argument("--misc-output", type=str, default="misc.bib")
parser.add_argument("--signature", action="store_true")

args = parser.parse_args()

template = open(args.template, "r").read()

cv = open(args.tex_output, "w")

for key, value in placeholders.items():
    template = template.replace(key, value)

if args.signature:
    template = template.replace("@legalnotice", legalnotice)
    template = template.replace("@legalstart", "")
    template = template.replace("@legalend", "")
else:
    template = re.sub('@legalstart.*@legalend', "", template, flags=re.DOTALL)

cv.write(template)
cv.close()

bibliography = open(args.bibliography_output, "w")
for pub in mejson["publications"]:
    bibliography.write(getpubBibTeX(pub))
bibliography.close()

misc = open(args.misc_output, "w")
for proj in mejson["projects"]:
    misc.write(getProjectBibTex(proj))
for lecture in mejson["lectures"]:
    misc.write(getLectureBibTex(lecture))
for thesis in mejson["advised_theses"]:
    misc.write(getThesisBibTex(thesis))
for role in mejson["roles"]["journals"]:
    misc.write(getJorunalRoleBibTex(role))
for role in mejson["roles"]["conferences"]:
    misc.write(getConferenceRoleBibTex(role))
misc.close()