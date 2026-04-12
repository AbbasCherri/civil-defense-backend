#!/usr/bin/env python
"""
Initialize the database by creating all tables and enum types.
This script must be run before the application can work.
"""
import asyncio
import os
from pathlib import Path

# Add the project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from app.core.database import engine
from app.models.models import Base


async def create_enum_types(connection):
    """Create PostgreSQL enum types."""
    print("[*] Creating enum types...")
    
    # These enum values must match the Python models in app/models/models.py
    enum_types = {
        'userrole': ['Citizen', 'Dispatcher', 'Responder', 'Admin', 'External'],
        'incidentstatus': ['Waiting', 'Active', 'Closed'],
        'incidentcategory': ['Fire', 'Medical', 'Traffic', 'Accident', 'Flood', 'Other'],
        'incidentpriority': ['Low', 'Medium', 'High', 'Critical'],
        'mediatype': ['image', 'video', 'voice', 'document'],
        'resourcetype': ['Vehicle', 'Equipment'],
        'resourcestatus': ['Available', 'Unavailable', 'Maintenance'],
        'teamstatus': ['Available', 'Deployed']
    }
    
    for enum_name, values in enum_types.items():
        try:
            # Drop existing enum type if it exists
            await connection.execute(text(f"DROP TYPE IF EXISTS {enum_name} CASCADE"))
            print(f"  ✓ Dropped existing {enum_name}")
            
            # Create enum type with quoted values
            values_str = ", ".join(f"'{v}'" for v in values)
            create_sql = f"CREATE TYPE {enum_name} AS ENUM ({values_str})"
            await connection.execute(text(create_sql))
            print(f"  ✓ Created {enum_name} with values: {', '.join(values)}")
        except Exception as e:
            print(f"  ✗ Error creating {enum_name}: {e}")
            raise


async def create_tables(connection):
    """Create all tables using SQLAlchemy models."""
    print("\n[*] Creating tables from SQLAlchemy models...")
    
    # Drop all existing tables first
    await connection.run_sync(Base.metadata.drop_all)
    print("  ✓ Dropped existing tables")
    
    # Create all tables from models
    await connection.run_sync(Base.metadata.create_all)
    
    print("  ✓ All tables created successfully")


async def main():
    """Main initialization function."""
    print("=" * 60)
    print("DATABASE INITIALIZATION")
    print("=" * 60)
    
    try:
        async with engine.begin() as connection:
            await create_enum_types(connection)
            await create_tables(connection)
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Database initialized successfully!")
        print("=" * 60)
        print("\nYou can now start the server with: .\\run.bat")
        
    except Exception as e:
        print(f"\n[ERROR] Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
