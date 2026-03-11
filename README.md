# AI Auto-Commit Tool 🤖

Genera mensajes de commit profesionales automáticamente usando IA local (**Ollama**).

## 🚀 Requisitos Precios

1. **Instalar Ollama**: Descárgalo en [ollama.com](https://ollama.com).
2. **Descargar el Modelo**: Ejecuta `ollama pull qwen2.5-coder:7b`.
3. **Mantener Ollama Abierto**: La herramienta se comunica con el servidor local de Ollama.

## 🚀 Instalación Profesional (Uso Global)

Para poder usar `git-ai` en **cualquier proyecto** de tu máquina, sigue estos pasos:

1.  **Instalación**:
    Desde la carpeta de este proyecto, ejecuta:
    ```bash
    pip install .
    ```
    *(O `pip install -e .` si quieres seguir desarrollando).*

2.  **Configuración Global**:
    Crea una carpeta en tu usuario y copia el archivo `.env`:
    - **Windows**: `C:\Users\tu_usuario\.git-ai\.env`
    - **Linux/Mac**: `~/.git-ai/.env`

3.  **Uso en cualquier proyecto**:
    Ve a cualquier repositorio de Git y activa la IA:
    ```bash
    git-ai install  # Instala el hook en ese proyecto
    git-ai generate # Genera un commit manual
    ```

Ahora el comando `git-ai` estará disponible en todo tu sistema.

## ⚙️ Configuración (Multi-IA)
Puedes alternar entre diferentes proveedores editando el archivo `.env`:

1.  **Ollama (Local)**:
    - `AI_PROVIDER=ollama`
    - Configura `OLLAMA_MODEL` (ej. `qwen2.5-coder:7b`).
2.  **OpenAI**:
    - `AI_PROVIDER=openai`
    - Agrega tu `OPENAI_API_KEY`.
3.  **Gemini**:
    - `AI_PROVIDER=gemini`
    - Agrega tu `GEMINI_API_KEY`.
4.  **Anthropic (Claude)**:
    - `AI_PROVIDER=anthropic`
    - Agrega tu `ANTHROPIC_API_KEY`.

Cada vez que ejecutes `python src/main.py generate`, la herramienta usará el proveedor configurado automáticamente.

