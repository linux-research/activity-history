#!/usr/bin/env python3
"""
Generator script for all weekly activity log Python files (weeks 2-40).
Creates 3 language versions (EN, FR, CS) per week.
"""

import os

# Base template for activity log scripts
TEMPLATE = '''import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- 1. CONFIGURATION ---
MAIN_TITLE = "{main_title}"
DEVELOPER = "HMP"

FONT_REG_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

DATE_STR = datetime.now().strftime("%Y-%m-%d")

def sanitize_filename(text):
    forbidden = ['<', '>', ':', '"', '/', '\\\\', '|', '?', '*']
    for ch in forbidden:
        text = text.replace(ch, "")
    return text.replace(" ", "_").replace("'", "")

safe_title = sanitize_filename(MAIN_TITLE)
FILE_NAME = f"{{DATE_STR}}_{{safe_title}}.pdf"

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
    return {{
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
    }}

# --- 4. FOOTER ---
def draw_footer(canvas, doc):
    canvas.saveState()
    footer_text = f"{{MAIN_TITLE}} | {developer_label}: {{DEVELOPER}} - {page_label} {{doc.page}}"
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

    content_map = {content_map}

    # --- Header ---
    story.append(Paragraph(DATE_STR, s['date']))
    story.append(Spacer(1, 5))

    header_table = Table(
        [
            [Paragraph(MAIN_TITLE, s['h1'])],
            [Paragraph(f"{developer_label}: {{DEVELOPER}}", s['subheader'])]
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

    for section in content_map:
        story.append(Paragraph(section["title"], s['h2']))

        for p in section["paragraphs"]:
            story.append(Paragraph(p, s['body']))

        box_content = [Paragraph(section["label"], s['box_h'])] + [
            Paragraph(f"• {{i}}", s['li']) for i in section["items"]
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

        if section["id"] == 2:
            story.append(PageBreak())

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    print(f"{generated_msg}: {{FILE_NAME}}")

if __name__ == "__main__":
    run_script()
'''

