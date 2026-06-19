import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- 1. CONFIGURATION ---
MAIN_TITLE = "Activity History: Week 1 - Python Basics and Control Flow"
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
    footer_text = f"{MAIN_TITLE} | Developer: {DEVELOPER} - Page {doc.page}"
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
            "title": "I. Environment Setup and Initial Configuration",
            "paragraphs": [
                "The first step involves installing Python version 3.10 or later from the official python.org distribution. "
                "During installation, the PATH environment variable is configured to allow command-line access to the Python "
                "interpreter from any directory.",

                "A code editor is selected for development. VS Code with the Python extension is chosen as the primary environment "
                "for its integrated terminal, syntax highlighting, and debugging capabilities. "
                "PyCharm Community Edition is an alternative offering a full IDE experience.",

                "The installation is verified by executing 'python --version' in the terminal. A test file named 'hello.py' is created "
                "with a print statement. The file is executed via 'python hello.py', confirming the environment is operational."
            ],
            "label": "Configuration Completed",
            "items": [
                "Python 3.10+ installed with PATH configuration",
                "VS Code configured with Python extension",
                "First program executed: print(\"Hello, World!\")"
            ]
        },
        {
            "id": 2,
            "title": "II. Variables and Data Types",
            "paragraphs": [
                "Variables in Python store data without explicit type declarations. The interpreter determines the type at runtime. "
                "Variable names must start with a letter or underscore, can contain alphanumeric characters, and are case-sensitive. "
                "The snake_case naming convention is standard in Python.",

                "Five primary data types are covered: integers (int) for whole numbers, floats (float) for decimal values, "
                "strings (str) for text data enclosed in quotes, booleans (bool) for True/False values, "
                "and None for representing absence of value. The type() function returns the class of any object.",

                "String operations include concatenation (+), repetition (*), and length measurement (len()). "
                "Multi-line strings use triple quotes. Underscores improve numeric literal readability (e.g., 1_000_000)."
            ],
            "label": "Data Types Covered",
            "items": [
                "int: whole numbers (42, -10, 1_000_000)",
                "float: decimal numbers (19.99, 3.14159, 2.5e6)",
                "str: text with single, double, or triple quotes",
                "bool: True or False values / None: absence of value"
            ]
        },
        {
            "id": 3,
            "title": "III. Input/Output Operations and Operators",
            "paragraphs": [
                "The print() function outputs data to the console. It accepts multiple arguments and two optional parameters: "
                "'sep' defines the separator between values (default is space), 'end' defines the line terminator "
                "(default is newline). F-strings provide formatted output: f\"text {variable}\".",

                "The input() function captures user input and returns a string. The int() and float() functions convert "
                "text input to numeric types. Validation is necessary since input() always returns a string.",

                "Three categories of operators are covered. Arithmetic: +, -, *, /, // (floor division), % (modulo), ** (power). "
                "Comparison: ==, !=, <, >, <=, >= (return booleans). Logical: and, or, not (combine boolean expressions)."
            ],
            "label": "Operators Reference",
            "items": [
                "Arithmetic: +, -, *, /, //, %, **",
                "Comparison: ==, !=, <, >, <=, >=",
                "Logical: and, or, not"
            ]
        },
        {
            "id": 4,
            "title": "IV. Control Flow Structures and Applied Project",
            "paragraphs": [
                "Conditional statements control program execution based on boolean expressions. The if statement executes a block "
                "when its condition is True. The else clause provides an alternative when the condition is False. "
                "The elif keyword chains multiple conditions in sequence.",

                "Python uses indentation to define code blocks. Consistent indentation of 4 spaces per level is required. "
                "Conditions can be combined using logical operators (and, or) and nested within other conditionals.",

                "The week concludes with a grade classifier project. The program receives a numeric score via input(), converts it "
                "to an integer, then uses chained if/elif/else statements to assign a letter grade (A, B, C, D, or F) based on "
                "defined thresholds. The result is displayed using an f-string with both the score and corresponding grade."
            ],
            "label": "Project Implementation",
            "items": [
                "input() receives the numeric score as string",
                "int() converts the string to an integer value",
                "if/elif/else evaluates thresholds and assigns grade",
                "f-string outputs the score and letter grade"
            ]
        }
    ]

    # --- Header ---
    story.append(Paragraph(DATE_STR, s['date']))
    story.append(Spacer(1, 5))

    header_table = Table(
        [
            [Paragraph(MAIN_TITLE, s['h1'])],
            [Paragraph(f"Developer: {DEVELOPER}", s['subheader'])]
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
    print(f"Activity log generated: {FILE_NAME}")

if __name__ == "__main__":
    run_script()
