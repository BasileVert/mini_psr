# Mini Enregistreur de Procedure

Outil Python minimal pour capturer une zone d'ecran a chaque clic souris.

## Fonctionnalites

- Selection d'une zone rectangulaire (multi-ecrans)
- Demarrage de l'enregistrement
- Capture PNG uniquement si le clic est dans la zone selectionnee
- Annotation visuelle du clic (cercle rouge) sur chaque image capturee par clic
- Option pour capturer aussi la touche `Enter`
- Compression PNG optimisee pour reduire la taille des fichiers
- Pause / reprise
- Arret
- Sauvegarde dans un dossier `procedure_YYYY-MM-DD` avec:
  - `1.png`, `2.png`, ...
  - `steps.json` avec `step`, `file` et `event` (`click` ou `enter`)

## Prerequis

- Python 3.10+
- Windows/macOS/Linux (permissions systeme de capture selon l'OS)

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python procedure_recorder/main.py
```

## Build .exe portable (Windows)

```bash
build_exe.bat
```

- L'executable est genere dans `dist\mini_psrv1.0.0_win.exe`
- En mode `.exe`, les captures sont enregistrees a cote de `mini_psrv1.0.0_win.exe`
- Dossier de sortie: `procedure_YYYY-MM-DD`

## Build macOS (binaire portable)

```bash
chmod +x build_macos.sh
./build_macos.sh
```

- Binaire genere: `dist/mini_psrv1.0.0_macos`

## Build Linux (binaire portable)

```bash
chmod +x build_linux.sh
./build_linux.sh
```

- Binaire genere: `dist/mini_psrv1.0.0_linux`

## Utilisation

1. Cliquer sur `Selectionner une zone`
2. Dessiner la zone a capturer
3. Activer `Capturer la touche Entree` si necessaire
4. Cliquer sur `Demarrer`
5. Cliquer dans la zone pour capturer des etapes annotees
6. Appuyer sur `Enter` pour capturer une etape clavier (option activee)
7. Utiliser `Pause` / `Reprendre` si besoin
8. Cliquer sur `Arreter`

## Structure

```text
procedure_recorder/
  main.py
  ui.py
  selector.py
  recorder.py
  utils.py
```

## Licence

MIT - voir `LICENSE`.
