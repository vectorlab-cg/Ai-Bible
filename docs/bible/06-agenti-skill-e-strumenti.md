# 6. Agenti, skill e strumenti

## 6.1 Che cosa rende un sistema agentico

Un agente non e semplicemente un modello che risponde. E un sistema che riceve un obiettivo, pianifica passi, usa strumenti, osserva risultati e aggiorna il piano.

Schema minimo:

`obiettivo -> piano -> azione -> osservazione -> verifica -> prossimo passo`

Il ciclo aumenta la capacita, ma anche il numero di punti in cui possono comparire errori o azioni indesiderate.

## 6.2 Skill: conoscenza procedurale

Una skill insegna come eseguire un compito specifico. Il valore non sta in istruzioni generiche come "gestisci gli errori", ma in conoscenza concreta:

- ordine dei passaggi;
- condizioni per scegliere un percorso;
- eccezioni e gotcha;
- criteri di successo;
- criteri di stop;
- momento in cui chiedere aiuto umano;
- esempi verificati.

Le correzioni manuali ripetute sono segnali di conoscenza procedurale mancante e dovrebbero diventare parte della skill.

## 6.3 Progressive disclosure

Un agente con molte skill non deve caricare tutte le istruzioni nel contesto iniziale. Prima usa nome e descrizione per decidere quali skill possono servire, poi carica le istruzioni e infine eventuali riferimenti o script.

Questo riduce rumore e costo, ma rende la descrizione una parte critica del comportamento: se e vaga, la skill puo non attivarsi; se e troppo ampia, puo attivarsi nel momento sbagliato.

## 6.4 Strumenti e MCP

Gli strumenti danno all'agente la possibilita di agire su file, terminale, database, web e servizi esterni. MCP puo standardizzare il collegamento tra l'harness e questi sistemi.

Ogni strumento deve avere:

- scopo limitato;
- schema di input e output;
- permessi minimi;
- timeout e limiti di costo;
- gestione degli errori;
- logging;
- proprietario e ciclo di revisione.

Un catalogo grande di strumenti non e automaticamente migliore: aumenta il rischio di scelta errata e di combinazioni inattese.

## 6.5 Memoria

La memoria di un agente deve distinguere almeno:

- contesto temporaneo della richiesta;
- memoria della sessione;
- conoscenza persistente del progetto;
- preferenze o dati personali.

Ogni memoria deve avere durata, fonte, livello di fiducia e regola di cancellazione. Conservare tutto senza controllo crea rumore, rischio privacy e informazioni obsolete.

## 6.6 Human in the loop

L'intervento umano non e un fallimento dell'agente. E un controllo architetturale per i casi ambigui, ad alto impatto o irreversibili.

Definire in anticipo quando l'agente deve:

- fermarsi;
- chiedere conferma;
- proporre ma non eseguire;
- escalare a un responsabile;
- annullare o ripristinare un'azione.

La soglia deve dipendere dal rischio, non dalla comodita della demo.

## Fonti di partenza

- `Skills vs MCP vs RAG vs Memory What AI Agents Need to Know`
- `5 Best Practices for Building AI Agent Skills`
- `What AI Agent Skills Are and How They Work`
- `AI Model vs Agentic Harness What Actually Drives AI`
- `Why Does AI Need Access to the Web`
- `When Should AI Systems Use Super Agents`
