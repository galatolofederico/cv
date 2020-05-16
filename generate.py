import json

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

mejson = json.load(open("me.json/me.json", "r"))

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


template = open("template.tex", "r").read()
cv = open("cv.tex", "w")
for key, value in placeholders.items():
    template = template.replace(key, value)
cv.write(template)
cv.close()

bibliography = open("bibliography.bib", "w")
for pub in mejson["publications"]:
    bibliography.write(getpubBibTeX(pub))
bibliography.close()

misc = open("misc.bib", "w")
for proj in mejson["projects"]:
    misc.write(getProjectBibTex(proj))
for lecture in mejson["lectures"]:
    misc.write(getLectureBibTex(lecture))
for thesis in mejson["advised_theses"]:
    misc.write(getThesisBibTex(thesis))
misc.close()