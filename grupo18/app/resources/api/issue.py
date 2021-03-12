from flask import jsonify
from app.models.issue import Issue


def index():
    issues = Issue.all()

    data = []

    for issue in issues:
        data.append(
            {
                "email":
                issue.email,
                "description":
                issue.description
            }
        )

    return jsonify(issues=data)
