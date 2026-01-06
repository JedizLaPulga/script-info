import argparse
import sys
from ..core import get_system_info
from ..reporting import PDFReporter

def main():
    """
    Main entry point for the CLI application.
    """
    parser = argparse.ArgumentParser(
        description="Script Info - Collect system information and metadata",
        add_help=False
    )

    parser.add_argument('-all', action='store_true', help='Collect and display all system information')
    parser.add_argument('--help', action='store_true', help='Show help message')
    parser.add_argument('--pdf', type=str, metavar='FILENAME', help='Export system information to PDF file')

    args = parser.parse_args()

    if args.help:
        print("Script Info CLI Help:")
        print("  -all           : Collect and display all system information")
        print("  --pdf FILENAME : Export system information to PDF file (use with -all)")
        print("  --help         : Show this help message")
        return

    if args.all:
        try:
            print("Collecting system information... (this may take a moment)")
            info = get_system_info()
            print(f"Collected {len(info)} items")

            print("\nSystem Information Summary:")
            print("=" * 50)

            # Flat print for console
            count = 0
            for key, value in info.items():
                if count < 15: # Show a bit more than 10
                    if isinstance(value, dict):
                         print(f"{key}: [Complex Data]")
                    else:
                         print(f"{key}: {value}")
                    count += 1
                else:
                    break

            print(f"\n... and {len(info) - count} more items")
            print("\nCollection complete.")

            if args.pdf:
                print(f"\nGenerating PDF report: {args.pdf}")
                reporter = PDFReporter(args.pdf)
                if reporter.generate(info):
                    print(f"PDF report saved successfully: {args.pdf}")
                else:
                    print("Failed to generate PDF report.")
                    sys.exit(1)

        except Exception as e:
            print(f"Error collecting system information: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    else:
        print("No valid option specified. Use --help for usage information.")
        sys.exit(1)

if __name__ == "__main__":
    main()