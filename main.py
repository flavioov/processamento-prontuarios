import os
import getpass
import pathlib

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import word_document
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import StateGraph
from langgraph.constants import END

from docx import Document
from langgraph.types import Command

from pydantic import BaseModel, Field

from typing_extensions import Optional, Annotated

from datetime import date, time


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

class Documents(BaseModel):
    documents: Optional[list[dict[str, str]]] = Field(..., description="Lista de documentos carregados do S.O.")

class InstrumentoColetaDados(BaseModel):
    filename: Optional[str] = Field(None, description="Nome do documento")
    content: Optional[str] = Field(None, description="Conteúdo do documento")
    tema_documento: Optional[str] = Field(
        None,
        description="Resposta concisa com máximo de 50 caraceteres retornando o tema do documento",
    )
    # # Informações do projeto
    responsavel_coleta: Optional[str] = Field(
        None,
        description="Resposta concisa com máximo de 50 do nome da pessoa responsável pela coleta. Se não encontrar, retorne 'Não informado'.",
    )
    # data_coleta: Optional[date]
    # horario_coleta: Optional[time]
    id_paciente: Optional[str] = Field(
        None,
        description="Resposta concisa do Id do paciente. O Id é toda qualificação "
        "do paciente. Costuma ser toda informação após 'id:' ou todo "
        "e qualquer detalhe ou característica sobre o paciente. Se "
        "não encontrar, retorne 'Não informado'.",
    )
    #
    # # 1. Dados demográficos e socioeconômicos
    nasceu_apos_2000: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente nasceu após o ano"
        " de 2000 ou não. Se não encontrar, retorne "
        "'Não informado'.",
    )
    sexo_masculino: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente é do sexo masculino"
        " ou não. Se não encontrar, retorne 'Não informado'.",
    )
    reside_em_campo_grande_ms: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente reside "
        "em campo grande ou não. Se não encontrar, "
        "retorne 'Não informado'.",
    )
    escolaridade_ate_ensino_medio: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente "
        "possui escolaridade até ensino médio ou "
        "não. Se não encontrar, retorne "
        "'Não informado'.",
    )
    autodeclarado_pardo_ou_preto: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente "
        "foi declarado pardo ou preto ou não. "
        "Se não encontrar, retorne 'Não informado'.",
    )
    casado_ou_uniao_estavel: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente é casado"
        ", possui união estável ou não. Caso contrário"
        "a resposta é 'Não informado'",
    )
    possui_ocupacao_remunerada: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente "
        "possui ocupação remunerada ou não. Se não "
        "encontrar, retorne 'Não informado'.",
    )
    #
    # # 2. Hábitos de vida
    tabagista: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente é tabagista ou não. "
        "Se não encontrar, retorne 'Não informado'.",
    )
    consome_alcool_regularmente: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente "
        "consome bebida alcoolica regularmente ou não. ",
    )
    utilizou_drogas_ilicitas: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente "
        "utiliza drogas ilícitas ou não. Se não "
        "encontrar, retorne 'Não informado'.",
    )
    pratica_atividade_fisica: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente pratica atividade física regular ou não. "
                    "Se não encontrar, retorne 'Não informado'."
    )

    comorbidades_previas: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente possui "
        "comorbidades prévias ou não. Se não encontrar, retorne "
        "'Não informado'.",
    )
    uso_medicamentos_pre_ei: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente faz uso de "
        "medicamentos pré-EI ou não. Se não encontrar, retorne "
        "'Não informado'.",
    )
    uso_fitoterapicos_pre_ei: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente faz uso de "
        "fitoterápicos pré-EI ou não. Se não encontrar, "
        "retorne 'Não informado'.",
    )

    procedimento_odontologico_pre_ei: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente "
        "realizou procedimento odontológico pré-EI ou "
        "não. Se não encontrar, retorne 'Não informado'.",
    )
    complicacoes_odontologicas: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente teve "
        "complicações odontológicas ou não. Se não "
        "encontrar, retorne 'Não informado'.",
    )
    endocardite_previa: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente teve endocardite "
        "prévia ou não. Se não encontrar, retorne 'Não informado'.",
    )
    valvula_protetica_ou_marcapasso: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente "
        "possui válvula protética ou marca-passo ou "
        "não. Se não encontrar, retorne 'Não informado'.",
    )
    cirurgia_cardiaca_previa: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente realizou "
        "cirurgia cardíaca prévia ou não. Se não encontrar, "
        "retorne 'Não informado'.",
    )
    febre: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente apresenta febre ou não. Se "
        "não encontrar, retorne 'Não informado'.",
    )
    sopros_cardiacos: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente apresenta sopros "
        "cardíacos ou não. Se não encontrar, retorne 'Não informado'.",
    )
    manifestacoes_cutaneas: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente apresenta "
        "manifestações cutâneas ou não. Se não encontrar, "
        "retorne 'Não informado'.",
    )
    insuficiencia_cardiaca: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente apresenta "
        "insuficiência cardíaca ou não. Se não encontrar, "
        "retorne 'Não informado'.",
    )
    eventos_embolicos: Optional[bool] = Field(
        None,
        description="Resposta do tipo boolean se o paciente apresenta eventos "
        "embólicos ou não. Se não encontrar, retorne 'Não informado'.",
    )


