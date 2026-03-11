# AI Auto-Commit Tool 🤖

Genera mensajes de commit profesionales automáticamente usando IA local (**Ollama**).

## 🚀 Requisitos Precios

1. **Instalar Ollama**: Descárgalo en [ollama.com](https://ollama.com).
2. **Descargar el Modelo**: Ejecuta `ollama pull qwen2.5-coder:7b`.
3. **Mantener Ollama Abierto**: La herramienta se comunica con el servidor local de Ollama.

## 🛠️ Instalación

1. Clona este repositorio o copia los archivos.
2. Crea el entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Instala el Hook de Git (opcional pero recomendado):
   ```bash
   python src/main.py install
   ```

## 📖 Uso

### Generar Commit Manualmente
Si tienes cambios en el stage (`git add .`), ejecuta:
```bash
python src/main.py generate
```

### Generar Commit Automáticamente (vía Hook)
Si instalaste el hook, cada vez que ejecutes `git commit`, la herramienta analizará los cambios y escribirá el mensaje por ti.

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

