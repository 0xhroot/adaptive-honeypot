
import asyncio
from honeypot.services.ssh import SSHHoneypot

asyncio.run(SSHHoneypot().start())
