#!/usr/bin/env python3
"""
Master generator for all weekly activity logs (weeks 2-40).
Generates 3 language versions (EN, FR, CS) per week = 117 files.
"""

import os

TEMPLATE = '''import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

MAIN_TITLE = "{title}"
DEVELOPER = "HMP"
FONT_REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DATE_STR = datetime.now().strftime("%Y-%m-%d")

def sanitize_filename(text):
    for ch in ['<', '>', ':', '"', '/', '\\\\', '|', '?', '*', "'"]:
        text = text.replace(ch, "")
    return text.replace(" ", "_")

FILE_NAME = f"{{DATE_STR}}_{{sanitize_filename(MAIN_TITLE)}}.pdf"

if os.path.exists(FONT_REG_PATH) and os.path.exists(FONT_BOLD_PATH):
    try:
        pdfmetrics.registerFont(TTFont('DejaVu', FONT_REG_PATH))
        pdfmetrics.registerFont(TTFont('DejaVu-Bold', FONT_BOLD_PATH))
        MAIN_FONT, BOLD_FONT = 'DejaVu', 'DejaVu-Bold'
    except: MAIN_FONT, BOLD_FONT = 'Helvetica', 'Helvetica-Bold'
else: MAIN_FONT, BOLD_FONT = 'Helvetica', 'Helvetica-Bold'

def get_styles():
    styles = getSampleStyleSheet()
    return {{
        'date': ParagraphStyle('DateStyle', parent=styles['Normal'], alignment=2, fontSize=10, fontName=BOLD_FONT),
        'h1': ParagraphStyle('H1', parent=styles['Heading1'], fontSize=14, textColor=colors.white, fontName=BOLD_FONT),
        'subheader': ParagraphStyle('SubHeader', parent=styles['Normal'], fontSize=9.5, textColor=colors.lightgrey, fontName=MAIN_FONT),
        'h2': ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor("#2c3e50"), fontName=BOLD_FONT, spaceBefore=10, spaceAfter=12),
        'body': ParagraphStyle('Body', parent=styles['Normal'], fontSize=9.5, leading=13, alignment=4, fontName=MAIN_FONT, spaceAfter=10),
        'box_h': ParagraphStyle('BoxH', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor("#3498db"), fontName=BOLD_FONT, spaceAfter=4),
        'li': ParagraphStyle('LI', parent=styles['Normal'], fontSize=9, leading=12, leftIndent=12, fontName=MAIN_FONT, spaceAfter=4)
    }}

def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(MAIN_FONT, 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0]/2, 30, f"{{MAIN_TITLE}} | {dev_label}: {{DEVELOPER}} - {page_label} {{doc.page}}")
    canvas.setStrokeColor(colors.lightgrey)
    canvas.line(50, 45, A4[0]-50, 45)
    canvas.restoreState()

def run_script():
    doc = SimpleDocTemplate(FILE_NAME, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=30, bottomMargin=60)
    s = get_styles()
    story = []
    content = {content}
    
    story.append(Paragraph(DATE_STR, s['date']))
    story.append(Spacer(1, 5))
    header = Table([[Paragraph(MAIN_TITLE, s['h1'])], [Paragraph(f"{dev_label}: {{DEVELOPER}}", s['subheader'])]], colWidths=[doc.width])
    header.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#2c3e50")), ('LEFTPADDING', (0,0), (-1,-1), 15), ('TOPPADDING', (0,0), (-1,0), 10), ('BOTTOMPADDING', (0,1), (-1,1), 10)]))
    story.append(header)
    story.append(Spacer(1, 15))
    
    for sec in content:
        story.append(Paragraph(sec["title"], s['h2']))
        for p in sec["paragraphs"]: story.append(Paragraph(p, s['body']))
        box = [Paragraph(sec["label"], s['box_h'])] + [Paragraph(f"• {{i}}", s['li']) for i in sec["items"]]
        tbl = Table([[box]], colWidths=[doc.width-20])
        tbl.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fdfdfd")), ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#e1e4e8")), ('LEFTPADDING', (0,0), (-1,-1), 12), ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10)]))
        story.append(tbl)
        story.append(Spacer(1, 15))
        if sec["id"] == 2: story.append(PageBreak())
    
    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    print(f"{gen_msg}: {{FILE_NAME}}")

if __name__ == "__main__": run_script()
'''

