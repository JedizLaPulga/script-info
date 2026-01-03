import argparse
import sys
from ..core import get_system_info


def generate_pdf_report(info, filename):
    """Generate PDF report from system information."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.colors import blue, black, green
        import datetime

        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center
            textColor=blue
        )

        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=blue
        )

        key_style = ParagraphStyle(
            'KeyStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=green,
            fontName='Helvetica-Bold'
        )

        value_style = ParagraphStyle(
            'ValueStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=black
        )

        # Build PDF content
        content = []

        # Title
        content.append(Paragraph("System Information Report", title_style))
        content.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        content.append(Spacer(1, 20))

        # Group information by categories
        categories = {
            'System': ['OS', 'Hostname', 'Current User', 'Uptime', 'System Age', 'System Status', 'Is Virtual Machine'],
            'Hardware': ['CPU', 'Memory', 'GPU', 'Battery', 'BIOS'],
            'Storage': ['Disk', 'Partition'],
            'Network': ['IP Address', 'Network', 'WiFi', 'DNS', 'Open Ports'],
            'Security': ['Windows Defender', 'Firewall', 'UAC', 'Windows Updates'],
            'Software': ['Python', 'Development Tools', 'Installed Programs', 'Browser History'],
            'Environment': ['Environment Variables', 'Locale', 'Timezone']
        }

        for category_name, keywords in categories.items():
            category_content = []
            for key, value in info.items():
                if any(keyword.lower() in key.lower() for keyword in keywords):
                    category_content.append((key, value))

            if category_content:
                content.append(Paragraph(category_name, header_style))
                for key, value in category_content:
                    content.append(Paragraph(f"{key}:", key_style))
                    content.append(Paragraph(str(value), value_style))
                    content.append(Spacer(1, 5))
                content.append(Spacer(1, 15))

        # Generate PDF
        doc.build(content)
        return True

    except ImportError:
        print("Error: PDF generation requires 'reportlab' library.")
        print("Install it with: pip install reportlab")
        return False
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False


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
        '--help',
        action='store_true',
        help='Show help message'
    )

    parser.add_argument(
        '--pdf',
        type=str,
        metavar='FILENAME',
        help='Export system information to PDF file'
    )

    # Parse arguments
    args = parser.parse_args()

    # Handle --help flag
    if args.help:
        print("Script Info CLI Help:")
        print("  -all           : Collect and display all system information")
        print("  --pdf FILENAME : Export system information to PDF file (use with -all)")
        print("  --help         : Show this help message")
        print("\nUsage examples:")
        print("  script-info-cli -all")
        print("  script-info-cli -all --pdf report.pdf")
        print("  script-info-cli --help")
        return

    # Handle -all flag
    if args.all:
        try:
            print("Collecting system information...\n")
            info = get_system_info()
            print(f"Collected {len(info)} items")

            print("System Information Summary:")
            print("=" * 50)

            # Print first 10 items as summary
            for i, (key, value) in enumerate(info.items()):
                if i < 10:
                    print(f"{key}: {value}")
                else:
                    break

            print(f"\n... and {len(info) - 10} more items")

            print("\nCollection complete.")

            # If PDF export requested
            if args.pdf:
                print(f"\nGenerating PDF report: {args.pdf}")
                if generate_pdf_report(info, args.pdf):
                    print(f"PDF report saved successfully: {args.pdf}")
                else:
                    print("Failed to generate PDF report.")
                    sys.exit(1)

        except Exception as e:
            print(f"Error collecting system information: {e}")
            sys.exit(1)

    else:
        print("No valid option specified. Use -help for usage information.")
        sys.exit(1)


if __name__ == "__main__":
    main()