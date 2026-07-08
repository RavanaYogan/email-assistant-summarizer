from crewai import Task

def create_reader_task(agent, emails):
    return Task(
        description=f"""
Review the following unread emails.

Emails:
{emails}

Return:
- Sender
- Subject
- Snippet
""",
        expected_output="Structured email overview.",
        agent=agent,
    )


def create_classifier_task(agent, emails):
    return Task(
        description=f"""
Classify the following emails.

Emails:
{emails}

Categories:
- IMPORTANT
- WORK
- PERSONAL
- PROMOTION
- SPAM

For each email provide:
- Category
- Importance
- Reason
""",
        expected_output="Email classification report.",
        agent=agent,
    )


def create_response_task(agent, emails):
    return Task(
        description=f"""
Generate professional reply drafts for emails
that require a response.

Emails:
{emails}
""",
        expected_output="Professional email draft.",
        agent=agent,
    )