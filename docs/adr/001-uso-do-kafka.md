# 001. Adoção do Apache Kafka para Processamento de Stream de Dados

* **Status:** Aceito
* **Data:** 2025-11-28
* **Decisores:** [Seu Nome/Cargo]
* **Tags:** infra, dados, streaming, kafka

## Contexto e Problema
O projeto requer um sistema de mensageria para processar dados de entrada para os modelos de ML em tempo real. Os requisitos principais são:
1.  **Desacoplamento:** Produtores de dados (scrapers/APIs) não devem impactar a performance do consumidor (Modelo de ML).
2.  **Replayability (Rejogabilidade):** Capacidade de reprocessar dados passados para re-treino de modelos ou correção de bugs (feature vital para MLOps).
3.  **Escalabilidade:** Suportar picos de tráfego sem perda de dados.

Precisamos de uma solução que atenda a isso mantendo a filosofia de **mínima infraestrutura viável**.

## Opções Consideradas

* **Opção 1: RabbitMQ**
    * *Pros:* Leve, fácil de configurar, ótimo para roteamento complexo.
    * *Contras:* Retenção de mensagens a longo prazo (Log) é custosa e difícil; focado em filas, não em streaming de logs persistentes.
* **Opção 2: Google Pub/Sub (ou AWS SQS/Kinesis)**
    * *Pros:* Totalmente gerenciado (Serverless), zero infraestrutura para manter.
    * *Contras:* Custo pode escalar linearmente e tornar-se imprevisível; vendor lock-in.
* **Opção 3: Apache Kafka**
    * *Pros:* Padrão da indústria, alta vazão (throughput), persistência em disco nativa (excelente para ML Feature Store), ecossistema rico.
    * *Contras:* Historicamente pesado (JVM + Zookeeper).

## Decisão
Escolhemos a **Opção 3: Apache Kafka**.

Para mitigar o consumo de recursos (alinhado aos princípios do projeto), utilizaremos o Kafka em modo **KRaft (Kafka Raft Metadata mode)**.

### Justificativa Técnica
1.  **MLOps:** O Kafka permite que configuremos um `retention.ms` longo, permitindo que novos modelos "leiam o passado" para treino inicial sem precisar buscar em um Data Lake separado.
2.  **Eficiência (KRaft):** O modo KRaft remove a dependência do Zookeeper. Isso significa menos um serviço para gerenciar, menos consumo de CPU/RAM e uma arquitetura mais simples (um único binário).
3.  **Compatibilidade:** Integração nativa com Spark Structured Streaming e bibliotecas Python (faust, confluent-kafka).

## Consequências

### Positivas
* Arquitetura orientada a eventos robusta.
* Centralização da ingestão de dados.
* Eliminação do Zookeeper reduz a pegada de infraestrutura em cerca de 40% comparado ao Kafka legado.

### Negativas / Riscos
* **Curva de Aprendizado:** Operar Kafka (mesmo sem Zookeeper) é mais complexo que RabbitMQ.
* **Recursos:** Mesmo otimizado, a JVM consome mais memória base que soluções em Go ou C++. É necessário monitoramento rigoroso da *heap size*.

## Notas de Implementação
* Utilizar imagem Docker `bitnami/kafka` configurada com `KAFKA_CFG_PROCESS_ROLES=controller,broker` (modo combinado para economizar nodes).