from aws_cdk import (
    Duration,
    aws_sqs as sqs,
)
from constructs import Construct


class SqsConstruct(Construct):
    """SQS Standard queues for plans_extractor (main + DLQ)."""

    plans_extractor_queue: sqs.Queue
    plans_extractor_dlq: sqs.Queue

    def __init__(self, scope: Construct, construct_id: str, stage: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stage_lower = stage.lower()

        self.plans_extractor_dlq = sqs.Queue(
            self,
            "PlansExtractorDlq",
            queue_name=f"devmedias-plans-extractor-{stage_lower}-dlq",
            retention_period=Duration.days(14),
        )

        self.plans_extractor_queue = sqs.Queue(
            self,
            "PlansExtractorQueue",
            queue_name=f"devmedias-plans-extractor-{stage_lower}",
            visibility_timeout=Duration.seconds(1800),
            retention_period=Duration.days(14),
            dead_letter_queue=sqs.DeadLetterQueue(
                max_receive_count=3,
                queue=self.plans_extractor_dlq,
            ),
        )
