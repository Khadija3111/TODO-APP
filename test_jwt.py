import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Test JWT import
try:
    import jwt
    print("JWT import successful")

    # Test encoding/decoding
    token = jwt.encode({"sub": "test"}, "secret", algorithm="HS256")
    print(f"Token created: {token}")

    decoded = jwt.decode(token, "secret", algorithms=["HS256"])
    print(f"Token decoded: {decoded}")

except ImportError as e:
    print(f"JWT import error: {e}")
except Exception as e:
    print(f"JWT error: {e}")