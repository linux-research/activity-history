import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

MAIN_TITLE = "Historie aktivit: Týden 27 - Automatizace prohlížeče"
DEVELOPER = "HMP"
FONT_REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DATE_STR = datetime.now().strftime("%Y-%m-%d")

def sanitize_filename(text):
    for ch in ['<', '>', ':', '"', '/', '\\', '|', '?', '*', "'"]:
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
    canvas.drawCentredString(A4[0]/2, 30, f"{MAIN_TITLE} | Vývojář: {DEVELOPER} - Strana {doc.page}")
    canvas.setStrokeColor(colors.lightgrey)
    canvas.line(50, 45, A4[0]-50, 45)
    canvas.restoreState()

def run_script():
    doc = SimpleDocTemplate(FILE_NAME, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=30, bottomMargin=60)
    s = get_styles()
    story = []
    content = [{'id': 1, 'title': 'I. Základní koncepty', 'paragraphs': ['Tato sekce pokrývá základní koncepty Automatizace prohlížeče. Základní principy vytvářejí základ pro pochopení pokročilých technik. Klíčová terminologie a definice jsou představeny.', 'Teoretický základ poskytuje kontext pro praktické aplikace. Pochopení těchto konceptů umožňuje efektivní implementaci.', 'Stavební bloky jsou stanoveny pro praktická cvičení. Každý koncept se propojuje s reálnými vývojovými scénáři.'], 'label': 'Klíčové body', 'items': ['Základní principy Automatizace prohlížeče', 'Klíčová terminologie a definice', 'Teoretický základ stanoven', 'Propojení s předchozím učením']}, {'id': 2, 'title': 'II. Detaily implementace', 'paragraphs': ['Implementace Automatizace prohlížeče následuje zavedené vzory. Příklady kódu demonstrují praktické použití. Syntaxe a struktura jsou podrobně vysvětleny.', 'Běžné vzory a idiomy jsou prezentovány. Zpracování chyb a hraniční případy jsou řešeny.', 'Průvodce implementací krok za krokem vede proces učení. Organizace kódu následuje osvědčené postupy.'], 'label': 'Technické shrnutí', 'items': ['Implementační vzory demonstrovány', 'Příklady kódu s vysvětlením', 'Zpracování chyb řešeno', 'Výkonnostní aspekty zmíněny']}, {'id': 3, 'title': 'III. Praktické aplikace', 'paragraphs': ['Praktické aplikace Automatizace prohlížeče řeší reálné problémy. Případy použití z profesionálního vývoje jsou prozkoumány. Integrace s existujícími kódovými základnami je diskutována.', 'Běžné scénáře demonstrují typické použití. Techniky ladění a řešení problémů jsou pokryty.', 'Příklady z reálného světa ilustrují klíčové koncepty. Osvědčené postupy z průmyslové praxe jsou sdíleny.'], 'label': 'Vzory použití', 'items': ['Reálné případy použití', 'Integrační strategie', 'Techniky ladění', 'Optimalizační přístupy']}, {'id': 4, 'title': 'IV. Projekt a osvědčené postupy', 'paragraphs': ['Týdenní projekt aplikuje koncepty Automatizace prohlížeče. Požadavky jsou jasně definovány. Implementace následuje naučené vzory.', 'Testování validuje implementaci. Dokumentace zachycuje designová rozhodnutí.', 'Dokončený projekt demonstruje zdatnost. Dovednosti se přenášejí do budoucích projektů.'], 'label': 'Implementace projektu', 'items': ['Požadavky projektu definovány', 'Implementace dokončena', 'Testování validuje správnost', 'Dokumentace poskytnuta']}]
    
    story.append(Paragraph(DATE_STR, s['date']))
    story.append(Spacer(1, 5))
    header = Table([[Paragraph(MAIN_TITLE, s['h1'])], [Paragraph(f"Vývojář: {DEVELOPER}", s['subheader'])]], colWidths=[doc.width])
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
    print(f"Historie aktivit vygenerována: {FILE_NAME}")

if __name__ == "__main__": run_script()
