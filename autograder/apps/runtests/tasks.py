import logging
from typing import Dict, Any
from celery import shared_task
from django.db import transaction

from .models import Submission
from ...coderunner.handlers import run_code_handler

logger = logging.getLogger(__name__)


@transaction.atomic
def _update_submission_from_result(submission_id: int, result_data: Dict[str, Any]):
    submission = Submission.objects.select_for_update().get(id=submission_id)
    submission.verdict = result_data.get("verdict", "ER")
    submission.runtime = result_data.get("runtime", -1)
    submission.memory = result_data.get("memory", -1)
    submission.insight = result_data.get("output", "")
    submission.save()


@transaction.atomic
def _mark_submission_as_error(submission_id: int, error_message: str):
    try:
        submission = Submission.objects.select_for_update().get(id=submission_id)
        submission.verdict = "Internal Server Error"
        submission.insight = error_message
        submission.runtime = -1
        submission.memory = -1
        submission.save()
    except Submission.DoesNotExist:
        logger.error(f"Could not find submission {submission_id} to mark as an error.")


@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue="coderunner_queue")
def grade_submission_task(self, submission_id: int):
    try:
        submission = Submission.objects.select_related("problem").get(id=submission_id)
        if submission.verdict == "Skipped":
            logger.info(
                f"Submission {submission_id} is marked as 'Skipped'. Aborting task."
            )
            return

    except Submission.DoesNotExist:
        logger.error(f"Submission {submission_id} not found. Task will not be retried.")
        return

    response = run_code_handler(
        submission.problem.tl,
        submission.problem.ml,
        submission.language,
        submission.problem.id,
        submission.id,
        submission.code,
    )
    if "error" in response:
        logger.exception(
            f"An error occurred while processing submission {submission.id}"
        )
        _mark_submission_as_error(submission_id, response["error"])
    else:
        _update_submission_from_result(submission_id, response)
