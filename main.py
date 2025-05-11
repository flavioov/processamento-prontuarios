import os
import getpass
import pathlib
import time

from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import StateGraph
from langgraph.constants import END

from docx import Document
from langgraph.types import Command

from pydantic import BaseModel, Field

from typing_extensions import Optional, Annotated

from datetime import date


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

class Documents(BaseModel):
    documents: Optional[list[dict[str, str]]] = Field(..., description="Lista de documentos carregados do S.O.")

class InstrumentoColetaDados(BaseModel):
    content: Optional[str] = Field(str, description="Conteúdo do documento")
    tema_documento: Optional[str] = Field(
        None,
        description="Resposta concisa com máximo de 50 caraceteres retornando o tema e assunto do documento.",
    )
    # # Informações do projeto
    responsavel_coleta: Optional[str] = Field(
        None,
        description="Resposta concisa com máximo de 50 do nome da pessoa responsável pela coleta.Retorna o nome do"
                    "responsável pela coleta, se não encontrar, retorne Não informado.",
    )
    # data_coleta: Optional[date]
    # horario_coleta: Optional[time]
    id_paciente: Optional[str] = Field(
        None,
        description="Resposta concisa do Id do paciente. O Id é toda qualificação "
        "do paciente. Costuma ser toda informação após 'id:' ou todo "
        "e qualquer detalhe ou característica sobre o paciente. Retorna todas as caracteristicas do paciente, se não encontrar, "
        "retorne Não informado.",
    )
    #
    # # 1. Dados demográficos e socioeconômicos
    nasceu_apos_2000: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente nasceu após o ano"
        " de 2000 ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    sexo_masculino: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente é do sexo masculino"
        " ou não.Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    reside_em_campo_grande_ms: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente reside "
        "em campo grande ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    escolaridade_ate_ensino_medio: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "possui escolaridade até ensino médio ou "
        "não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    autodeclarado_pardo_ou_preto: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "foi declarado pardo ou preto ou não. "
        "Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    casado_ou_uniao_estavel: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente é casado"
        ", possui união estável ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    possui_ocupacao_remunerada: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "possui ocupação remunerada ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    #
    # # 2. Hábitos de vida
    tabagista: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente é tabagista ou não. "
        "Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    consome_alcool_regularmente: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "consome bebida alcoolica regularmente ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    utilizou_drogas_ilicitas: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "utiliza drogas ilícitas ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado..",
    )
    pratica_atividade_fisica: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente pratica atividade física regular ou não. "
                    "Retorna sim ou não, se não encontrar, "
                    "retorne Não informado."
    )

    comorbidades_previas: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente possui "
        "comorbidades prévias ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    uso_medicamentos_pre_ei: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente faz uso de "
        "medicamentos pré-EI ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    uso_fitoterapicos_pre_ei: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente faz uso de "
        "fitoterápicos pré-EI ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )

    procedimento_odontologico_pre_ei: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "realizou procedimento odontológico pré-EI ou "
        "não.Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    complicacoes_odontologicas: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente teve "
        "complicações odontológicas ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    endocardite_previa: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente teve endocardite "
        "prévia ou não.Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    valvula_protetica_ou_marcapasso: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "possui válvula protética ou marca-passo ou "
        "não.Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    cirurgia_cardiaca_previa: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente realizou "
        "cirurgia cardíaca prévia ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    febre: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente apresenta febre ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    sopros_cardiacos: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente apresenta sopros "
        "cardíacos ou não.Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    manifestacoes_cutaneas: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente apresenta "
        "manifestações cutâneas ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    insuficiencia_cardiaca: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente apresenta "
        "insuficiência cardíaca ou não. Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )
    eventos_embolicos: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente apresenta eventos "
        "embólicos ou não.Retorna sim ou não, se não encontrar, "
        "retorne Não informado.",
    )

def extrai_dados(state: InstrumentoColetaDados) -> InstrumentoColetaDados:
    prompt = (
        f"hoje é: {date.today()}. Você é um médico assistente. Normalize os caracteres para utf-8. Com base no documento a seguir extraia as "
        f"informações relevantes: {state.content}. Outras informações relevantes: {legenda}"
    )
    response = llm.with_structured_output(InstrumentoColetaDados).invoke(prompt)
    # print(f"response: {response}")
    return response

def write_files(state: InstrumentoColetaDados):
    pathlib.Path("docs/output").mkdir(parents=True, exist_ok=True)
    with open(f"docs/output/{filename}.txt", "w", encoding="utf-8") as f:
        for key, value in state.model_dump().items():
            if key == "content" or key == "filename":
                continue
            f.write(f"{key}: {value}\n")
    print(f"📁 Files written to docs/output/{filename}.txt")

memory = MemorySaver()
graph_builder = StateGraph(InstrumentoColetaDados)
graph_builder.add_node("processor", extrai_dados)
graph_builder.add_node("writer", write_files)

