import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- 1. CONFIGURATION ---
MAIN_TITLE = "Historique d'activité : Semaine 1 - Bases Python et Flux de Contrôle"
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
    footer_text = f"{MAIN_TITLE} | Développeur : {DEVELOPER} - Page {doc.page}"
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
            "title": "I. Configuration de l'environnement",
            "paragraphs": [
                "La première étape consiste à installer Python version 3.10 ou ultérieure depuis la distribution officielle python.org. "
                "Lors de l'installation, la variable d'environnement PATH est configurée pour permettre l'accès à l'interpréteur Python "
                "en ligne de commande depuis n'importe quel répertoire.",

                "Un éditeur de code est sélectionné pour le développement. VS Code avec l'extension Python est retenu comme environnement "
                "principal pour son terminal intégré, sa coloration syntaxique et ses capacités de débogage. "
                "PyCharm Community Edition constitue une alternative offrant une expérience IDE complète.",

                "L'installation est vérifiée en exécutant 'python --version' dans le terminal. Un fichier test nommé 'hello.py' est créé "
                "avec une instruction print. Le fichier est exécuté via 'python hello.py', confirmant que l'environnement est opérationnel."
            ],
            "label": "Configuration terminée",
            "items": [
                "Python 3.10+ installé avec configuration PATH",
                "VS Code configuré avec l'extension Python",
                "Premier programme exécuté : print(\"Hello, World!\")"
            ]
        },
        {
            "id": 2,
            "title": "II. Variables et types de données",
            "paragraphs": [
                "Les variables Python stockent des données sans déclaration de type explicite. L'interpréteur détermine le type à l'exécution. "
                "Les noms de variables commencent par une lettre ou un tiret bas, contiennent des caractères alphanumériques, "
                "et sont sensibles à la casse. La convention snake_case est le standard Python.",

                "Cinq types de données principaux sont abordés : les entiers (int) pour les nombres entiers, les flottants (float) pour "
                "les valeurs décimales, les chaînes (str) pour le texte entre guillemets, les booléens (bool) pour True/False, "
                "et None pour l'absence de valeur. La fonction type() retourne la classe d'un objet.",

                "Les opérations sur les chaînes comprennent la concaténation (+), la répétition (*), et la mesure de longueur (len()). "
                "Les chaînes multilignes utilisent les triples guillemets. Les tirets bas améliorent la lisibilité des nombres (1_000_000)."
            ],
            "label": "Types de données couverts",
            "items": [
                "int : nombres entiers (42, -10, 1_000_000)",
                "float : nombres décimaux (19.99, 3.14159, 2.5e6)",
                "str : texte avec guillemets simples, doubles ou triples",
                "bool : valeurs True ou False / None : absence de valeur"
            ]
        },
        {
            "id": 3,
            "title": "III. Entrées/sorties et opérateurs",
            "paragraphs": [
                "La fonction print() affiche des données dans la console. Elle accepte plusieurs arguments et deux paramètres optionnels : "
                "'sep' définit le séparateur entre les valeurs (espace par défaut), 'end' définit le terminateur de ligne (retour à la ligne "
                "par défaut). Les f-strings permettent un affichage formaté : f\"texte {variable}\".",

                "La fonction input() récupère la saisie utilisateur et retourne une chaîne. Les fonctions int() et float() convertissent "
                "les entrées textuelles en types numériques. La validation est nécessaire car input() retourne toujours une chaîne.",

                "Trois catégories d'opérateurs sont couvertes. Arithmétiques : +, -, *, /, // (division entière), % (modulo), ** (puissance). "
                "Comparaison : ==, !=, <, >, <=, >= (retournent des booléens). Logiques : and, or, not (combinent des expressions booléennes)."
            ],
            "label": "Référence des opérateurs",
            "items": [
                "Arithmétiques : +, -, *, /, //, %, **",
                "Comparaison : ==, !=, <, >, <=, >=",
                "Logiques : and, or, not"
            ]
        },
        {
            "id": 4,
            "title": "IV. Structures de contrôle et projet appliqué",
            "paragraphs": [
                "Les instructions conditionnelles contrôlent l'exécution selon des expressions booléennes. L'instruction if exécute un bloc "
                "lorsque la condition est True. La clause else fournit une alternative quand la condition est False. "
                "Le mot-clé elif permet d'enchaîner plusieurs conditions.",

                "Python utilise l'indentation pour définir les blocs de code. Une indentation cohérente de 4 espaces par niveau est requise. "
                "Les conditions sont combinées avec les opérateurs logiques (and, or) et peuvent être imbriquées.",

                "Le projet de fin de semaine est un classificateur de notes. Le programme reçoit un score numérique via input(), le convertit "
                "en entier, puis utilise des instructions if/elif/else enchaînées pour attribuer une lettre (A, B, C, D ou F) selon des seuils "
                "définis. Le résultat est affiché avec une f-string montrant le score et la note correspondante."
            ],
            "label": "Implémentation du projet",
            "items": [
                "input() reçoit le score numérique en chaîne",
                "int() convertit la chaîne en valeur entière",
                "if/elif/else évalue les seuils et attribue la note",
                "f-string affiche le score et la lettre de note"
            ]
        }
    ]

    # --- Header ---
    story.append(Paragraph(DATE_STR, s['date']))
    story.append(Spacer(1, 5))

    header_table = Table(
        [
            [Paragraph(MAIN_TITLE, s['h1'])],
            [Paragraph(f"Développeur : {DEVELOPER}", s['subheader'])]
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
    print(f"Historique d'activité généré : {FILE_NAME}")

if __name__ == "__main__":
    run_script()
