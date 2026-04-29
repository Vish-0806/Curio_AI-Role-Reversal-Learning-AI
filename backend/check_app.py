import sys
import traceback
import os

try:
    sys.path.insert(0, os.path.abspath("."))
    from app.main import app
    print("Successfully imported app")
except Exception as e:
    print("Error importing app:")
    traceback.print_exc()
