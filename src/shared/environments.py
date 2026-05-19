import enum
from enum import Enum
import os

from src.shared.infra.external.dynamo.academic_catalog.academic_catalog_naming import physical_table_name


class STAGE(Enum):
    DOTENV = "DOTENV"
    DEV = "DEV"
    HOMOLOG = "HOMOLOG"
    PROD = "PROD"
    TEST = "TEST"


class Environments:
    """
    Defines the environment variables for the application. You should not instantiate this class directly. Please use Environments.get_envs() method instead.

    Usage:

    """
    stage: STAGE
    region: str
    endpoint_url: str = None
    cloud_front_distribution_domain: str

    def _configure_local(self):
        from dotenv import load_dotenv
        load_dotenv()
        os.environ["STAGE"] = os.environ.get("STAGE") or STAGE.DOTENV.value

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.DOTENV.value:
            self._configure_local()

        self.stage = STAGE[os.environ.get("STAGE")]

        if self.stage == STAGE.TEST:
            self.region = "sa-east-1"
            self.endpoint_url = os.environ.get("ENDPOINT_URL") or "http://localhost:8000"
            self.cloud_front_distribution_domain = "https://d3q9q9q9q9q9q9.cloudfront.net"

        else:
            self.region = os.environ.get("AWS_REGION")
            self.endpoint_url = os.environ.get("ENDPOINT_URL")
            self.cloud_front_distribution_domain = os.environ.get("CLOUD_FRONT_DISTRIBUTION_DOMAIN")

        self.academic_catalog_table_name = (
            os.environ.get("ACADEMIC_CATALOG_TABLE_NAME")
            or os.environ.get("ENTITY_TABLE_NAME")
            or os.environ.get("DISCIPLINA_TABLE_NAME")
            or os.environ.get("CURSO_TABLE_NAME")
            or physical_table_name(self.stage.value)
        )
        self.disciplina_table_name = self.academic_catalog_table_name
        self.curso_table_name = self.academic_catalog_table_name

    # @staticmethod
    # def get_product_repo() -> IProductRepository:
    #     if Environments.get_envs().stage == STAGE.TEST:
    #         from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
    #         return UserRepositoryDynamo
    #     elif Environments.get_envs().stage in [STAGE.PROD, STAGE.DEV, STAGE.HOMOLOG]:
    #         from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo#from src.shared.infra.repositories.product_repository_dynamo import ProductRepositoryDynamo
    #         return UserRepositoryDynamo #ProductRepositoryDynamo        
    #     else:
    #         raise Exception("No repository found for this stage")

    @staticmethod
    def get_disciplina_repo():
        stage = os.environ.get("STAGE")
        running_in_ci = os.environ.get("GITHUB_ACTIONS", "").strip().lower() == "true"
        if stage == STAGE.TEST.value or running_in_ci:
            from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock

            return DisciplinaRepositoryMock()

        from src.shared.infra.repositories.disciplina_repository_dynamo import DisciplinaRepositoryDynamo

        return DisciplinaRepositoryDynamo()

    @staticmethod
    def get_envs() -> "Environments":
        """
        Returns the Environments object. This method should be used to get the Environments object instead of instantiating it directly.
        :return: Environments (stage={self.stage}, s3_bucket_name={self.s3_bucket_name}, region={self.region}, endpoint_url={self.endpoint_url})

        """
        envs = Environments()
        envs.load_envs()
        return envs

    def __repr__(self):
        return self.__dict__
