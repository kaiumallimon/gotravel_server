"""
LangChain Tools for Travel Assistant
Defines all tools that the AI agent can use to fetch data and perform actions
"""
from typing import Optional, List, Dict, Any
from langchain.tools import tool
from src.services.database import supabase_client
from src.config import settings
import httpx
import json
import logging

logger = logging.getLogger(__name__)


# ==================== HOTEL TOOLS ====================

@tool
def search_hotels(
    city: Optional[str] = None,
    country: Optional[str] = None
) -> str:
    """
    Search for hotels based on location criteria.
    
    Use this tool when users ask about:
    - Hotels in a specific city or country
    - Accommodations
    - Places to stay
    
    Args:
        city: City name to search hotels in (e.g., "Dhaka", "Cox's Bazar")
        country: Country name to search hotels in (e.g., "Bangladesh")
    
    Returns:
        JSON string with list of hotels including name, location, rating, price, and amenities
    """
    try:
        hotels = supabase_client.search_hotels(
            city=city,
            country=country,
            limit=10
        )
        
        if not hotels:
            return json.dumps({
                "success": False,
                "message": f"No hotels found matching the criteria: city={city}, country={country}",
                "data": []
            })
        
        # Format hotel data for better readability
        formatted_hotels = []
        for hotel in hotels:
            formatted_hotels.append({
                "id": hotel.get("id"),
                "name": hotel.get("name"),
                "city": hotel.get("city"),
                "country": hotel.get("country"),
                "address": hotel.get("address"),
                "rating": hotel.get("rating"),
                "reviews_count": hotel.get("reviews_count"),
                "phone": hotel.get("phone"),
                "email": hotel.get("contact_email"),
                "description": hotel.get("description", "")[:200] + "..." if hotel.get("description") else ""
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_hotels),
            "data": formatted_hotels
        }, indent=2)
    except Exception as e:
        logger.error(f"Error in search_hotels tool: {e}")
        return json.dumps({"success": False, "error": str(e)})


@tool
def get_hotel_rooms(hotel_id: str) -> str:
    """
    Get available rooms for a specific hotel.
    
    Use this tool when users ask about:
    - Room types and prices in a hotel
    - Available rooms
    - Room amenities and capacity
    
    Args:
        hotel_id: The unique ID of the hotel
    
    Returns:
        JSON string with list of available rooms with type, price, capacity, and amenities
    """
    try:
        rooms = supabase_client.get_hotel_rooms(hotel_id)
        
        if not rooms:
            return json.dumps({
                "success": False,
                "message": f"No available rooms found for hotel ID: {hotel_id}",
                "data": []
            })
        
        formatted_rooms = []
        for room in rooms:
            formatted_rooms.append({
                "id": room.get("id"),
                "room_type": room.get("room_type"),
                "price_per_night": room.get("price_per_night"),
                "currency": room.get("currency"),
                "capacity": room.get("capacity"),
                "bed_type": room.get("bed_type"),
                "amenities": room.get("amenities", []),
                "available_count": room.get("available_count")
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_rooms),
            "data": formatted_rooms
        }, indent=2)
    except Exception as e:
        logger.error(f"Error in get_hotel_rooms tool: {e}")
        return json.dumps({"success": False, "error": str(e)})


# ==================== PACKAGE TOOLS ====================

@tool
def search_packages(
    destination: Optional[str] = None,
    country: Optional[str] = None,
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    duration_days: Optional[int] = None
) -> str:
    """
    Search for travel packages based on various criteria.
    
    Use this tool when users ask about:
    - Travel packages to specific destinations
    - Tours with specific duration or price range
    - Package categories (adventure, luxury, beach, cultural, etc.)
    
    Args:
        destination: Destination name (e.g., "Sylhet", "Sundarbans")
        country: Country name (e.g., "Bangladesh")
        category: Package category (e.g., "adventure", "luxury", "beach", "cultural")
        max_price: Maximum price filter
        duration_days: Package duration in days
    
    Returns:
        JSON string with list of packages including name, destination, price, duration, and details
    """
    try:
        packages = supabase_client.search_packages(
            destination=destination,
            country=country,
            category=category,
            max_price=max_price,
            duration_days=duration_days,
            limit=10
        )
        
        if not packages:
            return json.dumps({
                "success": False,
                "message": f"No packages found matching the criteria",
                "data": []
            })
        
        formatted_packages = []
        for pkg in packages:
            formatted_packages.append({
                "id": pkg.get("id"),
                "name": pkg.get("name"),
                "destination": pkg.get("destination"),
                "country": pkg.get("country"),
                "category": pkg.get("category"),
                "duration_days": pkg.get("duration_days"),
                "price": pkg.get("price"),
                "currency": pkg.get("currency"),
                "max_participants": pkg.get("max_participants"),
                "available_slots": pkg.get("available_slots"),
                "rating": pkg.get("rating"),
                "reviews_count": pkg.get("reviews_count"),
                "included_services": pkg.get("included_services", []),
                "description": pkg.get("description", "")[:200] + "..." if pkg.get("description") else ""
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_packages),
            "data": formatted_packages
        }, indent=2)
    except Exception as e:
        logger.error(f"Error in search_packages tool: {e}")
        return json.dumps({"success": False, "error": str(e)})


