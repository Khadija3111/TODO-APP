import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import the app to test for import errors
try:
    from backend.main import app
    print("App imported successfully")
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()

# Test the auth endpoint directly
try:
    from backend.api.auth import register
    print("Auth module imported successfully")
except Exception as e:
    print(f"Auth import error: {e}")
    import traceback
    traceback.print_exc()