import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Test bcrypt directly
from passlib.context import CryptContext

try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    print("CryptContext created successfully")

    # Test hashing
    password = "testpass123"
    print(f"Testing with password: {password} (length: {len(password)})")

    hashed = pwd_context.hash(password)
    print(f"Password hashed successfully: {hashed[:20]}...")

    # Test verification
    verified = pwd_context.verify(password, hashed)
    print(f"Password verification: {verified}")

    print("Bcrypt is working correctly!")

except Exception as e:
    print(f"Error with bcrypt: {e}")
    import traceback
    traceback.print_exc()