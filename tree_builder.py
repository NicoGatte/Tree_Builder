import os
import sys
import re

def parse_and_create(tree_text, base_path="."):
    lines = [line for line in tree_text.splitlines() if line.strip()]
    if not lines:
        print("❌ Nessun input fornito.")
        return

    # Stack per tracciare la gerarchia: lista di tuple (livello_indentazione, percorso_assoluto)
    stack = []

    for line in lines:
        # Trova l'inizio del nome effettivo del file/cartella ignorando i simboli dell'albero
        match = re.search(r'[^\s│├└──\-]', line)
        if not match:
            continue

        indent_pos = match.start()
        name = line[indent_pos:].strip()

        # Determina se è una cartella
        is_dir = name.endswith('/')
        clean_name = name.rstrip('/')

        # Rimuovi dallo stack gli elementi con indentazione uguale o maggiore
        while stack and stack[-1][0] >= indent_pos:
            stack.pop()

        # Calcola il percorso corrente
        if stack:
            parent_path = stack[-1][1]
            current_path = os.path.join(parent_path, clean_name)
        else:
            current_path = os.path.join(base_path, clean_name)

        # Salva nello stack se è una cartella o se finisce con '/'
        if is_dir:
            os.makedirs(current_path, exist_ok=True)
            print(f"📁 Cartella creata: {current_path}")
            stack.append((indent_pos, current_path))
        else:
            # Se ha estensione o non ha slash, assicurati che la cartella padre esista e crea il file
            parent_dir = os.path.dirname(current_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            
            # Crea il file se non esiste già
            if not os.path.exists(current_path):
                with open(current_path, 'w', encoding='utf-8') as f:
                    pass
                print(f"📄 File creato:     {current_path}")
            else:
                print(f"⚠️  File esistente:  {current_path}")

            # Nel caso in cui una cartella nell'albero non avesse il '/' finale
            # ma ha elementi figli dopo di sé, la teniamo nello stack
            stack.append((indent_pos, current_path))

def main():
    print("--- Tree Structure Generator ---")
    
    # Legge da pipe (es: type tree.txt | tree_builder.exe) o da argomento
    if not sys.stdin.isatty():
        content = sys.stdin.read()
    elif len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        print("Incolla la struttura dell'albero qui sotto (premi INVIO, poi CTRL+Z su Windows o CTRL+D su Linux/Mac e INVIO per confermare):\n i file verranno creati nella cartella corrente.'C:Users/ingga/Desktop/vscode/dist'\n")
        content = sys.stdin.read()

    print("\nCreazione della struttura in corso...\n")
    parse_and_create(content)
    print("\n✅ Struttura generata con successo!")

if __name__ == "__main__":
    main()