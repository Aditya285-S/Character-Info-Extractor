import json
import os
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import re


load_dotenv()
GROQ_API_KEY = os.environ.get('GROQ_API')
MISTRAL_API = os.environ.get('MISTRAL_API')
DB_FAISS_PATH = 'vectorstore\db_faiss'


def get_character_info(character_name):
    embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    vectorstore = FAISS.load_local(DB_FAISS_PATH, embedding, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatGroq(
        temperature=0.5, 
        model_name="mixtral-8x7b-32768", 
        groq_api_key=GROQ_API_KEY
    )

    # llm = ChatMistralAI(
    #     model = "mistral-large-latest",
    #     api_key = MISTRAL_API,
    #     temperature = 0.5
    # )

    template = (
        "You are a highly skilled story summarizer and character extractor tasked with analyzing provided context. "
        "Here is the relevant context:\n\n"
        "{context}\n\n"
        "Your task is to extract detailed information about the character '{question}' and return it in JSON format. "
        "The JSON output must include the following fields:\n\n"
        "1. name: The full name of the character.\n"
        "2. storyTitle: The heading title of the story.\n"
        "3. summary: A brief but clear summary of the character's role and significance in the story.\n"
        "4. relations: A list of the character's relationships with other characters. Each relationship should include:\n"
        "   - name: The related character's name.\n"
        "   - relation: The type of relationship (e.g., sibling, friend, rival).\n"
        "5. characterType: The character's role in the story (e.g., protagonist, antagonist, side character).\n\n"
        "Important Notes:\n"
        "- Ensure the JSON output is strictly formatted, accurate, and well-structured.\n"
        "- If the character '{question}' is not found or no relevant information is available, return the following JSON:\n"
        "  {{\n"
        "      \"name\": false,\n"
        "      \"storyTitle\": null,\n"
        "      \"summary\": null,\n"
        "      \"relations\": [],\n"
        "      \"characterType\": null\n"
        "  }}\n"
        "- Always follow the specified JSON format, even if no details are found. Replace only the values with appropriate placeholders.\n"
        "- Do not include any information not explicitly provided in the context or any assumptions beyond the input data.\n\n"
        "Now, provide the JSON output for the character '{question}'."
    )

    rag_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            ("human", "{question}"),
        ]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": rag_prompt},
    )

    result = qa_chain.invoke(character_name)
    return result


def clean_json_output(output):
    match = re.search(r"\{.*\}", output, re.DOTALL)
    if match:
        return match.group(0).strip()
    else:
        raise ValueError("No JSON found in the output.")


def filter_Data(name):
    result = get_character_info(name)

    try:
        output = clean_json_output(result['result'])
        final_result = json.loads(output)
    except ValueError as e:
        return f"Error extracting JSON: {e}"
    except json.JSONDecodeError as e:
        return f"Error decoding JSON: {e}"

    if bool(final_result['name']) == False:
        return f'The {name} name is not found in any story.'
    else:
        return json.dumps(final_result, indent=4)


if __name__ == "__main__":
    name = input('Enter the character name: ')
    result = filter_Data(name)
    print(result)
