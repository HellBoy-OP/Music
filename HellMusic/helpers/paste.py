from html_telegraph_poster import TelegraphPoster


async def telegraph_paste(
    title, text, auth="[ †he Hêllẞø† ]", url="https://t.me/its_hellbot"
):
    client = TelegraphPoster(use_api=True)
    client.create_api_token(auth)
    post_page = client.post(
        title=title,
        author=auth,
        author_url=url,
        text=text,
    )
    return post_page["url"]
