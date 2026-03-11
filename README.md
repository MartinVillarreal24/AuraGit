# AuraGit: Mensajes de Commit Inteligentes 🤖✨

**Git AI** es una herramienta de línea de comandos profesional diseñada para automatizar la generación de mensajes de commit utilizando Inteligencia Artificial local (Ollama) o proveedores en la nube (OpenAI, Gemini, Anthropic). 

Eleva la calidad de tu historial de Git siguiendo la especificación de [Conventional Commits](https://www.conventionalcommits.org/) de manera automática y profesional.

## ✨ Características Principales

- **Multi-Proveedor**: Soporte listo para usar con:
  - 🏠 **Ollama** (100% local, privacidad total).
  - 🤖 **OpenAI** (GPT-4o, GPT-3.5).
  - ♊ **Google Gemini** (1.5 Pro/Flash).
  - 🅰️ **Anthropic** (Claude 3.5 Sonnet).
- **Multi-Idioma**: Genera mensajes en **Español** o **Inglés** con un solo ajuste.
- **Integración Nativa**: Se instala como un **Git Hook** (`prepare-commit-msg`), integrándose invisiblemente en tu flujo de trabajo.
- **Configuración Global**: Define tus API Keys una vez en tu carpeta de usuario y úsalas en todos tus proyectos.
- **Formato Profesional**: Genera títulos concisos y descripciones detalladas de los cambios técnicos.

---

## 🚀 Instalación Rápida

### 1. Requisitos
- Python 3.8 o superior.
- (Opcional) [Ollama](https://ollama.com/) para ejecución 100% local.

### 2. Instalación del Paquete
Clona este repositorio y desde la raíz, ejecuta:
```bash
pip install .
```

### 3. Configuración Global
Para no tener que configurar cada proyecto, crea un archivo `.env` en la carpeta `.git-ai` de tu usuario:

- **Windows**: `C:\Users\TU_USUARIO\.git-ai\.env`
- **macOS/Linux**: `~/.git-ai/.env`

Puedes usar el archivo `.env.example` de este repositorio como plantilla.

---

## 📖 Modo de Uso

### Uso como Git Hook (Recomendado)
Activa la IA en cualquier repositorio de Git:
```bash
git-ai install
```
A partir de ahora, cada vez que hagas `git commit`, la IA analizará tus cambios y redactará el mensaje automáticamente.

### Uso Manual
Si prefieres generar el mensaje sin el hook:
```bash
git add .
git-ai generate
```

---

## ⚙️ Parámetros de Configuración

Edita tu `.env` para personalizar la experiencia:

| Variable | Descripción | Valores Ejemplo |
|----------|-------------|-----------------|
| `AI_PROVIDER` | Proveedor de IA activo | `ollama`, `openai`, `gemini`, `anthropic` |
| `AI_LANGUAGE` | Idioma del mensaje | `es`, `en` |
| `COMMIT_STYLE`| Estilo del commit | `conventional` |
| `OPENAI_API_KEY`| Tu llave de OpenAI | `sk-...` |

---

## 🤝 Contribución
¡Las contribuciones son bienvenidas! Consulta nuestra [Guía de Contribución](CONTRIBUTING.md) para más detalles sobre cómo empezar.

## 📄 Licencia
Este proyecto está bajo la licencia MIT. Siéntete libre de usarlo, modificarlo y compartirlo.

---
*Desarrollado con ❤️ para agilizar el flujo de trabajo de los desarrolladores.*
