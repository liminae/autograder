import os
import django
import random
import datetime
from datetime import timedelta
from django.utils import timezone


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autograder.settings")
django.setup()

from autograder.apps.index.models import GraderUser  # noqa: E402
from autograder.apps.contests.models import Contest  # noqa: E402
from autograder.apps.problems.models import Problem  # noqa: E402
from autograder.apps.runtests.models import Submission  # noqa: E402


def create_users():
    users = []
    for i in range(10):
        user = GraderUser(
            email="example@example.com",
            password="password123",
            username=f"user{i}",
            display_name="User User",
            cf_handle=random.choice(["tourist", "jiangly", "orzdevinwang", "ksun48"]),
            grade=random.choice(["freshman", "sophomore", "junior", "senior"]),
            usaco_division=random.choice(list(GraderUser.USACO_DIVISIONS.keys())),
        )
        user.save()
        users.append(user)
    return users


def create_contests():
    contests = []
    now = timezone.now()
    for i in range(1, 6):
        start_time = now - timedelta(days=random.randint(30, 365))
        end_time = start_time + timedelta(hours=2)
        contest = Contest(
            name=f"Contest {i}",
            rated=True,
            season=2025,
            tjioi=(False if i < 5 else True),
            start=start_time,
            end=end_time,
            editorial="editorial goes here",
        )
        contest.save()
        contests.append(contest)
    return contests


def create_problems_and_submissions(users, contests):
    problem_id = 1
    problems = []

    for contest in contests:
        # Create 5 problems for each contest
        for i in range(5):
            problem = Problem(
                name=f"Problem {problem_id}",
                contest=contest,
                points=(i + 1) * 100,
                statement="Statement",
                inputtxt="Input Format",
                outputtxt="Output Format",
                samples="Samples",
                tl=1000,
                ml=256,
                interactive=False,
                secret=False,
                testcases_zip="problem_testcases/example_testcases.zip",
            )
            problem.save()
            problems.append(problem)
            problem_id += 1

        for user in users:
            for problem in Problem.objects.filter(contest=contest):
                if random.random() < 0.75:
                    start = contest.start
                    end = contest.end
                    delta = (end - start).total_seconds()
                    random_seconds = random.uniform(0, delta)
                    timestamp = start + datetime.timedelta(seconds=random_seconds)

                    sub = Submission(
                        language=random.choice(["python", "cpp", "java"]),
                        code="code goes here",
                        usr=user,
                        verdict=random.choice(["AC", "Wrong Answer"]),
                        runtime=random.randint(10, 2000),
                        contest=contest,
                        problem=problem,
                        insight="insight here",
                        timestamp=timestamp,
                    )
                    sub.save()

    return problems


if __name__ == "__main__":
    users = create_users()
    contests = create_contests()
    problems = create_problems_and_submissions(users, contests)
    print("Filler data created successfully.")
