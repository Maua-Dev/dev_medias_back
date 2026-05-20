import json

from src.modules.plans_extractor.app.course_extractor import generate_json_with_bedrock
from src.modules.plans_extractor.app.helper.course.course import Course


class _FakeBody:
    def __init__(self, payload: dict):
        self._payload = payload

    def read(self):
        return json.dumps(self._payload).encode("utf-8")


class _FakeBedrockClient:
    def __init__(self, response_text: str):
        self.response_text = response_text

    def invoke_model(self, modelId, body):
        return {
            "body": _FakeBody(
                {
                    "output": {
                        "message": {
                            "content": [{"text": self.response_text}],
                        }
                    }
                }
            )
        }


def _course():
    return Course(
        name="Algoritmos",
        code="ADS1003",
        criteria="criterios",
        exams_and_projects_info="provas e trabalhos",
    )


def test_parseia_resposta_bedrock_com_markdown_fence(monkeypatch):
    response_text = """```json
{"name":"Algoritmos","code":"ADS1003","examWeight":0.5}
```"""
    monkeypatch.setattr(
        "src.modules.plans_extractor.app.course_extractor.boto3.client",
        lambda *_args, **_kwargs: _FakeBedrockClient(response_text),
    )

    extracted = generate_json_with_bedrock(_course())

    assert extracted == {"name": "Algoritmos", "code": "ADS1003", "examWeight": 0.5}


def test_parseia_resposta_bedrock_incompleta_sem_falhar(monkeypatch):
    response_text = """```json
{"name":"Algoritmos","code":"ADS1003"}
```"""
    monkeypatch.setattr(
        "src.modules.plans_extractor.app.course_extractor.boto3.client",
        lambda *_args, **_kwargs: _FakeBedrockClient(response_text),
    )

    extracted = generate_json_with_bedrock(_course())

    assert extracted == {"name": "Algoritmos", "code": "ADS1003"}
