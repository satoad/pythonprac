import asyncio

def sqroots(coeffs:str) -> str:
    coeffs = coeffs.split()
    a, b, c = int(coeffs[0]), int(coeffs[1]), int(coeffs[2])
    d = b ** 2 - 4 * a * c
    
    if d < 0:
        return ""
    elif d == 0:
        return (-b/(2 * a), -b/(2 * a))
    else:
        root1 = (-b + d**0.5) / (2 * a)
        root2 = (-b - d**0.5) / (2 * a)
        return (min(root1, root2), max(root1, root2))

async def echo(reader, writer):
    while data := await reader.readline():
        me = "{}:{}".format(*writer.get_extra_info('peername'))
        print(me)

        writer.write(str(sqroots(data)) + "\n").encode())
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
