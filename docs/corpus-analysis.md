# Analisi iniziale del corpus

## Stato del corpus

Il materiale disponibile proviene da trascrizioni di video e contiene:

- 65 file totali;
- 63 file `.srt`;
- 2 file `.txt`;
- almeno un duplicato esatto: le due trascrizioni di `What Is MLflow Tracing...` hanno lo stesso SHA-256;
- trascrizioni automatiche con errori, ripetizioni, interruzioni e riferimenti temporali.

Le fonti originali sono esterne al repository e non devono essere committate.

## Principio editoriale

La Bibbia non sara una raccolta di trascrizioni ripulite. Sara una conoscenza derivata, organizzata e verificabile:

1. estrarre le idee dalle fonti;
2. separare definizioni, principi, procedure, esempi, rischi e opinioni;
3. unire i contenuti ripetuti;
4. segnalare conflitti e affermazioni dipendenti dalla data;
5. riscrivere i capitoli in forma autonoma e coerente;
6. mantenere la provenienza senza conservare il testo integrale nella versione finale;
7. verificare il capitolo prima di eliminare le fonti di lavorazione.

## Prima mappa tematica

### Fondamenti

- AI, ML, LLM e generative AI;
- training, inference, fine-tuning e LoRA;
- embeddings, vector database e RAG;
- context engineering, memory, tools e agentic harness;
- hallucination, reasoning e limiti dei benchmark.

### Architettura e decisioni

- scelta tra persone, regole, ML e generative AI;
- agenti rispetto a business rules;
- RAG per documenti complessi e approcci chunkless;
- model selection, routing, costi e prestazioni;
- GPU, CPU, llama.cpp e vLLM;
- quando non usare l'AI.

### Engineering e sviluppo

- agentic engineering rispetto al software engineering;
- AI coding, code review e qualita del codice;
- consapevolezza del repository e contesto architetturale;
- skills e progressive disclosure;
- MLflow tracing e osservabilita;
- produttivita, outcome e valutazione dei risultati.

### Sicurezza e governance

- prompt injection e red teaming;
- eccesso di privilegi e controllo degli agenti;
- sandbox, containment e accesso al web;
- sicurezza del codice generato;
- AI management system, ISO 42001, NIST e AI Act;
- sovranita digitale e controllo dei dati;
- data breach, remediation e threat intelligence.

### News e contenuti temporali

Le puntate su modelli, acquisizioni, partnership, report annuali e incidenti saranno una sezione separata. Non devono diventare principi permanenti senza una verifica indipendente della data e della fonte.

## Schema minimo dei contenuti derivati

Ogni concetto o capitolo dovrebbe avere almeno:

- `id` stabile;
- `title`;
- `domain`;
- `type`: definition, principle, procedure, comparison, risk, example o case-study;
- `summary`;
- `claims` verificabili;
- `practical_implications`;
- `limitations`;
- `related_concepts`;
- `source_ids`;
- `status`: extracted, reviewed o approved;
- `temporal_scope`, quando il contenuto puo invecchiare.

## Pipeline prevista

`SRT/TXT originali -> parsing dei timestamp -> testo normalizzato -> segmenti concettuali -> concetti atomici -> capitoli -> revisione -> indice finale`

Il parser deve conservare temporaneamente `start_time` e `end_time`, cosi ogni affermazione puo essere ricondotta alla lezione di origine durante la revisione.

La prima segmentazione automatica ha prodotto 383 blocchi di lavorazione, con un massimo di 750 parole per blocco. La classificazione aggiornata ha trovato 1.363 collegamenti tra segmenti e concetti su tutti i 383 segmenti; un saluto finale e marcato come esclusione editoriale. I blocchi completi e la mappa dei candidati sono stati scritti nella cartella esterna `vectorlab-working`, non nel repository. Il repository conserva soltanto gli strumenti e i metadati necessari a ripetere il processo.

La matrice di copertura e disponibile in `docs/source-coverage.json`. Tutte le 65 fonti hanno almeno un segmento associato e tutti i 383 segmenti hanno un candidato concettuale, ma questo non dimostra che tutto il contenuto sia gia confluito nei capitoli. La distinzione tra copertura del corpus e copertura editoriale e descritta in [coverage-review.md](coverage-review.md).

## Regola di eliminazione

Le fonti originali potranno essere eliminate solo quando:

- tutti i segmenti utili sono stati processati;
- i duplicati sono stati identificati;
- i capitoli derivati sono stati revisionati;
- i riferimenti di provenienza sono stati registrati;
- il contenuto finale e stato esportato e verificato.

La loro eliminazione dal filesystem non rimuoverebbe eventuali copie gia committate nella storia Git; per questo le fonti non devono entrare nel repository.
