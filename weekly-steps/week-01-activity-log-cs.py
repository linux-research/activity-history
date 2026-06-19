import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- 1. CONFIGURATION ---
MAIN_TITLE = "Historie aktivit: Týden 1 - Základy Pythonu a řídicí struktury"
DEVELOPER = "HMP"

FONT_REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

DATE_STR = datetime.now().strftime("%Y-%m-%d")

# --- Filename sanitization ---
def sanitize_filename(text):
    forbidden = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for ch in forbidden:
        text = text.replace(ch, "")
    return text.replace(" ", "_")

safe_title = sanitize_filename(MAIN_TITLE)
FILE_NAME = f"{DATE_STR}_{safe_title}.pdf"

# --- 2. FONT REGISTRATION ---
if os.path.exists(FONT_REG_PATH) and os.path.exists(FONT_BOLD_PATH):
    try:
        pdfmetrics.registerFont(TTFont('DejaVu', FONT_REG_PATH))
        pdfmetrics.registerFont(TTFont('DejaVu-Bold', FONT_BOLD_PATH))
        MAIN_FONT, BOLD_FONT = 'DejaVu', 'DejaVu-Bold'
    except Exception:
        MAIN_FONT, BOLD_FONT = 'Helvetica', 'Helvetica-Bold'
else:
    MAIN_FONT, BOLD_FONT = 'Helvetica', 'Helvetica-Bold'

# --- 3. STYLES ---
def get_custom_styles():
    styles = getSampleStyleSheet()
    return {
        'date': ParagraphStyle('DateStyle', parent=styles['Normal'], alignment=2,
                               fontSize=10, fontName=BOLD_FONT),

        'h1': ParagraphStyle('H1', parent=styles['Heading1'], fontSize=14,
                             textColor=colors.white, fontName=BOLD_FONT),

        'subheader': ParagraphStyle('SubHeader', parent=styles['Normal'],
                                    fontSize=9.5, textColor=colors.lightgrey,
                                    alignment=0, fontName=MAIN_FONT),

        'h2': ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12,
                             textColor=colors.HexColor("#2c3e50"),
                             fontName=BOLD_FONT, borderPadding=(0, 0, 3, 0),
                             borderSides='B', borderWidth=1,
                             borderColor=colors.HexColor("#3498db"),
                             spaceBefore=10, spaceAfter=12),

        'body': ParagraphStyle('Body', parent=styles['Normal'], fontSize=9.5,
                               leading=13, alignment=4, fontName=MAIN_FONT,
                               spaceAfter=10),

        'box_h': ParagraphStyle('BoxH', parent=styles['Normal'], fontSize=8,
                                textColor=colors.HexColor("#3498db"),
                                fontName=BOLD_FONT, textTransform='uppercase',
                                spaceAfter=4),

        'li': ParagraphStyle('LI', parent=styles['Normal'], fontSize=9,
                             leading=12, leftIndent=12, fontName=MAIN_FONT,
                             spaceAfter=4)
    }

# --- 4. FOOTER ---
def draw_footer(canvas, doc):
    canvas.saveState()
    footer_text = f"{MAIN_TITLE} | Vývojář: {DEVELOPER} - Strana {doc.page}"
    canvas.setFont(MAIN_FONT, 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 30, footer_text)
    canvas.setStrokeColor(colors.lightgrey)
    canvas.line(50, 45, A4[0] - 50, 45)
    canvas.restoreState()

