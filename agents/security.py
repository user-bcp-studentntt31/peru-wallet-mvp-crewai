"""Agente inicial del taller."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = "security"
LABEL = "Analista de seguridad"
SPEC_FILE = "security_report.md"
EXTRACT_CODE = False

INSTRUCTIONS = (
    "HU-01: comprueba autorización sobre la wallet en cada operación, "
    "rechazo de sesiones inválidas y acceso cruzado, "
    "Valida datos en servidor solo según reglas aprobadas. No inventes campos KYC, DNI, celular, "
    "formatos ni proveedor de identidad. Comprueba que datos personales, credenciales y tokens no "
    "se expongan en respuestas, logs o almacenamiento sin protección evidenciada.\n"
    "HU-02: comprueba que únicamente pasos y verificaciones aprobados permitan al backend "
    "activar la wallet; estados pendientes, fallidos, rechazados, desconocidos o simulados no deben "
    "activar una wallet productiva. Revisa que la identidad propietaria autorice cada operación, "
    "que solicitudes repetidas o concurrentes mantengan transiciones consistentes e idempotentes, "
    "y que el punto de entrada requiera una activación válida. No describas ese punto como si "
    "procesara pagos o transferencias.\n"
    "HU-03: revisa que los eventos reflejen transiciones confirmadas por el servidor, tengan "
    "timestamp de servidor. No "
    "infieras una salida explícita por desconexión o fin de sesión. Comprueba minimización de "
    "eventos, seudonimización, acceso a informes/eventos y protección de claves; no deben incluir "
    "documentos, credenciales, respuestas KYC ni valores de formularios. Separa actividad mock "
    "de productiva; no llames MAU a activaciones y marca CAC como no disponible si faltan fuente "
    "de gasto, regla de atribución o denominador aprobados.\n"
    "Para cada riesgo, aporta evidencia concreta, archivo y ubicación si están disponibles, "
    "historia/criterio relacionado, escenario y precondiciones, impacto, probabilidad solo si "
    "puede justificarse, corrección y comprobación reproducible. Marca como pendiente lo que no "
    "pueda confirmarse y explica qué falta. Distingue propuestas de verificaciones realmente "
    "ejecutadas; no inventes hallazgos, resultados, obligaciones ni controles. Usa OWASP, CWE, "
    "NIST o referencias legales solo cuando sean pertinentes y verificables; no amplíes el alcance "
    "a PCI DSS, pagos procesados ni otros dominios no cubiertos por las historias."
)
agent = Agent(
    role="Analista de seguridad",
    goal=(
        "Evaluar la seguridad del onboarding, la activación de wallet y las métricas"    ),
    backstory=(
        "Analizas flujos, identidades, permisos, datos y transiciones de estado. "
        "Fundamentas los hallazgos en evidencia del código y distingues riesgos "
        "confirmados de aspectos pendientes."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def build_task(feature: dict) -> Task:
    description = (
        INSTRUCTIONS
        + "\nFeature: "
        + str(feature.get("title", ""))
        + "\n"
        + str(feature.get("description", ""))
        + "\n"
        + str(feature.get("acceptance_criteria", []))
    )
    return Task(
        description=description,
        expected_output=(
            "Un único informe Markdown para security_report.md con secciones de alcance y "
            "limitaciones, hallazgos, decisiones abiertas y verificaciones. Para cada "
            "hallazgo incluye identificador, estado confirmado/pendiente, historia y criterio "
            "relacionados, evidencia y ubicación, escenario y precondiciones, impacto, "
            "probabilidad justificada si hay datos suficientes, corrección propuesta y "
            "comprobación reproducible. Separa las verificaciones propuestas de las "
            "ejecutadas y reporta resultados solo si fueron proporcionados u observados. "
            "Si no hay hallazgos, indica qué se revisó y las limitaciones; no inventes "
            "resultados, controles ni obligaciones."
        ),
        agent=agent,
    )