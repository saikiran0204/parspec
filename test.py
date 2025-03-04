import requests
import threading
import time
import uuid

BASE_URL = "http://127.0.0.1:5000"
NUM_REQUESTS = 2000  # Number of concurrent requests to simulate

# Store request times
request_times = []

# Function to place an order and measure response time
def place_order():
    payload = {
        "user_id": str(uuid.uuid4()),
        "item_ids": [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())],
        "total_amount": 150.75
    }
    
    start = time.time()  # Start time
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    end = time.time()  # End time
    
    if response.status_code == 200:
        request_times.append(end - start)  # Store the request time
    else:
        print(f"Error: {response.status_code}, Response: {response.text}")

# Start load test
start_time = time.time()
threads = []

for _ in range(NUM_REQUESTS):
    thread = threading.Thread(target=place_order)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end_time = time.time()
total_time = end_time - start_time

# Calculate metrics
if request_times:
    avg_time = sum(request_times) / len(request_times)
    max_time = max(request_times)
    min_time = min(request_times)
else:
    avg_time = max_time = min_time = 0

print(f"Sent {NUM_REQUESTS} requests in {total_time:.2f} seconds")
print(f"Average response time: {avg_time:.4f} seconds")
print(f"Max response time: {max_time:.4f} seconds")
print(f"Min response time: {min_time:.4f} seconds")
