"""Perfil inicial opcional para equipos de siete: datos y persistencia."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'data'
LABEL = 'Datos y persistencia'
SPEC_FILE = 'data_spec.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Solo para un equipo de siete. Diseña el contrato del archivo JSON mock de la HU Wallet desde arquitectura aprobada y el formato real de `wallet-store.json`. Define entidades, campos ficticios, estados, eventos, relaciones por ID, version de esquema, restricciones, comportamiento ante archivo ausente/corrupto, escritura atomica, concurrencia, recuperacion y aislamiento de tests. No incluyas datos personales reales ni secretos. No propongas tablas SQL, JDBC, H2 ni migraciones: el producto acordado usa JSON mock. Coordina con Backend y deja pendientes los datos KYC que no haya aprobado Cumplimiento. Entrega data_spec.md con ejemplos JSON ficticios y comprobaciones; no inventes que ejecutaste pruebas."""
agent = Agent(role=LABEL, goal="Definir un contrato JSON mock seguro y compatible para la persistencia del onboarding Wallet.",
              backstory="Eres responsable de datos del equipo de siete; diseñas integridad y recuperacion de archivos JSON y coordinas el contrato con Backend, sin introducir una base SQL fuera de alcance.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='data_spec.md con esquema JSON versionado, campos ficticios, restricciones, concurrencia, escritura segura, recuperacion y pruebas propuestas. '
                'No generar SQL ni migraciones. No ejecutar cambios sobre el archivo real. Marcar NO EJECUTADO cuando falte evidencia.', agent=agent)
