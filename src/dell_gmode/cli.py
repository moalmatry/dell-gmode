"""Dell G15 G-Mode Command-Line Interface."""
import argparse
import sys
from .controller import GModeController
from .daemon import GModeDaemon


def main():
    parser = argparse.ArgumentParser(
        prog="dell-gmode",
        description="Dell G15 Fn+F9 G-Mode (Game Shift) hardware performance controller",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # toggle
    subparsers.add_parser("toggle", help="Toggle between Balanced and Performance (G-Mode)")

    # performance
    subparsers.add_parser("performance", help="Engage High Performance G-Mode (Fans 100%)")

    # balanced
    subparsers.add_parser("balanced", help="Restore normal Balanced Mode (Quiet Fans)")

    # status
    subparsers.add_parser("status", help="Show current performance mode and status")

    # daemon
    subparsers.add_parser("daemon", help="Run the background Fn+F9 hardware key listener")

    args = parser.parse_args()

    if not args.command:
        # If invoked without arguments, default to toggle or print help
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(0)
        args.command = "toggle"

    if args.command == "toggle":
        mode = GModeController.toggle(notify=True)
        print(f"[✓] Switched to {mode.upper()} mode.")
    elif args.command == "performance":
        GModeController.set_mode("performance", notify=True)
        print("[⚡] High Performance G-Mode engaged (Fans Maximum).")
    elif args.command == "balanced":
        GModeController.set_mode("balanced", notify=True)
        print("[🍃] Balanced Mode engaged.")
    elif args.command == "status":
        mode = GModeController.get_mode()
        print(f"Current mode: {mode.upper()}")
    elif args.command == "daemon":
        daemon = GModeDaemon()
        daemon.run()


if __name__ == "__main__":
    main()
