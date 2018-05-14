import asyncio, logging
import aiohttp
from aiohttp import web
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s')
logger = logging.getLogger(__name__)
routes = web.RouteTableDef()

async def index(request):
    return web.Response(text='Hello Aiohttp!')

async def join(request):
    ''' join the game'''
    data = await request.json()

async def exam_post(request):
    post = await request.json()
    try:
        resp = web.Response(text='Post data %s'% post['name'])
    except Exception as e:
        resp =  web.Response(text=str(e))

    return resp

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data+'/answer')

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())
    print('websocket connection closed')

    return ws


'''
from flask.ext.aiohttp import websocket


@app.route('/echo')
@websocket
def echo():
    while True:
        msg = yield from aio.ws.receive_msg()

        if msg.tp == aiohttp.MsgType.text:
            aio.ws.send_str(msg.data)
        elif msg.tp == aiohttp.MsgType.close:
            print('websocket connection closed')
            break
        elif msg.tp == aiohttp.MsgType.error:
            print('ws connection closed with exception %s',
                  aio.ws.exception())
            break
You also can use most features of flask with websocket.

from flask.ext.aiohttp import websocket


@app.route('/hello/<name>')
@websocket
def hello(name):
    while True:
        msg = yield from aio.ws.receive_msg()

        if msg.tp == aiohttp.MsgType.text:
            aio.ws.send_str('Hello, {}'.format(name))
        elif msg.tp == aiohttp.MsgType.close:
            print('websocket connection closed')
            break
        elif msg.tp == aiohttp.MsgType.error:
            print('ws connection closed with exception %s',
                  aio.ws.exception())
            break'''
