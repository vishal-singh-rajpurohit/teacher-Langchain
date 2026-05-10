from langchain_core.prompts import PromptTemplate


label_prompt_template = PromptTemplate(
    template="""
      Act as a Label Writer to rewrite the given prompt in 50 Words for header as a converation or Post,
      prompt -> {prompt}
    """,
    input_variables=['prompt']
)