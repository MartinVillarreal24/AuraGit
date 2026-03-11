# Historial de Cambios

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [No Lanzado]

## [0.2.0] - 2026-03-11
### Añadido
- Nuevo sistema de memoria persistente (Engram) para mantener contexto entre sesiones.
- Comando `git-ai memory save` para guardar decisiones, patrones y descubrimientos.
- Comando `git-ai memory list` para visualizar los últimos engrams guardados.
- Comando `git-ai memory search` para buscar engrams por palabra clave.
### Cambiado
- El comando `git-ai generate` ahora consulta automáticamente la memoria reciente para generar mensajes de commit más inteligentes y contextualizados.

## [0.1.4] - 2026-03-11
### Cambiado
- Traducido el archivo `CHANGELOG.md` íntegramente al español.
- Actualizada la skill `git-flow-enforcer` para establecer el español como idioma obligatorio para la documentación.

## [0.1.3] - 2026-03-11
### Añadido
- Mejorada la skill `git-flow-enforcer` para incluir Tagging de Git obligatorio, mantenimiento de `CHANGELOG.md` y aplicación estricta de SemVer.
- Actualizado `.gitignore` para permitir el rastreo de las skills del proyecto en el directorio `.agents/`.

## [0.1.2] - 2026-03-11
### Corregido
- Actualizado el SDK de Gemini de `google-generativeai` a `google-genai` para resolver advertencias de obsolescencia.
- Resuelto el error de "API Key filtrada" mediante la guía para restablecer credenciales.
### Cambiado
- Refinadas las dependencias en `pyproject.toml` y `requirements.txt`, eliminando paquetes no utilizados.

## [0.1.1] - 2026-03-11
### Añadido
- Nuevo comando `git-ai config init` para automatizar la creación de la carpeta de configuración global (`.git-ai`) y la plantilla `.env`.
### Cambiado
- Actualizado `README.md` con mejores instrucciones de instalación y configuración.

## [0.1.0] - 2026-03-11
### Añadido
- Lanzamiento inicial de AuraGit.
- Soporte para múltiples proveedores de IA: Ollama, OpenAI, Gemini y Anthropic.
- Generación automática de mensajes de commit siguiendo Conventional Commits.
- Integración como Hook de Git (`prepare-commit-msg`).
- Soporte multi-idioma (Español e Inglés).
