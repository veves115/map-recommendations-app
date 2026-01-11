import googlemaps
from typing import List, Dict, Any, Optional
from app.core.config import settings

class MapsService:
    def __init__(self):
        self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    
    def get_nearby_places(
        self,
        latitude: float,
        longitude: float,
        radius: int = 1000,
        place_type: Optional[str] = None,
        keyword: Optional[str] = None
    ) -> List[Dict]:
        """
        Obtener lugares cercanos a una ubicación
        
        Args:
            latitude: Latitud
            longitude: Longitud
            radius: Radio de búsqueda en metros (default 1km)
            place_type: Tipo de lugar (restaurant, cafe, museum, etc.)
            keyword: Palabra clave para filtrar
        
        Returns:
            Lista de lugares cercanos
        """
        try:
            location = (latitude, longitude)
            
            # Parámetros de búsqueda
            params = {
                'location': location,
                'radius': radius
            }
            
            if place_type:
                params['type'] = place_type
            
            if keyword:
                params['keyword'] = keyword
            
            # Realizar búsqueda
            places_result = self.client.places_nearby(**params)
            
            # Procesar resultados
            places = []
            for place in places_result.get('results', []):
                places.append({
                    'place_id': place.get('place_id'),
                    'name': place.get('name'),
                    'address': place.get('vicinity'),
                    'types': place.get('types', []),
                    'rating': place.get('rating'),
                    'user_ratings_total': place.get('user_ratings_total'),
                    'location': {
                        'lat': place['geometry']['location']['lat'],
                        'lng': place['geometry']['location']['lng']
                    },
                    'open_now': place.get('opening_hours', {}).get('open_now'),
                    'photos': [photo['photo_reference'] for photo in place.get('photos', [])][:3]
                })
            
            return places
            
        except Exception as e:
            print(f"Error al buscar lugares: {e}")
            return []
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """
        Obtener detalles completos de un lugar
        
        Args:
            place_id: ID del lugar en Google Maps
        
        Returns:
            Detalles del lugar
        """
        try:
            place_result = self.client.place(place_id=place_id)
            
            if place_result.get('status') == 'OK':
                place = place_result['result']
                return {
                    'place_id': place.get('place_id'),
                    'name': place.get('name'),
                    'formatted_address': place.get('formatted_address'),
                    'phone': place.get('formatted_phone_number'),
                    'website': place.get('website'),
                    'rating': place.get('rating'),
                    'user_ratings_total': place.get('user_ratings_total'),
                    'price_level': place.get('price_level'),
                    'types': place.get('types', []),
                    'location': {
                        'lat': place['geometry']['location']['lat'],
                        'lng': place['geometry']['location']['lng']
                    },
                    'opening_hours': place.get('opening_hours', {}).get('weekday_text'),
                    'reviews': [
                        {
                            'author': review.get('author_name'),
                            'rating': review.get('rating'),
                            'text': review.get('text'),
                            'time': review.get('time')
                        }
                        for review in place.get('reviews', [])[:5]
                    ]
                }
            return None
            
        except Exception as e:
            print(f"Error al obtener detalles del lugar: {e}")
            return None
    
    def geocode_address(self, address: str) -> Optional[Dict]:
        """
        Convertir dirección a coordenadas
        
        Args:
            address: Dirección a geocodificar
        
        Returns:
            Coordenadas y dirección formateada
        """
        try:
            geocode_result = self.client.geocode(address)
            
            if geocode_result:
                result = geocode_result[0]
                return {
                    'formatted_address': result.get('formatted_address'),
                    'location': {
                        'lat': result['geometry']['location']['lat'],
                        'lng': result['geometry']['location']['lng']
                    },
                    'place_id': result.get('place_id')
                }
            return None
            
        except Exception as e:
            print(f"Error al geocodificar dirección: {e}")
            return None

# Instancia global del servicio
maps_service = MapsService()