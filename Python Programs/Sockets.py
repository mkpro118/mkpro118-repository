import socketio
import random

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files={
    '/': 'D:/Projects & Programs/HTML-CSS-JavaScipt Programs/Socket Test/',
})

request_count = 0
client_count = 0
clients = []

board = [['', '', ''],
         ['', '', ''],
         ['', '', '']]


@sio.event
async def connect(sid, environ):
    global client_count
    global request_count
    client_count += 1
    request_count += 1
    print(f'active clients {client_count}')
    print(f'total requests {request_count}')
    if client_count > 2:
        client_count -= 1
        return False
    clients.append(sid)
    if client_count == 2:
        for client in clients:
            sio.enter_room(client, 'Room 1')
        x = random.choice(clients)
        o = clients[0] if x == clients[1] else clients[1]
        await sio.emit('turn', 'XO', to=x)
        await sio.emit('turn', 'OX', to=o)


@sio.event
async def disconnect(sid):
    for client in clients:
        sio.leave_room(client, 'Room 1')
    clients.remove(sid)
    global client_count
    client_count -= 1


@sio.event
async def move(sid, data):
    await sio.emit('move', data, room='Room 1', skip_sid=sid)