# graph 1

def read_all_docx(state: InstrumentoColetaDados):
    folder = pathlib.Path("docs/input")
    docs = []

    for file in folder.glob("*.docx"):
        print(f"Reading {file}")
        document = Document(file)
        text = "\n".join(p.text for p in document.paragraphs)
        docs.append({
            "filename": file.name,
            "content": text
        })
        print(text)

    for doc in state.documents:
        Command(
            update={
                "content": doc["content"],
                "filename": doc["filename"]
            },
            goto="processor"
        )


# graph 2
def extrai_dados(state: InstrumentoColetaDados):
    prompt = (
        f"hoje é: {date.today()}. Você é um médico assistente. Com base no documento a seguir extraia as "
        f"informações relevantes: {state.content}. Outras informações relevantes: {legenda}"
    )
    response = llm.with_structured_output(InstrumentoColetaDados).invoke(prompt)

    return Command(update=response, goto="writer")

def write_files(state: InstrumentoColetaDados):
    pathlib.Path("docs/output").mkdir(parents=True, exist_ok=True)
    with open(f"docs/output/{state.filename}.txt", "w", encoding="utf-8") as f:
        for key, value in state.model_dump().items():
            if key == "content" or key == "filename":
                pass
            f.write(f"{key}: {value}\n")
    return state

memory = MemorySaver()
graph_builder = StateGraph(InstrumentoColetaDados)
graph_builder.add_node("read_the_docs", read_all_docx)
graph_builder.add_node("processor", extrai_dados)
graph_builder.add_node("writer", write_files)

graph_builder.set_entry_point("processor")

graph = graph_builder.compile()

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
    query = """
    ANAMNESE 2
    Id: Maria Luiza Ramos, 52 anos, feminina, casada, parda, natural de Dourados - MS, procedente de Campo Grande - MS, aposentada (ex-professora), católica.
    QP: “Febre, cansaço e inchaço nas pernas há uma semana”
    HDA: Paciente procura atendimento na UBS referindo febre intermitente (máximas de 38,7ºC) associada a astenia progressiva e dispneia aos esforços moderados há 7 dias. Relata também edema em membros inferiores, principalmente vespertino, e sensação de palpitação ocasional. Nega dor torácica, tosse ou expectoração. Reforça perda de apetite, sudorese noturna e calafrios. Há cerca de 20 dias realizou extração dentária em consultório sem cobertura antibiótica prévia. Desde então, refere início dos sintomas. Nega hemoptise, náuseas ou vômitos.
    HMP: Portadora de valvopatia mitral reumática diagnosticada na juventude, em uso irregular de enalapril. Relata uma internação hospitalar há 5 anos por descompensação cardíaca. Nega alergias conhecidas. Não usa fitoterápicos. Esquema vacinal incompleto, sem doses atualizadas para COVID-19 ou Influenza.
    HFS: Nega etilismo ou tabagismo. Casada, em relação estável, nega ISTs prévias. Mora em casa com saneamento básico adequado. Alimentação irregular. Relata cuidado oral deficiente, com episódios recorrentes de gengivite e cáries. Sem contato com animais doentes ou viagens recentes.
    HFam: Pai falecido aos 70 anos por IAM. Mãe viva, hipertensa e diabética. Um irmão falecido por AVC aos 59 anos.
    ________________________________________
    Exame Físico Geral e Sinais Vitais:
    REG, corada, anictérica, sem linfadenomegalias palpáveis. Extremidades quentes, com presença de petéquias subungueais e palmas com lesões eritematosas não dolorosas (lesões de Janeway?). TEC 2s. FC: 104 bpm; FR: 20 irpm; Temp: 38,2ºC; PA: 100/60 mmHg; SpO2: 95% em ar ambiente.
    ________________________________________
    Exame físico respiratório:
    Tórax simétrico, expansibilidade preservada, murmúrio vesicular presente bilateralmente, sem ruídos adventícios. Percussão normal, sem alterações.
    ________________________________________
    Exame físico cardiovascular:
    Bulhas hipofonéticas, ritmo regular em 2T, presença de sopro diastólico em foco mitral, não referido previamente. Sem IJV. Pulso de amplitude reduzida.
    ________________________________________
    Exame físico abdominal:
    Plano, flácido, indolor à palpação, RHA presentes. Fígado palpável a 2 cm do rebordo costal direito, sugestivo de congestão hepática.
    """

    _set_env("OPENAI_API_KEY")
    model = "gpt-4.1-mini"
    llm = ChatOpenAI(model=model)
    events = graph.invoke({})
