import datetime

class PDFReporter:
    def __init__(self, filename):
        self.filename = filename

    def generate(self, info):
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.colors import blue, black, green
        except ImportError:
            print("ReportLab is not installed.")
            return False

        try:
            doc = SimpleDocTemplate(self.filename, pagesize=letter)
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

            content = []
            content.append(Paragraph("System Information Report", title_style))
            content.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            content.append(Spacer(1, 20))

            # Categorize the flattened info dict for better display
            # This is a heuristic mapping based on keys
            categories = {
                'System': ['OS', 'Hostname', 'User', 'Uptime', 'Boot'],
                'Hardware': ['CPU', 'Memory', 'GPU', 'Battery', 'BIOS'],
                'Storage': ['Disk', 'Partition'],
                'Network': ['IP', 'Interface', 'DNS', 'WiFi', 'Port', 'Network'],
                'Software': ['Python', 'Tool', 'Program', 'Browser'],
                'Security': ['Defender', 'Firewall', 'UAC', 'Update']
            }
            
            # Helper to check if key matches category
            def get_category(key):
                for cat, keywords in categories.items():
                    if any(k.lower() in key.lower() for k in keywords):
                        return cat
                return 'Other'

            # Grouping
            grouped_info = {cat: [] for cat in categories}
            grouped_info['Other'] = []
            
            for k, v in info.items():
                cat = get_category(k)
                grouped_info[cat].append((k, v))

            # Render
            for cat, items in grouped_info.items():
                if items:
                    content.append(Paragraph(cat, header_style))
                    for k, v in items:
                        # Handle nested dicts (like from browser info)
                        if isinstance(v, dict):
                            content.append(Paragraph(f"{k}:", key_style))
                            for sub_k, sub_v in v.items():
                                 content.append(Paragraph(f"&nbsp;&nbsp;{sub_k}: {sub_v}", value_style))
                        else:
                            content.append(Paragraph(f"{k}:", key_style))
                            content.append(Paragraph(str(v), value_style))
                        content.append(Spacer(1, 4))
                    content.append(Spacer(1, 10))

            doc.build(content)
            return True

        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
