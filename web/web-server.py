#!/usr/bin/env python3

import argparse
import http.server
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


MY_RUFF = os.environ.get("MY_RUFF", "ruff")
MAX_FIRMWARE_BYTES = 16 * 1024 * 1024


class Hazard3DoomRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Serve static files and load console firmware through local GDB."""

    firmware_loader = Path()
    repo_root = Path()

    def send_json(self, status: int, response: dict[str, object]) -> None:
        payload = json.dumps(response).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        if self.path == "/api/console-firmware/status":
            self.send_json(
                200,
                {
                    "available": self.firmware_loader.is_file()
                    and os.access(self.firmware_loader, os.X_OK),
                },
            )
            return
        super().do_GET()

    def do_POST(self) -> None:
        if self.path != "/api/console-firmware/load":
            self.send_error(404)
            return
        if self.headers.get("X-Hazard3-Doom-Local") != "1":
            self.send_json(403, {"ok": False, "error": "Missing local request header."})
            return
        if self.headers.get_content_type() != "application/octet-stream":
            self.send_json(415, {"ok": False, "error": "Expected an ELF byte stream."})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"ok": False, "error": "Invalid Content-Length."})
            return

        if content_length < 52 or content_length > MAX_FIRMWARE_BYTES:
            self.send_json(
                400,
                {
                    "ok": False,
                    "error": "Firmware must be a 32-bit RISC-V ELF no larger than 16 MiB.",
                },
            )
            return
        if not self.firmware_loader.is_file() or not os.access(
            self.firmware_loader,
            os.X_OK,
        ):
            self.send_json(
                503,
                {
                    "ok": False,
                    "error": "Firmware loader script was not found or is not executable.",
                },
            )
            return

        firmware = self.rfile.read(content_length)
        if len(firmware) != content_length:
            self.send_json(400, {"ok": False, "error": "Firmware upload ended early."})
            return
        if (
            firmware[:4] != b"\x7fELF"
            or firmware[4] != 1
            or firmware[5] != 1
            or firmware[6] != 1
            or int.from_bytes(firmware[16:18], "little") != 2
            or int.from_bytes(firmware[18:20], "little") != 243
            or int.from_bytes(firmware[20:24], "little") != 1
        ):
            self.send_json(
                400,
                {
                    "ok": False,
                    "error": "Selected file is not a 32-bit little-endian RISC-V ELF.",
                },
            )
            return

        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                prefix="hazard3-console-firmware-",
                suffix=".elf",
                delete=False,
            ) as temporary:
                temporary.write(firmware)
                temporary_path = Path(temporary.name)

            result = subprocess.run(
                [str(self.firmware_loader), str(temporary_path)],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=180,
                check=False,
            )
            output = "".join((result.stdout, result.stderr))
            if result.returncode != 0:
                self.send_json(
                    500,
                    {
                        "ok": False,
                        "error": f"Firmware loader exited with status {result.returncode}.",
                        "output": output,
                    },
                )
                return

            self.send_json(200, {"ok": True, "output": output})
        except subprocess.TimeoutExpired as error:
            stdout = (
                error.stdout.decode(errors="replace")
                if isinstance(error.stdout, bytes)
                else error.stdout
            )
            stderr = (
                error.stderr.decode(errors="replace")
                if isinstance(error.stderr, bytes)
                else error.stderr
            )
            output = "".join((stdout or "", stderr or ""))
            self.send_json(
                504,
                {
                    "ok": False,
                    "error": "Firmware loader timed out after 180 seconds.",
                    "output": output,
                },
            )
        except OSError as error:
            self.send_json(500, {"ok": False, "error": str(error)})
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)


def check_python_script() -> None:
    """Check this script before continuing."""
    script = Path(__file__).resolve()

    subprocess.run(
        [sys.executable, "-m", "py_compile", str(script)],
        check=True,
    )

    # Check if the executable is available in the PATH.
    if shutil.which(MY_RUFF):
        result = subprocess.run(
            [MY_RUFF, "check", str(script)],
            stdout=sys.stderr,
            stderr=sys.stderr,
            check=False,
        )
        if result.returncode != 0:
            raise SystemExit(result.returncode)
    else:
        print(
            f"{MY_RUFF} is not installed. "
            "Please install it if changes to this script have been made.",
            file=sys.stderr,
        )


def main() -> None:
    check_python_script()

    parser = argparse.ArgumentParser(
        description="Serve the Hazard3-Doom web UI.",
    )
    parser.add_argument(
        "port",
        nargs="?",
        type=int,
        default=8000,
        help="HTTP port (default: 8000)",
    )
    parser.add_argument(
        "--firmware-loader",
        type=Path,
        help="firmware loader script (default: ../scripts/load-firmware.sh)",
    )
    args = parser.parse_args()

    web_dir = Path(__file__).resolve().parent
    repo_root = web_dir.parent
    firmware_loader = (
        args.firmware_loader.resolve()
        if args.firmware_loader
        else repo_root / "scripts" / "load-firmware.sh"
    )
    Hazard3DoomRequestHandler.firmware_loader = firmware_loader
    Hazard3DoomRequestHandler.repo_root = repo_root
    os.chdir(web_dir)

    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", args.port),
        Hazard3DoomRequestHandler,
    )

    print("Serving Hazard3-Doom web UI from:")
    print(f"  {web_dir}")
    print()
    print("Open:")
    print(f"  http://127.0.0.1:{args.port}/")
    print()
    print("Console firmware loader:")
    print(f"  {firmware_loader}")
    print()
    print("Press Ctrl-C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Server stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
