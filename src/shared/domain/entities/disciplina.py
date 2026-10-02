from pydantic import BaseModel, ConfigDict, Field


class ItemAvaliacao(BaseModel):
    """Componente ponderado de prova ou trabalho (ex.: P1, T1)."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    weight: float


class Disciplina(BaseModel):
    """
    Disciplina com pesos de avaliação e vínculos a cursos (códigos de grade → período).

    Catálogo oficial: device_id=None, is_custom=False (owner Dynamo GLOBAL).
    Custom do app: device_id=<uuid>, is_custom=True (owner Dynamo = device_id).
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
    courses: dict[str, int] = Field(default_factory=dict, description="Cursos e anos")
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
    device_id: str | None = Field(
        default=None,
        alias="deviceId",
        description="UUID do dispositivo dono (somente matérias custom)",
    )
    is_custom: bool = Field(
        default=False,
        alias="isCustom",
        description="True se criada pelo app (não faz parte do catálogo oficial)",
    )
    created_at: str | None = Field(
        default=None,
        alias="createdAt",
        description="ISO-8601 UTC de criação",
    )
    updated_at: str | None = Field(
        default=None,
        alias="updatedAt",
        description="ISO-8601 UTC da última atualização",
    )
