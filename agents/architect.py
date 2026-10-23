"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Analiza el Issue recibido de registro y activación del MVP Wallet Perú, sus
criterios y la arquitectura Java 21/Quarkus 3.27 existente. Define componentes,
responsabilidades y límites del cambio; describe contrato API (entradas,
respuestas y errores) y cómo el backend JSON mock y el frontend comparten estados.
Relaciona cada criterio con una decisión verificable.

No inventes pasos, KYC, documentos, consentimiento legal, identidad, métricas ni
contratos que no estén aprobados. Mantén explícitas las preguntas abiertas de
Producto/Cumplimiento, en especial frontera inicio-fin, cohortes, MAU y CAC.
Separa activación de actividad y pagos reales. No diseñes SQL ni una base de datos.
No escribas código. Entrega user_story.md con alcance, contrato, criterios,
supuestos, riesgos, preguntas pendientes y archivos/componentes posiblemente
afectados; la lista de archivos es propuesta, no evidencia del repo."""
agent = Agent(role='Arquitecto de requisitos y API para Wallet Perú',
              goal="Definir una solución verificable para onboarding Wallet sin inventar requisitos regulatorios ni de analítica.",
              backstory="Eres responsable de convertir la HU Wallet aprobada en límites y contratos claros para Backend, Frontend, Pruebas y Seguridad.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Una historia de usuario.', agent=agent)
