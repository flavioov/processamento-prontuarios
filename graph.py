import pathlib

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import StateGraph
from langgraph.constants import END

from datetime import date

from typing_extensions import Optional

from domain.InstrumentoColetaDados import InstrumentoColetaDados

from IPython.display import display, Image


class LLMGraph:

    def __init__(self, file_name: Optional[str] = None):
        self.llm = ChatOpenAI(model="gpt-4.1")
        self.memory = MemorySaver()
        self.file_name = None
        self.legenda = """
        Legenda:
    
        QP: Queixa principal
        HDA: Historia da Doença Atual
        HMP: Historia Morbida pregressa
        HFS: Hábitos de Vida e História Social
        HFAM: Historico Familiar
        Beg = Bom estado geral
        Reg = regular estado geral
        """

    def get_graph(self):
        graph_builder = StateGraph(InstrumentoColetaDados)
        graph_builder.add_node("processor", self._process_data)
        graph_builder.add_node("writer", self._write_files)

        graph_builder.set_entry_point("processor")
        graph_builder.add_edge("processor", "writer")
        graph_builder.add_edge("writer", END)

        graph = graph_builder.compile()

        return graph

    def set_filename(self, file_name: str):
        self.file_name = file_name.removesuffix(".docx") + ".txt"

    async def _process_data(
        self, state: InstrumentoColetaDados
    ) -> InstrumentoColetaDados:
        prompt = (
            f"hoje é: {date.today()}. Você é um médico assistente. Normalize os caracteres para utf-8. Com base no documento a seguir extraia as "
            f"informações relevantes: {state.document_content}. Outras informações relevantes: {self.legenda}"
        )
        response = await self.llm.with_structured_output(
            InstrumentoColetaDados
        ).ainvoke(prompt)
        return response

    async def _write_files(self, state: InstrumentoColetaDados):
        pathlib.Path("docs/output").mkdir(parents=True, exist_ok=True)
        with open(f"docs/output/{self.file_name}", "w", encoding="utf-8") as f:
            for key, value in state.model_dump().items():
                if key == "document_content" or key == "document_name":
                    continue
                f.write(f"{key}: {value}\n")
        print(f"📁 Arquivo criado em docs/output/{self.file_name}")
