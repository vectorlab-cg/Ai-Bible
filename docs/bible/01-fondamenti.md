# 1. Fondamenti

## 1.1 AI non significa solo modello

Un sistema AI va descritto su piu livelli:

- il modello fornisce capacita di previsione, classificazione o generazione;
- il contesto porta informazioni rilevanti per la richiesta;
- gli strumenti permettono di leggere dati, eseguire operazioni o chiamare servizi;
- la memoria conserva informazioni tra una fase e l'altra;
- il ciclo agentico pianifica, agisce, osserva il risultato e ripete;
- i controlli limitano cio che il sistema puo fare.

Un modello isolato e capace di produrre testo, ma non conosce automaticamente le fonti operative dell'organizzazione e non dovrebbe ricevere privilegi impliciti.

## 1.2 Modello, training e inference

Il training modifica i pesi del modello usando grandi quantita di dati. L'inference e l'uso del modello per produrre un risultato a partire da un input.

Il fine-tuning adatta un modello a un compito o stile piu specifico, ma ha costi di aggiornamento e valutazione. Quando la conoscenza deve cambiare spesso o deve restare separata dai pesi, il retrieval e il context engineering sono alternative piu adatte.

La scelta non e ideologica:

- usare RAG quando servono fonti aggiornabili e citabili;
- usare skill quando serve una procedura ripetibile;
- usare fine-tuning quando il comportamento o il formato devono essere stabilizzati su un compito;
- usare regole quando la decisione e esplicita e deterministica.

## 1.3 Dal dato alla conoscenza

Un dato isolato ha poco significato. Il contesto chiarisce da dove proviene e in quale situazione vale. Le relazioni mostrano come si collega ad altri elementi.

Per una Bibbia AI questo implica che ogni concetto dovrebbe avere:

- una definizione;
- il contesto di applicazione;
- le relazioni con altri concetti;
- esempi e controesempi;
- limiti e condizioni;
- una fonte verificabile.

Una risposta semanticamente simile non e automaticamente una risposta corretta. Il sistema deve recuperare la fonte giusta e usare il contesto corretto.

## 1.4 RAG e grounding

Retrieval Augmented Generation recupera informazioni da fonti esterne e le inserisce nel contesto del modello prima della generazione. Riduce la dipendenza dalla memoria interna del modello, ma non elimina gli errori.

Un RAG affidabile richiede:

1. estrazione corretta dal documento;
2. segmentazione che conservi il significato;
3. metadati e permessi coerenti;
4. ricerca lessicale e semantica;
5. citazioni verificabili;
6. valutazione su domande reali.

Nei documenti complessi, il significato puo dipendere da intestazioni, date, tabelle, definizioni e relazioni tra pagine. Spezzare il testo solo per numero di caratteri puo distruggere proprio quel contesto.

## 1.5 Allucinazione

Un modello genera una continuazione plausibile, non una garanzia di verita. L'allucinazione nasce quando il sistema riempie una lacuna con un contenuto non verificato.

Gli strumenti, il retrieval e i controlli possono ridurre il rischio, ma un agente introduce anche piu passaggi e quindi piu punti di possibile errore. Un errore che resta testo puo diventare un errore operativo quando l'agente aggiorna dati, crea ticket o chiama un servizio.

Regola pratica: quando una risposta deve essere vera, il sistema deve poter controllare una fonte o dichiarare di non poter verificare.

## Fonti di partenza

- `AI Simplified 6 Concepts You Need to Know About Modern AI`
- `5 AI Myths & The Truth Behind Them ML, Context, Agents & More`
- `Understanding AI Agent Hallucination in AI Systems`
- `Is Fine-Tuning Still Needed LLMs, RAG, & LoRA`
- `Why RAG Solutions Fail with Complex Documents & Vector Databases`
- `AI & Data Science Periodic Tables How They Work Together`
