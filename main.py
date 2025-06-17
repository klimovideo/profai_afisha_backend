from afisha_client import AfishaClient

def main():
    try:
        client = AfishaClient()
        
        # Get cities
        print("Available cities:")
        cities = client.get_cities()
        for city in cities:
            print(f"- {city['name']} (ID: {city['id']})")
        
        # Example: Get events for the first city
        if cities:
            first_city = cities[0]
            print(f"\nEvents in {first_city['name']}:")
            events = client.get_events(first_city['id'])
            for event in events.get('items', []):
                print(f"- {event['title']}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
    
    