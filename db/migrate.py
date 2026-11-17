#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path

ALLOWED_COMMANDS = {
    "status",
    "migrate",
    "rollback",
    "new",
    "up",
    "down",
    "wait",
}


def dbmate_local(*args: str) -> None:
    command = [
        "docker",
        "run",
        "--rm",
        "--network",
        "job-market-network",
        "--user",
        f"{os.getuid()}:{os.getgid()}",
        "--env-file",
        "app.env",
        "-v",
        f"{Path.cwd() / 'db'}:/db",
        "ghcr.io/amacneil/dbmate",
        "--no-dump-schema",
        *args,
    ]

    subprocess.run(command, check=True)


def main() -> None:
    Path("db/migrations").mkdir(parents=True, exist_ok=True)

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <command> [arguments...]")
        print(f"Allowed commands: {', '.join(sorted(ALLOWED_COMMANDS))}")
        sys.exit(1)

    dbmate_command = sys.argv[1]

    if dbmate_command not in ALLOWED_COMMANDS:
        print(f"Error: Command '{dbmate_command}' is not allowed in dbmate.")
        sys.exit(1)

    dbmate_local(*sys.argv[1:])


if __name__ == "__main__":
    main()
