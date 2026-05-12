from langchain_text_splitters import RecursiveCharacterTextSplitter


recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=150
)