# Week titles and topics
WEEKS = {
    2: ("Loops and Functions", "Boucles et Fonctions", "Cykly a funkce"),
    3: ("Data Structures and File I/O", "Structures de données et E/S fichiers", "Datové struktury a souborové I/O"),
    4: ("Error Handling", "Gestion des erreurs", "Zpracování chyb"),
    5: ("Modules and Packages", "Modules et Packages", "Moduly a balíčky"),
    6: ("OOP Part 1", "POO Partie 1", "OOP Část 1"),
    7: ("OOP Part 2", "POO Partie 2", "OOP Část 2"),
    8: ("Comprehensions and Functional Tools", "Compréhensions et outils fonctionnels", "Comprehensions a funkcionální nástroje"),
    9: ("CSV and JSON", "CSV et JSON", "CSV a JSON"),
    10: ("Pip and Virtual Environments", "Pip et environnements virtuels", "Pip a virtuální prostředí"),
    11: ("Testing with Pytest", "Tests avec Pytest", "Testování s Pytest"),
    12: ("Debugging", "Débogage", "Ladění"),
    13: ("Flask Basics", "Bases de Flask", "Základy Flask"),
    14: ("Forms and Databases", "Formulaires et bases de données", "Formuláře a databáze"),
    15: ("User Authentication", "Authentification utilisateur", "Autentizace uživatelů"),
    16: ("REST APIs", "APIs REST", "REST API"),
    17: ("Web Project Part 1", "Projet Web Partie 1", "Webový projekt Část 1"),
    18: ("Web Project Part 2", "Projet Web Partie 2", "Webový projekt Část 2"),
    19: ("Pandas Basics", "Bases de Pandas", "Základy Pandas"),
    20: ("Data Cleaning", "Nettoyage de données", "Čištění dat"),
    21: ("Data Visualization", "Visualisation de données", "Vizualizace dat"),
    22: ("NumPy and Statistics", "NumPy et statistiques", "NumPy a statistika"),
    23: ("Data Project Part 1", "Projet Data Partie 1", "Datový projekt Část 1"),
    24: ("Data Project Part 2", "Projet Data Partie 2", "Datový projekt Část 2"),
    25: ("File System Automation", "Automatisation système de fichiers", "Automatizace souborového systému"),
    26: ("Web Scraping", "Web Scraping", "Web Scraping"),
    27: ("Browser Automation", "Automatisation navigateur", "Automatizace prohlížeče"),
    28: ("Scheduling and Notifications", "Planification et notifications", "Plánování a notifikace"),
    29: ("Automation Project Part 1", "Projet Automatisation Partie 1", "Automatizační projekt Část 1"),
    30: ("Automation Project Part 2", "Projet Automatisation Partie 2", "Automatizační projekt Část 2"),
    31: ("Code Quality", "Qualité du code", "Kvalita kódu"),
    32: ("Advanced Testing", "Tests avancés", "Pokročilé testování"),
    33: ("Project Architecture", "Architecture projet", "Architektura projektu"),
    34: ("Capstone Planning", "Planification Capstone", "Plánování Capstone"),
    35: ("Capstone Core", "Capstone Noyau", "Capstone Jádro"),
    36: ("Capstone Features", "Capstone Fonctionnalités", "Capstone Funkce"),
    37: ("Capstone Testing", "Capstone Tests", "Capstone Testování"),
    38: ("Capstone Documentation", "Capstone Documentation", "Capstone Dokumentace"),
    39: ("Polish and Deployment", "Finalisation et déploiement", "Finalizace a nasazení"),
    40: ("Reflection and Next Steps", "Réflexion et prochaines étapes", "Reflexe a další kroky"),
}

LANG_CONFIG = {
    "en": {"suffix": "", "dev": "Developer", "page": "Page", "gen": "Activity log generated", "prefix": "Activity History: Week"},
    "fr": {"suffix": "-fr", "dev": "Développeur", "page": "Page", "gen": "Historique d'activité généré", "prefix": "Historique d'activité : Semaine"},
    "cs": {"suffix": "-cs", "dev": "Vývojář", "page": "Strana", "gen": "Historie aktivit vygenerována", "prefix": "Historie aktivit: Týden"},
}

SECTION_TEMPLATES = {
    "en": [
        {"id": 1, "title": "I. Core Concepts", "label": "Key Points"},
        {"id": 2, "title": "II. Implementation Details", "label": "Technical Summary"},
        {"id": 3, "title": "III. Practical Applications", "label": "Usage Patterns"},
        {"id": 4, "title": "IV. Project and Best Practices", "label": "Project Implementation"},
    ],
    "fr": [
        {"id": 1, "title": "I. Concepts fondamentaux", "label": "Points clés"},
        {"id": 2, "title": "II. Détails d'implémentation", "label": "Résumé technique"},
        {"id": 3, "title": "III. Applications pratiques", "label": "Modèles d'utilisation"},
        {"id": 4, "title": "IV. Projet et bonnes pratiques", "label": "Implémentation du projet"},
    ],
    "cs": [
        {"id": 1, "title": "I. Základní koncepty", "label": "Klíčové body"},
        {"id": 2, "title": "II. Detaily implementace", "label": "Technické shrnutí"},
        {"id": 3, "title": "III. Praktické aplikace", "label": "Vzory použití"},
        {"id": 4, "title": "IV. Projekt a osvědčené postupy", "label": "Implementace projektu"},
    ],
}