# --- 5. CORE GENERATOR ---
def run_script():
    doc = SimpleDocTemplate(
        FILE_NAME,
        pagesize=A4,
        rightMargin=50, leftMargin=50,
        topMargin=30, bottomMargin=60
    )

    s = get_custom_styles()
    story = []

    # --- Content Map (4 sections) ---
    content_map = [
        {
            "id": 1,
            "title": "I. Konfigurace prostředí",
            "paragraphs": [
                "Prvním krokem je instalace Pythonu verze 3.10 nebo novější z oficiální distribuce python.org. "
                "Během instalace se konfiguruje proměnná prostředí PATH pro přístup k interpreteru Pythonu "
                "z příkazové řádky z libovolného adresáře.",

                "Pro vývoj je vybrán editor kódu. VS Code s rozšířením pro Python je zvolen jako primární prostředí "
                "díky integrovanému terminálu, zvýrazňování syntaxe a možnostem ladění. "
                "PyCharm Community Edition představuje alternativu s kompletním IDE.",

                "Instalace se ověří spuštěním 'python --version' v terminálu. Vytvoří se testovací soubor 'hello.py' "
                "s příkazem print. Soubor se spustí příkazem 'python hello.py', čímž se potvrdí funkčnost prostředí."
            ],
            "label": "Konfigurace dokončena",
            "items": [
                "Python 3.10+ nainstalován s konfigurací PATH",
                "VS Code nakonfigurován s rozšířením pro Python",
                "První program spuštěn: print(\"Hello, World!\")"
            ]
        },
        {
            "id": 2,
            "title": "II. Proměnné a datové typy",
            "paragraphs": [
                "Proměnné v Pythonu ukládají data bez explicitní deklarace typu. Interpret určuje typ za běhu. "
                "Názvy proměnných začínají písmenem nebo podtržítkem, obsahují alfanumerické znaky "
                "a rozlišují velká a malá písmena. Konvence snake_case je standardem v Pythonu.",

                "Probírá se pět základních datových typů: celá čísla (int), desetinná čísla (float), "
                "řetězce (str) pro text v uvozovkách, booleovské hodnoty (bool) pro True/False "
                "a None pro absenci hodnoty. Funkce type() vrací třídu objektu.",

                "Operace s řetězci zahrnují spojování (+), opakování (*) a měření délky (len()). "
                "Víceřádkové řetězce používají trojité uvozovky. Podtržítka zlepšují čitelnost čísel (1_000_000)."
            ],
            "label": "Probrané datové typy",
            "items": [
                "int: celá čísla (42, -10, 1_000_000)",
                "float: desetinná čísla (19.99, 3.14159, 2.5e6)",
                "str: text v jednoduchých, dvojitých nebo trojitých uvozovkách",
                "bool: hodnoty True nebo False / None: absence hodnoty"
            ]
        },
        {
            "id": 3,
            "title": "III. Vstup/výstup a operátory",
            "paragraphs": [
                "Funkce print() zobrazuje data v konzoli. Přijímá více argumentů a dva volitelné parametry: "
                "'sep' definuje oddělovač mezi hodnotami (výchozí je mezera), 'end' definuje ukončení řádku "
                "(výchozí je nový řádek). F-strings umožňují formátovaný výstup: f\"text {proměnná}\".",

                "Funkce input() získává vstup uživatele a vrací řetězec. Funkce int() a float() převádějí "
                "textový vstup na číselné typy. Validace je nutná, protože input() vždy vrací řetězec.",

                "Probírají se tři kategorie operátorů. Aritmetické: +, -, *, /, // (celočíselné dělení), % (modulo), ** (mocnina). "
                "Porovnávací: ==, !=, <, >, <=, >= (vrací booleovské hodnoty). Logické: and, or, not (kombinují výrazy)."
            ],
            "label": "Přehled operátorů",
            "items": [
                "Aritmetické: +, -, *, /, //, %, **",
                "Porovnávací: ==, !=, <, >, <=, >=",
                "Logické: and, or, not"
            ]
        },
        {
            "id": 4,
            "title": "IV. Řídicí struktury a projekt",
            "paragraphs": [
                "Podmínkové příkazy řídí průběh programu podle booleovských výrazů. Příkaz if vykoná blok kódu, "
                "když je podmínka True. Klauzule else poskytuje alternativu, když je podmínka False. "
                "Klíčové slovo elif umožňuje řetězení více podmínek.",

                "Python používá odsazení k definování bloků kódu. Konzistentní odsazení 4 mezerami na úroveň je vyžadováno. "
                "Podmínky se kombinují logickými operátory (and, or) a mohou být vnořené.",

                "Týdenním projektem je klasifikátor známek. Program přijímá číselné skóre přes input(), převádí jej na celé číslo "
                "a pomocí zřetězených příkazů if/elif/else přiřazuje písmeno (A, B, C, D nebo F) podle definovaných prahů. "
                "Výsledek se zobrazí pomocí f-stringu se skóre a odpovídající známkou."
            ],
            "label": "Implementace projektu",
            "items": [
                "input() přijímá číselné skóre jako řetězec",
                "int() převádí řetězec na celé číslo",
                "if/elif/else vyhodnocuje prahy a přiřazuje známku",
                "f-string zobrazuje skóre a písmeno známky"
            ]
        }
    ]

    # --- Header ---
    story.append(Paragraph(DATE_STR, s['date']))
    story.append(Spacer(1, 5))

    header_table = Table(
        [
            [Paragraph(MAIN_TITLE, s['h1'])],
            [Paragraph(f"Vývojář: {DEVELOPER}", s['subheader'])]
        ],
        colWidths=[doc.width]
    )

    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#2c3e50")),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 10)
    ]))

    story.append(header_table)
    story.append(Spacer(1, 15))

    # --- Build Sections ---
    for section in content_map:
        story.append(Paragraph(section["title"], s['h2']))

        for p in section["paragraphs"]:
            story.append(Paragraph(p, s['body']))

        box_content = [Paragraph(section["label"], s['box_h'])] + [
            Paragraph(f"• {i}", s['li']) for i in section["items"]
        ]

        b_table = Table([[box_content]], colWidths=[doc.width - 20])
        b_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#fdfdfd")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#e1e4e8")),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
        ]))

        story.append(b_table)
        story.append(Spacer(1, 15))

        # Page break after section 2 only (sections 1-2 on page 1, sections 3-4 on page 2)
        if section["id"] == 2:
            story.append(PageBreak())

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    print(f"Historie aktivit vygenerována: {FILE_NAME}")

if __name__ == "__main__":
    run_script()
