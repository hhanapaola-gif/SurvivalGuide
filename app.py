from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "aventura_movil"


sections = [

    {
        "id": 0,

        "title": "La cámara de las reglas",

        "content": """
Reglas del reino universitario en Programación móvil

• Se requiere 80% de asistencia para tener derecho a evaluación.
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
                "answer": "80"
            },

            {
                "question": "¿Cuántos minutos de tolerancia se tienen al inicio de la clase?",
                "answer": "10"
            }

        ]
    },



    {
        "id": 1,

        "title": "El oráculo de las notas",

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
                "answer": "50"
            },

            {
                "question": "¿Cuánto vale la evidencia de conocimiento (examen) en el 1er y 2do parcial?",
                "answer": "40"
            }

        ]
    },



    {
        "id": 2,

        "title": "Skills a desbloquear",

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
                "answer": "Aplicaciones móviles"
            },

            {
                "question": "¿Verás algo relacionado con programación orientada a objetos (POO)?",
                "answer": "Sí"
            }

        ]
    },



    {
        "id": 3,

        "title": "La línea del tiempo",

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
                "answer": "01-06-26"
            },

            {
                "question": "¿Cuándo es el examen final?",
                "answer": "17-08-26"
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

            user_answer = request.form.get(f"q{i}", "").lower().strip()

            if user_answer == q["answer"]:
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