graph_builder.set_entry_point("processor")
graph_builder.add_edge("processor", "writer")
graph_builder.add_edge("writer", END)

graph = graph_builder.compile()

class NewDocxHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            path = pathlib.Path(event.src_path)
            print(f"is_valid_docx_file: {is_valid_docx_file(path)}")
            if not is_valid_docx_file(path):
                print(f"📄 Novo prontuário detectado: {path.name}")
                if path.suffix == ".docx":
                    print(f"New .docx file detected: {path}")
                    content = load_docx_content(path)
                    response = graph.invoke({"content": content})
                    # print(f"response: {response}")

# Load DOCX file content
def load_docx_content(file_path: Path, retries=5, delay=0.5) -> str:
    for attempt in range(retries):
        try:
            document = Document(file_path)
            content = "\n".join([para.text for para in document.paragraphs])
            print(f"📄 Conteúdo do documento carregado: {content}")
            return content
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
                continue
            else:
                raise RuntimeError(f"Falha ao abrir {file_path.name} após {retries} tentativas.")

def is_valid_docx_file(file_path: Path) -> bool:
    # Ignore temporary or lock files
    filename = file_path.name
    return (
        filename.startswith("~$")      # MS Word lock file
        or filename.startswith(".~lock")  # LibreOffice lock file
        or file_path.stat().st_size > 0       # avoid empty files
    )

def watch_folder(folder_path: str):
    observer = Observer()
    handler = NewDocxHandler()
    observer.schedule(handler, folder_path, recursive=False)
    observer.start()
    print(f"📁 Watching for new .docx files in: {folder_path}")
    try:
        while True:
            time.sleep(30)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    legenda = """
    Legenda:

    QP: Queixa principal
    HDA: Historia da Doença Atual
    HMP: Historia Morbida pregressa
    HFS: Hábitos de Vida e História Social
    HFAM: Historico Familiar
    Beg = Bom estado geral
    Reg = regular estado geral
    """
    content = """
    ANAMNESE 1
    
    Id: João Barreto, 39 anos, masculino, solteiro, branco, natural e procedente de São José do Rio Preto - SP, pedreiro, evangélico.
    
    QP: “Febre e dor no peito há três dias”
    
    HDA: Paciente vem à UPA com sintomas de febre alta (39ºC), calafrios intensos, dispneia aos pequenos esforços e dor em região retroesternal tipo pontada que irradia para membro superior esquerdo, sem fator de melhora, iniciados há 3 dias. Nega tosse, náuseas, vômitos e hemoptise. Nega palpitações, taquicardias e dispneia ao repouso. Refere também mialgia e mal-estar geral. Admitiu uso crônico de cocaína injetável regularmente, última utilização há 15 dias, sem assepsia correta e utilizando a mesma seringa para várias aplicações. 
    
    HMP: Afirma HAS, mas sem realizar tratamento. Nega outras comorbidades. Nega internações prévias, cirurgias e procedimentos. Nega alergias, uso de fitoterápicos e hemotransfusões, afirma a vacinação irregular. Tomou apenas uma dose para COVID-19.
    
    HFS: Paciente alcoolista, tabagista (30 maços-ano) e usuário de cocaína injetável. Afirma relações sexuais desprotegida com múltiplos parceiros. Mora em casa de alvenaria, região urbana, sem saneamento básico adequado (falta de água encanada). Nega viagens recentes e contato com animais doentes.
    
    HFam:: Relata mãe falecida aos 64 anos devido câncer de esôfago. Não possui informações sobre pais. Não possui irmãos.
    
    
    Exame Físico Geral e Sinais Vitais:
    REG, LOTE, Acianótico e anictérico, fáceis atípicas, sem circulação colateral, sem alteração de peles e fâneros. Linfonodos não palpáveis. 
    Presença de nódulos em região distal de mãos (nódulos de Osler?). Lesões em botões rosa em troncos e membros (lesões de Janeway?).
    TEC < 3s
    FC: 60 bpm; FR: 16 irpm; TA: 38,5ºC; PA: 90/60 mmHg; O2: 97%
    
    Exame físico respiratório:
    Tórax normal, simétrico. Respiração torácica, expansibilidade normal, sem pontos dolorosos e frêmito toracovocal sem alterações. Percussão timpânica, murmúrio vesicular universalmente audível.
    
    Exame físico cardiovascular:
    BNF em 2t, presença de sopro holossistólico em foco mitral. Sem ingurgitamento jugular. 
    
    Exame físico abdominal:
    Plano, sem cicatrizes, sem dor a toque superficial e profundo, ruídos hidroaéreos presentes. 
    """

    _set_env("OPENAI_API_KEY")
    model = "gpt-4.1-mini"
    llm = ChatOpenAI(model=model)
    filename = "anamnese_1"
    # events = graph.invoke({"content": content})
    watch_folder("docs/input")