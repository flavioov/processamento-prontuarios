# processamento-prontuarios
Esta aplicação dispõe de uma lógica simples e específica e um agente inteligente que recebe prontuários de pacientes 
e responde um formulário pré definido a partir destas informações.

## TL;DR
Para rodar  o projeto execute os comandos abaixo. É necessário ter documentos em `doc/input/`, por
exemplo `doc/input/prontuario.docx`

````shell
export OPENAI_API_KEY=<api-key>
python main.py
````

## Saída
Como saída será gerado um arquivo `doc/output/formulario.txt` respondendo os questionamentos 
presentes no formulário.

### 📌 Finalidade

O formulário tem como objetivo **estruturar informações de prontuários clínicos em um modelo padrão**, permitindo:

- Coleta automatizada de dados para pesquisa clínica
- Padronização de registros médicos para uso acadêmico ou institucional


---

### 📋 Estrutura do Formulário

#### 👤 Informações da Coleta

| Campo                  | Descrição | Valores possíveis |
|------------------------|-----------|--------------------|
| `responsavel_coleta`   | Nome da pessoa responsável pela coleta. Retorna "não informado" se ausente | texto ou "não informado" |
| `id_paciente`          | Informações de identificação ou características do paciente | texto ou "não informado" |

---

#### 🧬 1. Dados demográficos e socioeconômicos

| Campo                          | Descrição | Valores possíveis |
|--------------------------------|-----------|--------------------|
| `nasceu_apos_2000`             | O paciente nasceu após o ano 2000? | sim / não / não informado |
| `sexo_masculino`               | O paciente é do sexo masculino? | sim / não / não informado |
| `reside_em_campo_grande_ms`   | Reside em Campo Grande - MS? | sim / não / não informado |
| `escolaridade_ate_ensino_medio` | Escolaridade até ensino médio? | sim / não / não informado |
| `autodeclarado_pardo_ou_preto` | Se declarou pardo ou preto? | sim / não / não informado |
| `casado_ou_uniao_estavel`     | É casado ou vive em união estável? | sim / não / não informado |
| `possui_ocupacao_remunerada`  | Possui ocupação remunerada? | sim / não / não informado |

---

#### 💬 2. Hábitos de vida

| Campo                          | Descrição | Valores possíveis |
|--------------------------------|-----------|--------------------|
| `tabagista`                    | É ou foi tabagista? | sim / não / não informado |
| `consome_alcool_regularmente` | Consome álcool regularmente? | sim / não / não informado |
| `utilizou_drogas_ilicitas`    | Já utilizou drogas ilícitas? | sim / não / não informado |
| `pratica_atividade_fisica`    | Pratica atividade física regularmente? | sim / não / não informado |

---

#### 🏥 3. Histórico clínico e antecedentes

| Campo                             | Descrição | Valores possíveis |
|----------------------------------|-----------|--------------------|
| `comorbidades_previas`            | Possui comorbidades prévias? | sim / não / não informado |
| `uso_medicamentos_pre_ei`        | Faz uso de medicamentos pré-EI? | sim / não / não informado |
| `uso_fitoterapicos_pre_ei`       | Faz uso de fitoterápicos? | sim / não / não informado |
| `procedimento_odontologico_pre_ei` | Realizou procedimento odontológico? | sim / não / não informado |
| `complicacoes_odontologicas`     | Teve complicações odontológicas? | sim / não / não informado |
| `endocardite_previa`             | Já teve endocardite prévia? | sim / não / não informado |
| `valvula_protetica_ou_marcapasso`| Possui válvula protética ou marca-passo? | sim / não / não informado |
| `cirurgia_cardiaca_previa`       | Já fez cirurgia cardíaca? | sim / não / não informado |

---

#### 🩺 4. Manifestações clínicas


| Campo                      | Descrição | Valores possíveis |
|----------------------------|-----------|--------------------|
| `febre`                    | Apresenta febre? | sim / não / não informado |
| `sopros_cardiacos`         | Apresenta sopros cardíacos? | sim / não / não informado |
| `manifestacoes_cutaneas`  | Apresenta manifestações cutâneas? | sim / não / não informado |
| `insuficiencia_cardiaca`   | Apresenta insuficiência cardíaca? | sim / não / não informado |
| `eventos_embolicos`        | Apresenta eventos embólicos? | sim / não / não informado |

---


## Grafo do agente
````mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        processor(processor)
        writer(writer)
        __end__([<p>__end__</p>]):::last
        __start__ --> processor;
        processor --> writer;
        writer --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc
````