import asyncio
import traceback

from honeypot.core.config import load_config
from honeypot.services.ssh import SSHHoneypot


async def start():
    """
    Main honeypot bootstrap.
    Fail-safe by design: never crashes silently.
    """
    try:
        # Load configs
        services_config = load_config("config/services.yaml")

        # Start SSH honeypot only if enabled
        if services_config.get("services", {}).get("ssh", {}).get("enabled", False):
            ssh_service = SSHHoneypot(services_config)
            await ssh_service.start()
        else:
            print("[!] SSH service disabled in config")

    except KeyboardInterrupt:
        print("\n[!] Honeypot stopped by user (CTRL+C)")

    except Exception as e:
        print("[FATAL] Honeypot crashed safely!")
        print("Reason:", e)
        print("Traceback:")
        traceback.print_exc()

    finally:
        print("[+] Honeypot shutdown complete")


if __name__ == "__main__":
    asyncio.run(start())
