"""
Supabase Database Client
Handles all database operations for the GoTravel AI Backend
"""
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
from src.config import settings
import logging

logger = logging.getLogger(__name__)


class SupabaseClient:
    """Client for interacting with Supabase database"""
    
    def __init__(self):
        """Initialize Supabase client"""
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
    
    # ==================== HOTELS ====================
    
    def search_hotels(
        self,
        city: Optional[str] = None,
        country: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for hotels based on various filters
        
        Args:
            city: Filter by city name
            country: Filter by country name
            limit: Maximum number of results
            
        Returns:
            List of hotel records
        """
        try:
            query = self.client.table("hotels").select("*")
            
            if city:
                query = query.ilike("city", f"%{city}%")
            if country:
                query = query.ilike("country", f"%{country}%")
            
            query = query.limit(limit)
            response = query.execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error searching hotels: {e}")
            return []
    
    def get_hotel_by_id(self, hotel_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific hotel by ID"""
        try:
            response = self.client.table("hotels").select("*").eq("id", hotel_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error fetching hotel {hotel_id}: {e}")
            return None
    
    def get_hotel_rooms(self, hotel_id: str) -> List[Dict[str, Any]]:
        """Get available rooms for a hotel"""
        try:
            response = (
                self.client.table("rooms")
                .select("*")
                .eq("hotel_id", hotel_id)
                .gt("available_count", 0)
                .order("price_per_night")
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching rooms for hotel {hotel_id}: {e}")
            return []
    
    # ==================== PACKAGES ====================
    
    def search_packages(
        self,
        destination: Optional[str] = None,
        country: Optional[str] = None,
        category: Optional[str] = None,
        max_price: Optional[float] = None,
        min_price: Optional[float] = None,
        duration_days: Optional[int] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for travel packages based on various filters
        
        Args:
            destination: Destination filter
            country: Country filter
            category: Category filter (e.g., adventure, luxury, beach)
            max_price: Maximum price filter
            min_price: Minimum price filter
            duration_days: Duration in days
            limit: Maximum number of results
            
        Returns:
            List of package records
        """
        try:
            query = (
                self.client.table("packages")
                .select("*")
                .eq("is_active", True)
                .gt("available_slots", 0)
            )
            
            if destination:
                query = query.ilike("destination", f"%{destination}%")
            if country:
                query = query.ilike("country", f"%{country}%")
            if category:
                query = query.ilike("category", f"%{category}%")
            if max_price:
                query = query.lte("price", max_price)
            if min_price:
                query = query.gte("price", min_price)
            if duration_days:
                query = query.eq("duration_days", duration_days)
            
            query = query.limit(limit)
            response = query.execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error searching packages: {e}")
            return []
    
    def get_package_by_id(self, package_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific package by ID"""
        try:
            response = self.client.table("packages").select("*").eq("id", package_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error fetching package {package_id}: {e}")
            return None
    
    def get_cheapest_packages(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the cheapest available packages"""
        try:
            response = (
                self.client.table("packages")
                .select("*")
                .eq("is_active", True)
                .gt("available_slots", 0)
                .order("price")
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching cheapest packages: {e}")
            return []
    
    def get_packages_sorted_by_price(self, ascending: bool = True, limit: int = 10) -> List[Dict[str, Any]]:
        """Get packages sorted by price"""
        try:
            response = (
                self.client.table("packages")
                .select("*")
                .eq("is_active", True)
                .gt("available_slots", 0)
                .order("price", desc=not ascending)
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching packages sorted by price: {e}")
            return []
    
    # ==================== PLACES ====================
    
    def search_places(
        self,
        country: Optional[str] = None,
        city: Optional[str] = None,
        category: Optional[str] = None,
        near_city: Optional[str] = None,
        is_featured: Optional[bool] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for tourist places based on various filters
        
        Args:
            country: Country filter
            city: City filter
            category: Category filter (beach, mountain, historical, etc.)
            near_city: Find places near a specific city
            is_featured: Filter by featured places
            limit: Maximum number of results
            
        Returns:
            List of place records
        """
        try:
            query = (
                self.client.table("places")
                .select("*")
                .eq("is_active", True)
            )
            
            if country:
                query = query.ilike("country", f"%{country}%")
            if city:
                query = query.ilike("city", f"%{city}%")
            if category:
                query = query.ilike("category", f"%{category}%")
            if near_city:
                # Search in city or state_province fields
                query = query.or_(
                    f"city.ilike.%{near_city}%,state_province.ilike.%{near_city}%"
                )
            if is_featured is not None:
                query = query.eq("is_featured", is_featured)
            
            query = query.order("popular_ranking", desc=True).limit(limit)
            response = query.execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error searching places: {e}")
            return []
    
    def get_place_by_id(self, place_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific place by ID"""
        try:
            response = self.client.table("places").select("*").eq("id", place_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error fetching place {place_id}: {e}")
            return None
    
    def get_popular_places(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular places"""
        try:
            response = (
                self.client.table("places")
                .select("*")
                .eq("is_active", True)
                .order("popular_ranking", desc=True)
                .order("visit_count", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching popular places: {e}")
            return []
    
    def get_hotels_sorted_by_price(self, city: Optional[str] = None, country: Optional[str] = None, ascending: bool = True, limit: int = 10) -> List[Dict[str, Any]]:
        """Get hotels sorted by average room price"""
        try:
            # This is a simplified version - you may need to join with rooms table for accurate pricing
            query = self.client.table("hotels").select("*")
            
            if city:
                query = query.ilike("city", f"%{city}%")
            if country:
                query = query.ilike("country", f"%{country}%")
            
            # Order by rating as proxy for price tier (in production, join with rooms table)
            query = query.order("rating", desc=not ascending).limit(limit)
            response = query.execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error fetching hotels sorted by price: {e}")
            return []
    
    # ==================== USER FAVORITES ====================
    
    def get_user_favorites(self, user_id: str, item_type: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user's favorite items"""
        try:
            query = (
                self.client.table("user_favorites")
                .select("*")
                .eq("user_id", user_id)
            )
            
            if item_type:
                query = query.eq("item_type", item_type)
            
            query = query.order("created_at", desc=True).limit(limit)
            response = query.execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error fetching user favorites: {e}")
            return []
    
    def add_user_favorite(self, user_id: str, item_type: str, item_id: str) -> Optional[Dict[str, Any]]:
        """Add item to user favorites"""
        try:
            favorite_data = {
                "user_id": user_id,
                "item_type": item_type,
                "item_id": item_id
            }
            
            response = self.client.table("user_favorites").insert(favorite_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error adding favorite: {e}")
            return None
    
    def remove_user_favorite(self, user_id: str, item_type: str, item_id: str) -> bool:
        """Remove item from user favorites"""
        try:
            response = (
                self.client.table("user_favorites")
                .delete()
                .eq("user_id", user_id)
                .eq("item_type", item_type)
                .eq("item_id", item_id)
                .execute()
            )
            return True
        except Exception as e:
            logger.error(f"Error removing favorite: {e}")
            return False
    
    # ==================== BOOKINGS ====================
    
    def create_booking(
        self,
        user_id: str,
        booking_type: str,
        item_id: str,
        primary_guest_name: str,
        primary_guest_email: str,
        primary_guest_phone: str,
        total_amount: float,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new booking
        
        Args:
            user_id: User ID making the booking
            booking_type: 'package' or 'hotel'
            item_id: Package ID or Hotel ID
            primary_guest_name: Name of primary guest
            primary_guest_email: Email of primary guest
            primary_guest_phone: Phone of primary guest
            total_amount: Total booking amount
            **kwargs: Additional booking details
            
        Returns:
            Created booking record
        """
        try:
            import uuid
            
            booking_data = {
                "user_id": user_id,
                "booking_type": booking_type,
                "item_id": item_id,
                "booking_reference": f"BK{uuid.uuid4().hex[:8].upper()}",
                "primary_guest_name": primary_guest_name,
                "primary_guest_email": primary_guest_email,
                "primary_guest_phone": primary_guest_phone,
                "total_amount": total_amount,
                "base_price": kwargs.get("base_price", total_amount),
                "currency": kwargs.get("currency", "BDT"),
                "total_participants": kwargs.get("total_participants", 1),
                "booking_status": "pending",
                "payment_status": "pending",
                **kwargs
            }
            
            response = self.client.table("bookings").insert(booking_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating booking: {e}")
            return None
    
    def get_booking_by_reference(self, booking_reference: str) -> Optional[Dict[str, Any]]:
        """Get booking by reference number"""
        try:
            response = (
                self.client.table("bookings")
                .select("*")
                .eq("booking_reference", booking_reference)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error fetching booking {booking_reference}: {e}")
            return None
    
    def get_user_bookings(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get all bookings for a user"""
        try:
            response = (
                self.client.table("bookings")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching bookings for user {user_id}: {e}")
            return []


# Create a global instance
supabase_client = SupabaseClient()