@tool
def get_cheapest_packages() -> str:
    """
    Get the cheapest available travel packages.
    
    Use this tool when users ask about:
    - Budget packages
    - Cheapest travel options
    - Affordable tours
    
    Returns:
        JSON string with list of cheapest packages
    """
    try:
        packages = supabase_client.get_cheapest_packages(limit=5)
        
        if not packages:
            return json.dumps({
                "success": False,
                "message": "No packages available",
                "data": []
            })
        
        formatted_packages = []
        for pkg in packages:
            formatted_packages.append({
                "id": pkg.get("id"),
                "name": pkg.get("name"),
                "destination": pkg.get("destination"),
                "duration_days": pkg.get("duration_days"),
                "price": pkg.get("price"),
                "currency": pkg.get("currency"),
                "category": pkg.get("category"),
                "available_slots": pkg.get("available_slots"),
                "description": pkg.get("description", "")[:150] + "..."
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_packages),
            "data": formatted_packages
        }, indent=2)
    except Exception as e:
        logger.error(f"Error in get_cheapest_packages tool: {e}")
        return json.dumps({"success": False, "error": str(e)})


@tool
def get_packages_by_price(sort_order: str = "low_to_high") -> str:
    """
    Get travel packages sorted by price.
    
    Use this tool when users ask about:
    - Packages sorted by price
    - Cheapest to most expensive packages
    - Most expensive to cheapest packages
    - Budget-friendly to luxury packages
    
    Args:
        sort_order: Sort order - "low_to_high" for cheapest first, "high_to_low" for most expensive first
    
    Returns:
        JSON string with list of packages sorted by price
    """
    try:
        ascending = sort_order.lower() == "low_to_high"
        packages = supabase_client.get_packages_sorted_by_price(ascending=ascending, limit=10)
        
        if not packages:
            return json.dumps({
                "success": False,
                "message": "No packages available",
                "data": []
            })
        
        formatted_packages = []
        for pkg in packages:
            formatted_packages.append({
                "id": pkg.get("id"),
                "name": pkg.get("name"),
                "destination": pkg.get("destination"),
                "duration_days": pkg.get("duration_days"),
                "price": pkg.get("price"),
                "currency": pkg.get("currency"),
                "category": pkg.get("category"),
                "available_slots": pkg.get("available_slots"),
                "rating": pkg.get("rating"),
                "reviews_count": pkg.get("reviews_count"),
                "description": pkg.get("description", "")[:150] + "..."
            })
        
        return json.dumps({
            "success": True,
            "sort_order": sort_order,
            "count": len(formatted_packages),
            "data": formatted_packages
        }, indent=2)
    except Exception as e:
        logger.error(f"Error in get_packages_by_price tool: {e}")
        return json.dumps({"success": False, "error": str(e)})


# ==================== PLACE TOOLS ====================

@tool
def search_places(
    country: Optional[str] = None,
    city: Optional[str] = None,
    category: Optional[str] = None,
    near_city: Optional[str] = None
) -> str:
    """
    Search for tourist places and destinations.
    
    Use this tool when users ask about:
    - Tourist places in a location
    - Places to visit near a city
    - Specific types of places (beaches, mountains, historical sites, etc.)
    
    Args:
        country: Country name (e.g., "Bangladesh")
        city: City name (e.g., "Dhaka")
        category: Place category (e.g., "beach", "mountain", "historical", "cultural")
        near_city: Find places near this city
    
    Returns:
        JSON string with list of places including name, location, category, and activities
    """
    try:
        places = supabase_client.search_places(
            country=country,
            city=city,
            category=category,
            near_city=near_city,
            limit=10
        )
        
        if not places:
            return json.dumps({
                "success": False,
                "message": f"No places found matching the criteria",
                "data": []
            })
        
        formatted_places = []
        for place in places:
            formatted_places.append({
                "id": place.get("id"),
                "name": place.get("name"),
                "city": place.get("city"),
                "country": place.get("country"),
                "category": place.get("category"),
                "rating": place.get("rating"),
                "famous_for": place.get("famous_for", []),
                "activities": place.get("activities", []),
                "best_time_to_visit": place.get("best_time_to_visit"),
                "description": place.get("description", "")[:200] + "..." if place.get("description") else ""
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_places),
            "data": formatted_places
        }, indent=2)
    except Exception as e:
        logger.error(f"Error in search_places tool: {e}")
        return json.dumps({"success": False, "error": str(e)})


