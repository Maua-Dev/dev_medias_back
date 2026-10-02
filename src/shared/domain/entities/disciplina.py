from pydantic import BaseModel, ConfigDict, Field


class ItemAvaliacao(BaseModel):
    """Componente ponderado de prova ou trabalho (ex.: P1, T1)."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    weight: float


class Disciplina(BaseModel):
    """
    Disciplina com pesos de avaliação e vínculos a cursos (códigos de grade → período).
    """

    model_config = ConfigDict(str_strip_whitespace=True, populate_by_name=True)

    course: str = Field(..., description="Curso da disciplina")
    name: str = Field(..., description="Nome da disciplina")
    code: str = Field(..., description="Código da disciplina")
    period: str = Field(..., description="Período da disciplina")
    exam_weight: float = Field(..., alias="examWeight", description="Peso das provas")
    assignment_weight: float = Field(..., alias="assignmentWeight", description="Peso dos trabalhos")
    exams: list[ItemAvaliacao] = Field(..., description="Provas")
    assignments: list[ItemAvaliacao] = Field(..., description="Trabalhos")
    courses: dict[str, int] = Field(..., description="Cursos e anos")
    study_plan_download_pdf_url: str | None = Field(
        default=None,
        alias="studyPlanDownloadPdfUrl",
        description="URL HTTP do plano de ensino (CloudFront/S3)",
    )
    exams_code: str | None = Field(
        default=None,
        alias="examsCode",
        description="Código do critério de aprovação (ex.: C4/2015)",
    )
