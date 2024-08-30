import markdown

def parse_md(md_file: str):
    with open(md_file, 'r') as f:
        tempMd = f.read()

    tempHtml = markdown.markdown(tempMd)
    return tempHtml


def html_to_xml(html: str):
    html = html.replace('<', '&lt;')
    html = html.replace('>', '&gt;')
    return html
