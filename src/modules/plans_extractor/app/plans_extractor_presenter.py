import json
import boto3
import urllib.parse
import os
from urllib.parse import unquote_plus
import fitz

def lambda_handler(event, context):
    """
    Função principal da Lambda que é acionada por um evento do S3.
    """
    
    print("Evento recebido:", json.dumps(event))
    
    plans_bucket = os.environ.get("PLANS_BUCKET_NAME")
    
    s3 = boto3.client("s3")
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
    
    try:
        
        for record in event["Records"]:
            
            bucket_name = record['s3']['bucket']['name']
            object_key = unquote_plus(record['s3']['object']['key'])
            
            print(f"Processing file: {object_key} from bucket: {bucket_name}")
            
            # Downloading from plans bucket
            response = s3.get_object(Bucket=bucket_name, Key=object_key)
            file_content = response['Body'].read()
            
            # Try to decode the file content as text or prepare for document analysis
            content_for_claude = None
            if object_key.lower().endswith(('.txt', '.csv', '.json')):
                try:
                    text_content = file_content.decode('utf-8')
                    content_for_claude = {"type": "text", "content": text_content}
                except UnicodeDecodeError:
                    content_for_claude = {"type": "text", "content": "Binary file content that couldn't be decoded"}
            elif object_key.lower().endswith('.pdf'):
                # CORREÇÃO: Extrai o texto do PDF antes de enviar para o Claude
                try:
                    with fitz.open(stream=file_content, filetype="pdf") as doc:
                        pdf_text = ""
                        for page in doc:
                            pdf_text += page.get_text()
                    content_for_claude = {"type": "text", "content": pdf_text}
                except Exception as e:
                    print(f"Failed to extract text from PDF {object_key}: {e}")
                    content_for_claude = {"type": "text", "content": "Error extracting text from PDF."}

            else:
                # For other file types, convert to base64 for analysis
                import base64
                base64_content = base64.b64encode(file_content).decode('utf-8')
                content_for_claude = {"type": "text", "content": f"Binary file content (base64): {base64_content[:1000]}..."}
            
            # Call Claude Sonnet 4 to extract structured course data
            structured_data = extract_course_data_with_claude(bedrock, content_for_claude, object_key)
            print(structured_data)
            
            # Create the processed file with structured data
            processed_key = f"processed-{object_key.split('.')[0]}.json"
            
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Files processed successfully with Claude Sonnet 4',
                'processed_files': len(event['Records'])
            })
        }
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }


