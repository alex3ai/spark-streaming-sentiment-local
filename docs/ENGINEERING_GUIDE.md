# GEMINI.md - Contexto do Projeto & Diretrizes de Engenharia

> **Nota para IA:** Este arquivo contém as "Leis Universais" deste projeto. Leia-o antes de sugerir alterações arquiteturais ou de código.

## 1. Identidade do Projeto
* **Nome:** Spark Streaming + Kafka (Zero Custo/Low Ops)
* **Objetivo:** Processamento de dados em tempo real com arquitetura orientada a eventos, focando em eficiência máxima de recursos (CPU/RAM).
* **Perfil do Engenheiro:** MLE & SRE Sênior. Prioriza robustez, escalabilidade e economia (FinOps).

## 2. Princípios de Engenharia (The "Gold Standard")
1.  **Economia Radical (FinOps):** Nunca suba um serviço se ele não for essencial. Ex: Usamos Kafka em modo KRaft para eliminar o custo do Zookeeper.
2.  **Infraestrutura Mínima:** Containers devem ter limites de recursos (`deploy.resources`) definidos. Nada de "ilimitado".
3.  **Shift-Left Quality:** Erros devem ser pegos no commit, não no CI. Uso obrigatório de `pre-commit`.
4.  **Caminhos Absolutos:** Em Docker/Produção, nunca confie em caminhos relativos. Use `/opt/spark/bin/...` explicitamente.
5.  **Documentação Viva:** Toda decisão complexa deve virar uma ADR (`docs/adr/`).
6.  **Commits Atômicos:** Um contexto lógico = Um commit. Mensagens em Inglês seguindo Conventional Commits (`feat:`, `fix:`, `infra:`, `docs:`).

## 3. Stack Tecnológico & Decisões (ADRs)

### Infraestrutura (Docker & Serviços)
* **Apache Kafka (KRaft Mode):**
    * *Imagem:* `apache/kafka:3.7.0` (Oficial, evitando tags flutuantes da Bitnami).
    * *Por que:* Elimina dependência do Zookeeper (-512MB RAM).
* **Apache Spark (Standalone Cluster):**
    * *Imagem:* Customizada baseada em `python:3.10-slim-bookworm`.
    * *Base OS:* Debian Bookworm (Estável) para garantir suporte ao Java 17.
    * *Master/Worker:* Separados, mas com recursos travados (1 Core, 512MB-1GB RAM).
* **Orquestração:** `docker-compose.yml` na raiz.

### Desenvolvimento (Python & Tooling)
* **Linguagem:** Python 3.10+.
* **Libs Principais:** `pyspark` (Processamento), `kafka-python-ng` (Ingestão leve).
* **Automação:** `Makefile` para abstrair comandos Docker longos.
* **Qualidade:** `pre-commit` com `black` (formatação), `flake8` (linting) e `trailing-whitespace`.

