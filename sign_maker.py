import click
from path import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, landscape, inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, PageBreak, Spacer
from reportlab.lib.utils import simpleSplit

OUT_DIR = Path("output")

PAGE_SIZE = landscape(letter)
DEFAULT_WIDTH, DEFAULT_HEIGHT = PAGE_SIZE

def render_sign_elements(base_name, label, elements):
    try:
        OUT_DIR.makedirs()
    except:
        # Dir already exists
        pass
    filename = OUT_DIR / "{}-sign-{}.pdf".format(base_name, label.replace(" ", "_"))
    doc = SimpleDocTemplate(filename, pagesize=PAGE_SIZE,
            rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0)
    doc.build(elements)
    print("Wrote {}".format(filename))

def sign_elements(labels, size=128):
    title_style = ParagraphStyle("Title",
            fontName="Helvetica-Bold", fontSize=size, leading=size,
            alignment=TA_CENTER)
    elements = list()
    for label in labels:
        if elements:
            elements.append(PageBreak())
        if "Therese's" in label:
            line_style = title_style.clone("smaller")
            line_style.fontSize -= 28
        else:
            line_style = title_style
        paragraph = Paragraph(label, line_style)
        text_height = get_text_height([paragraph])
        elements.append(Spacer(1, (DEFAULT_HEIGHT - text_height) / 3))
        elements.append(paragraph)
    return elements

def get_text_height(lines, width=DEFAULT_WIDTH):
    answer = 0
    for line in lines:
        # simpleSplit calculates how reportlab will break up the lines for
        # display in a paragraph, by using width/fontsize.
        # Default Frame padding is 6px on left & right
        split = simpleSplit(line.text, line.style.fontName, line.style.fontSize, width - 12)
        answer += len(split) * line.style.leading
    return answer

@click.command()
def main(signs_path="signs.txt", base_name="signs"):
    lines = [line.strip() for line in Path(signs_path).lines()]
    elements = sign_elements(lines)
    render_sign_elements(base_name, "ALL", elements)

if __name__ == '__main__':
    main()
