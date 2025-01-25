# Character-Info-Extractor

## Clone the repository

```bash
git clone https://github.com/Aditya285-S/Character-Info-Extractor
```

## Create Virtual Environment

```bash
pip install virtualenv
```

```bash
virtualenv <env-name>
```

```bash
./<env-name>/scripts/activate
```

## Download requirements

```bash
pip install -r requirements.txt
```

## Create .env file and declare API keys
-.env
```bash
GROQ_API = <your_api_key>
MISTRAL_API = <your_mistral_api_key>
```

## CLI Command 1: compute-embedding
- To compute the embedding of the data and store it in the Vector Database.

```bash
python compute_embeddings.py 
```

## CLI Command 2: get-character-info
- To get the character information from the story.

-- Option 1: Use terminal

```bash
python get_character_info.py
```
Enter the character name: <enter-character-name>

-- Option 2: On Streamlit UI

```bash
streamlit run app.py
```
