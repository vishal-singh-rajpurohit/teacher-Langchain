from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from .model import label_model
from .parsers import string_output_parser
from .prompts import label_prompt_template, answer_prompt_template, general_query_prompt
from .parsers import pydantic_parser



label_chain = label_prompt_template | label_model | string_output_parser

# main_query_chain = (
#     RunnableParallel({
#         "content": retriver,
#         "query": RunnablePassthrough()
#     }) | 
#     RunnablePassthrough.assign(
#         format_instructions=lambda _: pydantic_parser.get_format_instructions()
#     ) | 
#     answer_prompt_template | 
#     label_model | 
#     pydantic_parser)