from src.modules.export_legacy_catalog.app.export_legacy_catalog_usecase import (
    ExportLegacyCatalogUsecase,
)


class _FakeTable:
    def scan(self, **kwargs):
        return {
            "Items": [
                {
                    "pk": "GLOBAL#DISCIPLINA#XYZ1",
                    "entity_type": "DISCIPLINA",
                    "code": "XYZ1",
                    "name": "Subject X",
                    "course": "Course",
                    "period": "A",
                    "exam_weight": 1,
                    "assignment_weight": 0,
                    "exams": [{"name": "P1", "weight": 1}],
                    "assignments": [],
                    "courses": {"CIC": 1},
                },
                {
                    "pk": "GLOBAL#CURSO#CIC",
                    "entity_type": "CURSO",
                    "código": "CIC",
                    "nome": "Ciência da Computação",
                },
            ]
        }


class _FakeS3:
    def __init__(self):
        self.puts = []

    def put_object(self, **kwargs):
        self.puts.append(kwargs)
        return {}


def test_export_usecase_writes_both_json_files():
    s3 = _FakeS3()
    usecase = ExportLegacyCatalogUsecase(
        table_name="DevMediasAcademicCatalogTable-v2-dev",
        bucket_name="legacy-bucket",
        subjects_key="allSubjects.json",
        courses_key="courses.json",
        dynamodb_table=_FakeTable(),
        s3_client=s3,
    )

    result = usecase()

    assert result["ok"] is True
    assert result["subjects_count"] == 1
    assert result["courses_count"] == 1
    assert result["subjects_uri"] == "s3://legacy-bucket/allSubjects.json"
    assert result["courses_uri"] == "s3://legacy-bucket/courses.json"
    assert len(s3.puts) == 2
    assert {p["Key"] for p in s3.puts} == {"allSubjects.json", "courses.json"}
    assert all(p["ContentType"].startswith("application/json") for p in s3.puts)
