"""
Decides how the honeypot adapts responses.
"""
from honeypot.adapt import strategies

class AdaptiveEngine:
    def __init__(self):
        pass

    async def pre_command(self, profile: str):
        """
        Executed BEFORE command handling.
        """
        if profile == "bruteforce_bot":
            await strategies.slow_response()

        if profile == "automated_scanner":
            await strategies.slow_response()

    def post_command(self, profile: str, command: str, default_output: str) -> str:
        """
        Executed AFTER command handling.
        """
        if profile == "automated_scanner":
            return strategies.fake_errors(command)

        if profile == "human_interactive":
            return strategies.deep_filesystem(command)

        return default_output

