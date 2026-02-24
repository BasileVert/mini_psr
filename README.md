# Mini Enregistreur de Procedure

Outil Python minimal pour capturer une zone d'ecran a chaque clic souris.

## Fonctionnalites

- Selection d'une zone rectangulaire (multi-ecrans)
- Demarrage de l'enregistrement
- Capture PNG a chaque clic global dans la periode d'enregistrement
- Pause / reprise
- Arret
- Sauvegarde dans un dossier `procedure_YYYY-MM-DD_HH-MM-SS` avec:
  - `1.png`, `2.png`, ...
  - `steps.json` avec `step` et `file`

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

## Utilisation

1. Cliquer sur `Selectionner une zone`
2. Dessiner la zone a capturer
3. Cliquer sur `Demarrer`
4. Utiliser `Pause` / `Reprendre` si besoin
5. Cliquer sur `Arreter`

## Structure

```text
procedure_recorder/
  main.py
  ui.py
  selector.py
  recorder.py
  utils.py
```