@tool
def get_popular_places() -> str:
    """
    Get the most popular tourist places.
    
    Use this tool when users ask about:
    - Popular destinations
    - Top tourist attractions
    - Most visited places
    
    Returns:
        JSON string with list of popular places
    """
    try:
        places = supabase_client.get_popular_places(limit=10)
        
        if not places:
            return json.dumps({
                "success": False,
                "message": "No popular places found",
                "data": []
            })
        
        formatted_places = []
        for place in places:
            formatted_places.append({
                "id": place.get("id"),
                "name": place.get("name"),
                "city": place.get("city"),
                "country": place.get("country"),
                "category": place.get("category"),
                "rating": place.get("rating"),
                "popular_ranking": place.get("popular_ranking"),
                "famous_for": place.get("famous_for", []),
                "description": place.get("description", "")[:150] + "..."
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_places),
            "data": formatted_places
        }, indent=2)
    except Exception as e:
        logger.error(f"Error in get_popular_places tool: {e}")
        return json.dumps({"success": False, "error": str(e)})


# ==================== HOTEL PRICE SORTING ====================

@tool
def get_hotels_by_price(
    city: Optional[str] = None,
    country: Optional[str] = None,
    sort_order: str = "low_to_high"
) -> str:
    """
    Get hotels sorted by price.
    
    Use this tool when users ask about:
    - Hotels sorted by price
    - Cheapest to most expensive hotels
    - Budget hotels to luxury hotels
    - Hotel price comparison
    
    Args:
        city: City name to filter hotels (e.g., "Dhaka")
        country: Country name to filter hotels (e.g., "Bangladesh")
        sort_order: Sort order - "low_to_high" for cheapest first, "high_to_low" for most expensive first
    
    Returns:
        JSON string with list of hotels sorted by price
    """
    try:
        ascending = sort_order.lower() == "low_to_high"
        hotels = supabase_client.get_hotels_sorted_by_price(
            city=city,
            country=country,
            ascending=ascending,
            limit=10
        )
        
        if not hotels:
            return json.dumps({
                "success": False,
                "message": f"No hotels found",
                "data": []
            })
        
        formatted_hotels = []
        for hotel in hotels:
            formatted_hotels.append({
                "id": hotel.get("id"),
                "name": hotel.get("name"),
                "city": hotel.get("city"),
                "country": hotel.get("country"),
                "address": hotel.get("address"),
                "rating": hotel.get("rating"),
                "reviews_count": hotel.get("reviews_count"),
                "phone": hotel.get("phone"),
                "email": hotel.get("contact_email"),
                "description": hotel.get("description", "")[:200] + "..." if hotel.get("description") else ""
            })
        
        return json.dumps({
            "success": True,
            "sort_order": sort_order,
            "count": len(formatted_hotels),
            "data": formatted_hotels
        }, indent=2)
    except Exception as e:
        logger.error(f"Error in get_hotels_by_price tool: {e}")
        return json.dumps({"success": False, "error": str(e)})


# ==================== USER FAVORITES ====================

@tool
def get_user_favorites(user_id: str, item_type: Optional[str] = None) -> str:
    """
    Get user's favorite items (hotels, packages, or places).
    
    Use this tool when users ask about:
    - Their favorites
    - Saved items
    - Bookmarked hotels/packages/places
    - "What are my favorites?"
    - "Show my saved packages"
    
    Args:
        user_id: The user's ID
        item_type: Optional filter - "hotel", "package", or "place"
    
    Returns:
        JSON string with list of user's favorite items
    """
    try:
        favorites = supabase_client.get_user_favorites(
            user_id=user_id,
            item_type=item_type,
            limit=20
        )
        
        if not favorites:
            return json.dumps({
                "success": False,
                "message": "No favorites found",
                "data": []
            })
        
        formatted_favorites = []
        for fav in favorites:
            formatted_favorites.append({
                "id": fav.get("id"),
                "item_type": fav.get("item_type"),
                "item_id": fav.get("item_id"),
                "created_at": fav.get("created_at")
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_favorites),
            "data": formatted_favorites,
            "message": f"Found {len(formatted_favorites)} favorite items"
        }, indent=2)
    except Exception as e:
        logger.error(f"Error in get_user_favorites tool: {e}")
        return json.dumps({"success": False, "error": str(e)})


