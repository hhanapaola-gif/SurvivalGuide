from flask import Flask, render_template, request, redirect, url_for, session
import unicodedata

app = Flask(__name__)
app.secret_key = "aventura_movil"


def normalize_text(text):
    text = text.lower().strip()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text

sections = [
    {
        "id": 0,
        "title": "La cámara de las reglas",
        "image": "reglas.png",
        "content": """
Reglas del reino universitario en Programación móvil

• Se requiere 80 porciento de asistencia para tener derecho a evaluación.
• Se permiten 10 minutos de tolerancia.
• Las faltas deben ser justificadas por el tutor en un máximo de 24 horas.
• Las tareas y trabajos deben entregarse en Google Classroom.
• El plagio será condicionado a reprobar la asignatura.
• Está prohibido usar audífonos durante la clase.
• Está prohibido comer y/o tomar líquidos durante la clase.
• Los dispositivos móviles solo deben utilizarse para actividades que lo requieran.
        """,

        "questions": [
            {
                "question": "¿Qué porcentaje de asistencia se necesita para tener derecho a examen?",
                "answers": [
                    "80",
                    "80%",
                    "80 porciento",
                    "80 por ciento"
                ]
            },
            {
                "question": "¿Cuántos minutos de tolerancia se tienen al inicio de la clase?",
                "answers": [
                    "10",
                    "10 minutos",
                    "diez",
                    "diez minutos"
                ]
            }
        ]
    },

    {
        "id": 1,
        "title": "El oráculo de las notas",
        "image": "evaluacion.png",
        "content": """
Lineamientos de evaluación

Primer parcial
• Evidencia de conocimiento: 40%
• Evidencia de desempeño: 20%
• Evidencia de producto: 30%
• PI: 10%

Segundo parcial
• Evidencia de conocimiento: 40%
• Evidencia de desempeño: 20%
• Evidencia de producto: 30%
• PI: 10%

Tercer parcial
• Evidencia de conocimiento: 10%
• Evidencia de desempeño: 10%
• Evidencia de producto: 30%
• PI: 50%
        """,

        "questions": [
            {
                "question": "¿Cuánto vale el proyecto integrador en el 3er parcial?",
                "answers": [
                    "50",
                    "50%",
                    "50 porciento",
                ]
            },
            {
                "question": "¿Cuánto vale la evidencia de conocimiento (examen) en el 1er y 2do parcial?",
                "answers": [
                    "40",
                    "40%",
                    "40 porciento",
                ]
            }
        ]
    },

    {
        "id": 2,
        "title": "Skills a desbloquear",
        "image": "skills.png",
        "content": """
Habilidades que obtendrá el aventurero

Objetivo general:
Desarrollar aplicaciones móviles mediante lenguajes de programación, entornos de
desarrollo, diseño de interfaces de usuario, arquitecturas, patrones de diseño y herramientas de
programación móvil

Competencias:
• Soluciones tecnológicas multiplataforma.
• Programación orientada a objetos.
• Uso de frameworks móviles.
• Bases de datos.
• Estándares de calidad y diseño.
        """,

        "questions": [
            {
                "question": "¿Qué tipo de aplicaciones desarrollarás?",
                "answers": [
                    "aplicaciones moviles",
                    "aplicaciones móviles",
                    "apps moviles",
                    "apps móviles",
                    "moviles",
                    "móviles"
                ]
            },
            {
                "question": "¿Verás algo relacionado con programación orientada a objetos (POO)?",
                "answers": [
                    "si",
                    "sí",
                    "claro",
                    "correcto"
                ]
            }
        ]
    },

    {
        "id": 3,
        "title": "La línea del tiempo",
        "image": "fechas.png",

        "content": """
Fechas clave 

• 1er Parcial: 01-06-26
• 2do Parcial: 06-07-26
• 3er Parcial: 10-08-26
• Examen Final: 17-08-26

También existe:
• Receso académico (puentes y vacaciones).
• Entrega de actas.
• Revisión de proyecto integrador.
• Publicación de becas.
• Fin del cuatrimestre.
        """,

        "questions": [
            {
                "question": "¿Cuándo es el 1er parcial?",
                "answers": [
                    "01-06-26",
                    "1-6-26",
                    "01/06/26",
                    "01-06-2026"
                    "1 junio 2026"
                ]
            },
            {
                "question": "¿Cuándo es el examen final?",
                "answers": [
                    "17-08-26",
                    "17/08/26",
                    "17-8-26",
                    "17-08-2026",
                    "17 agosto 2026"
                ]
            }
        ]
    }
]


@app.route("/")
def index():
    unlocked = session.get("unlocked", [0])
    return render_template(
        "index.html",
        sections=sections,
        unlocked=unlocked
    )

@app.route("/section/<int:section_id>", methods=["GET", "POST"])
def section(section_id):
    unlocked = session.get("unlocked", [0])
    if section_id not in unlocked:
        return redirect(url_for("index"))
    current_section = sections[section_id]
    passed = False
    score = 0

    if request.method == "POST":
        for i, q in enumerate(current_section["questions"]):
            user_answer = normalize_text(
                request.form.get(f"q{i}", "")
            )

            valid_answers = [
                normalize_text(ans)
                for ans in q["answers"]
            ]

            if user_answer in valid_answers:
                score += 1

        if score >= 2:

            if request.form.get("commit") == "on":
                passed = True
                next_section = section_id + 1

                if next_section < len(sections):
                    if next_section not in unlocked:
                        unlocked.append(next_section)
                session["unlocked"] = unlocked

    return render_template(
        "section.html",
        section=current_section,
        passed=passed,
        score=score
    )

if __name__ == "__main__":
    app.run(debug=True)