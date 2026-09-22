# 2. Architettura e scelta del metodo

## 2.1 Il modello e il suo harness

Le prestazioni percepite di un prodotto AI non dipendono solo dal modello. L'harness comprende strumenti, memoria, regole operative, ciclo di esecuzione, verifica e accesso ai dati.

Un agente puo essere rappresentato cosi:

`modello + contesto + strumenti + memoria + ciclo plan/act/observe + controlli`

La stessa rete neurale puo comportarsi in modo molto diverso se viene collegata a file, terminale, database, web o servizi esterni. Per questo l'architettura deve essere valutata come sistema completo.

## 2.2 Quattro modi di risolvere un problema

| Metodo | Usarlo quando | Limite principale |
|---|---|---|
| Persona | servono giudizio, responsabilita o gestione dell'ambiguita | costo, lentezza e scarsa scalabilita |
| Regola o codice | la logica e esplicita, stabile e deterministica | non generalizza casi imprevisti |
| Machine learning | esistono pattern in dati strutturati e servono previsioni | drift e spiegabilita variabile |
| Generative AI o agente | input non strutturati, interpretazione e sintesi | non determinismo, costo e rischio operativo |

Non sono gradini obbligatori. La domanda corretta e quale metodo minimizza il rischio e la complessita per quel problema.

## 2.3 Regole e agenti insieme

Le business rules producono un risultato prevedibile da condizioni esplicite. Gli agenti interpretano contesto e possono gestire casi che non erano stati previsti.

Un'architettura ibrida usa spesso:

1. regole per i casi semplici, sensibili o ad alta certezza;
2. agente per interpretare input ambigui o non strutturati;
3. regole finali e approvazione umana prima di un'azione irreversibile.

Questo evita di usare un modello probabilistico per una decisione che richiede logica booleana e audit deterministico.

## 2.4 Quattro forme di conoscenza per un agente

### Skill

Una skill contiene conoscenza procedurale: passi, condizioni, esempi, errori frequenti e criteri di escalation. Il suo valore e il modo specifico di svolgere un compito, non la ripetizione di istruzioni generiche.

### MCP

Model Context Protocol collega un agente a sistemi esterni tramite server che espongono strumenti. La skill puo dire cosa controllare; MCP fornisce il collegamento per farlo.

### RAG

RAG recupera contenuto informativo al momento della richiesta. E adatto a documenti, policy, manuali e fonti che cambiano.

### Memoria

La memoria conserva informazioni utili tra richieste o sessioni. Non dovrebbe diventare un deposito indistinto: servono scopo, durata, proprietario e regole di cancellazione.

## 2.5 Progressive disclosure

Un catalogo di skill non dovrebbe caricare tutte le istruzioni nel contesto iniziale. E preferibile caricare prima nome e descrizione, poi il corpo della skill quando il compito la richiede, e infine riferimenti o script solo quando necessari.

Lo stesso principio vale per la Bibbia: l'indice deve aiutare a trovare il capitolo, il capitolo deve fornire il concetto, e le fonti devono essere consultate solo per verifica o approfondimento.

## Fonti di partenza

- `AI Model vs Agentic Harness What Actually Drives AI`
- `Skills vs MCP vs RAG vs Memory What AI Agents Need to Know`
- `What AI Agent Skills Are and How They Work`
- `5 Best Practices for Building AI Agent Skills`
- `AI Agents vs Business Rules Which Should Make Decisions`
- `Knowing When Not to Use AI AI Agents vs Rules vs ML`
- `What Is Chunkless RAG How Docling & AI Agents Navigate Documents`