# ==================== WEATHER TOOL ====================

@tool
def get_weather(city: str) -> str:
    """
    Get current weather information for a city using OpenWeatherMap API.
    
    Use this tool when users ask about:
    - Current weather in a location
    - Temperature, humidity, conditions
    - Weather forecasts
    
    Args:
        city: City name to get weather for (e.g., "Dhaka", "Cox's Bazar")
    
    Returns:
        JSON string with current weather information
    """
    try:
        if not settings.openweather_api_key:
            return json.dumps({
                "success": False,
                "message": "Weather API key not configured"
            })
        
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": settings.openweather_api_key,
            "units": "metric"
        }
        
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        
        weather_info = {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "description": data.get("weather", [{}])[0].get("description"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "pressure": data.get("main", {}).get("pressure")
        }
        
        return json.dumps({
            "success": True,
            "data": weather_info
        }, indent=2)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return json.dumps({
                "success": False,
                "message": f"City '{city}' not found"
            })
        return json.dumps({
            "success": False,
            "message": f"Weather API error: {e}"
        })
    except Exception as e:
        logger.error(f"Error in get_weather tool: {e}")
        return json.dumps({"success": False, "error": str(e)})


# ==================== BOOKING TOOL ====================

@tool
def create_booking(
    booking_type: str,
    item_id: str,
    guest_name: str,
    guest_email: str,
    guest_phone: str,
    total_participants: int = 1,
    user_id: Optional[str] = None
) -> str:
    """
    Create a booking for a package or hotel.
    
    Use this tool when users want to:
    - Book a travel package
    - Reserve a hotel room
    - Make a reservation
    
    Args:
        booking_type: Type of booking - either "package" or "hotel"
        item_id: ID of the package or hotel to book
        guest_name: Full name of the primary guest
        guest_email: Email address of the primary guest
        guest_phone: Phone number of the primary guest
        total_participants: Number of people in the booking (default: 1)
        user_id: Optional user ID (use temporary ID if not authenticated)
    
    Returns:
        JSON string with booking confirmation details including booking reference
    """
    try:
        # Validate booking type
        if booking_type not in ["package", "hotel"]:
            return json.dumps({
                "success": False,
                "message": "Invalid booking type. Must be 'package' or 'hotel'"
            })
        
        # Get item details to calculate price
        if booking_type == "package":
            item = supabase_client.get_package_by_id(item_id)
            if not item:
                return json.dumps({
                    "success": False,
                    "message": f"Package with ID {item_id} not found"
                })
            total_amount = float(item.get("price", 0)) * total_participants
        else:  # hotel
            item = supabase_client.get_hotel_by_id(item_id)
            if not item:
                return json.dumps({
                    "success": False,
                    "message": f"Hotel with ID {item_id} not found"
                })
            # For hotels, we'd need room selection, but for demo purposes:
            total_amount = 5000.0  # Default amount, should be calculated from room prices
        
        # Use a temporary user ID if not provided
        if not user_id:
            import uuid
            user_id = str(uuid.uuid4())
        
        # Create the booking
        booking = supabase_client.create_booking(
            user_id=user_id,
            booking_type=booking_type,
            item_id=item_id,
            primary_guest_name=guest_name,
            primary_guest_email=guest_email,
            primary_guest_phone=guest_phone,
            total_amount=total_amount,
            total_participants=total_participants,
            base_price=total_amount
        )
        
        if not booking:
            return json.dumps({
                "success": False,
                "message": "Failed to create booking"
            })
        
        return json.dumps({
            "success": True,
            "message": "Booking created successfully",
            "data": {
                "booking_reference": booking.get("booking_reference"),
                "booking_type": booking.get("booking_type"),
                "guest_name": booking.get("primary_guest_name"),
                "total_amount": booking.get("total_amount"),
                "currency": booking.get("currency"),
                "status": booking.get("booking_status"),
                "payment_status": booking.get("payment_status")
            }
        }, indent=2)
    except Exception as e:
        logger.error(f"Error in create_booking tool: {e}")
        return json.dumps({"success": False, "error": str(e)})


# Export all tools as a list
tools = [
    search_hotels,
    get_hotel_rooms,
    get_hotels_by_price,
    search_packages,
    get_cheapest_packages,
    get_packages_by_price,
    search_places,
    get_popular_places,
    get_user_favorites,
    get_weather,
    create_booking
]
