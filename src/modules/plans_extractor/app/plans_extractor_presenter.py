import json
import boto3
import os
import re
from io import BytesIO 
from pypdf import PdfReader 
import pandas as pd
from urllib.parse import unquote_plus

def clean_and_optimize_text(raw_text: str) -> str:
    """
    Limpa e otimiza o texto extraído de um PDF para minimizar o uso de tokens.
    """
    # 1. Remove as tags 
    text = re.sub(r'\\s*', '', raw_text)
    
    # 2. Remove marcadores de página e de tabelas
    text = re.sub(r'--- PAGE \d+ ---', '', text)
    text = re.sub(r'"The following table:"', '', text, flags=re.IGNORECASE)
    
    # 3. Reformata as linhas da tabela para um formato mais limpo
    text = re.sub(r'"([^"]+)"\s*,\s*"([^"]*)"\s*,\s*"([^"]*);"', r'Semana \1: \2 (EAA: \3)', text)
    text = re.sub(r'"([^"]+)"\s*,\s*,\s*"([^"]*);"', r'Semana \1: (EAA: \2)', text)

    # 4. Normaliza espaços em branco e remove linhas vazias excessivas
    text = re.sub(r'(\n\s*){2,}', '\n', text)
    
    return text.strip()


def lambda_handler(event, context):
    """
    Função principal da Lambda que é acionada por um evento do S3.
    """
    print("Evento recebido:", json.dumps(event))
    
    s3 = boto3.client("s3")
    bedrock_region = os.environ.get("BEDROCK_REGION", "us-east-1")
    bedrock = boto3.client("bedrock-runtime", region_name=bedrock_region)
    
    try:
        first_record_bucket = event["Records"][0]['s3']['bucket']['name']
        print(f"Carregando a fonte da verdade de: {first_record_bucket}/relacao_disciplinas.xlsx")
        excel_response = s3.get_object(Bucket=first_record_bucket, Key="relacao_disciplinas.xlsx")
        excel_bytes = excel_response["Body"].read()
        df_truth = pd.read_excel(BytesIO(excel_bytes), skiprows=1)  # Ajustado para skiprows=1 baseado na estrutura
        # Assumindo colunas: Ano, Turno, CODIGO DISCIPLINA, DISCIPLINA, CURSO, PERIODO, SERIE, SEMESTRALIDADE, ...
        # Renomear colunas se necessário para consistência, mas usando nomes aproximados
        print("Fonte da verdade carregada com sucesso.")

        for record in event["Records"]:
            bucket_name = record['s3']['bucket']['name']
            object_key = unquote_plus(record['s3']['object']['key'])
            
            if object_key.startswith("plans/"):
                print(f"Processing plan file: {object_key}")

                filename = os.path.basename(object_key)
                subject_code = filename.split('.')[0]
                print(f"Extracted subject code: {subject_code}")

                context_from_excel = ""
                all_matching_rows = df_truth[df_truth['CODIGO DISCIPLINA'] == subject_code]
            
                if not all_matching_rows.empty:
                    print(f"Encontradas {len(all_matching_rows)} entradas para {subject_code} no Excel.")
                    info_list = all_matching_rows.to_dict(orient='records')
                    
                    context_from_excel = (
                        "Aqui estão os dados da fonte da verdade (Excel) para esta disciplina. "
                        "Use estes dados para preencher ou corrigir as informações do PDF, especialmente os campos 'period' (baseado em SEMESTRALIDADE: S1/S2 -> 'S', A1/A2 -> 'A') e 'courses' (extraia o prefixo de CURSO como chave, e use SERIE para determinar o ano: 1ª Série -> 1, 2ª Série -> 2, etc., até 5).\n"
                        f"{json.dumps(info_list, indent=2, ensure_ascii=False)}"
                    )
                else:
                    context_from_excel = "AVISO: Nenhuma informação de contexto encontrada no arquivo Excel para este código de disciplina."
                    print(f"Contexto para {subject_code} não encontrado no Excel.")

                pdf_response = s3.get_object(Bucket=bucket_name, Key=object_key)
                pdf_bytes = pdf_response['Body'].read()
                raw_text = "".join([page.extract_text() or "" for page in PdfReader(BytesIO(pdf_bytes)).pages])
                optimized_text = clean_and_optimize_text(raw_text)
                content_for_claude = {"type": "text", "content": optimized_text}

                final_data = extract_course_data_with_claude(
                    bedrock, 
                    content_for_claude, 
                    object_key, 
                    context_from_excel  
                )


                print("Dados Finais (processados pelo Claude com contexto):")
                print(json.dumps(final_data, indent=2))
            
            else:
                print(f"Skipping file, not a plan file: {object_key}")

        return {'statusCode': 200, 'body': json.dumps({'message': 'Event processed successfully'})}
        
    except Exception as e:
        print(f"Erro geral no handler: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}


def extract_course_data_with_claude(bedrock_client, content_data, filename, context_from_excel: str):
    """
    Usa o Claude 3 Sonnet para extrair dados estruturados do conteúdo.
    """
    schema = {
        "type": "object",
        "properties": {
            "course": {"type": "string", "description": "Nome do curso ou ciclo (ex: 'Ciclo Básico', extraído do PDF)"},
            "name": {"type": "string", "description": "Nome completo da disciplina (extraído do PDF)"},
            "code": {"type": "string", "description": "Código da disciplina (ex: DSG244, extraído do PDF)"},
            "period": {"type": "string", "enum": ["A", "S"], "description": "A para Anual, S para Semestral (PRIORIDADE: Excel, baseado em SEMESTRALIDADE)"},
            "examWeight": {"type": "number", "minimum": 0, "maximum": 100, "description": "Peso das provas em % (extraído do PDF)"},
            "assignmentWeight": {"type": "number", "minimum": 0, "maximum": 100, "description": "Peso dos trabalhos em % (extraído do PDF)"},
            "exams": {
                "type": "array",
                "maxItems": 4,
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "enum": ["P1", "P2", "P3", "P4"]},
                        "weight": {"type": "number", "minimum": 0, "maximum": 1}
                    }, "required": ["name", "weight"]
                }
            },
            "assignments": {
                "type": "array",
                "maxItems": 10,
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "enum": ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10"]},
                        "weight": {"type": "number", "minimum": 0, "maximum": 1}
                    }, "required": ["name", "weight"]
                }
            },
            "courses": {
                "type": "object",
                "description": "Informações sobre quais cursos possuem esta disciplina e em qual ano (PRIORIDADE: Excel, use prefixo de CURSO como chave, ano de SERIE)",
                "patternProperties": {
                    "^(EAL|ECA|ECM|EEN|EET|EMC|EPM|EQM|ETC|ADM|DSG|CIC|SIN|IA|ARQ|RI|ADS|AL|CA|CMP|CV|EN|ET|FB|MC|PM|QM)$": {
                        "type": "number", "minimum": 1, "maximum": 5, "description": "Ano do curso (1 a 5)"
                    }
                }
            }
        },
        "required": ["course", "name", "code", "period", "examWeight", "assignmentWeight", "exams", "assignments", "courses"]
    }
    
    schema_prompt = f"""
Você é um assistente de extração de dados altamente preciso. Sua tarefa é analisar o contexto de um arquivo Excel (fonte da verdade para 'period' e 'courses') e o texto de um plano de ensino em PDF (para todos os outros campos) para preencher um objeto JSON de acordo com um esquema específico.

Siga estas regras rigorosamente:

1.  **Prioridade da Fonte da Verdade (Excel):** Use o conteúdo dentro das tags <excel_context> APENAS para os campos 'period' e 'courses'. 
   - Para 'period': Baseado em 'SEMESTRALIDADE'. Se contém 'S' (ex: S1, S2), use 'S'. Se contém 'A' (ex: A1, A2), use 'A'. Se múltiplas linhas, use o mais comum ou o primeiro.
   - Para 'courses': Agregue por disciplina. Para cada linha única, extraia o prefixo de 3 letras do campo 'CURSO' (ex: 'ADM/21' -> 'ADM', 'EFB' -> 'EFB', etc.) como chave. Determine o ano do campo 'SERIE' (ex: '1ª Série' -> 1, '2º Semestre' -> 2, '4ª Série' -> 4). Se múltiplas linhas para o mesmo curso, use o ano mais apropriado (mínimo ou médio). Ignore linhas duplicadas para o mesmo curso/ano.
   - Se o Excel estiver vazio, use inferência do PDF ou valores padrão (period: 'S', courses: vazio).

2.  **Extração do PDF:** Para todos os outros campos ('course', 'name', 'code', 'examWeight', 'assignmentWeight', 'exams', 'assignments'), use EXCLUSIVAMENTE o texto dentro das tags <pdf_text>. Inferir pesos, nomes de provas/trabalhos logicamente do conteúdo (ex: pesos totais devem somar 1.0 para exams e assignments; examWeight + assignmentWeight = 100).

3.  **Raciocínio Lógico:** Antes de gerar o JSON final, pense passo a passo dentro de tags <thinking>. Descreva como você encontrou cada valor, especialmente como processou 'period' e 'courses' do Excel, e o resto do PDF. Explique agregações em 'courses' se houver múltiplas linhas.

4.  **Formato de Saída:** Após a tag </thinking>, forneça APENAS o objeto JSON válido, sem comentários, explicações ou formatação de bloco de código. Certifique-se de que é um JSON válido e completo conforme o schema.

---
**EXEMPLO DE USO:**

<excel_context>
[
  {{
    "CODIGO DISCIPLINA": "ADM112",
    "DISCIPLINA": "Cálculo Aplicado à Administração",
    "CURSO": "ADM",
    "PERIODO": "ADM/21",
    "SERIE": "1ª Série",
    "SEMESTRALIDADE": "S1"
  }},
  {{
    "CODIGO DISCIPLINA": "ADM113",
    "DISCIPLINA": "Cálculo e Pesquisa Operacional",
    "CURSO": "ADM",
    "PERIODO": "ADM/21",
    "SERIE": "1ª Série",
    "SEMESTRALIDADE": "S1"
  }},
  {{
    "CODIGO DISCIPLINA": "ADM114",
    "DISCIPLINA": "Inovação e Novas Abordagens em Administração",
    "CURSO": "ADM",
    "PERIODO": "ADM/21",
    "SERIE": "4ª Série",
    "SEMESTRALIDADE": "S1"
  }}
]
</excel_context>

<pdf_text>
Disciplina: Cálculo Aplicado à Administração
Código da Disciplina: ADM112
Peso de Provas: 70%
Peso de Trabalhos: 30%
Provas: P1 (0.4), P2 (0.3), P3 (0.3)
Trabalhos: T1 (0.5), T2 (0.5)
Curso: Administração
</pdf_text>

<json_schema>
{json.dumps(schema, indent=2)}
</json_schema>

**SAÍDA ESPERADA (para ADM112):**

<thinking>
1. **course**: Extraído do PDF: "Administração" (ou inferido como nome do curso).
2. **name**: Do PDF: "Cálculo Aplicado à Administração".
3. **code**: Do PDF: "ADM112".
4. **period**: Prioridade Excel. Para ADM112, SEMESTRALIDADE="S1" -> "S".
5. **examWeight**: Do PDF: 70.
6. **assignmentWeight**: Do PDF: 30.
7. **exams**: Do PDF: P1(0.4), P2(0.3), P3(0.3).
8. **assignments**: Do PDF: T1(0.5), T2(0.5).
9. **courses**: Prioridade Excel. Apenas uma linha para ADM112: CURSO="ADM" (prefixo 'ADM'), SERIE="1ª Série" -> ano 1. Então {{"ADM": 1}}. (Nota: As outras linhas são para códigos diferentes, ignoradas para este código).
</thinking>
{{
  "course": "Administração",
  "name": "Cálculo Aplicado à Administração",
  "code": "ADM112",
  "period": "S",
  "examWeight": 70.0,
  "assignmentWeight": 30.0,
  "exams": [
    {{"name": "P1", "weight": 0.4}},
    {{"name": "P2", "weight": 0.3}},
    {{"name": "P3", "weight": 0.3}}
  ],
  "assignments": [
    {{"name": "T1", "weight": 0.5}},
    {{"name": "T2", "weight": 0.5}}
  ],
  "courses": {{"ADM": 1}}
}}

---
**AGORA, SUA VEZ. ANALISE OS DADOS A SEGUIR E GERE A SAÍDA NO FORMATO DESCRITO.**
"""

    message_content = [{
        "type": "text",
        "text": (
            f"<excel_context>\n{context_from_excel}\n</excel_context>\n\n"
            f"<pdf_text>\n{content_data['content']}\n</pdf_text>\n\n"
            f"<json_schema>\n{json.dumps(schema, indent=2)}\n</json_schema>\n\n"
            f"{schema_prompt}"
        )
    }]

    try:
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "messages": [{"role": "user", "content": message_content}],
                "temperature": 0.1
            })
        )
        
        response_body = json.loads(response['body'].read())
        claude_response = response_body['content'][0]['text']
        
        thinking_block_end = "</thinking>"
        if thinking_block_end in claude_response:
            json_part = claude_response.split(thinking_block_end, 1)[1].strip()
            
            json_part = re.sub(r'^```json\s*', '', json_part)
            json_part = re.sub(r'```$', '', json_part)

            structured_data = json.loads(json_part)
        else:
            print("Bloco <thinking> não encontrado. Tentando parse direto do JSON.")
            structured_data = json.loads(claude_response)
        
        usage = response_body.get('usage', {})
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)
        
        estimated_cost = (input_tokens * 0.003 / 1000) + (output_tokens * 0.015 / 1000)
        
        print(f"Claude API Usage - Input: {input_tokens}, Output: {output_tokens}, Total: {input_tokens + output_tokens}")
        print(f"File: {filename} - Estimated cost: ${estimated_cost:.6f}")
        
        try:
            structured_data = json.loads(claude_response)
        except json.JSONDecodeError:
            print("Direct JSON parsing failed. Attempting to extract JSON from response...")
            json_match = re.search(r'\{.*\}', claude_response, re.DOTALL)
            if json_match:
                structured_data = json.loads(json_match.group(0))
            else:
                raise ValueError("Could not extract valid JSON from Claude's response")
        
        structured_data['token_usage'] = {
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens,
            'estimated_cost_usd': estimated_cost
        }
        
        return structured_data
        
    except Exception as e:
        print(f"Error calling Claude: {str(e)}")
        return {"error": f"Failed to process with Claude: {str(e)}"}