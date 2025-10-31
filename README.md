## 🚀 AIAssistant

### 📝 Aperçu du Projet

Ce dépôt contient le code d'un **assistant vocal (Co-pilote IA)** développé pour fonctionner de manière *légère* et *locale*. L'architecture est conçue pour externaliser uniquement l'appel au modèle de langage étendu (LLM) à l'API de **Google Gemini**, garantissant une latence minimale pour le traitement audio (STT/TTS).

Le projet est entièrement **configurable** via un fichier d'environnement, permettant d'ajuster facilement le mot d'activation et la personnalité de l'IA sans modifier le code source.

Inspiré par le travail de [Defend Intelligence](https://github.com/anisayari/AIAssistantStreamer)

## 🛠️ Configuration et Installation

### 1\. Prérequis Système

Assurez-vous d'avoir les outils suivants :

  * **Python 3.x**
  * **Git**
  * **FFmpeg :** **Indispensable** pour la lecture audio avec `pydub`. Téléchargez les binaires et ajoutez le chemin du dossier `/bin` à la variable d'environnement **`PATH`** de votre système.

### 2\. Cloner le Dépôt

Récupérez le code source :

```bash
git clone https://github.com/RaphTHLN/AIAssistant.git
cd AIAssistant
```

### 3\. Installation des Dépendances Python

Installez les librairies requises :

```bash
pip install -r requirements.txt
```

### 4\. Configuration du Fichier `.env`

Le fichier `.env` est le centre de configuration du projet. **Créez-le** à la racine de votre répertoire et renseignez les variables :

| Variable | Description |
| :--- | :--- |
| `GEMINI_API_KEY` | Clé d'authentification pour l'API Google Gemini. |
| `WAKE_WORD` | Le mot qui active l'assistant (par défaut : **Luna**). |
| `SYSTEM_INSTRUCTION` | Le prompt initial qui définit la personnalité et le rôle de l'IA. |

**Exemple de `.env` :**

```env
# Remplacer par votre clé Gemini
GEMINI_API_KEY="AIzaSy..."

# Mot d'activation de l'assistant
WAKE_WORD="Assistant"

# Instructions complètes pour la personnalité de l'IA (sur une seule ligne)
SYSTEM_INSTRUCTION="Tu es une IA copilote. Réponds de manière courte et concise."
```

-----

## ▶️ Exécution et Utilisation

### Démarrage

Lancez l'assistant :

```bash
python3 index.py
```

### Cycle d'Interaction

L'assistant reste en **veille** et n'active le microphone que lorsque le **`WAKE_WORD`** est prononcé. Après activation, il écoute la commande complète, envoie la requête à Gemini, et fournit la réponse en français via TTS.

### Arrêt

Pour mettre fin à la session, prononcez le mot d'activation suivi d'une commande d'arrêt aprés avoir réveillé l'assistant : **"Stop"** ou **"Quitte"**.
