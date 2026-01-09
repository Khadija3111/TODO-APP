# Simple test to see if the import works
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test just importing the models
try:
    from backend.models.user import User, UserCreate, UserRead
    print("User models imported successfully")
except Exception as e:
    print(f"Error importing user models: {e}")
    import traceback
    traceback.print_exc()