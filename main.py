import pickle
from dotenv import load_dotenv
load_dotenv()

import time
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

print("Loading...")

start_time = time.time()

persist_directory = 'db/chroma'
embeddings = OpenAIEmbeddings()

print("Loaded documents")

should_load_from_cache = input("Load from cached embedding DB? (y/n) ") == "y"

if not should_load_from_cache:
    loader = DirectoryLoader('data/txt/marginal-revolution')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    db = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_directory)
else:
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

end_time = time.time()

chain = load_qa_with_sources_chain(OpenAI(temperature=0), chain_type="stuff")

print(f"Loaded in {end_time - start_time} seconds")

print("\n\nWelcome to TAIler Cowen\n\n")

print(open("tyler.txt").read())

if __name__ == "__main__":
    try:
        while True:
            user_input = input("\033[1;32mEnter your query (Ctrl+C to exit):\033[0m ")

            docs = db.similarity_search(user_input)
            result = chain({"input_documents": docs, "question": user_input}, return_only_outputs=True)
            
            print(f"\033[1;34mResult:\033[0m {result['output_text']}")
    except KeyboardInterrupt:
        print("\n\033[1;31mExiting...\033[0m")
        exit()
