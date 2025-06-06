# https://github.com/Infamous-Hydra/YaeMiko
# https://github.com/Team-ProjectCodeX

# <============================================== IMPORTS =========================================================>
from aiohttp import ClientSession
from httpx import AsyncClient, Timeout
from Python_ARQ import ARQ

# <=============================================== SETUP ========================================================>
# Aiohttp Async Client
session: ClientSession = None # Initialize as None
state: AsyncClient = None # Initialize as None

# <=============================================== ARQ SETUP ========================================================>
ARQ_API_KEY = "RLWCED-WZASYO-AWOLTB-ITBWTP-ARQ"  # GET API KEY FROM @ARQRobot
ARQ_API_URL = "arq.hamker.dev"

arq: ARQ = None # Initialize as None
# <===================================================== END ==================================================>

# Async initialization function
async def aiohttp_session_init():
    global session, state, arq
    if session is None:
        session = ClientSession()
    if state is None:
        state = AsyncClient(
            http2=True,
            verify=False,
            headers={
                "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
            },
            timeout=Timeout(20),
        )
    if arq is None:
        arq = ARQ(ARQ_API_URL, ARQ_API_KEY, session)
