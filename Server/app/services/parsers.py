from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field


string_output_parser = StrOutputParser()


class AnswerPyParser(BaseModel):
    answer: str

pydantic_parser = PydanticOutputParser(pydantic_object=AnswerPyParser)

