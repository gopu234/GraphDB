from faker import Faker
import csv

fake = Faker()

number_of_nodes = 100

road_network_file = "road_network.csv"
road_places_file = "road_places.csv"
road_network_relation_file = "road_network_relation.csv"

interceptor_points=[]
places_points=[]

for _ in range(number_of_nodes):
    name = fake.street_name()
    place_name = fake.company().replace(",", "")  # commas would break unquoted CSV
    place_type = fake.random_element(elements=('shop', 'hospital', 'restaurant', 'office', 'mall', 'park'))
    latitude = fake.latitude()
    longitude = fake.longitude()

    places_points.append({
            "place_name":place_name,
            "place_type":place_type,
            "latitude":latitude,
            "longitude":longitude,
            "type":"Place"
    })
    interceptor_points.append({ "name":name, "type":"Interceptor" })

with open(road_network_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
    writer.writerow(['name', 'type'])

    writer.writerows([[point['name'],point['type']] for point in interceptor_points])

with open(road_places_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
    writer.writerow(['place_name', 'place_type', 'latitude', 'longitude', 'type'])

    writer.writerows([[point['place_name'],point['place_type'],point['latitude'],point['longitude'],point['type']] for point in places_points])

with open(road_network_relation_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['start_point', 'end_point', 'distance_km', 'time' , 'speed_limit_kmh', 'road_type','traffic_factor'])

    for interceptor in interceptor_points:
        distance_km = round(fake.random_number(digits=2)+ fake.random.random() , 2)
        time = round(distance_km/(fake.random_number(digits=2)+20) * 60, 2)  #min
        speed_limit_kmh = fake.random_element(elements=(30,50,70,90,110,130,140))
        road_type = fake.random_element(elements=('highway','main road','dirt road','residential road'))
        traffic_factor = round(fake.random.uniform(0.5,2),2)
        
        random_interceptor_point=fake.random.randint(0, len(interceptor_points)-1)
        writer.writerow([
            interceptor['name'],
            interceptor_points[random_interceptor_point]['name'],
            distance_km,
            time,
            speed_limit_kmh,
            road_type,
            traffic_factor
        ])
    
    