def extract_course_data_with_claude(bedrock_client, content_data, filename):
    """
    Use Claude Sonnet 4 to extract structured course data from the content
    """
    
    # Define the JSON schema for a single subject
    schema = {
        "type": "object",
        "properties": {
            "course": {"type": "string", "description": "Nome completo do curso"},
            "name": {"type": "string", "description": "Nome completo da disciplina"},
            "code": {"type": "string", "description": "Código da disciplina (ex: DSG244)"},
            "period": {"type": "string", "enum": ["A", "S"], "description": "A para Anual, S para Semestral"},
            "examWeight": {"type": "number", "minimum": 0.0, "maximum": 100.0, "description": "Peso das provas em %"},
            "assignmentWeight": {"type": "number", "minimum": 0.0, "maximum": 100.0, "description": "Peso dos trabalhos em %"},
            "exams": {
                "type": "array",
                "maxItems": 4,
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "enum": ["P1", "P2", "P3", "P4"]},
                        "weight": {"type": "number", "minimum": 0.0, "maximum": 1.0}
                    },
                    "required": ["name", "weight"]
                }
            },
            "assignments": {
                "type": "array",
                "maxItems": 10,
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "enum": ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10"]},
                        "weight": {"type": "number", "minimum": 0.0, "maximum": 1.0}
                    },
                    "required": ["name", "weight"]
                }
            },
            "courses": {
                "type": "object",
                "description": "Informações sobre quais cursos possuem esta disciplina e em qual ano",
                "patternProperties": {
                    "^(EAL|ECA|ECM|EEN|EET|EMC|EPM|EQM|ETC|ADM|DSG|CIC|SIN|IA|ARQ|RI|ADS)$": {
                        "type": "number",
                        "minimum": 1,
                        "maximum": 5,
                        "description": "Ano do curso (1 a 5)"
                    }
                }
            }
        },
        "required": ["course", "name", "code", "period", "examWeight", "assignmentWeight", "exams", "assignments"]
    }
    
    # Create the base prompt for JSON schema
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
        - Procure por "Peso de MT(%)" e "Peso de MP(%)" na seção de avaliação
        - MT = Média dos Trabalhos, MP = Média de Prova
        - Se encontrar "Peso de MP(%): 0,7" significa examWeight = 70
        - Se encontrar "Peso de MT(%): 0,3" significa assignmentWeight = 30
        - examWeight + assignmentWeight DEVE somar 100
        7. PESOS INDIVIDUAIS:
        - Para cada prova/trabalho: peso individual que soma 1.0 dentro do respectivo array
        - Ex: 4 provas = 0.25 cada; 3 trabalhos = 0.33, 0.33, 0.34
        8. COURSES: Identifique para quais cursos esta disciplina é oferecida e em que ano
        9. SEJA PRECISO: Use as informações EXATAS do documento, não invente dados

        FORMATO DE RESPOSTA:
        Retorne APENAS o JSON válido, sem texto adicional antes ou depois. Comece sua resposta com {{ e termine com }}.
    """

    message_content = [
        {
            "type": "text",
            "text": f"Conteúdo do arquivo '{filename}':\n{content_data['content']}\n\n{schema_prompt}",
        }
    ]

    try:
        # Call Claude Sonnet 4 using cross-region inference profile
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "user",
                        "content": message_content
                    }
                ],
                "temperature": 0.1
            })
        )
        
        # Parse the response
        response_body = json.loads(response['body'].read())
        claude_response = response_body['content'][0]['text']
        
        # Log token usage information
        usage = response_body.get('usage', {})
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)
        total_tokens = input_tokens + output_tokens
        
        print(f"Claude API Usage - Input tokens: {input_tokens}, Output tokens: {output_tokens}, Total tokens: {total_tokens}")
        print(f"File: {filename} - Token cost: ${float(total_tokens * 0.000015):.6f}")  # Approximate cost for Claude 4 Sonnet
        
        # Extract JSON from Claude's response
        try:
            # Try to parse the JSON directly
            structured_data = json.loads(claude_response)
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from the response
            import re
            print(f"Direct JSON parsing failed. Attempting to extract JSON from response...")
            print(f"Claude response preview: {claude_response[:500]}...")
            
            # Try multiple regex patterns to extract JSON
            json_patterns = [
                r'\{.*\}',  # Basic pattern
                r'```json\s*(\{.*\})\s*```',  # JSON in code blocks
                r'JSON:\s*(\{.*\})',  # JSON after "JSON:" label
                r'```\s*(\{.*\})\s*```',  # JSON in any code blocks
            ]
            
            structured_data = None
            for pattern in json_patterns:
                json_match = re.search(pattern, claude_response, re.DOTALL | re.IGNORECASE)
                if json_match:
                    try:
                        # Extract the matched group (or the whole match if no groups)
                        json_text = json_match.group(1) if json_match.groups() else json_match.group(0)
                        structured_data = json.loads(json_text)
                        print(f"Successfully extracted JSON using pattern: {pattern}")
                        break
                    except json.JSONDecodeError:
                        continue
            
            if structured_data is None:
                print(f"All JSON extraction attempts failed. Full Claude response: {claude_response}")
                raise ValueError("Could not extract valid JSON from Claude's response")
        
        # Add token usage information to the structured data
        structured_data['token_usage'] = {
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': total_tokens,
            'estimated_cost_usd': float(total_tokens * 0.000015)
        }
        
        return structured_data
        
    except Exception as e:
        print(f"Error calling Claude: {str(e)}")
        # Return a default structure if Claude fails
        content_preview = ""
        if content_data["type"] == "text":
            content_text = content_data["content"]
            content_preview = content_text[:500] + "..." if len(content_text) > 500 else content_text
        else:
            content_preview = f"Document file: {filename}"
            
        return {
            "course": "Unknown",
            "name": "Unknown Subject", 
            "code": "UNK000",
            "period": "Unknown",
            "examWeight": 50,
            "assignmentWeight": 50,
            "exams": [],
            "assignments": [],
            "courses": {},
            "error": f"Failed to process with Claude: {str(e)}",
            "original_content_preview": content_preview
        }