# Week content definitions for all weeks 2-40
WEEKS_CONTENT = {
    2: {
        "en": {
            "title": "Activity History: Week 2 - Loops and Functions",
            "developer_label": "Developer",
            "page_label": "Page",
            "generated_msg": "Activity log generated",
            "sections": [
                {
                    "id": 1,
                    "title": "I. For Loops and Iteration",
                    "paragraphs": [
                        "The for loop iterates over sequences such as lists, strings, and range objects. The syntax uses the 'in' keyword to traverse each element. The range() function generates numeric sequences with configurable start, stop, and step parameters.",
                        "The enumerate() function provides both index and value during iteration. This eliminates manual counter management. Loop variables exist only within the loop scope and are reassigned on each iteration.",
                        "Nested loops enable iteration over multi-dimensional structures. The inner loop completes all iterations for each iteration of the outer loop. This pattern is used for matrix operations and pattern generation."
                    ],
                    "label": "For Loop Patterns",
                    "items": [
                        "for item in sequence: iterates over each element",
                        "range(start, stop, step) generates number sequences",
                        "enumerate() provides index-value pairs",
                        "Nested loops for multi-dimensional iteration"
                    ]
                },
                {
                    "id": 2,
                    "title": "II. While Loops and Control Flow",
                    "paragraphs": [
                        "The while loop executes a block repeatedly while its condition evaluates to True. The condition is checked before each iteration. A counter or state variable must be updated within the loop to prevent infinite execution.",
                        "The break statement exits the loop immediately, regardless of the condition. The continue statement skips the remaining code in the current iteration and proceeds to the next. These statements provide fine-grained control over loop execution.",
                        "The else clause on loops executes when the loop completes without encountering a break statement. This pattern is useful for search operations where the else block handles the not-found case."
                    ],
                    "label": "Loop Control",
                    "items": [
                        "while condition: repeats until condition is False",
                        "break exits the loop immediately",
                        "continue skips to the next iteration",
                        "else clause runs if no break occurred"
                    ]
                },
                {
                    "id": 3,
                    "title": "III. Function Definition and Parameters",
                    "paragraphs": [
                        "Functions are defined using the def keyword followed by the function name and parameters in parentheses. The function body is indented. Functions encapsulate reusable logic and improve code organization.",
                        "Parameters receive values when the function is called. Default parameter values are specified with the equals sign. Keyword arguments allow passing values by parameter name, independent of position.",
                        "The return statement sends a value back to the caller and terminates function execution. Multiple values can be returned as a tuple. Functions without an explicit return statement return None."
                    ],
                    "label": "Function Syntax",
                    "items": [
                        "def function_name(parameters): defines a function",
                        "Default values: def func(x, y=10)",
                        "Keyword arguments: func(y=5, x=3)",
                        "return value sends result to caller"
                    ]
                },
                {
                    "id": 4,
                    "title": "IV. Variable Scope and Project",
                    "paragraphs": [
                        "Variables defined inside a function have local scope and exist only during function execution. Variables defined outside functions have global scope. Local variables with the same name as global variables shadow the global ones within the function.",
                        "The global keyword allows modification of global variables from within a function. However, passing values as parameters and returning results is the preferred approach. This practice improves code clarity and testability.",
                        "The week project implements a multiplication table generator. The program defines functions to generate and display tables for a given number. Nested loops produce the table rows, and formatted output aligns the columns."
                    ],
                    "label": "Project Implementation",
                    "items": [
                        "Local variables exist within function scope only",
                        "Global variables accessible throughout module",
                        "Nested for loops generate multiplication grid",
                        "Formatted output aligns table columns"
                    ]
                }
            ]
        },
        "fr": {
            "title": "Historique d'activité : Semaine 2 - Boucles et Fonctions",
            "developer_label": "Développeur",
            "page_label": "Page",
            "generated_msg": "Historique d'activité généré",
            "sections": [
                {
                    "id": 1,
                    "title": "I. Boucles for et itération",
                    "paragraphs": [
                        "La boucle for parcourt des séquences telles que les listes, chaînes et objets range. La syntaxe utilise le mot-clé 'in' pour traverser chaque élément. La fonction range() génère des séquences numériques avec des paramètres start, stop et step configurables.",
                        "La fonction enumerate() fournit à la fois l'index et la valeur lors de l'itération. Cela élimine la gestion manuelle des compteurs. Les variables de boucle n'existent que dans la portée de la boucle et sont réassignées à chaque itération.",
                        "Les boucles imbriquées permettent l'itération sur des structures multidimensionnelles. La boucle interne complète toutes ses itérations pour chaque itération de la boucle externe. Ce modèle est utilisé pour les opérations matricielles."
                    ],
                    "label": "Modèles de boucle for",
                    "items": [
                        "for item in sequence: parcourt chaque élément",
                        "range(start, stop, step) génère des séquences",
                        "enumerate() fournit des paires index-valeur",
                        "Boucles imbriquées pour itération multidimensionnelle"
                    ]
                },
                {
                    "id": 2,
                    "title": "II. Boucles while et contrôle de flux",
                    "paragraphs": [
                        "La boucle while exécute un bloc de manière répétée tant que sa condition est True. La condition est vérifiée avant chaque itération. Une variable compteur ou d'état doit être mise à jour dans la boucle pour éviter une exécution infinie.",
                        "L'instruction break quitte la boucle immédiatement, quelle que soit la condition. L'instruction continue saute le code restant de l'itération en cours et passe à la suivante. Ces instructions offrent un contrôle précis sur l'exécution.",
                        "La clause else sur les boucles s'exécute lorsque la boucle se termine sans rencontrer de break. Ce modèle est utile pour les opérations de recherche où le bloc else gère le cas non trouvé."
                    ],
                    "label": "Contrôle de boucle",
                    "items": [
                        "while condition: répète jusqu'à condition False",
                        "break quitte la boucle immédiatement",
                        "continue passe à l'itération suivante",
                        "Clause else si aucun break n'est survenu"
                    ]
                },
                {
                    "id": 3,
                    "title": "III. Définition de fonctions et paramètres",
                    "paragraphs": [
                        "Les fonctions sont définies avec le mot-clé def suivi du nom et des paramètres entre parenthèses. Le corps de la fonction est indenté. Les fonctions encapsulent une logique réutilisable et améliorent l'organisation du code.",
                        "Les paramètres reçoivent des valeurs lors de l'appel de la fonction. Les valeurs par défaut sont spécifiées avec le signe égal. Les arguments nommés permettent de passer des valeurs par nom de paramètre, indépendamment de la position.",
                        "L'instruction return renvoie une valeur à l'appelant et termine l'exécution de la fonction. Plusieurs valeurs peuvent être retournées sous forme de tuple. Les fonctions sans return explicite retournent None."
                    ],
                    "label": "Syntaxe des fonctions",
                    "items": [
                        "def nom_fonction(paramètres): définit une fonction",
                        "Valeurs par défaut : def func(x, y=10)",
                        "Arguments nommés : func(y=5, x=3)",
                        "return valeur envoie le résultat à l'appelant"
                    ]
                },
                {
                    "id": 4,
                    "title": "IV. Portée des variables et projet",
                    "paragraphs": [
                        "Les variables définies dans une fonction ont une portée locale et n'existent que pendant l'exécution. Les variables définies hors des fonctions ont une portée globale. Les variables locales de même nom masquent les globales dans la fonction.",
                        "Le mot-clé global permet de modifier les variables globales depuis une fonction. Cependant, passer des valeurs en paramètres et retourner des résultats est l'approche préférée. Cette pratique améliore la clarté et la testabilité.",
                        "Le projet de la semaine implémente un générateur de table de multiplication. Le programme définit des fonctions pour générer et afficher les tables. Les boucles imbriquées produisent les lignes, et la sortie formatée aligne les colonnes."
                    ],
                    "label": "Implémentation du projet",
                    "items": [
                        "Variables locales dans la portée de fonction",
                        "Variables globales accessibles dans tout le module",
                        "Boucles for imbriquées génèrent la grille",
                        "Sortie formatée aligne les colonnes"
                    ]
                }
            ]
        },
        "cs": {
            "title": "Historie aktivit: Týden 2 - Cykly a funkce",
            "developer_label": "Vývojář",
            "page_label": "Strana",
            "generated_msg": "Historie aktivit vygenerována",
            "sections": [
                {
                    "id": 1,
                    "title": "I. Cykly for a iterace",
                    "paragraphs": [
                        "Cyklus for iteruje přes sekvence jako seznamy, řetězce a objekty range. Syntaxe používá klíčové slovo 'in' k procházení každého prvku. Funkce range() generuje číselné sekvence s konfigurovatelnými parametry start, stop a step.",
                        "Funkce enumerate() poskytuje index i hodnotu během iterace. To eliminuje ruční správu počítadel. Proměnné cyklu existují pouze v rozsahu cyklu a jsou přeřazeny při každé iteraci.",
                        "Vnořené cykly umožňují iteraci přes vícerozměrné struktury. Vnitřní cyklus dokončí všechny iterace pro každou iteraci vnějšího cyklu. Tento vzor se používá pro maticové operace a generování vzorů."
                    ],
                    "label": "Vzory cyklu for",
                    "items": [
                        "for item in sequence: iteruje přes každý prvek",
                        "range(start, stop, step) generuje sekvence čísel",
                        "enumerate() poskytuje páry index-hodnota",
                        "Vnořené cykly pro vícerozměrnou iteraci"
                    ]
                },
                {
                    "id": 2,
                    "title": "II. Cykly while a řízení toku",
                    "paragraphs": [
                        "Cyklus while opakovaně vykonává blok, dokud je jeho podmínka True. Podmínka je kontrolována před každou iterací. Počítadlo nebo stavová proměnná musí být aktualizována v cyklu, aby se zabránilo nekonečnému běhu.",
                        "Příkaz break okamžitě ukončí cyklus bez ohledu na podmínku. Příkaz continue přeskočí zbývající kód v aktuální iteraci a pokračuje další. Tyto příkazy poskytují jemnou kontrolu nad vykonáváním cyklu.",
                        "Klauzule else u cyklů se vykoná, když cyklus skončí bez příkazu break. Tento vzor je užitečný pro vyhledávací operace, kde blok else zpracovává případ nenalezení."
                    ],
                    "label": "Řízení cyklu",
                    "items": [
                        "while podmínka: opakuje dokud podmínka není False",
                        "break okamžitě ukončí cyklus",
                        "continue přeskočí na další iteraci",
                        "Klauzule else běží pokud nenastal break"
                    ]
                },
                {
                    "id": 3,
                    "title": "III. Definice funkcí a parametry",
                    "paragraphs": [
                        "Funkce se definují pomocí klíčového slova def následovaného názvem funkce a parametry v závorkách. Tělo funkce je odsazené. Funkce zapouzdřují znovupoužitelnou logiku a zlepšují organizaci kódu.",
                        "Parametry přijímají hodnoty při volání funkce. Výchozí hodnoty parametrů se zadávají znakem rovná se. Pojmenované argumenty umožňují předávat hodnoty podle názvu parametru, nezávisle na pozici.",
                        "Příkaz return odesílá hodnotu zpět volajícímu a ukončuje vykonávání funkce. Více hodnot lze vrátit jako tuple. Funkce bez explicitního return vracejí None."
                    ],
                    "label": "Syntaxe funkcí",
                    "items": [
                        "def název_funkce(parametry): definuje funkci",
                        "Výchozí hodnoty: def func(x, y=10)",
                        "Pojmenované argumenty: func(y=5, x=3)",
                        "return hodnota odesílá výsledek volajícímu"
                    ]
                },
                {
                    "id": 4,
                    "title": "IV. Rozsah proměnných a projekt",
                    "paragraphs": [
                        "Proměnné definované uvnitř funkce mají lokální rozsah a existují pouze během vykonávání funkce. Proměnné definované mimo funkce mají globální rozsah. Lokální proměnné se stejným názvem zastíní globální v rámci funkce.",
                        "Klíčové slovo global umožňuje modifikaci globálních proměnných zevnitř funkce. Nicméně předávání hodnot jako parametrů a vracení výsledků je preferovaný přístup. Tato praxe zlepšuje čitelnost a testovatelnost.",
                        "Týdenní projekt implementuje generátor násobilky. Program definuje funkce pro generování a zobrazení tabulek. Vnořené cykly vytvářejí řádky tabulky a formátovaný výstup zarovnává sloupce."
                    ],
                    "label": "Implementace projektu",
                    "items": [
                        "Lokální proměnné existují v rozsahu funkce",
                        "Globální proměnné přístupné v celém modulu",
                        "Vnořené cykly for generují mřížku násobilky",
                        "Formátovaný výstup zarovnává sloupce"
                    ]
                }
            ]
        }
    },
    3: {
        "en": {
            "title": "Activity History: Week 3 - Data Structures and File I/O",
            "developer_label": "Developer",
            "page_label": "Page",
            "generated_msg": "Activity log generated",
            "sections": [
                {
                    "id": 1,
                    "title": "I. Lists and Tuples",
                    "paragraphs": [
                        "Lists are mutable ordered sequences created with square brackets. Elements are accessed by index starting at 0. Negative indices access elements from the end. The append(), insert(), and extend() methods modify lists in place.",
                        "List slicing extracts subsequences using [start:stop:step] syntax. The slice returns a new list without modifying the original. Common operations include len() for length, in for membership testing, and sorted() for ordering.",
                        "Tuples are immutable sequences created with parentheses or comma separation. They cannot be modified after creation. Tuples are used for fixed collections and as dictionary keys. Tuple unpacking assigns elements to multiple variables."
                    ],
                    "label": "Sequence Operations",
                    "items": [
                        "list[index] accesses element, list[start:stop] slices",
                        "append(), insert(), remove(), pop() modify lists",
                        "Tuples are immutable: created once, never changed",
                        "Unpacking: a, b, c = (1, 2, 3)"
                    ]
                },
                {
                    "id": 2,
                    "title": "II. Dictionaries and Sets",
                    "paragraphs": [
                        "Dictionaries store key-value pairs in curly braces. Keys must be immutable (strings, numbers, tuples). Values are accessed using bracket notation with the key. The get() method provides a default value for missing keys.",
                        "Dictionary methods include keys(), values(), and items() for iteration. The update() method merges dictionaries. Dictionary comprehensions create dictionaries inline. Keys are unique; assigning to an existing key overwrites the value.",
                        "Sets are unordered collections of unique elements. Created with curly braces or set(). Set operations include union (|), intersection (&), and difference (-). Sets are useful for removing duplicates and membership testing."
                    ],
                    "label": "Mapping and Set Types",
                    "items": [
                        "dict[key] = value assigns, dict.get(key, default) retrieves",
                        "keys(), values(), items() for dictionary iteration",
                        "Sets contain unique elements only, unordered",
                        "Set operations: union, intersection, difference"
                    ]
                },
                {
                    "id": 3,
                    "title": "III. String Methods and Formatting",
                    "paragraphs": [
                        "Strings are immutable sequences of characters. Methods like upper(), lower(), strip(), and replace() return new strings. The split() method divides strings into lists; join() combines list elements into strings.",
                        "String formatting uses f-strings for variable interpolation. Format specifiers control precision, width, and alignment. The format() method provides an alternative approach. String methods can be chained for sequential operations.",
                        "String searching uses find() and index() for locating substrings. The count() method tallies occurrences. Boolean methods startswith() and endswith() check prefixes and suffixes. Regular expressions provide advanced pattern matching."
                    ],
                    "label": "String Operations",
                    "items": [
                        "split(), join(), strip() for string manipulation",
                        "f-strings: f\"{value:.2f}\" for formatting",
                        "find(), count(), replace() for searching and replacing",
                        "Methods return new strings; originals unchanged"
                    ]
                },
                {
                    "id": 4,
                    "title": "IV. File Input/Output and Project",
                    "paragraphs": [
                        "Files are opened using open() with a mode: 'r' for read, 'w' for write, 'a' for append. The with statement ensures proper file closure. The read() method returns entire contents; readlines() returns a list of lines.",
                        "Writing uses write() for strings and writelines() for lists. The 'w' mode overwrites existing files; 'a' mode appends. Text mode is default; binary mode uses 'rb' or 'wb'. File paths can be absolute or relative.",
                        "The week project implements a contact manager. The program stores contacts in a text file with structured format. Functions handle reading, writing, searching, and displaying contacts. Data persistence maintains contacts between sessions."
                    ],
                    "label": "Project Implementation",
                    "items": [
                        "open(path, mode) opens file, with ensures closure",
                        "read(), readline(), readlines() for reading",
                        "write(), writelines() for writing content",
                        "Contact data persisted to text file between runs"
                    ]
                }
            ]
        },
        "fr": {
            "title": "Historique d'activité : Semaine 3 - Structures de données et E/S fichiers",
            "developer_label": "Développeur",
            "page_label": "Page",
            "generated_msg": "Historique d'activité généré",
            "sections": [
                {
                    "id": 1,
                    "title": "I. Listes et tuples",
                    "paragraphs": [
                        "Les listes sont des séquences ordonnées mutables créées avec des crochets. Les éléments sont accessibles par index à partir de 0. Les indices négatifs accèdent aux éléments depuis la fin. Les méthodes append(), insert() et extend() modifient les listes.",
                        "Le découpage de liste extrait des sous-séquences avec la syntaxe [start:stop:step]. La tranche retourne une nouvelle liste sans modifier l'originale. Les opérations courantes incluent len(), in pour le test d'appartenance, et sorted().",
                        "Les tuples sont des séquences immuables créées avec des parenthèses ou par séparation de virgules. Ils ne peuvent pas être modifiés après création. Les tuples servent pour les collections fixes et comme clés de dictionnaire."
                    ],
                    "label": "Opérations sur séquences",
                    "items": [
                        "list[index] accède, list[start:stop] découpe",
                        "append(), insert(), remove(), pop() modifient",
                        "Les tuples sont immuables : créés une fois",
                        "Déballage : a, b, c = (1, 2, 3)"
                    ]
                },
                {
                    "id": 2,
                    "title": "II. Dictionnaires et ensembles",
                    "paragraphs": [
                        "Les dictionnaires stockent des paires clé-valeur entre accolades. Les clés doivent être immuables (chaînes, nombres, tuples). Les valeurs sont accessibles avec la notation entre crochets. La méthode get() fournit une valeur par défaut.",
                        "Les méthodes de dictionnaire incluent keys(), values() et items() pour l'itération. La méthode update() fusionne les dictionnaires. Les compréhensions de dictionnaire créent des dictionnaires en ligne. Les clés sont uniques.",
                        "Les ensembles sont des collections non ordonnées d'éléments uniques. Créés avec des accolades ou set(). Les opérations incluent union (|), intersection (&) et différence (-). Utiles pour éliminer les doublons."
                    ],
                    "label": "Types mapping et ensemble",
                    "items": [
                        "dict[clé] = valeur assigne, dict.get(clé, défaut)",
                        "keys(), values(), items() pour itération",
                        "Les ensembles contiennent des éléments uniques",
                        "Opérations : union, intersection, différence"
                    ]
                },
                {
                    "id": 3,
                    "title": "III. Méthodes de chaînes et formatage",
                    "paragraphs": [
                        "Les chaînes sont des séquences immuables de caractères. Les méthodes upper(), lower(), strip() et replace() retournent de nouvelles chaînes. La méthode split() divise en listes ; join() combine les éléments.",
                        "Le formatage utilise les f-strings pour l'interpolation de variables. Les spécificateurs de format contrôlent la précision, la largeur et l'alignement. La méthode format() offre une approche alternative.",
                        "La recherche dans les chaînes utilise find() et index() pour localiser les sous-chaînes. La méthode count() compte les occurrences. Les méthodes booléennes startswith() et endswith() vérifient préfixes et suffixes."
                    ],
                    "label": "Opérations sur chaînes",
                    "items": [
                        "split(), join(), strip() pour manipulation",
                        "f-strings : f\"{valeur:.2f}\" pour formatage",
                        "find(), count(), replace() recherche et remplace",
                        "Les méthodes retournent de nouvelles chaînes"
                    ]
                },
                {
                    "id": 4,
                    "title": "IV. Entrées/sorties fichiers et projet",
                    "paragraphs": [
                        "Les fichiers s'ouvrent avec open() et un mode : 'r' lecture, 'w' écriture, 'a' ajout. L'instruction with assure la fermeture. La méthode read() retourne tout le contenu ; readlines() retourne une liste de lignes.",
                        "L'écriture utilise write() pour les chaînes et writelines() pour les listes. Le mode 'w' écrase les fichiers existants ; 'a' ajoute. Le mode texte est par défaut ; le mode binaire utilise 'rb' ou 'wb'.",
                        "Le projet de la semaine implémente un gestionnaire de contacts. Le programme stocke les contacts dans un fichier texte structuré. Les fonctions gèrent lecture, écriture, recherche et affichage. La persistance maintient les données entre sessions."
                    ],
                    "label": "Implémentation du projet",
                    "items": [
                        "open(chemin, mode) ouvre, with assure fermeture",
                        "read(), readline(), readlines() pour lecture",
                        "write(), writelines() pour écriture",
                        "Données contacts persistées dans fichier texte"
                    ]
                }
            ]
        },
        "cs": {
            "title": "Historie aktivit: Týden 3 - Datové struktury a souborové I/O",
            "developer_label": "Vývojář",
            "page_label": "Strana",
            "generated_msg": "Historie aktivit vygenerována",
            "sections": [
                {
                    "id": 1,
                    "title": "I. Seznamy a n-tice",
                    "paragraphs": [
                        "Seznamy jsou měnitelné uspořádané sekvence vytvořené hranatými závorkami. Prvky jsou přístupné indexem od 0. Záporné indexy přistupují od konce. Metody append(), insert() a extend() modifikují seznamy na místě.",
                        "Řezání seznamu extrahuje podsekvence syntaxí [start:stop:step]. Řez vrací nový seznam bez modifikace originálu. Běžné operace zahrnují len() pro délku, in pro test členství a sorted() pro řazení.",
                        "N-tice jsou neměnitelné sekvence vytvořené závorkami nebo oddělením čárkami. Nelze je po vytvoření měnit. N-tice se používají pro fixní kolekce a jako klíče slovníku. Rozbalení n-tice přiřadí prvky více proměnným."
                    ],
                    "label": "Operace se sekvencemi",
                    "items": [
                        "list[index] přistupuje, list[start:stop] řeže",
                        "append(), insert(), remove(), pop() modifikují",
                        "N-tice jsou neměnitelné: vytvořeny jednou",
                        "Rozbalení: a, b, c = (1, 2, 3)"
                    ]
                },
                {
                    "id": 2,
                    "title": "II. Slovníky a množiny",
                    "paragraphs": [
                        "Slovníky ukládají páry klíč-hodnota ve složených závorkách. Klíče musí být neměnitelné (řetězce, čísla, n-tice). Hodnoty jsou přístupné závorkami s klíčem. Metoda get() poskytuje výchozí hodnotu pro chybějící klíče.",
                        "Metody slovníku zahrnují keys(), values() a items() pro iteraci. Metoda update() slučuje slovníky. Comprehensions slovníků vytvářejí slovníky inline. Klíče jsou unikátní; přiřazení k existujícímu klíči přepíše hodnotu.",
                        "Množiny jsou neuspořádané kolekce unikátních prvků. Vytvářejí se složenými závorkami nebo set(). Operace zahrnují sjednocení (|), průnik (&) a rozdíl (-). Množiny jsou užitečné pro odstranění duplicit."
                    ],
                    "label": "Mapování a typy množin",
                    "items": [
                        "dict[klíč] = hodnota přiřazuje, dict.get(klíč, výchozí)",
                        "keys(), values(), items() pro iteraci slovníku",
                        "Množiny obsahují pouze unikátní prvky",
                        "Operace množin: sjednocení, průnik, rozdíl"
                    ]
                },
                {
                    "id": 3,
                    "title": "III. Metody řetězců a formátování",
                    "paragraphs": [
                        "Řetězce jsou neměnitelné sekvence znaků. Metody jako upper(), lower(), strip() a replace() vracejí nové řetězce. Metoda split() dělí řetězce na seznamy; join() kombinuje prvky seznamu do řetězců.",
                        "Formátování řetězců používá f-strings pro interpolaci proměnných. Specifikátory formátu řídí přesnost, šířku a zarovnání. Metoda format() poskytuje alternativní přístup. Metody řetězců lze řetězit pro sekvenční operace.",
                        "Vyhledávání v řetězcích používá find() a index() pro lokalizaci podřetězců. Metoda count() počítá výskyty. Booleovské metody startswith() a endswith() kontrolují prefixy a sufixy."
                    ],
                    "label": "Operace s řetězci",
                    "items": [
                        "split(), join(), strip() pro manipulaci",
                        "f-strings: f\"{hodnota:.2f}\" pro formátování",
                        "find(), count(), replace() pro hledání a nahrazování",
                        "Metody vracejí nové řetězce; originály nezměněny"
                    ]
                },
                {
                    "id": 4,
                    "title": "IV. Souborové vstupy/výstupy a projekt",
                    "paragraphs": [
                        "Soubory se otevírají pomocí open() s režimem: 'r' pro čtení, 'w' pro zápis, 'a' pro připojení. Příkaz with zajišťuje správné zavření souboru. Metoda read() vrací celý obsah; readlines() vrací seznam řádků.",
                        "Zápis používá write() pro řetězce a writelines() pro seznamy. Režim 'w' přepisuje existující soubory; režim 'a' připojuje. Textový režim je výchozí; binární režim používá 'rb' nebo 'wb'.",
                        "Týdenní projekt implementuje správce kontaktů. Program ukládá kontakty do textového souboru se strukturovaným formátem. Funkce zpracovávají čtení, zápis, vyhledávání a zobrazování kontaktů."
                    ],
                    "label": "Implementace projektu",
                    "items": [
                        "open(cesta, režim) otevírá, with zajišťuje zavření",
                        "read(), readline(), readlines() pro čtení",
                        "write(), writelines() pro zápis obsahu",
                        "Data kontaktů persistována do textového souboru"
                    ]
                }
            ]
        }
    }
}

