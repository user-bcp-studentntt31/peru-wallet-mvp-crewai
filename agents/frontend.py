"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa únicamente la experiencia frontend de la HU de onboarding
Wallet Perú, basada en el contrato aprobado por Arquitectura y en la API existente
del backend Java 21/Quarkus 3.27. No inventes endpoints, pasos KYC ni decisiones
legales. El flujo de demo actualmente expone PROFILE, VERIFICATION y CONSENT;
confirma con el equipo antes de cambiarlo. Presenta claramente el paso actual,
progreso y siguiente acción; contempla carga, error, pendiente KYC, éxito y
reanudación. Impide doble envío en UI con estado ocupado e Idempotency-Key según
el contrato del backend.

Define campos y mensajes accionables, pero datos obligatorios y documentación KYC
siguen pendientes de Producto/Cumplimiento. Conserva accesibilidad, navegación por
teclado y foco visible. Backend sigue siendo responsable de validación y permisos.
No presentes la entrada de pagos MOCK como pago real. No afirmes alcanzar la meta
de 3 minutos ni MAU/CAC usando mocks.
Entrega frontend_spec.md y código Angular en bloques Markdown con ruta de archivo
en la primera línea, incluyendo pruebas propuestas y resultado real o NO EJECUTADO.
Para cada criterio de aceptación, incluye una comprobación con: criterio relacionado, acción o datos de entrada, resultado visible esperado, archivos o componentes afectados y estado EJECUTADO o NO EJECUTADO. Si se ejecutó, indica el comando y el resultado observado; si no, indica cómo ejecutarla y marca NO EJECUTADO. No afirmes que una comprobación pasó sin evidencia real.
Separa las pruebas ejecutadas de las propuestas. Indica bloqueos o riesgos pendientes. Si recibes feedback, corrige lo señalado y resume el cambio."""
agent = Agent(role='Desarrollador frontend para Wallet Perú', goal="Implementar el recorrido accesible del onboarding Wallet conforme al contrato API aprobado y a los criterios trazables.",
              backstory="Eres responsable de la interfaz del MVP Wallet. Coordinas estados y contratos con Backend, no implementas autenticación, KYC ni pagos fuera del alcance acordado, y señalas decisiones pendientes.",
              llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    criteria = feature.get("acceptance_criteria", [])
    if isinstance(criteria, (list, tuple)):
        criteria_text = "\n".join(f"- {item}" for item in criteria if str(item).strip())
    elif criteria:
        criteria_text = str(criteria)
    else:
        criteria_text = "No se proporcionaron criterios de aceptación."

    description = (
        INSTRUCTIONS
        + "\n\n## Feature\n"
        + str(feature.get("title", ""))
        + "\n\n## Descripción\n"
        + str(feature.get("description", ""))
        + "\n\n## Criterios de aceptación\n"
        + criteria_text
    )
    return Task(description=description,
                expected_output='frontend_spec.md con el recorrido, los estados, validaciones y una comprobación por criterio que indique criterio, acción o entrada, resultado visible esperado, archivos afectados y estado EJECUTADO o NO EJECUTADO; para lo ejecutado, incluye comando y resultado observado. Incluye código Angular en bloques Markdown con el nombre de archivo en la primera línea mediante un comentario válido para su tipo. Indica bloqueos o riesgos pendientes sin inventar resultados.', agent=agent)
