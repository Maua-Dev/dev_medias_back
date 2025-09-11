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
                "description": "Informações sobre quais cursos possuem esta disciplina e em qual ano (PRIORIDADE: Excel, use prefixo de CURSO_CORRIGIDO como chave, ano de PERIODO)",
                "patternProperties": {
                    "^(EAL|ECA|ECM|EEN|EET|EMC|EPM|EQM|ETC|ADM|DSG|CIC|SIN|IA|ARQ|RI|ADS|AL|CA|CMP|CV|EN|ET|FB|MC|PM|QM)$": {
                        "type": "number", "minimum": 1, "maximum": 6, "description": "Ano do curso (1 a 6)"
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
   - Para 'period': Baseado em 'SEMESTRALIDADE'. Se contém 'S' (ex: S1, S2), use 'S'. Se contém 'AN', use 'A'. Se múltiplas linhas, use o mais comum ou o primeiro.
   - Para 'courses': Agregue por disciplina. Para cada linha única, extraia o prefixo de 3 letras do campo 'CURSO_CORRIGIDO' (ex: 'ADM', 'CIC', etc.) como chave. Determine o ano do campo 'PERIODO' (ex: '1ª Série' -> 1, '2ª Série' -> 2). Se múltiplas linhas para o mesmo curso, use o ano mais apropriado (mínimo ou médio). Ignore linhas duplicadas para o mesmo curso/ano.
   - Se o Excel estiver vazio, use inferência do PDF ou valores padrão (period: 'S', courses: {{}}).

2.  **Extração do PDF:** Para todos os outros campos ('course', 'name', 'code', 'examWeight', 'assignmentWeight', 'exams', 'assignments'), use EXCLUSIVAMENTE o texto dentro das tags <pdf_text>. Inferir pesos, nomes de provas/trabalhos logicamente do conteúdo (ex: pesos totais devem somar 1.0 para exams e assignments; examWeight + assignmentWeight = 100).

3.  **Raciocínio Lógico:** Antes de gerar o JSON final, pense passo a passo dentro de tags <thinking>. Descreva como você encontrou cada valor, especialmente como processou 'period' e 'courses' do Excel, e o resto do PDF. Explique agregações em 'courses' se houver múltiplas linhas.

4.  **Formato de Saída:** Após a tag </thinking>, forneça APENAS o objeto JSON válido, sem comentários, explicações ou formatação de bloco de código. Certifique-se de que é um JSON válido e completo conforme o schema.
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
            modelId='us.anthropic.claude-sonnet-4-20250514-v1:0',
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
            
            # Remove marcações de bloco de código se existirem
            json_part = re.sub(r'^```json\s*', '', json_part)
            json_part = re.sub(r'```$', '', json_part)

            structured_data = json.loads(json_part)
        else:
            print("Bloco <thinking> não encontrado. Tentando parse direto do JSON.")
            structured_data = json.loads(claude_response)
        
        usage = response_body.get('usage', {})
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)
        
        # Custo estimado (USD) baseado nos preços do Claude 3 Sonnet no Bedrock (us-east-1) em Set/2025
        # Input: $0.003 / 1K tokens | Output: $0.015 / 1K tokens
        estimated_cost = (input_tokens * 0.003 / 1000) + (output_tokens * 0.015 / 1000)
        
        print(f"Claude API Usage - Input: {input_tokens}, Output: {output_tokens}, Total: {input_tokens + output_tokens}")
        print(f"File: {filename} - Estimated cost: ${estimated_cost:.6f}")
        
        structured_data['token_usage'] = {
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens,
            'estimated_cost_usd': estimated_cost
        }
        
        return structured_data
        
    except Exception as e:
        print(f"Error calling Claude: {str(e)}")
        print(f"Full response from Claude was: {claude_response}")
        return {"error": f"Failed to process with Claude: {str(e)}"}

def lambda_handler(event, context):
    """
    Função principal da Lambda que é acionada por um evento do S3.
    """
    print("Evento recebido:", json.dumps(event))
    
    s3 = boto3.client("s3")
    bedrock_region = os.environ.get("BEDROCK_REGION", "us-east-1")
    bedrock = boto3.client("bedrock-runtime", region_name=bedrock_region)
    
    # Dicionário para CORRIGIR siglas antigas para as siglas canônicas.
    # Esta parte é mantida para garantir a padronização.
    mapa_antigo_para_novo = {
        'AL': 'EAL', 'CA': 'ECA', 'CMP': 'ECM', 'EN': 'EEN', 'ET': 'EET',
        'MC': 'EMC', 'PM': 'EPM', 'QM': 'EQM', 'CV': 'ETC', 'RI': 'RIT',
        'ADM': 'ADM', 'DSG': 'DSG', 'CIC': 'CIC', 'SIN': 'SIN', 'ARQ': 'ARQ',
        'ICD': 'ICD'
    }

    # REMOVIDO: O mapa de código para nome completo não é mais necessário.

    try:
        bucket_name = event["Records"][0]['s3']['bucket']['name']
        excel_key = "relacao_disciplinas.xlsx"
        
        all_subjects_key = "allSubjects.json"
        all_subjects_data = {}
        try:
            print(f"Carregando arquivo de consolidação: s3://{bucket_name}/{all_subjects_key}")
            json_object = s3.get_object(Bucket=bucket_name, Key=all_subjects_key)
            all_subjects_data = json.loads(json_object['Body'].read().decode('utf-8'))
            print("Arquivo allSubjects.json carregado com sucesso.")
        except s3.exceptions.NoSuchKey:
            print("Arquivo allSubjects.json não encontrado. Um novo será criado.")
            all_subjects_data = {}
        
        print(f"Carregando a fonte da verdade de: s3://{bucket_name}/{excel_key}")
        excel_response = s3.get_object(Bucket=bucket_name, Key=excel_key)
        excel_bytes = excel_response["Body"].read()
        
        df_truth = pd.read_excel(BytesIO(excel_bytes), header=2)
        
        df_truth.columns = df_truth.columns.str.strip()
        df_truth.dropna(how='all', inplace=True)
        df_truth.dropna(subset=['CODIGO DISCIPLINA'], inplace=True)

        # CORREÇÃO DE SIGLAS: Cria uma nova coluna 'CURSO_CORRIGIDO' aplicando o mapa.
        df_truth['CURSO_CORRIGIDO'] = df_truth['CURSO'].map(mapa_antigo_para_novo).fillna(df_truth['CURSO'])
        print("Códigos de curso corrigidos com sucesso no DataFrame.")

        for record in event["Records"]:
            object_key = unquote_plus(record['s3']['object']['key'])
            
            if object_key.startswith("plans/"):
                print(f"Processando arquivo de plano: {object_key}")

                filename = os.path.basename(object_key)
                subject_code = filename.split('.')[0]
                print(f"Código da disciplina extraído: {subject_code}")

                all_matching_rows = df_truth[df_truth['CODIGO DISCIPLINA'] == subject_code]
            
                context_from_excel = ""
                if not all_matching_rows.empty:
                    # Usa a coluna corrigida para gerar o contexto para o Claude
                    context_df = all_matching_rows[['CODIGO DISCIPLINA', 'DISCIPLINA', 'CURSO_CORRIGIDO', 'GRADE', 'PERIODO', 'SEMESTRALIDADE']].copy()
                    context_df.rename(columns={'CURSO_CORRIGIDO': 'CURSO'}, inplace=True)
                    
                    info_list = context_df.to_dict(orient='records')
                    
                    context_from_excel = (
                        "Aqui estão os dados da fonte da verdade (Excel) para esta disciplina. "
                        "Use estes dados para preencher ou corrigir as informações do PDF, especialmente os campos 'period' e 'courses'.\n"
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

                # Chama o Claude para extrair os dados. A resposta já virá com as siglas corretas.
                dados_finais = extract_course_data_with_claude(
                    bedrock, 
                    content_for_claude, 
                    object_key, 
                    context_from_excel  
                )
                
                if 'error' not in dados_finais:
                    print(f"Atualizando dados para a disciplina {subject_code} no consolidado.")
                    all_subjects_data[subject_code] = dados_finais
                else:
                    print(f"Erro ao processar {subject_code}. Não será adicionado ao consolidado.")                
                
                print("Dados Finais (com siglas de cursos padronizadas):")
                print(json.dumps(dados_finais, indent=2, ensure_ascii=False))
            
            else:
                print(f"Pulando arquivo, não é um plano de ensino: {object_key}")
                
        print(f"Salvando arquivo consolidado atualizado em s3://{bucket_name}/{all_subjects_key}")
        s3.put_object(
            Bucket=bucket_name,
            Key=all_subjects_key,
            Body=json.dumps(all_subjects_data, indent=2, ensure_ascii=False),
            ContentType='application/json'
        )
        print("Arquivo allSubjects.json salvo com sucesso.")

        return {'statusCode': 200, 'body': json.dumps({'message': 'Event processed successfully'})}
        
    except KeyError as ke:
        print(f"Erro de Chave (KeyError): A coluna {str(ke)} não foi encontrada. Verifique o arquivo Excel e o código.")
        return {'statusCode': 500, 'body': json.dumps({'error': f"KeyError: {str(ke)}"})}
    except Exception as e:
        import traceback
        print(f"Erro geral no handler: {type(e).__name__} - {str(e)}")
        traceback.print_exc()
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}