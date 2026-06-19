import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

MAIN_TITLE = "Historique d'activité : Semaine 23 - Projet Data Partie 1"
DEVELOPER = "HMP"
FONT_REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DATE_STR = datetime.now().strftime("%Y-%m-%d")

def sanitize_filename(text):
    for ch in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
        text = text.replace(ch, "")
    return text.replace(" ", "_")

FILE_NAME = f"{DATE_STR}_{sanitize_filename(MAIN_TITLE)}.pdf"

if os.path.exists(FONT_REG_PATH) and os.path.exists(FONT_BOLD_PATH):
    try:
        pdfmetrics.registerFont(TTFont('DejaVu', FONT_REG_PATH))
        pdfmetrics.registerFont(TTFont('DejaVu-Bold', FONT_BOLD_PATH))
        MAIN_FONT, BOLD_FONT = 'DejaVu', 'DejaVu-Bold'
    except: MAIN_FONT, BOLD_FONT = 'Helvetica', 'Helvetica-Bold'
else: MAIN_FONT, BOLD_FONT = 'Helvetica', 'Helvetica-Bold'

def get_styles():
    styles = getSampleStyleSheet()
    return {
        'date': ParagraphStyle('DateStyle', parent=styles['Normal'], alignment=2, fontSize=10, fontName=BOLD_FONT),
        'h1': ParagraphStyle('H1', parent=styles['Heading1'], fontSize=14, textColor=colors.white, fontName=BOLD_FONT),
        'subheader': ParagraphStyle('SubHeader', parent=styles['Normal'], fontSize=9.5, textColor=colors.lightgrey, fontName=MAIN_FONT),
        'h2': ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor("#2c3e50"), fontName=BOLD_FONT, spaceBefore=10, spaceAfter=12),
        'body': ParagraphStyle('Body', parent=styles['Normal'], fontSize=9.5, leading=13, alignment=4, fontName=MAIN_FONT, spaceAfter=10),
        'box_h': ParagraphStyle('BoxH', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor("#3498db"), fontName=BOLD_FONT, spaceAfter=4),
        'li': ParagraphStyle('LI', parent=styles['Normal'], fontSize=9, leading=12, leftIndent=12, fontName=MAIN_FONT, spaceAfter=4)
    }

def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(MAIN_FONT, 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0]/2, 30, f"{MAIN_TITLE} | Développeur: {DEVELOPER} - Page {doc.page}")
    canvas.setStrokeColor(colors.lightgrey)
    canvas.line(50, 45, A4[0]-50, 45)
    canvas.restoreState()

def run_script():
    doc = SimpleDocTemplate(FILE_NAME, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=30, bottomMargin=60)
    s = get_styles()
    story = []
    content = [{'id': 1, 'title': 'I. Concepts fondamentaux', 'paragraphs': ['Cette section couvre les concepts fondamentaux de Projet Data Partie 1. Les principes de base établissent la fondation pour comprendre les techniques avancées. La terminologie clé et les définitions sont introduites.', 'La base théorique fournit le contexte pour les applications pratiques. Comprendre ces concepts permet une implémentation efficace.', 'Les éléments de base sont établis pour les exercices pratiques. Chaque concept se connecte à des scénarios de développement réels.'], 'label': 'Points clés', 'items': ['Principes fondamentaux de Projet Data Partie 1', 'Terminologie et définitions clés', 'Fondation théorique établie', "Connexion à l'apprentissage précédent"]}, {'id': 2, 'title': "II. Détails d'implémentation", 'paragraphs': ["L'implémentation de Projet Data Partie 1 suit des modèles établis. Les exemples de code démontrent l'utilisation pratique. La syntaxe et la structure sont expliquées.", 'Les modèles et idiomes courants sont présentés. La gestion des erreurs et cas limites sont abordés.', "Des guides d'implémentation étape par étape accompagnent l'apprentissage. L'organisation du code suit les bonnes pratiques."], 'label': 'Résumé technique', 'items': ["Modèles d'implémentation démontrés", 'Exemples de code avec explications', 'Gestion des erreurs abordée', 'Considérations de performance']}, {'id': 3, 'title': 'III. Applications pratiques', 'paragraphs': ["Les applications pratiques de Projet Data Partie 1 résolvent des problèmes réels. Les cas d'utilisation professionnels sont examinés. L'intégration avec les bases de code existantes est discutée.", "Les scénarios courants démontrent l'utilisation typique. Les techniques de débogage sont couvertes.", "Les exemples réels illustrent les concepts clés. Les bonnes pratiques de l'industrie sont partagées."], 'label': "Modèles d'utilisation", 'items': ["Cas d'utilisation réels", "Stratégies d'intégration", 'Techniques de débogage', "Approches d'optimisation"]}, {'id': 4, 'title': 'IV. Projet et bonnes pratiques', 'paragraphs': ["Le projet de la semaine applique les concepts de Projet Data Partie 1. Les exigences sont clairement définies. L'implémentation suit les modèles appris.", "Les tests valident l'implémentation. La documentation capture les décisions de conception.", 'Le projet complété démontre la maîtrise. Les compétences se transfèrent aux projets futurs.'], 'label': 'Implémentation du projet', 'items': ['Exigences du projet définies', 'Implémentation complétée', 'Tests valident la correction', 'Documentation fournie']}]
    
    story.append(Paragraph(DATE_STR, s['date']))
    story.append(Spacer(1, 5))
    header = Table([[Paragraph(MAIN_TITLE, s['h1'])], [Paragraph(f"Développeur: {DEVELOPER}", s['subheader'])]], colWidths=[doc.width])
    header.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#2c3e50")), ('LEFTPADDING', (0,0), (-1,-1), 15), ('TOPPADDING', (0,0), (-1,0), 10), ('BOTTOMPADDING', (0,1), (-1,1), 10)]))
    story.append(header)
    story.append(Spacer(1, 15))
    
    for sec in content:
        story.append(Paragraph(sec["title"], s['h2']))
        for p in sec["paragraphs"]: story.append(Paragraph(p, s['body']))
        box = [Paragraph(sec["label"], s['box_h'])] + [Paragraph(f"• {i}", s['li']) for i in sec["items"]]
        tbl = Table([[box]], colWidths=[doc.width-20])
        tbl.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fdfdfd")), ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#e1e4e8")), ('LEFTPADDING', (0,0), (-1,-1), 12), ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10)]))
        story.append(tbl)
        story.append(Spacer(1, 15))
        if sec["id"] == 2: story.append(PageBreak())
    
    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    print(f"Historique d'activité généré: {FILE_NAME}")

if __name__ == "__main__": run_script()
