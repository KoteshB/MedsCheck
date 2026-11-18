"""Call the local Claude Code CLI (`claude -p`) and return the result.

Uses your Claude subscription login instead of an Anthropic API key.
For personal use only. Do not put this behind a service other people use.

Requirements:
- `claude` is on PATH and you are logged in (`claude`, then `/login`).
- ANTHROPIC_API_KEY is NOT set. If it is, the CLI bills the API instead.
"""

import json
import os
import subprocess
import tempfile
from typing import Optional


class ClaudeCLIError(RuntimeError):
    pass


def ask_claude(
    prompt: str,
    system: Optional[str] = None,
    schema: Optional[dict] = None,
    model: Optional[str] = None,
    timeout: int = 180,
) -> str:
    """Run one prompt through the CLI with no tools and return the text result.

    Runs from an empty temp directory so the repo's CLAUDE.md is not loaded.
    """
    cmd = ["claude", "-p", prompt, "--output-format", "json", "--tools", ""]
    if system:
        cmd += ["--system-prompt", system]
    if schema:
        cmd += ["--json-schema", json.dumps(schema)]
    if model:
        cmd += ["--model", model]

    # Force subscription billing: drop any API key from the child environment.
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}

    with tempfile.TemporaryDirectory() as neutral_cwd:
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=neutral_cwd,
                env=env,
            )
        except FileNotFoundError as e:
            raise ClaudeCLIError("`claude` CLI not found on PATH") from e
        except subprocess.TimeoutExpired as e:
            raise ClaudeCLIError(f"claude CLI timed out after {timeout}s") from e

    if proc.returncode != 0:
        raise ClaudeCLIError(f"claude CLI failed ({proc.returncode}): {proc.stderr.strip()}")

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise ClaudeCLIError(f"Unparseable CLI output: {proc.stdout[:200]!r}") from e

    if data.get("is_error"):
        raise ClaudeCLIError(f"claude CLI returned an error: {data.get('result')}")

    return data["result"]


if __name__ == "__main__":
    print(ask_claude("Reply with the single word: ok"))
