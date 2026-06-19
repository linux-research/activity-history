import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

MAIN_TITLE = "Activity History: Week 6 - OOP Part 1"
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
    canvas.drawCentredString(A4[0]/2, 30, f"{MAIN_TITLE} | Developer: {DEVELOPER} - Page {doc.page}")
    canvas.setStrokeColor(colors.lightgrey)
    canvas.line(50, 45, A4[0]-50, 45)
    canvas.restoreState()

def run_script():
    doc = SimpleDocTemplate(FILE_NAME, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=30, bottomMargin=60)
    s = get_styles()
    story = []
    content = [{'id': 1, 'title': 'I. Core Concepts', 'paragraphs': ['This section covers the fundamental concepts of OOP Part 1. The core principles establish the foundation for understanding more advanced techniques. Key terminology and definitions are introduced.', 'The theoretical basis provides context for practical applications. Understanding these concepts enables effective implementation. Prerequisites from previous weeks are integrated.', 'Building blocks are established for the practical exercises. Each concept connects to real-world development scenarios. The progression follows a logical learning sequence.'], 'label': 'Key Points', 'items': ['Core principles of OOP Part 1', 'Key terminology and definitions', 'Theoretical foundation established', 'Connection to previous learning']}, {'id': 2, 'title': 'II. Implementation Details', 'paragraphs': ['Implementation of OOP Part 1 follows established patterns. Code examples demonstrate practical usage. Syntax and structure are explained in detail.', 'Common patterns and idioms are presented. Error handling and edge cases are addressed. Performance considerations are discussed.', 'Step-by-step implementation guides the learning process. Code organization follows best practices. Testing strategies ensure correctness.'], 'label': 'Technical Summary', 'items': ['Implementation patterns demonstrated', 'Code examples with explanations', 'Error handling addressed', 'Performance considerations noted']}, {'id': 3, 'title': 'III. Practical Applications', 'paragraphs': ['Practical applications of OOP Part 1 solve real problems. Use cases from professional development are examined. Integration with existing codebases is discussed.', 'Common scenarios demonstrate typical usage. Debugging and troubleshooting techniques are covered. Optimization strategies improve efficiency.', 'Real-world examples illustrate key concepts. Best practices from industry experience are shared. Common pitfalls and how to avoid them are explained.'], 'label': 'Usage Patterns', 'items': ['Real-world use cases', 'Integration strategies', 'Debugging techniques', 'Optimization approaches']}, {'id': 4, 'title': 'IV. Project and Best Practices', 'paragraphs': ['The week project applies OOP Part 1 concepts. Requirements are defined clearly. Implementation follows the learned patterns.', 'Testing validates the implementation. Documentation captures design decisions. Code review ensures quality.', 'The completed project demonstrates proficiency. Skills transfer to future projects. Foundation for advanced topics is established.'], 'label': 'Project Implementation', 'items': ['Project requirements defined', 'Implementation completed', 'Testing validates correctness', 'Documentation provided']}]
    
    story.append(Paragraph(DATE_STR, s['date']))
    story.append(Spacer(1, 5))
    header = Table([[Paragraph(MAIN_TITLE, s['h1'])], [Paragraph(f"Developer: {DEVELOPER}", s['subheader'])]], colWidths=[doc.width])
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
    print(f"Activity log generated: {FILE_NAME}")

if __name__ == "__main__": run_script()
