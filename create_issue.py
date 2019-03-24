import asyncio
import textwrap
import os

from octomachinery.github.api.tokens import GitHubOAuthToken
from octomachinery.github.api.raw_client import RawGitHubAPI

access_token = GitHubOAuthToken(os.environ["GITHUB_TOKEN"].strip())
gh = RawGitHubAPI(access_token, user_agent='encukou-octomachinery-tutorial')

async def main():
    print('hello world')
    await close_issue()


async def new_comment():
    await gh.post(
        '/repos/mariatta/strange-relationship/issues/163/comments',
        data={'body': "Oh! I thought she's OOOS!  (I'm also a bot)"},
    )


async def close_issue():
    await gh.patch(
        '/repos/mariatta/strange-relationship/issues/163',
        data={'state': 'closed'},
    )

async def new_issue():
    await gh.post(
        '/repos/mariatta/strange-relationship/issues',
        data={
            'title': 'This is an automated announcement',
            'body': textwrap.dedent('''
                Hello from @webknjaz's PyCon SK tutorial
                We're following https://tutorial.octomachinery.dev/en/latest/octomachinery-cmd-line.html

                Thank you for the tutorial!
            '''),
        },
    )

asyncio.run(main())
