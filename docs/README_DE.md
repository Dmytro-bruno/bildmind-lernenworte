# Bildmind-lernenworte – Vokabellernen mit KI

Dieses Repository enthält das **öffentliche Modul** des Projekts **BuildMind**,  
das für das **effiziente Erlernen von Fremdsprachenvokabular**  
mithilfe eines adaptiven Wiederholungssystems, Beispielen, Tests und Statistiken entwickelt wurde.

---

## 🎯 Zweck

Das Modul `LernenWorte` (Wortlernen) implementiert ein MVP-System für:

- das Hinzufügen eigener Wörter zum persönlichen Wörterbuch
- individuelles Wiederholen basierend auf Intervallen
- das Durchführen von täglichen Tests
- das Führen von persönlicher Statistik und Fortschrittsverfolgung

> Der Benutzer fügt ein Wort hinzu → das System plant Wiederholungen → der Benutzer macht Tests → Langzeitgedächtnis wird aufgebaut.

---

## 🧩 Hauptkomponenten

- `main.py` — Einstiegspunkt der FastAPI-Anwendung
- `alembic/` — Migrationssystem für die Datenbank
- `api/` — HTTP-Endpunkte für Benutzerinteraktion
- `config/` — Umgebungsvariablen und globale Einstellungen
- `core/` — Grundlegende Business-Logik ohne KI
- `crud/` — Basisoperationen mit der Datenbank (create/read/update/delete)
- `db/` — Datenbankmodelle und Schemas:
- `models/` — ORM-Modelle mit SQLAlchemy
- `schemas/` — Pydantic-Schemas für Anfragen und Antworten
- `database.py` — Datenbankverbindung
- `init_data.py` — Initialdaten
- `deps/` — Abhängigkeiten für Endpunkte (z. B. aktueller Benutzer, Sicherheit)
- `sdk/` — SDK oder Client-Interface für mobile Anwendungen

---

## 💾 Entitäten

- **User** – Basisinformationen über den Benutzer
- **Word** – Globales Wörterbuch
- **UserWord** – Benutzerdefinierte Lernwörter
- **TestSession** – Testverlauf
- **UserStats / DailyProgress / LevelProgress** – Lernfortschritt und Motivation

---

## 🔐 Besonderheiten

- Adaptives Wiederholungssystem (Spaced Repetition)
- Soft-Delete für Wörter (verstecken statt löschen)
- Unterstützung mehrerer Sprachen und Schwierigkeitsstufen
- JSON Web Token (JWT) Autorisierung
- Kompatibel mit FastAPI, SQLAlchemy und Alembic

---

## 🚀 Deployment

### 1. Klonen des Repositories

```bash
git clone https://github.com/your-org/BuildMind-LernenWorte.git
cd BuildMind-LernenWorte
```
## 👤 Autor

Dieses Projekt wurde initiiert und wird gepflegt von:  
Dmytro Movchan | bildmind.com

## 📜 Lizenz

Dieses Repository steht unter der Lizenz Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0).  
Sie dürfen:

- den Code einsehen und zu Lernzwecken verwenden  
- ihn in nicht-kommerziellen Projekten nutzen  
- das Original weitergeben, sofern die Urheberschaft angegeben wird

## ❗️Verboten:

- die Nutzung des Codes für kommerzielle Zwecke ohne schriftliche Genehmigung des Autors  
- Änderungen oder Ableitungen dieses Codes zu erstellen

## 💡 Besondere Bedingung

Alle Rechte an diesem Code liegen bei Dmytro Movchan.  
Die Nutzung dieses öffentlichen Codes in kommerziellen Produkten ist ausschließlich möglich:

- im Rahmen einer Zusammenarbeit mit dem Autor  
- oder auf Grundlage einer offiziellen Vereinbarung mit einer gemeinnützigen Organisation (Verein), die eine Lizenz von Dmytro Movchan erhält.

Trigger test — 2025-06-02 20:00