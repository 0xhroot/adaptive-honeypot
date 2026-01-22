"""
Deception strategies.
"""
import asyncio
import random

async def slow_response():
    await asyncio.sleep(random.uniform(2.0, 5.0))

def fake_errors(command: str) -> str:
    errors = [
        f"{command}: Permission denied",
        f"{command}: Segmentation fault",
        f"{command}: Operation not permitted",
    ]
    return random.choice(errors)

def deep_filesystem(command: str) -> str:
    if command == "ls":
        return "bin  boot  dev  etc  home  lib  opt  root  tmp  var"
    if command.startswith("cd"):
        return ""
    return f"{command}: command not found"

