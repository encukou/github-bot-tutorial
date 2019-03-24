from octomachinery.app.server.runner import run as run_app
from octomachinery.app.routing import process_event_actions
from octomachinery.app.routing.decorators import process_webhook_payload
from octomachinery.app.runtime.context import RUNTIME_CONTEXT


@process_event_actions('issues', {'opened'})
@process_webhook_payload
async def on_issue_opened(
        *,
        action, issue, repository, sender, installation,
        assignee=None, changes=None,
):
    """Whenever an issue is opened, greet the author and say thanks."""
    github_api = RUNTIME_CONTEXT.app_installation_client

    comments_api_url = issue["comments_url"]

    author = issue["user"]["login"]
    message = (
        f"Thanks for the report @{author}! "
        f"My human companion will look into it ASAP! (I'm a bot [¤_¤])."
    )

    await github_api.post(comments_api_url, data={"body": message})


@process_event_actions('issue_comment', {'created'})
@process_webhook_payload
async def on_comment_created(
        *,
        action, changes, issue, comment,
        repository=None, sender=None, installation=None,
        assignee=None,
):
    """Whenever an issue comment is added, add reaction."""
    comments_api_url = comment['url']
    reactions_url = comments_api_url + '/reactions'

    await github_api.post(
        reactions_url,
        data={"body": "+1"},
        preview_api_version='squirrel-girl-preview',
    )


if __name__ == "__main__":
    run_app(
        name='Comment Reactor - PyCon SK tutorial (@encukou)',
        version='1.0.0',
        url='https://github.com/apps/comment-reactor-pycon-sk-tutorial',
    )
