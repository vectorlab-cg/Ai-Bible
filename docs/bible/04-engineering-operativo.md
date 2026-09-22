# 4. Engineering operativo

## 4.1 Il primo output non deve essere codice

Un sistema AI per lo sviluppo dovrebbe prima costruire comprensione e solo dopo modificare i file.

Prima di proporre una patch deve identificare:

- il problema e il risultato atteso;
- i file e i test pertinenti;
- le convenzioni architetturali del repository;
- i servizi, tipi e utility gia esistenti;
- i confini che non deve oltrepassare;
- i controlli necessari per verificare la modifica.

Un piano breve e verificabile permette alla persona responsabile di correggere la direzione prima che il codice renda costose le decisioni sbagliate.

## 4.2 La qualita e anche una proprieta del sistema

Codice leggibile, testabile e manutenibile resta importante. Nell'era dell'AI, pero, la qualita non coincide con la correttezza locale del codice.

Una modifica puo compilare e superare un test, ma essere comunque sbagliata se:

- duplica una utility esistente;
- introduce una dipendenza non necessaria;
- bypassa un service layer;
- ignora permessi, logging o gestione degli errori;
- contraddice l'architettura del repository;
- risolve il caso felice ma peggiora il comportamento operativo.

La domanda non e soltanto "funziona?". E anche "appartiene a questo sistema?".

## 4.3 Sicurezza durante la generazione

Il codice generato non e codice fidato. La verifica deve includere il risultato e le sue dipendenze.

Controllare almeno:

- autenticazione e autorizzazioni;
- esposizione o esfiltrazione di dati;
- gestione di input non validi;
- comportamento in caso di errore;
- segreti incorporati;
- pacchetti, licenze e vulnerabilita delle dipendenze;
- test statici, dinamici e di integrazione.

La sicurezza lasciata alla fine diventa un collo di bottiglia proprio quando la generazione accelera.

## 4.4 Osservabilita degli agenti

Metriche HTTP come codice di risposta, latenza e tasso di errore non spiegano da sole perche un agente abbia prodotto una risposta sbagliata.

L'osservabilita deve rendere visibili, secondo i permessi applicabili:

- input e output rilevanti;
- prompt e versione delle istruzioni;
- modello e configurazione usati;
- strumenti chiamati e relativi risultati;
- passaggi tra agenti;
- token, costi e latenza;
- errori, retry e interventi umani.

Il tracing serve a ricostruire il percorso completo, non a registrare indiscriminatamente ogni dato sensibile.

## 4.5 Valutare prima della produzione

Un benchmark generale non dimostra che un'applicazione funzioni nel proprio ambiente. La valutazione deve combinare modello, harness, dati e traffico realistico.

Misurare almeno:

- correttezza rispetto a una risposta attesa o a una rubrica;
- groundedness e qualita delle citazioni;
- robustezza su casi limite e input avversari;
- latenza e throughput;
- costo per richiesta e per risultato utile;
- tasso di escalation e intervento umano;
- regressioni tra versioni.

Un giudice automatico puo ridurre il lavoro di triage, ma va calibrato contro valutazioni umane esperte. Il suo punteggio e un segnale, non una prova assoluta.

## 4.6 Misurare gli esiti

Numero di token, richieste o suggerimenti accettati sono metriche di attività. Non dimostrano da sole valore.

Metriche piu significative dipendono dal processo, ma possono includere:

- tempo risparmiato senza aumento del rework;
- deployment completati correttamente;
- difetti o vulnerabilita risolti;
- tempo di risposta migliorato;
- casi risolti al primo tentativo;
- costo per outcome;
- qualita percepita dagli utenti.

L'obiettivo non e usare piu AI o meno AI in astratto. E ottenere risultati migliori con un livello di rischio e costo accettabile.

## Fonti di partenza

- `Agentic Engineering vs Software Engineering Beyond Vibe Coding`
- `Code Quality in the Age of AI Why Great Code Isn't Enough`
- `How AI Coding Agents Understand Your Codebase & Developer Tools`
- `How Developers Secure AI-Generated Code 5 Security Best Practices`
- `What Is MLflow Tracing AI Agents & LLM Workflows`
- `LLM & AI Agent Benchmarks vs Reality Why AI Applications Break`
- `Goodbye Tokenmaxxing From AI Usage to Agentic AI Outcomes`
