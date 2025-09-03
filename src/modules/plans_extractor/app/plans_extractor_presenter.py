
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
        for record in event["Records"]:
            
            bucket_name = record['s3']['bucket']['name']
            object_key = unquote_plus(record['s3']['object']['key'])
            
            # 1. Verifica de forma mais robusta se o arquivo está na pasta 'plans'
            if object_key.startswith("plans/"):
            
                print(f"Processing plan file: {object_key} from bucket: {bucket_name}")

                # 2. Extrai o código da disciplina do nome do arquivo
                # ex: 'plans/ARQ203.pdf' -> 'ARQ203.pdf' -> 'ARQ203'
                filename = os.path.basename(object_key)
                subject_code = filename.split('.')[0]
                print(f"Extracted subject code: {subject_code}")

                # 3. Carrega o arquivo Excel da "fonte da verdade"
                try:
                    excel_response = s3.get_object(Bucket=bucket_name, Key="relacao_disciplinas.xlsx")
                    excel_bytes = excel_response["Body"].read()
                    df_truth = pd.read_excel(BytesIO(excel_bytes), skiprows=2)
                    print("Fonte da verdade carregada com sucesso.")
                    
                except Exception as e:
                    print(f"Erro ao ler ou processar o arquivo Excel: {e}")
                    context_from_excel = f"ERRO: Falha ao carregar dados de contexto do Excel: {e}\n\n"


                for record in event["Records"]:
                    bucket_name = record['s3']['bucket']['name']
                    object_key = unquote_plus(record['s3']['object']['key'])
        
                    if object_key.startswith("plans/"):
                        print(f"Processing plan file: {object_key}")

                        # 1. Extrai o código da disciplina do nome do arquivo
                        filename = os.path.basename(object_key)
                        subject_code = filename.split('.')[0]
                        print(f"Extracted subject code: {subject_code}")

                        # 2. Busca TODAS as linhas no Excel e monta o objeto 'courses'
                        courses_from_excel = {}
                        period_from_excel = "S" # Default para Semestral
                        
                        all_matching_rows = df_truth[df_truth['CODIGO DISCIPLINA'] == subject_code]
            
                    if not all_matching_rows.empty:
                        print(f"Encontradas {len(all_matching_rows)} entradas para {subject_code} no Excel.")
                        for index, row in all_matching_rows.iterrows():
                            course_acronym = row['CURSO']
                            # Extrai o número do período/ano do texto (ex: "2º Semestre" -> 2)
                            periodo_match = re.search(r'(\d+)', str(row['PERIODO']))
                            if periodo_match:
                                year = int(int(periodo_match.group(1)) / 2) if int(periodo_match.group(1)) > 5 else int(periodo_match.group(1))
                                courses_from_excel[course_acronym] = year

                        # Pega a semestralidade da primeira linha encontrada (deve ser igual para todas)
                        semestralidade = str(all_matching_rows.iloc[0]['SEMESTRALIDADE']).strip().upper()
                        if semestralidade.startswith('A'):
                            period_from_excel = 'A'
                    else:
                        print(f"Nenhuma entrada para {subject_code} encontrada na fonte da verdade.")

                    # 3. Processa o PDF para extrair o texto
                    pdf_response = s3.get_object(Bucket=bucket_name, Key=object_key)
                    pdf_bytes = pdf_response['Body'].read()
                    raw_text = "".join([page.extract_text() or "" for page in PdfReader(BytesIO(pdf_bytes)).pages])
                    optimized_text = clean_and_optimize_text(raw_text)
                    content_for_claude = {"type": "text", "content": optimized_text}

                    # 4. Chama o Claude para extrair os dados DO PDF
                    structured_data_from_claude = extract_course_data_with_claude(bedrock, content_for_claude, object_key)

                    if "error" in structured_data_from_claude:
                        print(f"Erro na extração do Claude para {object_key}. Pulando.")
                        continue

                    # 5. MERGE: Corrige os dados do Claude com a fonte da verdade do Excel
                    print("Mesclando dados do Claude com a fonte da verdade do Excel...")
                    structured_data_from_claude['courses'] = courses_from_excel
                    structured_data_from_claude['period'] = period_from_excel
                    
                    final_data = structured_data_from_claude

                    print("Dados Finais Corrigidos:")
                    print(json.dumps(final_data, indent=2))
                    
                    # Salvar `final_data` no S3 de destino
                
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
            "course": {"type": "string", "description": "Nome completo do curso"},
            "name": {"type": "string", "description": "Nome completo da disciplina"},
            "code": {"type": "string", "description": "Código da disciplina (ex: DSG244)"},
            "period": {"type": "string", "enum": ["A", "S"], "description": "A para Anual, S para Semestral"},
            "examWeight": {"type": "number", "minimum": 0, "maximum": 100, "description": "Peso das provas em %"},
            "assignmentWeight": {"type": "number", "minimum": 0, "maximum": 100, "description": "Peso dos trabalhos em %"},
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
                "description": "Informações sobre quais cursos possuem esta disciplina e em qual ano",
                "patternProperties": {
                    "^(EAL|ECA|ECM|EEN|EET|EMC|EPM|EQM|ETC|ADM|DSG|CIC|SIN|IA|ARQ|RI|ADS)$": {
                        "type": "number", "minimum": 1, "maximum": 5, "description": "Ano do curso (1 a 5)"
                    }
                }
            }
        },
        "required": ["course", "name", "code", "period", "examWeight", "assignmentWeight", "exams", "assignments"]
    }
    
    schema_prompt = f"""
Analise o conteúdo do documento e extraia informações de UMA disciplina específica no formato JSON especificado.

Por favor, extraia os dados da disciplina e formate de acordo com este esquema JSON:
{json.dumps(schema, indent=2)}

Lembretes Importantes:

1. CORRESPONDENCIA DE MATERIAS:
o nome dos cursos segue o seguinte padrao em relacao ao codigo das disciplinas
EAL - Engenharia de Alimentos
ECA - Engenharia de Controle e Automação
ECM - Engenharia de Computação
ENN - Engenharia Eletronica
EET - Engenharia Elétrica
EMC - Engenharia Mecanica
EPM - Engenharia de Produção
EQM - Engenharia Química
ETC - Engenharia Civil
ADM - Administração
DSG - Design
CIC - Ciencia da Computação
SIN - Sistemas da Informação
IA - Inteligêngia Artificial e Dados
ARQ - Arquitetura e Urbanismo
RI - Relações Internacionais

2. O PDF TALVEZ ESTEJA ERRADO EM RELACAO A: PERIODO e NOME DO CURSO, procure antes no conteudo do excel e confie mais no excel do que no pdf. 


INSTRUÇÕES IMPORTANTES:
1. NOME DA DISCIPLINA: Extraia o nome EXATO da disciplina conforme aparece no plano de ensino
2. CÓDIGO: Extraia o código exato da disciplina (ex: ECM401)
3. PERÍODO: Use "A" para disciplinas ANUAIS, "S" para disciplinas SEMESTRAIS
4. PROVAS: 
   - Procure pela seção "AVALIAÇÃO" ou "INSTRUMENTOS DE AVALIAÇÃO"
   - Se encontrar texto como "com trabalhos e provas (quatro e duas substitutivas)", isso significa 4 provas
   - Conte APENAS as provas principais (P1, P2, P3, P4)
   - NÃO conte provas substitutivas ou de recuperação
   - Se mencionar "quatro provas", crie: [{{"name": "P1", "weight": 0.25}}, {{"name": "P2", "weight": 0.25}}, {{"name": "P3", "weight": 0.25}}, {{"name": "P4", "weight": 0.25}}]
5. TRABALHOS:
   - Procure por "trabalhos", "Individual e/ou em Equipes"
   - Siga os pesos em K a quantidade de trabalhos inddicados
6. PESOS PERCENTUAIS (IMPORTANTE):
   - Procure por "Peso de MT(kt)" e "Peso de MP(kp)" na seção de avaliação
   - MT = Média dos Trabalhos, MP = Média de Prova
   - Se encontrar "Peso de MP(kp): 7" significa examWeight = 70
   - Se encontrar "Peso de MT(kt): 3" significa assignmentWeight = 30
   - examWeight + assignmentWeight DEVE somar 100
7. PESOS INDIVIDUAIS:
   - Para cada prova/trabalho: peso individual que soma 1.0 dentro do respectivo array
   - Ex: 4 provas = 0.25 cada; 3 trabalhos = 0.33, 0.33, 0.34
8. COURSES: Identifique para quais cursos esta disciplina é oferecida e em que ano, inserindo o CODIGO DO CURSO (ex: ECM, EQM, ADM....) seguido do ano (ex: ECM:1 caso ecm apareca no primeiro ano dessa materia)
9. SEJA PRECISO: Use as informações EXATAS do documento, não invente dados

FORMATO DE RESPOSTA:
Retorne APENAS o JSON válido, sem texto adicional antes ou depois. Comece sua resposta com {{ e termine com }}.
"""

    message_content = [{
        "type": "text",
        "text": (
            f"--- Conteudo do excel ---"
            f"{context_from_excel}"
            f"Analise o conteúdo do arquivo PDF '{filename}' a seguir:\n\n"
            f"--- INÍCIO DO CONTEÚDO DO PDF ---\n"
            f"{content_data['content']}\n"
            f"--- FIM DO CONTEÚDO DO PDF ---\n\n"
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