## 4. Estrutura de Diretórios Crítica
```text
.
├── app/
│   ├── jobs/          # Scripts Spark (Executados dentro do container)
│   ├── schemas/       # Definições de Schema (StructType)
│   └── producer.py    # Script local para gerar dados de teste
├── docs/
│   └── adr/           # Registros de Decisão de Arquitetura (MADR)
├── infra/
│   └── Dockerfile     # Imagem Otimizada do Spark (Multi-stage/Slim)
├── docker-compose.yml # Definição da Infraestrutura
├── Makefile           # Atalhos de comandos (make up, make logs)
└── GEMINI.md          # Este arquivo

Aqui está uma proposta robusta para o seu arquivo GEMINI.md.Este arquivo servirá como o "cérebro" do projeto. Sempre que você (ou outra IA) precisar entender o contexto, a arquitetura e as regras de ouro deste repositório, basta ler este arquivo. Ele reflete exatamente o seu perfil T-Shaped (MLE + SRE) e a filosofia de custo zero.Salve-o na raiz do projeto como GEMINI.md.Markdown# GEMINI.md - Contexto do Projeto & Diretrizes de Engenharia

> **Nota para IA:** Este arquivo contém as "Leis Universais" deste projeto. Leia-o antes de sugerir alterações arquiteturais ou de código.

## 1. Identidade do Projeto
* **Nome:** Spark Streaming + Kafka (Zero Custo/Low Ops)
* **Objetivo:** Processamento de dados em tempo real com arquitetura orientada a eventos, focando em eficiência máxima de recursos (CPU/RAM).
* **Perfil do Engenheiro:** MLE & SRE Sênior. Prioriza robustez, escalabilidade e economia (FinOps).

## 2. Princípios de Engenharia (The "Gold Standard")
1.  **Economia Radical (FinOps):** Nunca suba um serviço se ele não for essencial. Ex: Usamos Kafka em modo KRaft para eliminar o custo do Zookeeper.
2.  **Infraestrutura Mínima:** Containers devem ter limites de recursos (`deploy.resources`) definidos. Nada de "ilimitado".
3.  **Shift-Left Quality:** Erros devem ser pegos no commit, não no CI. Uso obrigatório de `pre-commit`.
4.  **Caminhos Absolutos:** Em Docker/Produção, nunca confie em caminhos relativos. Use `/opt/spark/bin/...` explicitamente.
5.  **Documentação Viva:** Toda decisão complexa deve virar uma ADR (`docs/adr/`).
6.  **Commits Atômicos:** Um contexto lógico = Um commit. Mensagens em Inglês seguindo Conventional Commits (`feat:`, `fix:`, `infra:`, `docs:`).

## 3. Stack Tecnológico & Decisões (ADRs)

### Infraestrutura (Docker & Serviços)
* **Apache Kafka (KRaft Mode):**
    * *Imagem:* `apache/kafka:3.7.0` (Oficial, evitando tags flutuantes da Bitnami).
    * *Por que:* Elimina dependência do Zookeeper (-512MB RAM).
* **Apache Spark (Standalone Cluster):**
    * *Imagem:* Customizada baseada em `python:3.10-slim-bookworm`.
    * *Base OS:* Debian Bookworm (Estável) para garantir suporte ao Java 17.
    * *Master/Worker:* Separados, mas com recursos travados (1 Core, 512MB-1GB RAM).
* **Orquestração:** `docker-compose.yml` na raiz.

### Desenvolvimento (Python & Tooling)
* **Linguagem:** Python 3.10+.
* **Libs Principais:** `pyspark` (Processamento), `kafka-python-ng` (Ingestão leve).
* **Automação:** `Makefile` para abstrair comandos Docker longos.
* **Qualidade:** `pre-commit` com `black` (formatação), `flake8` (linting) e `trailing-whitespace`.

## 4. Estrutura de Diretórios Crítica
```text
.
├── app/
│   ├── jobs/          # Scripts Spark (Executados dentro do container)
│   ├── schemas/       # Definições de Schema (StructType)
│   └── producer.py    # Script local para gerar dados de teste
├── docs/
│   └── adr/           # Registros de Decisão de Arquitetura (MADR)
├── infra/
│   └── Dockerfile     # Imagem Otimizada do Spark (Multi-stage/Slim)
├── docker-compose.yml # Definição da Infraestrutura
├── Makefile           # Atalhos de comandos (make up, make logs)
└── GEMINI.md          # Este arquivo

## 5. Comandos Frequentes (Cheat Sheet)AçãoComandoDescriçãoSubir Inframake upSobe Kafka + Spark (Build force)Derrubar Inframake downRemove containers e redesLogsmake logsAcompanha logs em tempo realRodar Jobdocker exec -it spark-master /opt/spark/bin/spark-submit ...Submete job ao clusterSetup Localmake setupInstala pre-commit e libs locais

Nota Final: Ao interagir com este projeto, mantenha o tom profissional, técnico e focado na solução. Priorize sempre a solução que consome menos memória RAM.
