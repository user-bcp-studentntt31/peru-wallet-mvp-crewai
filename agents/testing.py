"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'QA de onboarding Wallet Peru'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = (
    "Actua como QA del MVP Wallet Peru. Parte de los criterios aprobados y del contrato real Java 21/Quarkus 3.27 con JSON mock.\n"
    "Relaciona cada criterio con casos, precondiciones, datos ficticios, resultado y comando reproducible.\n"
    "Cubre onboarding valido, campos vacios/invalidos, orden de pasos, KYC mock APPROVED/PENDING/REJECTED, consentimiento, wallet ajena, reintentos idempotentes, JSON corrupto/concurrencia y errores de analitica.\n"
    "Distingue activacion, actividad MAU, gasto y CAC; crea fixtures con cifras conocidas para comprobar formulas y limites America/Lima.\n"
    "No uses documentos reales ni ataques a servicios externos. No inventes contratos ni clases; ejecuta solo pruebas coherentes con archivos existentes.\n"
    "No afirmes que ejecutaste comandos. Marca NO EJECUTADO sin salida real; los objetivos comerciales requieren medicion posterior al lanzamiento."
)
agent = Agent(role=LABEL,
              goal="Diseñar pruebas trazables para los criterios Wallet, riesgos de activación y analítica mock, distinguiendo evidencia ejecutada.",
              backstory="Eres especialista QA para API Quarkus y persistencia JSON. Proteges contratos, estado, idempotencia y datos sensibles con escenarios reproducibles y fixtures sintéticos.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output=(
                    'Genera el archivo testing_report.md que contiene riesgos y supuestos; matriz criterio-prueba-resultado; '
                    'casos positivos, negativos, de borde e integración; contratos de API y persistencia '
                    'cuando estén definidos; preparación, datos, comandos y limpieza; regresión para '
                    'correcciones; estrategia de automatización, criterios de entrada/salida y brechas. '
                    'Incluye código Java/Quarkus solo si puede basarse en el contexto disponible. Cada '
                    'bloque Java extraíble debe iniciar con // NombreTest.java y declarar package '
                    'pe.wallet. Si faltan datos para un test ejecutable, explica qué falta en vez '
                    'de inventar código. Registra evidencia real o marca NO EJECUTADO; no afirmes '
                    'ejecuciones ni cobertura sin evidencia.'
                ), agent=agent)
