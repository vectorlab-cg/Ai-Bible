# 3. Rischio, sicurezza e governance

## 3.1 Il rischio viene prima dell'architettura

La relazione corretta e:

`rischio -> requisiti -> architettura -> implementazione -> verifica`

Un principio come trasparenza o explainability e una dichiarazione di intenti. Per diventare utile deve essere tradotto in requisiti funzionali e non funzionali che un team possa implementare, testare e contrattualizzare.

Il livello di controllo deve essere proporzionato alla conseguenza dell'errore. Una raccomandazione di intrattenimento puo richiedere una spiegazione semplice; una decisione sanitaria, finanziaria o di accesso richiede tracciabilita, provenienza, test, riesame e responsabilita.

## 3.2 Modelli probabilistici, controlli deterministici

Le istruzioni nel prompt possono orientare il modello, ma non sono un controllo sufficiente. Un modello probabilistico puo interpretare una regola in modo inatteso o privilegiare il raggiungimento dell'obiettivo.

I confini critici devono essere applicati fuori dal modello:

- autorizzazioni esplicite e a privilegio minimo;
- allowlist di strumenti e destinazioni;
- sandbox e isolamento di rete;
- conferma umana per azioni irreversibili;
- logging completo delle chiamate e dei risultati;
- limiti di costo, tempo, dati e numero di tentativi;
- revoca immediata dell'accesso.

Un agente va trattato come un'identita privilegiata, non come un semplice testo generato.

## 3.3 Containment e prompt injection

Prompt injection, contenuti ostili e tool troppo permissivi possono spingere l'agente verso azioni non previste. La domanda non e solo se il modello sa rifiutare una richiesta, ma cosa puo fare se viene manipolato.

La difesa deve considerare l'intera catena:

1. contenuto ricevuto;
2. modello e istruzioni;
3. strumenti disponibili;
4. permessi dell'identita;
5. rete e sistemi raggiungibili;
6. validazione dell'azione;
7. audit e risposta all'incidente.

La sicurezza del modello non sostituisce la sicurezza dell'ambiente di esecuzione.

## 3.4 Governance continua

Un AI management system deve coprire contesto, responsabilita, valutazione del rischio, operazioni, monitoraggio, audit e miglioramento. Non e una checklist da compilare una volta.

Per ogni sistema occorre sapere:

- chi e il proprietario;
- quali dati usa e dove transitano;
- quali decisioni puo influenzare;
- quali sono i rischi accettati;
- come viene valutato prima e dopo il rilascio;
- cosa accade quando il modello cambia o fallisce;
- come una persona puo contestare o correggere il risultato.

## 3.5 Valutare il sistema, non solo il modello

Un benchmark del modello non dimostra che l'applicazione sia pronta. La valutazione deve coprire almeno:

- accuratezza e groundedness;
- latenza e capacita sotto carico;
- costo per richiesta e costo operativo;
- sicurezza e resistenza agli attacchi;
- qualita delle citazioni;
- comportamento sui casi limite;
- risultati effettivi per utenti e organizzazione.

Un sistema deve essere verificato con domande, traffico e vincoli simili a quelli reali. LLM-as-a-judge puo aiutare, ma richiede rubriche chiare e controllo umano sui punteggi.

## Fonti di partenza

- `Why Risk Should Determine Your AI Architecture`
- `Why won't AI agents just follow the rules`
- `How to Manage Your AI Before It Makes the Wrong Decision`
- `The OWASP LLM Top 10 has a few surprises for you`
- `How Developers Secure AI-Generated Code 5 Security Best Practices`
- `Hugging Face breach OpenAI's model breaks containment`
- `Oh look. Anthropic's AI models also broke containment.`
- `What Is Digital Sovereignty AI, Data & Control Explained`
