from langchain_core.prompts import PromptTemplate, ChatPromptTemplate


label_prompt_template = PromptTemplate(
    template="""
      Act as a Label Writer to rewrite the given prompt in 50 Words for header as a converation or Post,
      prompt -> {prompt}
    """,
    input_variables=['prompt']
)

general_query_prompt = PromptTemplate(
    template="""
User Query:
{query}

Response format:
{format_instructions}
""",
    input_variables=["query", "format_instructions"]
)


answer_prompt_template = ChatPromptTemplate.from_template("""
You are a highly skilled AI Tutor.

Your goal is to teach and explain concepts from the given content in the best possible way according to the user's query.

Guidelines:
1. Analyze the query to understand what the user wants to learn.
2. Use the provided content as the primary knowledge source.
3. Explain step-by-step in simple language.
4. Break down difficult concepts into smaller parts.
5. Provide examples, comparisons, or real-world analogies if useful.
6. Highlight key points and important terms.
7. If the content lacks enough information, mention the limitation politely.
8. Maintain an encouraging and educational tone.

Content:
----------------
{content}
----------------

User Query:
{query}

Response format:
{format_instructions}
""")
