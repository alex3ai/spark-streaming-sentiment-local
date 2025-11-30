#!/bin/bash

# ==============================================================================
# SCRIPT: generate_context_summary.sh
# DESCRIÇÃO: Gera um arquivo único contendo a estrutura e o conteúdo dos arquivos
#            do projeto para facilitar a análise por IAs (ChatGPT, Gemini, Claude).
# AUTOR: Lab Engenharia de Dados - Projeto 12 (S2v2)
# DATA: $(date +%Y-%m-%d)
# ==============================================================================

# Nome do arquivo de saída
OUTPUT_FILE="project_summary_for_ai.txt"

# Limpa o arquivo anterior se existir
echo "🔄 Iniciando geração do resumo do projeto..."
echo "==============================================================================" > "$OUTPUT_FILE"
echo "PROJETO: LAB ENGENHARIA DE DADOS (SPARK / KAFKA / DOCKER) - FASE S2" >> "$OUTPUT_FILE"
echo "Data de Geração: $(date)" >> "$OUTPUT_FILE"
echo "==============================================================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 1. Estrutura de Diretórios (Tree)
echo "### ESTRUTURA DE DIRETÓRIOS ###" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Verifica se o comando 'tree' existe
if command -v tree &> /dev/null; then
    # Ignora pastas de controle de versão, cache, builds e dados voláteis
    # Adicionado: .venv, build, data, kafka_data, img, egg-info
    tree -a -I '.git|.venv|venv|__pycache__|.pytest_cache|.mypy_cache|build|dist|*.egg-info|data|kafka_data|img|.vscode|.idea' >> "$OUTPUT_FILE"
else
    # Fallback robusto para 'find' caso não tenha 'tree'
    echo "." >> "$OUTPUT_FILE"
    find . -maxdepth 4 -not -path '*/.*' \
        -not -path './build*' \
        -not -path './dist*' \
        -not -path './data*' \
        -not -path './kafka_data*' \
        -not -path './img*' \
        -not -path './*egg-info*' \
        -not -path './__pycache__*' \
        | sed -e 's/[^-][^\/]*\//|-- /g' -e 's/^/|-- /' | sort >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# 2. Conteúdo dos Arquivos
echo "##############################################################################" >> "$OUTPUT_FILE"
echo "############################# CONTEÚDO DOS ARQUIVOS ##########################" >> "$OUTPUT_FILE"
echo "##############################################################################" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Lista de arquivos para leitura
# Inclui arquivos de configuração, documentação e código fonte
FILES_TO_READ=$(find . -type f \
    \( -name "*.py" \
    -o -name "*.yml" \
    -o -name "*.yaml" \
    -o -name "Dockerfile" \
    -o -name "Makefile" \
    -o -name "*.toml" \
    -o -name "*.md" \
    -o -name ".editorconfig" \
    -o -name ".gitignore" \
    -o -name ".flake8" \
    -o -name "LICENSE" \) \
    -not -path './.git/*' \
    -not -path './.venv/*' \
    -not -path './venv/*' \
    -not -path './build/*' \
    -not -path './dist/*' \
    -not -path './*.egg-info/*' \
    -not -path './__pycache__/*' \
    -not -path './data/*' \
    -not -path './kafka_data/*' \
    -not -path './img/*' \
    -not -name "$OUTPUT_FILE" \
    -not -name "generate_context_summary.sh" \
    -not -name "poetry.lock" \
    | sort)

# Loop para ler e formatar o conteúdo
count=0
for file in $FILES_TO_READ; do
    ((count++))
    echo "📄 Lendo: $file"

    echo "==============================================================================" >> "$OUTPUT_FILE"
    echo "ARQUIVO: $file" >> "$OUTPUT_FILE"
    echo "==============================================================================" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

    # Lê o arquivo
    cat "$file" >> "$OUTPUT_FILE"

    echo "" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
done

echo ""
echo "✅ Concluído!"
echo "📊 Total de arquivos processados: $count"
echo "📂 O arquivo '$OUTPUT_FILE' está pronto para ser enviado à IA."
