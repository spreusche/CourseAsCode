from bs4 import BeautifulSoup


def href_to_activity(activity, sections):
    if activity.module_name == "quiz" or activity.module_name == "resource" or activity.module_name == "assign":
        return
    soup = BeautifulSoup(activity.intro, "html.parser")
    a_tags = soup.find_all('a')

    for a in a_tags:
        href = a.get('href')
        new_href = parse_href(href, sections)
        a['href'] = new_href

    activity.intro = str(soup)


def parse_href(href: str, sections):
    href_sections = href.split("->")  # [module_name, file_name]

    for sec in sections:
        if href_sections[0] in sec.activities:
            for act in sec.activities[href_sections[0]]:
                if act.title == href_sections[1]:
                    return str(act.link)
        elif href_sections[0].lower() == "file":
            for f in sec.files:
                if f.name == href_sections[1]:
                    return str(f.link)