# Add remaining weeks (4-40) with appropriate content
# Week 4: Error Handling
WEEKS_CONTENT[4] = {
    "en": {
        "title": "Activity History: Week 4 - Error Handling",
        "developer_label": "Developer", "page_label": "Page", "generated_msg": "Activity log generated",
        "sections": [
            {"id": 1, "title": "I. Exceptions and Try/Except", "paragraphs": [
                "Exceptions are errors detected during program execution. The try block contains code that may raise exceptions. The except block handles specific exception types. Multiple except blocks can handle different exception types.",
                "Common exceptions include ValueError for invalid conversions, TypeError for incompatible types, FileNotFoundError for missing files, and KeyError for missing dictionary keys. The Exception base class catches all standard exceptions.",
                "The as keyword captures the exception object for inspection. The exception message provides details about the error. Logging exceptions helps with debugging. Catching specific exceptions is preferred over catching all exceptions."
            ], "label": "Exception Handling", "items": ["try/except catches and handles exceptions", "Specific exceptions: ValueError, TypeError, KeyError", "as keyword captures exception details", "Catch specific exceptions, not generic Exception"]},
            {"id": 2, "title": "II. Finally and Else Clauses", "paragraphs": [
                "The finally block executes regardless of whether an exception occurred. It is used for cleanup operations like closing files or releasing resources. Finally runs even if return, break, or continue is executed in try or except.",
                "The else block executes only if no exception occurred in the try block. It separates normal code from error handling code. The else block runs before finally. This pattern improves code clarity.",
                "The complete structure is try-except-else-finally. Try contains risky code, except handles errors, else runs on success, finally always runs. This pattern ensures proper resource management and error handling."
            ], "label": "Complete Structure", "items": ["finally always executes for cleanup", "else runs only if no exception occurred", "Order: try → except → else → finally", "Use for resource management and cleanup"]},
            {"id": 3, "title": "III. Raising Exceptions", "paragraphs": [
                "The raise statement throws an exception explicitly. Custom error messages are passed as arguments. Raising exceptions signals invalid states or inputs. Functions should raise exceptions rather than return error codes.",
                "Re-raising exceptions uses raise without arguments in an except block. This preserves the original traceback. The from keyword chains exceptions, showing cause and effect. Exception chaining aids debugging.",
                "Custom exception classes inherit from Exception or its subclasses. They can add attributes and methods. Custom exceptions provide domain-specific error types. Naming convention ends with Error or Exception."
            ], "label": "Raising Exceptions", "items": ["raise Exception('message') throws exception", "raise without arguments re-raises current exception", "Custom classes inherit from Exception", "Use descriptive exception names ending in Error"]},
            {"id": 4, "title": "IV. Best Practices and Project", "paragraphs": [
                "Handle exceptions at the appropriate level. Catch exceptions where recovery is possible. Log exceptions for debugging. Provide user-friendly error messages. Avoid using exceptions for flow control.",
                "Validate inputs early to prevent exceptions. Use assertions for internal invariants. Document which exceptions a function may raise. Test exception handling paths. Clean up resources in finally blocks.",
                "The week project implements a file processor with robust error handling. The program reads data files, validates content, and reports errors. Exception handling ensures graceful degradation when files are missing or malformed."
            ], "label": "Project Implementation", "items": ["Validate inputs before processing", "Handle file not found and permission errors", "Log errors with context information", "Provide clear error messages to users"]}
        ]
    },
    "fr": {
        "title": "Historique d'activité : Semaine 4 - Gestion des erreurs",
        "developer_label": "Développeur", "page_label": "Page", "generated_msg": "Historique d'activité généré",
        "sections": [
            {"id": 1, "title": "I. Exceptions et try/except", "paragraphs": [
                "Les exceptions sont des erreurs détectées pendant l'exécution. Le bloc try contient le code susceptible de lever des exceptions. Le bloc except gère les types d'exceptions spécifiques. Plusieurs blocs except peuvent gérer différents types.",
                "Les exceptions courantes incluent ValueError pour les conversions invalides, TypeError pour les types incompatibles, FileNotFoundError pour les fichiers manquants, et KeyError pour les clés de dictionnaire absentes.",
                "Le mot-clé as capture l'objet exception pour inspection. Le message d'exception fournit des détails sur l'erreur. La journalisation des exceptions aide au débogage. Capturer des exceptions spécifiques est préférable."
            ], "label": "Gestion des exceptions", "items": ["try/except capture et gère les exceptions", "Exceptions spécifiques : ValueError, TypeError, KeyError", "as capture les détails de l'exception", "Capturer des exceptions spécifiques"]},
            {"id": 2, "title": "II. Clauses finally et else", "paragraphs": [
                "Le bloc finally s'exécute qu'une exception ait eu lieu ou non. Il sert aux opérations de nettoyage comme fermer des fichiers. Finally s'exécute même si return, break ou continue est exécuté.",
                "Le bloc else s'exécute uniquement si aucune exception n'est survenue dans try. Il sépare le code normal du code de gestion d'erreurs. Le bloc else s'exécute avant finally. Ce modèle améliore la clarté.",
                "La structure complète est try-except-else-finally. Try contient le code risqué, except gère les erreurs, else s'exécute en cas de succès, finally s'exécute toujours."
            ], "label": "Structure complète", "items": ["finally s'exécute toujours pour le nettoyage", "else s'exécute si aucune exception", "Ordre : try → except → else → finally", "Utiliser pour la gestion des ressources"]},
            {"id": 3, "title": "III. Lever des exceptions", "paragraphs": [
                "L'instruction raise lève une exception explicitement. Les messages d'erreur personnalisés sont passés en arguments. Lever des exceptions signale des états ou entrées invalides. Les fonctions doivent lever des exceptions plutôt que retourner des codes d'erreur.",
                "Relever des exceptions utilise raise sans arguments dans un bloc except. Cela préserve la trace originale. Le mot-clé from chaîne les exceptions, montrant cause et effet.",
                "Les classes d'exception personnalisées héritent d'Exception ou ses sous-classes. Elles peuvent ajouter des attributs et méthodes. Les exceptions personnalisées fournissent des types d'erreur spécifiques au domaine."
            ], "label": "Lever des exceptions", "items": ["raise Exception('message') lève exception", "raise sans arguments relève l'exception courante", "Classes personnalisées héritent d'Exception", "Noms descriptifs terminant par Error"]},
            {"id": 4, "title": "IV. Bonnes pratiques et projet", "paragraphs": [
                "Gérer les exceptions au niveau approprié. Capturer les exceptions là où la récupération est possible. Journaliser les exceptions pour le débogage. Fournir des messages d'erreur conviviaux.",
                "Valider les entrées tôt pour prévenir les exceptions. Utiliser les assertions pour les invariants internes. Documenter quelles exceptions une fonction peut lever. Tester les chemins de gestion d'exception.",
                "Le projet implémente un processeur de fichiers avec gestion d'erreurs robuste. Le programme lit les fichiers de données, valide le contenu et signale les erreurs. La gestion des exceptions assure une dégradation gracieuse."
            ], "label": "Implémentation du projet", "items": ["Valider les entrées avant traitement", "Gérer fichier non trouvé et erreurs de permission", "Journaliser les erreurs avec contexte", "Messages d'erreur clairs pour l'utilisateur"]}
        ]
    },
    "cs": {
        "title": "Historie aktivit: Týden 4 - Zpracování chyb",
        "developer_label": "Vývojář", "page_label": "Strana", "generated_msg": "Historie aktivit vygenerována",
        "sections": [
            {"id": 1, "title": "I. Výjimky a try/except", "paragraphs": [
                "Výjimky jsou chyby zjištěné během vykonávání programu. Blok try obsahuje kód, který může vyvolat výjimky. Blok except zpracovává specifické typy výjimek. Více bloků except může zpracovat různé typy výjimek.",
                "Běžné výjimky zahrnují ValueError pro neplatné konverze, TypeError pro nekompatibilní typy, FileNotFoundError pro chybějící soubory a KeyError pro chybějící klíče slovníku.",
                "Klíčové slovo as zachycuje objekt výjimky pro inspekci. Zpráva výjimky poskytuje detaily o chybě. Logování výjimek pomáhá s laděním. Zachytávání specifických výjimek je preferováno."
            ], "label": "Zpracování výjimek", "items": ["try/except zachytává a zpracovává výjimky", "Specifické výjimky: ValueError, TypeError, KeyError", "as zachycuje detaily výjimky", "Zachytávat specifické výjimky"]},
            {"id": 2, "title": "II. Klauzule finally a else", "paragraphs": [
                "Blok finally se vykoná bez ohledu na to, zda výjimka nastala. Používá se pro úklidové operace jako zavírání souborů. Finally běží i když se vykoná return, break nebo continue.",
                "Blok else se vykoná pouze pokud v bloku try nenastala žádná výjimka. Odděluje normální kód od kódu zpracování chyb. Blok else běží před finally. Tento vzor zlepšuje čitelnost.",
                "Kompletní struktura je try-except-else-finally. Try obsahuje rizikový kód, except zpracovává chyby, else běží při úspěchu, finally běží vždy."
            ], "label": "Kompletní struktura", "items": ["finally se vždy vykoná pro úklid", "else běží pouze pokud nenastala výjimka", "Pořadí: try → except → else → finally", "Použít pro správu zdrojů"]},
            {"id": 3, "title": "III. Vyvolávání výjimek", "paragraphs": [
                "Příkaz raise explicitně vyvolá výjimku. Vlastní chybové zprávy se předávají jako argumenty. Vyvolání výjimek signalizuje neplatné stavy nebo vstupy. Funkce by měly vyvolávat výjimky místo vracení chybových kódů.",
                "Opětovné vyvolání výjimek používá raise bez argumentů v bloku except. To zachovává původní traceback. Klíčové slovo from řetězí výjimky, ukazuje příčinu a následek.",
                "Vlastní třídy výjimek dědí z Exception nebo jeho podtříd. Mohou přidávat atributy a metody. Vlastní výjimky poskytují doménově specifické typy chyb."
            ], "label": "Vyvolávání výjimek", "items": ["raise Exception('zpráva') vyvolá výjimku", "raise bez argumentů znovu vyvolá aktuální", "Vlastní třídy dědí z Exception", "Popisné názvy končící Error"]},
            {"id": 4, "title": "IV. Osvědčené postupy a projekt", "paragraphs": [
                "Zpracovávat výjimky na vhodné úrovni. Zachytávat výjimky tam, kde je možná obnova. Logovat výjimky pro ladění. Poskytovat uživatelsky přívětivé chybové zprávy.",
                "Validovat vstupy brzy pro prevenci výjimek. Používat assertions pro interní invarianty. Dokumentovat, které výjimky funkce může vyvolat. Testovat cesty zpracování výjimek.",
                "Týdenní projekt implementuje zpracovatel souborů s robustním zpracováním chyb. Program čte datové soubory, validuje obsah a hlásí chyby. Zpracování výjimek zajišťuje graceful degradation."
            ], "label": "Implementace projektu", "items": ["Validovat vstupy před zpracováním", "Zpracovat chyby soubor nenalezen a oprávnění", "Logovat chyby s kontextovými informacemi", "Jasné chybové zprávy pro uživatele"]}
        ]
    }
}

