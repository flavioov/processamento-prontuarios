from pydantic import BaseModel, Field

from typing_extensions import Optional


class InstrumentoColetaDados(BaseModel):
    document_content: Optional[str] = Field(None, description="Conteúdo do documento")
    document_name: Optional[str] = Field(
        None, description="Nome do documento. Ignorar."
    )
    tema_documento: Optional[str] = Field(
        None,
        description="Resposta concisa com máximo de 50 caraceteres retornando o tema e assunto do documento.",
    )
    # # Informações do projeto
    responsavel_coleta: Optional[str] = Field(
        None,
        description="Resposta concisa com máximo de 50 do nome da pessoa responsável pela coleta.Retorna o nome do"
        "responsável pela coleta, se nao encontrar, retorne nao informado.",
    )
    # data_coleta: Optional[date]
    # horario_coleta: Optional[time]
    id_paciente: Optional[str] = Field(
        None,
        description="Resposta concisa do Id do paciente. O Id é toda qualificação "
        "do paciente. Costuma ser toda informação após 'id:' ou todo "
        "e qualquer detalhe ou característica sobre o paciente. Retorna todas as caracteristicas do paciente, se nao encontrar, "
        "retorne nao informado.",
    )
    #
    # # 1. Dados demográficos e socioeconômicos
    nasceu_apos_2000: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente nasceu após o ano"
        " de 2000 ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    sexo_masculino: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente é do sexo masculino"
        " ou nao.Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    reside_em_campo_grande_ms: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente reside "
        "em campo grande ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    escolaridade_ate_ensino_medio: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "possui escolaridade até ensino médio ou "
        "nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    autodeclarado_pardo_ou_preto: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "foi declarado pardo ou preto ou nao. "
        "Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    casado_ou_uniao_estavel: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente é casado"
        ", possui união estável ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    possui_ocupacao_remunerada: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "possui ocupação remunerada ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    #
    # # 2. Hábitos de vida
    tabagista: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente é tabagista ou nao. "
        "Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    consome_alcool_regularmente: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "consome bebida alcoolica regularmente ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    utilizou_drogas_ilicitas: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "utiliza drogas ilícitas ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado..",
    )
    pratica_atividade_fisica: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente pratica atividade física regular ou nao. "
        "Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )

    comorbidades_previas: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente possui "
        "comorbidades prévias ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    uso_medicamentos_pre_ei: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente faz uso de "
        "medicamentos pré-EI ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    uso_fitoterapicos_pre_ei: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente faz uso de "
        "fitoterápicos pré-EI ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )

    procedimento_odontologico_pre_ei: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "realizou procedimento odontológico pré-EI ou "
        "nao.Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    complicacoes_odontologicas: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente teve "
        "complicações odontológicas ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    endocardite_previa: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente teve endocardite "
        "prévia ou nao.Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    valvula_protetica_ou_marcapasso: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente "
        "possui válvula protética ou marca-passo ou "
        "nao.Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    cirurgia_cardiaca_previa: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente realizou "
        "cirurgia cardíaca prévia ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    febre: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente apresenta febre ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    sopros_cardiacos: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente apresenta sopros "
        "cardíacos ou nao.Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    manifestacoes_cutaneas: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente apresenta "
        "manifestações cutâneas ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    insuficiencia_cardiaca: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente apresenta "
        "insuficiência cardíaca ou nao. Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
    eventos_embolicos: Optional[str] = Field(
        None,
        description="Resposta do tipo str se o paciente apresenta eventos "
        "embólicos ou nao.Retorna sim ou nao, se nao encontrar, "
        "retorne nao informado.",
    )
