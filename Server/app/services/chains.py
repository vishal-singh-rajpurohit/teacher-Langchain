from .model import label_model
from .parsers import string_output_parser
from .prompts import label_prompt_template



label_chain = label_prompt_template | label_model | string_output_parser