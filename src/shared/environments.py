import enum
from enum import Enum
import os


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
            self.endpoint_url = "http://localhost:8000"
            self.cloud_front_distribution_domain = "https://d3q9q9q9q9q9q9.cloudfront.net"

        else:
            self.region = os.environ.get("AWS_REGION")
            self.endpoint_url = os.environ.get("ENDPOINT_URL")
            self.cloud_front_distribution_domain = os.environ.get("CLOUD_FRONT_DISTRIBUTION_DOMAIN")

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
