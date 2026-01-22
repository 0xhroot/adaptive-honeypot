import asyncio
import uuid
from datetime import datetime

from honeypot.services.base import BaseService
from honeypot.core.session import Session
from honeypot.core.events import (
    EVENT_CONNECTION,
    EVENT_AUTH_ATTEMPT,
    EVENT_COMMAND,
    EVENT_DISCONNECT,
)
from honeypot.logging.logger import log_event
from honeypot.logging.formatter import format_event

from honeypot.adapt.engine import AdaptiveEngine
from honeypot.ml.features import extract_features_for_session, persist_features
from honeypot.ml.profiles import classify_profile, save_profile, load_profile


class SSHHoneypot(BaseService):
    """
    Async fake SSH honeypot with adaptive behavior.
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.port = config["services"]["ssh"]["port"]
        self.banner = config["services"]["ssh"]["banner"]

    async def start(self):
        server = await asyncio.start_server(
            self.handle_client,
            host="0.0.0.0",
            port=self.port
        )

        print(f"[+] SSH Honeypot listening on port {self.port}")

        async with server:
            await server.serve_forever()

    async def handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ):
        peer = writer.get_extra_info("peername")
        ip, port = peer[0], peer[1]

        session = Session(
            session_id=str(uuid.uuid4()),
            ip=ip,
            port=port,
            start_time=datetime.utcnow(),
        )

        # Persist session
        session.save()

        # Log connection
        log_event(format_event(EVENT_CONNECTION, session.__dict__))

        adaptive = AdaptiveEngine()

        try:
            # SSH banner
            writer.write(f"SSH-2.0-{self.banner}\r\n".encode())
            await writer.drain()

            username = await self._prompt(reader, writer, "login as: ")
            password = await self._prompt(
                reader,
                writer,
                f"{username}@password: ",
            )

            log_event(format_event(EVENT_AUTH_ATTEMPT, {
                "session_id": session.session_id,
                "username": username,
                "password": password,
            }))

            # Fake auth result
            writer.write(b"Permission denied, please try again.\n")
            writer.write(b"Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0)\n\n")
            await writer.drain()

            # Load profile if exists (else unknown)
            profile = load_profile(session.session_id)

            await self.fake_shell(
                reader=reader,
                writer=writer,
                session=session,
                adaptive=adaptive,
                profile=profile
            )

        except Exception as e:
            print(f"[!] SSH error: {e}")

        finally:
            # ML feature extraction on disconnect
            features = extract_features_for_session(session.session_id)
            persist_features(session.session_id, features)

            profile = classify_profile(features)
            save_profile(session.session_id, profile)

            log_event(format_event(EVENT_DISCONNECT, {
                "session_id": session.session_id,
                "profile": profile,
            }))

            writer.close()
            await writer.wait_closed()

    async def _prompt(self, reader, writer, prompt: str) -> str:
        writer.write(prompt.encode())
        await writer.drain()

        data = await reader.readline()
        return data.decode(errors="ignore").strip()

    async def fake_shell(
        self,
        reader,
        writer,
        session: Session,
        adaptive: AdaptiveEngine,
        profile: str
    ):
        """
        Fake interactive shell with adaptive behavior.
        """
        cwd = "/home/admin"

        while True:
            writer.write(f"admin@honeypot:{cwd}$ ".encode())
            await writer.drain()

            data = await reader.readline()
            if not data:
                break

            command = data.decode(errors="ignore").strip()

            log_event(format_event(EVENT_COMMAND, {
                "session_id": session.session_id,
                "command": command,
            }))

            if command in ("exit", "logout"):
                writer.write(b"logout\n")
                await writer.drain()
                break

            # Adaptive pre-command behavior
            await adaptive.pre_command(profile)

            output = self.handle_command(command, cwd)

            # Adaptive post-command mutation
            output = adaptive.post_command(profile, command, output)

            writer.write(output.encode() + b"\n")
            await writer.drain()

    def handle_command(self, command: str, cwd: str) -> str:
        """
        Safe fake command handler.
        """

        if command == "":
            return ""

        if command == "ls":
            return "Desktop  Documents  Downloads  secrets.txt"

        if command == "pwd":
            return cwd

        if command == "whoami":
            return "admin"

        if command.startswith("cat"):
            if "secrets.txt" in command:
                return "root:toor\nadmin:admin123\n"
            return "cat: No such file or directory"

        if command == "uname -a":
            return "Linux honeypot 5.15.0 #1 SMP Ubuntu"

        return f"{command}: command not found"

