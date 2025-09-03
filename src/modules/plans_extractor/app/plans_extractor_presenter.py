
import json
import boto3
import os
import re
import fitz  
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
            
            print(f"Processing file: {object_key} from bucket: {bucket_name}")
            
            response = s3.get_object(Bucket=bucket_name, Key=object_key)
            file_content_bytes = response['Body'].read()
            
            content_for_claude = None
            if object_key.lower().endswith(('.txt', '.csv', '.json')):
                try:
                    text_content = file_content_bytes.decode('utf-8')
                    content_for_claude = {"type": "text", "content": text_content}
                except UnicodeDecodeError:
                    content_for_claude = {"type": "text", "content": "Binary file content that couldn't be decoded"}
            
            elif object_key.lower().endswith('.pdf'):
                try:
                    print("PDF detectado. Extraindo e otimizando o texto...")
                    raw_text = ""
                    with fitz.open(stream=file_content_bytes, filetype="pdf") as doc:
                        for page in doc:
                            raw_text += page.get_text()
                    
                    print(f"Tamanho do texto bruto: {len(raw_text)} caracteres. Estimativa de tokens: ~{len(raw_text)/4:.0f}")

                    optimized_text = clean_and_optimize_text(raw_text)

                    print(f"Tamanho do texto otimizado: {len(optimized_text)} caracteres. Estimativa de tokens: ~{len(optimized_text)/4:.0f}")
                    
                    content_for_claude = {"type": "text", "content": optimized_text}
                except Exception as e:
                    print(f"Falha ao processar PDF {object_key}: {e}")
                    content_for_claude = {"type": "text", "content": f"Erro ao extrair texto do PDF: {e}"}
            else:
                import base64
                base64_content = base64.b64encode(file_content_bytes).decode('utf-8')
                content_for_claude = {"type": "text", "content": f"Binary file content (base64): {base64_content[:1000]}..."}
            
            structured_data = extract_course_data_with_claude(bedrock, content_for_claude, object_key)
            print("Dados estruturados recebidos do Claude:")
            print(json.dumps(structured_data, indent=2))
            
            processed_key = f"processed-{os.path.basename(object_key).split('.')[0]}.json"
            # Adicionar lógica para salvar 'structured_data' em um bucket de destino, se necessário
            
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Files processed successfully',
                'processed_files': len(event['Records'])
            })
        }
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}


def extract_course_data_with_claude(bedrock_client, content_data, filename):
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
8. COURSES: Identifique para quais cursos esta disciplina é oferecida e em que ano
9. SEJA PRECISO: Use as informações EXATAS do documento, não invente dados

FORMATO DE RESPOSTA:
Retorne APENAS o JSON válido, sem texto adicional antes ou depois. Comece sua resposta com {{ e termine com }}.
"""

    message_content = [{
        "type": "text",
        "text": f"Analise o conteúdo do arquivo '{filename}' a seguir:\n\n--- INÍCIO DO CONTEÚDO ---\n{content_data['content']}\n--- FIM DO CONTEÚDO ---\n\n{schema_prompt}",
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