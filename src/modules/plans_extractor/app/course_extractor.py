import urllib
import pymupdf
import boto3
import json
import re

from botocore.exceptions import ClientError
from helper.course.course import Course

HEADER_CROP_COORDS = pymupdf.Rect(0, 0, 595, 620)

INFO_COORDS: dict[str, pymupdf.Rect] = {
    "course_code": pymupdf.Rect(396, 715, 564, 730),
    "course_name": pymupdf.Rect(25, 717, 396, 729)
}

COURSE_CRITERIA_HEADER_REGEX = re.compile(r"AVALIAÇÃO (.*) e CRITÉRIOS DE APROVAÇÃO", re.IGNORECASE)
COURSE_EXAMS_AND_PROJECTS_HEADER_REGEX = re.compile(r"INFORMAÇÕES SOBRE PROVAS E TRABALHOS", re.IGNORECASE)

END_EXTRACTION_REGEX = re.compile(r"PLANO DE ENSINO PARA O ANO LETIVO DE \d{4}", re.IGNORECASE)

def extract_course_info_from_header(page: pymupdf.Page) -> dict[str, str]:
    ptm = page.transformation_matrix
    info_dict = {}

    for key, rect in INFO_COORDS.items():
        info = page.get_textbox(rect * ~ptm)
        if info == "":
            raise ValueError(f"Could not extract {key} from the PDF.")
        info_dict[key] = info

    return info_dict

def extract_course_criteria(doc: pymupdf.Document) -> str:
    extracting = False
    criteria_text = ""

    for page in doc:
        ptm = page.transformation_matrix
        page.set_cropbox(HEADER_CROP_COORDS * ~ptm)

        text = page.get_text()
        for line in text.splitlines():
            if COURSE_CRITERIA_HEADER_REGEX.search(line):
                extracting = True
                continue
            elif END_EXTRACTION_REGEX.search(line):
                extracting = False

            if extracting:
                criteria_text += line + "\n"

    if criteria_text == "":
        raise ValueError("Could not extract course criteria from the PDF.")
    
    return criteria_text

def extract_course_exams_and_projects_info(doc: pymupdf.Document) -> str:
    extracting = False
    exams_and_projects_text = ""

    for page in doc:
        text = page.get_text()
        for line in text.splitlines():
            if COURSE_EXAMS_AND_PROJECTS_HEADER_REGEX.search(line):
                extracting = True
                continue
            elif END_EXTRACTION_REGEX.search(line):
                extracting = False

            if extracting:
                exams_and_projects_text += line + "\n"

    if exams_and_projects_text == "":
        raise ValueError("Could not extract exams and projects info from the PDF.")
    
    return exams_and_projects_text

def generate_json_with_bedrock(course_info: Course) -> str:
    PROMPT_TEMPLATE = """Você é um extrator de dados acadêmicos. A partir do dicionário Python abaixo (gerado por um script de scraping), extraia e estruture as informações no formato JSON especificado.

    ## Entrada
    ```
    {INPUT_DATA}
    ```

    ## Saída esperada
    Retorne APENAS um JSON válido, sem texto adicional, sem markdown, sem explicações. O JSON deve seguir exatamente esta estrutura:

    {{
      "course": "<nome completo da disciplina>",
      "name": "<nome completo da disciplina, mesmo que 'course'>",
      "code": "<código da disciplina, ex: EFB1002>",
      "period": "<período da disciplina se disponível, senão null>",
      "examWeight": <peso das provas como número entre 0 e 1, ex: 0.5>,
      "assignmentWeight": <peso dos trabalhos como número entre 0 e 1, ex: 0.5>,
      "exams": [
        {{
          "id": "<identificador da prova, ex: P1>",
          "name": "<nome descritivo, ex: Primeira Prova Bimestral>",
          "weight": <peso relativo desta prova dentro das provas, entre 0 e 1>,
          "isSubstitute": <true se for prova substitutiva, false caso contrário>
        }}
      ],
      "assignments": [
        {{
          "id": "<identificador do trabalho, ex: T1>",
          "name": "<nome descritivo, ex: Trabalho do Primeiro Bimestre>",
          "weight": <peso relativo deste trabalho dentro dos trabalhos, entre 0 e 1>
        }}
      ],
      "courses": []
    }}

    ## Regras de extração
    - "examWeight" vem do campo "Peso de MP(kp)" dividido pela soma de kp+kt (ex: kp=5, kt=5 → examWeight=0.5)
    - "assignmentWeight" vem do campo "Peso de MT(kt)" dividido pela soma de kp+kt
    - "exams" deve listar todas as provas mencionadas (P1, P2, PS1, etc.)
    - Para provas bimestrais com pesos iguais, cada uma recebe weight = 1 / (número de provas regulares)
    - A prova substitutiva (PS, PS1, etc.) tem isSubstitute: true e weight: null
    - "assignments" deve listar todos os trabalhos mencionados (T1, T2, etc.) com pesos iguais entre si
    - "period" deve ser extraído se mencionado (ex: "1º semestre de 2024"), senão null
    - "courses" deve ser sempre um array vazio []
    - Todos os campos numéricos de peso devem ser números (não strings)"""

    # Create a Bedrock Runtime client in the AWS Region of your choice.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # Set the model ID, e.g., Claude 3 Haiku.
    model_id = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

    PROMPT = PROMPT_TEMPLATE.format(INPUT_DATA=json.dumps(course_info.__dict__, ensure_ascii=False))

    # Format the request payload using the model's native structure.
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": PROMPT}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        response = client.invoke_model(modelId=model_id, body=request)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract and print the response text.
    response_text = model_response["content"][0]["text"]
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    print(response_text)
    return response_text

def load_pdf_from_s3(event: dict) -> pymupdf.Document:
    s3 = boto3.client("s3")

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8'
    )

    print(f"Loading s3://{bucket}/{key}")

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        pdf_bytes = response['Body'].read()
        return pymupdf.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        print(f"Error getting object {key} from bucket {bucket}: {e}")
        raise

def lambda_handler(event, context):
    try:
        doc = load_pdf_from_s3(event)

        header_info = extract_course_info_from_header(doc[0])

        course_criteria = extract_course_criteria(doc)

        exams_and_projects_info = extract_course_exams_and_projects_info(doc)

        course = Course(
            name=header_info["course_name"],
            code=header_info["course_code"],
            criteria=course_criteria,
            exams_and_projects_info=exams_and_projects_info
        )

        generate_json_with_bedrock(course)
    except Exception as e:
        print(f"An error occurred: {e}")
