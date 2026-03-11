# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2026-03-11
### Fixed
- Updated Gemini SDK from `google-generativeai` to `google-genai` to resolve deprecation warnings and future-proof the integration.
- Resolved "Leaked API Key" error by guiding the user to reset security credentials.
### Changed
- Refined project dependencies in `pyproject.toml` and `requirements.txt`, removing unused `langchain` packages.
- Enhanced branch management following `fix/*` naming convention.

## [0.1.1] - 2026-03-11
### Added
- New command `git-ai config init` to automate the creation of the global configuration folder (`.git-ai`) and `.env` template.
### Changed
- Updated `README.md` with improved installation and configuration instructions.

## [0.1.0] - 2026-03-11
### Added
- Initial release of AuraGit.
- Support for multiple AI providers: Ollama, OpenAI, Gemini, and Anthropic.
- Automatic commit message generation following Conventional Commits.
- Integration as a Git Hook (`prepare-commit-msg`).
- Multilingual support (English and Spanish).