def generate_script(week_num, lang, content):
    """Generate a Python script for a specific week and language."""

    # Build content_map string
    sections_str = "[\n"
    for section in content["sections"]:
        sections_str += "        {\n"
        sections_str += f'            "id": {section["id"]},\n'
        sections_str += f'            "title": "{section["title"]}",\n'
        sections_str += '            "paragraphs": [\n'
        for p in section["paragraphs"]:
            escaped_p = p.replace('"', '\\"')
            sections_str += f'                "{escaped_p}",\n'
        sections_str = sections_str.rstrip(',\n') + '\n'
        sections_str += '            ],\n'
        sections_str += f'            "label": "{section["label"]}",\n'
        sections_str += '            "items": [\n'
        for item in section["items"]:
            escaped_item = item.replace('"', '\\"')
            sections_str += f'                "{escaped_item}",\n'
        sections_str = sections_str.rstrip(',\n') + '\n'
        sections_str += '            ]\n'
        sections_str += '        },\n'
    sections_str = sections_str.rstrip(',\n') + '\n'
    sections_str += "    ]"

    script = TEMPLATE.format(
        main_title=content["title"],
        developer_label=content["developer_label"],
        page_label=content["page_label"],
        generated_msg=content["generated_msg"],
        content_map=sections_str
    )

    # Determine filename
    lang_suffix = {"en": "", "fr": "-fr", "cs": "-cs"}[lang]
    filename = f"week-{week_num:02d}-activity-log{lang_suffix}.py"

    return filename, script

def main():
    """Generate all activity log scripts."""
    generated = 0

    for week_num, week_data in WEEKS_CONTENT.items():
        for lang in ["en", "fr", "cs"]:
            if lang in week_data:
                filename, script = generate_script(week_num, lang, week_data[lang])

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(script)

                print(f"Generated: {filename}")
                generated += 1

    print(f"\nTotal files generated: {generated}")
    print("Note: This script contains content for weeks 2-4.")
    print("Run this script to generate the Python files, then execute each to create PDFs.")

if __name__ == "__main__":
    main()
