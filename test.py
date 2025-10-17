"""
Test Script for GoTravel AI Backend
Run this to test the agent functionality
"""
import asyncio
from agent import travel_agent
from database import supabase_client
from config import settings, validate_settings
import json


async def test_agent():
    """Test the AI agent with various queries"""
    
    print("=" * 80)
    print("🤖 GoTravel AI Backend - Test Suite")
    print("=" * 80)
    print()
    
    # Validate configuration
    try:
        validate_settings()
        print("✅ Configuration validated")
        print(f"   Model: {settings.model_name}")
        print(f"   Supabase: {settings.supabase_url[:30]}...")
        print()
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return
    
    # Test queries
    test_cases = [
        {
            "query": "Show me hotels in Dhaka",
            "description": "Hotel Search - Basic"
        },
        {
            "query": "Find luxury hotels in Cox's Bazar with rating above 4",
            "description": "Hotel Search - Advanced"
        },
        {
            "query": "What are the cheapest travel packages?",
            "description": "Package Search - Budget"
        },
        {
            "query": "Show me travel packages to Sylhet for 3 days",
            "description": "Package Search - Specific"
        },
        {
            "query": "What's the weather in Dhaka?",
            "description": "Weather Information"
        },
        {
            "query": "Find popular tourist places in Bangladesh",
            "description": "Place Discovery"
        },
        {
            "query": "Show me places near Dhaka",
            "description": "Place Discovery - Location Based"
        }
    ]
    
    session_id = "test_session"
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"Test {i}/{len(test_cases)}: {test['description']}")
        print(f"{'=' * 80}")
        print(f"\n👤 User: {test['query']}")
        print()
        
        try:
            result = await travel_agent.process_message(
                test['query'],
                session_id=session_id
            )
            
            if result.get("success"):
                print(f"🤖 Assistant:\n{result.get('response')}")
                
                if result.get("tools_used"):
                    print(f"\n🛠️ Tools Used:")
                    for tool in result.get("tools_used", []):
                        print(f"   - {tool['tool']}: {json.dumps(tool['input'])}")
            else:
                print(f"❌ Error: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        print()
        
        # Small delay between requests
        await asyncio.sleep(1)
    
    print("=" * 80)
    print("✅ Test suite completed!")
    print("=" * 80)


async def test_database():
    """Test database connectivity"""
    print("\n🔍 Testing Database Connectivity...")
    print("-" * 80)
    
    tests = [
        ("Hotels", lambda: supabase_client.search_hotels(city="Dhaka", limit=2)),
        ("Packages", lambda: supabase_client.search_packages(country="Bangladesh", limit=2)),
        ("Places", lambda: supabase_client.search_places(country="Bangladesh", limit=2)),
    ]
    
    for name, test_func in tests:
        try:
            result = test_func()
            status = "✅" if result else "⚠️"
            count = len(result) if result else 0
            print(f"{status} {name}: Found {count} records")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
    
    print("-" * 80)


async def test_booking_flow():
    """Test the booking creation flow"""
    print("\n📝 Testing Booking Flow...")
    print("-" * 80)
    
    # This would typically require valid IDs from your database
    print("⚠️ Booking test requires valid package/hotel IDs from your database")
    print("   Skipping automated booking test to avoid test data")
    print("-" * 80)


async def main():
    """Main test runner"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                    GoTravel AI Backend Test Suite                        ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    # Test database
    await test_database()
    
    # Test agent
    await test_agent()
    
    # Test booking
    await test_booking_flow()
    
    print("\n✨ All tests completed!\n")


if __name__ == "__main__":
    asyncio.run(main())
