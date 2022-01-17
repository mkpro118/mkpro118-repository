from aiohttp import web


async def start_server(request):
    with open('index.html') as response:
        return web.Response(text=response.read(), content_type='text/html')

app = web.Application()
app.add_routes([web.get('/', start_server)])


def start_server_cli(args):
    app = web.Application()
    app.router.add_get("/", start_server)
    return app


if __name__ == '__main__':
    web.run_app(app)
