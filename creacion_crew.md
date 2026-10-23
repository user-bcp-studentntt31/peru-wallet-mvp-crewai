# Creación del CrewAI para el MVP Wallet Perú

## Objetivo

Se creó esta copia para usar CrewAI como orquestador del proyecto Wallet, manteniendo separados el backend, el frontend y el Crew:

```text
C:\Proyecto\peru-wallet-mvp\
  peru-wallet-mvp-back-grupo2\  backend Java 21 / Quarkus 3.27 / JSON mock
  peru-wallet-mvp-front-grupo2\ frontend del equipo
  crewai\                         agentes, workflow y salidas CrewAI
```

La fuente fue el CrewAI de trabajo del estudiante. Se copió su **contenido versionado** desde el commit `e7d245b` mediante `git archive`.

## Qué se copió

Se conservaron el workflow, `main.py`, los seis roles, el perfil opcional Datos, el cliente MCP, el adaptador Copilot, pruebas, scripts y documentación técnica versionada.

No se copiaron:

- `.git` ni el remoto personal `user-bcp-student14/crewai`, para evitar publicar accidentalmente en el repositorio anterior.
- `.env`, claves, tokens o credenciales. La copia usa una plantilla vacía/configurable.
- `.venv`, `output/`, checkpoints, JSON de trabajo, cachés o datos generados.
- Los cuatro resúmenes de clase no versionados que permanecían en el Crew anterior.

El backend, su `.git`, `.env`, `data/` y `target/` no se modificaron para crear esta copia.

## Adaptaciones para Wallet

- [.env.example](.env.example) ahora apunta como ejemplo a `user-bcp-studentntt31/peru-wallet-mvp-back-grupo2`; la clave MCP queda vacía para que el líder/instructor proporcione la correspondiente. No se creó `.env` porque no se compartió la configuración secreta del MCP.
- [README.md](README.md) explica los repos separados, responsabilidades, conexión MCP, verificación y ejecución del Crew integrado.
- `agents/backend.py` se enfoca en la HU de registro/activación, la API existente, Java 21, Quarkus 3.27, JSON mock e idempotencia. No debe generar SQL, KYC real ni pagos.
- `agents/architect.py`, `frontend.py`, `testing.py`, `security.py` y `chapter.py` se orientan a la misma HU y a sus decisiones aún pendientes.
- `agents/data.py`, solo si el equipo tiene siete integrantes, describe el contrato JSON; no plantea tablas ni migraciones SQL.
- El scaffold Java de `main.py` usa el BOM Quarkus 3.27.0, Java 21, REST/Jackson, OpenAPI, Health y Bean Validation. Quité los drivers H2/PostgreSQL, Hibernate ORM y referencias de login/BCP.
- La extracción y los bloques de ejemplo Java usan el paquete `pe.wallet` y rutas controller/service/model/repository/dto. El scaffold generado es una propuesta en `output/`, no sustituye el código real del backend.
- Las pruebas offline del Crew usan el Issue Wallet ficticio solo como fixture para probar el workflow; no se presenta como Issue real ni se llama a MCP/Copilot.

## Configuración pendiente

Antes de una ejecución real, el líder debe confirmar y completar en `.env` local:

1. `PROJECTS_MCP_URL` y `PROJECTS_MCP_API_KEY` entregados/autorizados por el equipo o instructor.
2. `GITHUB_OWNER` y `GITHUB_REPO` que usa el MCP para encontrar los Issues.
3. Project ReqFlow y el Issue aprobado de onboarding, con acceso y vínculo al repositorio que consulte el MCP.
4. Sesión de Copilot CLI (`copilot` y `/login`) y disponibilidad del modelo configurado.
5. Si el equipo tiene seis o siete integrantes. Por defecto se conserva `CREWAI_INCLUDE_DATA=false`.

En la conversación no se compartió un Issue numérico aprobado ni la clave del MCP. Por eso no se inventaron IDs, no se creó otro Project y no se ejecutó `main.py` contra servicios reales. No pegar credenciales en este documento.

## Cómo ejecutar

En PowerShell, desde `C:\Proyecto\peru-wallet-mvp\crewai`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
python tools/verify.py
```

Editar `.env` privadamente con los valores aprobados. No sustituir una configuración existente sin revisarla.

```powershell
python main.py
```

La ejecución integrada pasa por Arquitectura → Backend → Frontend → Pruebas → Seguridad → Chapter. Revisar cada artefacto antes de responder `s` (continuar), `r` (reintentar) o `n` (detener).

## Verificación de la copia

Ejecutado durante su preparación:

```powershell
python tools/verify.py
```

Resultado final: **6 pruebas aprobadas**, incluyendo construcción de tareas por rol, scaffold Java 21/Quarkus 3.27 y extracción `pe.wallet`, flujos de seis/siete perfiles, gate humano, rechazo, reanudación y checkpoint. No se llamó a Copilot, MCP ni GitHub.

Se creó `.venv` con Python 3.12 e instalaron los paquetes de `requirements.txt`; quedó verificado que `pip check` no reporta dependencias rotas. No se creó `.env` porque falta que el equipo/instructor confirme la URL y la clave del MCP. Tampoco se comprobó acceso a un Issue Wallet ni se ejecutó el Crew real. Las pruebas offline no prueban disponibilidad del modelo, credenciales ni artefactos generados.

## Remoto Git

Esta carpeta se creó sin metadata Git, para no heredar el remoto del Crew personal antiguo. No se configuró remoto, no se hizo commit y no se publicó nada. El repositorio backend existente sigue siendo un repositorio separado. El líder debe indicar el repositorio de equipo para CrewAI antes de conectar o publicar esta copia.