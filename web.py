from aiohttp import web
import asyncio
import time 

text = "Hello"
    
async def name(request):
    # name = request.match_info.get('name', "Anonymous")
    
    await asyncio.sleep(5)
    global text
    text = text + '\n' + "Hello" 
    # ts = time.time() - ts
    ts = time.time()
    ts = int(ts)
    return web.Response(text=text + str(ts))

async def reset(request):
    global text 
    text = "Hello"
    return web.Response(text="reset: " + text)

app = web.Application()
app.add_routes([web.get('/name', name),
                web.get('/reset', reset)
                ])

if __name__ == '__main__':
    web.run_app(app)