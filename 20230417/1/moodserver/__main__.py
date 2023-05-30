import asyncio
from .server import main

def serve():
    asyncio.run(main())

if __name__ == '__main__':
    serve()
