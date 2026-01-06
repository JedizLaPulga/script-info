import unittest
import os
import tempfile
from script_info.reporting import PDFReporter

class TestReporting(unittest.TestCase):
    def test_pdf_generation(self):
        # Create a temp file path
        fd, path = tempfile.mkstemp(suffix='.pdf')
        os.close(fd)
        
        try:
            reporter = PDFReporter(path)
            
            # Dummy data
            data = {
                'OS': 'Test OS',
                'CPU': 'Test CPU',
                'Complex': {'A': 1, 'B': 2}
            }
            
            result = reporter.generate(data)
            self.assertTrue(result, "PDF generation should return True on success")
            self.assertTrue(os.path.exists(path), "PDF file should exist")
            self.assertGreater(os.path.getsize(path), 100, "PDF file should not be empty")
            
        finally:
            # Cleanup
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass

if __name__ == '__main__':
    unittest.main()
