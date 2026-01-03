import argparse
import sys
from ..core import get_system_info


def main():
    """
    Main entry point for the CLI application.
    """
    parser = argparse.ArgumentParser(
        description="Script Info - Collect system information and metadata",
        add_help=False  # Disable default help to implement custom -help
    )

    # Add arguments
    parser.add_argument(
        '-all',
        action='store_true',
        help='Collect and display all system information'
    )

    parser.add_argument(
        '-help',
        action='store_true',
        help='Show help message'
    )

    # Parse arguments
    args = parser.parse_args()

    # Handle -help flag
    if args.help:
        print("Script Info CLI Help:")
        print("  -all    : Collect and display all system information")
        print("  -help   : Show this help message")
        print("\nUsage: script-info-cli -all")
        return

    # Handle -all flag
    if args.all:
        try:
            print("Collecting system information...\n")
            info = get_system_info()

            print("System Information:")
            print("=" * 50)

            for key, value in info.items():
                print(f"{key}: {value}")

            print("\nCollection complete.")

        except Exception as e:
            print(f"Error collecting system information: {e}")
            sys.exit(1)

    else:
        print("No valid option specified. Use -help for usage information.")
        sys.exit(1)


if __name__ == "__main__":
    main()