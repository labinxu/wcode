import asyncio
from aiohttp import web

async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body='<h1>Index</h1>')

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))

async def init(loop):
    app = web.Application(loop=loop, middlewares=(middleware1, middleware2))
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000')
    return srv

def test(request):
    print('Handler function called')
    return web.Response(text='Hello')
@web.middleware
async def middleware1(request, handler):
    print('Middleware 1 called')
    response = await handler(request)
    print('Middleware 1 finished')
    return response

@web.middleware
async def middleware2(request, handler):
    print('Middleware 2 called')
    response = await handler(request)
    print('Middleware 2 finished')
    return response


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
#from concurrent.futures import ThreadPoolExecutor
