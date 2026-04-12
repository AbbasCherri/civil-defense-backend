#!/usr/bin/env python
"""Debug script to test user registration."""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.core.security import get_password_hash, verify_password
from app.services.user_service import UserService
from app.core.database import async_session_maker, engine


async def test_password_hashing():
    """Test password hashing."""
    print("[*] Testing password hashing...")
    try:
        password = "TestPassword123"
        hashed = get_password_hash(password)
        print(f"  ✓ Password hashed: {hashed[:20]}... (length: {len(hashed)})")
        
        verified = verify_password(password, hashed)
        print(f"  ✓ Password verified: {verified}")
        
        wrong_verified = verify_password("WrongPassword", hashed)
        print(f"  ✓ Wrong password verification: {wrong_verified} (should be False)")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def test_user_registration():
    """Test user registration."""
    print("\n[*] Testing user registration...")
    try:
        async with async_session_maker() as session:
            service = UserService(session)
            
            result = await service.register_user(
                name="Test User",
                email="test@example.com",
                password="TestPassword123",
                role="Dispatcher"
            )
            
            print(f"  ✓ User created: {result}")
            if isinstance(result, dict) and "id" in result:
                print(f"    - ID: {result.get('id')}")
                print(f"    - Name: {result.get('name')}")
                print(f"    - Email: {result.get('email')}")
                print(f"    - Role: {result.get('role')}")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def main():
    """Main test function."""
    print("=" * 60)
    print("REGISTRATION TEST")
    print("=" * 60)
    
    hash_ok = await test_password_hashing()
    
    if hash_ok:
        register_ok = await test_user_registration()
        
        if register_ok:
            print("\n" + "=" * 60)
            print("[SUCCESS] All tests passed!")
            print("=" * 60)
        else:
            print("\n[FAILURE] Registration test failed")
    else:
        print("\n[FAILURE] Password hashing test failed")


if __name__ == "__main__":
    asyncio.run(main())