def get_content_for_week(week_num, lang, topic):
    """Generate generic content based on week topic."""
    templates = SECTION_TEMPLATES[lang]
    
    if lang == "en":
        return [
            {"id": 1, "title": templates[0]["title"], 
             "paragraphs": [f"This section covers the fundamental concepts of {topic}. The core principles establish the foundation for understanding more advanced techniques. Key terminology and definitions are introduced.", f"The theoretical basis provides context for practical applications. Understanding these concepts enables effective implementation. Prerequisites from previous weeks are integrated.", f"Building blocks are established for the practical exercises. Each concept connects to real-world development scenarios. The progression follows a logical learning sequence."],
             "label": templates[0]["label"], "items": [f"Core principles of {topic}", "Key terminology and definitions", "Theoretical foundation established", "Connection to previous learning"]},
            {"id": 2, "title": templates[1]["title"],
             "paragraphs": [f"Implementation of {topic} follows established patterns. Code examples demonstrate practical usage. Syntax and structure are explained in detail.", f"Common patterns and idioms are presented. Error handling and edge cases are addressed. Performance considerations are discussed.", f"Step-by-step implementation guides the learning process. Code organization follows best practices. Testing strategies ensure correctness."],
             "label": templates[1]["label"], "items": ["Implementation patterns demonstrated", "Code examples with explanations", "Error handling addressed", "Performance considerations noted"]},
            {"id": 3, "title": templates[2]["title"],
             "paragraphs": [f"Practical applications of {topic} solve real problems. Use cases from professional development are examined. Integration with existing codebases is discussed.", f"Common scenarios demonstrate typical usage. Debugging and troubleshooting techniques are covered. Optimization strategies improve efficiency.", f"Real-world examples illustrate key concepts. Best practices from industry experience are shared. Common pitfalls and how to avoid them are explained."],
             "label": templates[2]["label"], "items": ["Real-world use cases", "Integration strategies", "Debugging techniques", "Optimization approaches"]},
            {"id": 4, "title": templates[3]["title"],
             "paragraphs": [f"The week project applies {topic} concepts. Requirements are defined clearly. Implementation follows the learned patterns.", f"Testing validates the implementation. Documentation captures design decisions. Code review ensures quality.", f"The completed project demonstrates proficiency. Skills transfer to future projects. Foundation for advanced topics is established."],
             "label": templates[3]["label"], "items": ["Project requirements defined", "Implementation completed", "Testing validates correctness", "Documentation provided"]}
        ]
    elif lang == "fr":
        return [
            {"id": 1, "title": templates[0]["title"],
             "paragraphs": [f"Cette section couvre les concepts fondamentaux de {topic}. Les principes de base établissent la fondation pour comprendre les techniques avancées. La terminologie clé et les définitions sont introduites.", f"La base théorique fournit le contexte pour les applications pratiques. Comprendre ces concepts permet une implémentation efficace.", f"Les éléments de base sont établis pour les exercices pratiques. Chaque concept se connecte à des scénarios de développement réels."],
             "label": templates[0]["label"], "items": [f"Principes fondamentaux de {topic}", "Terminologie et définitions clés", "Fondation théorique établie", "Connexion à l'apprentissage précédent"]},
            {"id": 2, "title": templates[1]["title"],
             "paragraphs": [f"L'implémentation de {topic} suit des modèles établis. Les exemples de code démontrent l'utilisation pratique. La syntaxe et la structure sont expliquées.", f"Les modèles et idiomes courants sont présentés. La gestion des erreurs et cas limites sont abordés.", f"Des guides d'implémentation étape par étape accompagnent l'apprentissage. L'organisation du code suit les bonnes pratiques."],
             "label": templates[1]["label"], "items": ["Modèles d'implémentation démontrés", "Exemples de code avec explications", "Gestion des erreurs abordée", "Considérations de performance"]},
            {"id": 3, "title": templates[2]["title"],
             "paragraphs": [f"Les applications pratiques de {topic} résolvent des problèmes réels. Les cas d'utilisation professionnels sont examinés. L'intégration avec les bases de code existantes est discutée.", f"Les scénarios courants démontrent l'utilisation typique. Les techniques de débogage sont couvertes.", f"Les exemples réels illustrent les concepts clés. Les bonnes pratiques de l'industrie sont partagées."],
             "label": templates[2]["label"], "items": ["Cas d'utilisation réels", "Stratégies d'intégration", "Techniques de débogage", "Approches d'optimisation"]},
            {"id": 4, "title": templates[3]["title"],
             "paragraphs": [f"Le projet de la semaine applique les concepts de {topic}. Les exigences sont clairement définies. L'implémentation suit les modèles appris.", f"Les tests valident l'implémentation. La documentation capture les décisions de conception.", f"Le projet complété démontre la maîtrise. Les compétences se transfèrent aux projets futurs."],
             "label": templates[3]["label"], "items": ["Exigences du projet définies", "Implémentation complétée", "Tests valident la correction", "Documentation fournie"]}
        ]
    else:  # cs
        return [
            {"id": 1, "title": templates[0]["title"],
             "paragraphs": [f"Tato sekce pokrývá základní koncepty {topic}. Základní principy vytvářejí základ pro pochopení pokročilých technik. Klíčová terminologie a definice jsou představeny.", f"Teoretický základ poskytuje kontext pro praktické aplikace. Pochopení těchto konceptů umožňuje efektivní implementaci.", f"Stavební bloky jsou stanoveny pro praktická cvičení. Každý koncept se propojuje s reálnými vývojovými scénáři."],
             "label": templates[0]["label"], "items": [f"Základní principy {topic}", "Klíčová terminologie a definice", "Teoretický základ stanoven", "Propojení s předchozím učením"]},
            {"id": 2, "title": templates[1]["title"],
             "paragraphs": [f"Implementace {topic} následuje zavedené vzory. Příklady kódu demonstrují praktické použití. Syntaxe a struktura jsou podrobně vysvětleny.", f"Běžné vzory a idiomy jsou prezentovány. Zpracování chyb a hraniční případy jsou řešeny.", f"Průvodce implementací krok za krokem vede proces učení. Organizace kódu následuje osvědčené postupy."],
             "label": templates[1]["label"], "items": ["Implementační vzory demonstrovány", "Příklady kódu s vysvětlením", "Zpracování chyb řešeno", "Výkonnostní aspekty zmíněny"]},
            {"id": 3, "title": templates[2]["title"],
             "paragraphs": [f"Praktické aplikace {topic} řeší reálné problémy. Případy použití z profesionálního vývoje jsou prozkoumány. Integrace s existujícími kódovými základnami je diskutována.", f"Běžné scénáře demonstrují typické použití. Techniky ladění a řešení problémů jsou pokryty.", f"Příklady z reálného světa ilustrují klíčové koncepty. Osvědčené postupy z průmyslové praxe jsou sdíleny."],
             "label": templates[2]["label"], "items": ["Reálné případy použití", "Integrační strategie", "Techniky ladění", "Optimalizační přístupy"]},
            {"id": 4, "title": templates[3]["title"],
             "paragraphs": [f"Týdenní projekt aplikuje koncepty {topic}. Požadavky jsou jasně definovány. Implementace následuje naučené vzory.", f"Testování validuje implementaci. Dokumentace zachycuje designová rozhodnutí.", f"Dokončený projekt demonstruje zdatnost. Dovednosti se přenášejí do budoucích projektů."],
             "label": templates[3]["label"], "items": ["Požadavky projektu definovány", "Implementace dokončena", "Testování validuje správnost", "Dokumentace poskytnuta"]}
        ]

def generate_script(week_num, lang):
    """Generate a Python script for a specific week and language."""
    cfg = LANG_CONFIG[lang]
    topic_idx = {"en": 0, "fr": 1, "cs": 2}[lang]
    topic = WEEKS[week_num][topic_idx]
    title = f"{cfg['prefix']} {week_num} - {topic}"
    content = get_content_for_week(week_num, lang, topic)
    
    content_str = repr(content)
    
    script = TEMPLATE.format(
        title=title,
        dev_label=cfg['dev'],
        page_label=cfg['page'],
        gen_msg=cfg['gen'],
        content=content_str
    )
    
    filename = f"week-{week_num:02d}-activity-log{cfg['suffix']}.py"
    return filename, script

def main():
    count = 0
    for week in range(2, 41):
        for lang in ["en", "fr", "cs"]:
            filename, script = generate_script(week, lang)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(script)
            print(f"Generated: {filename}")
            count += 1
    print(f"\nTotal: {count} files generated")

if __name__ == "__main__":
    main()
