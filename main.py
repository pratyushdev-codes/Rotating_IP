import requests
import queue
import threading

q = queue.Queue()
valid_proxies = []


try:
    with open("proxy_list.txt", "r") as f:
        proxies = f.read().split("\n")
        for p in proxies:
            if p.strip():  
                q.put(p.strip())
    print(f"Loaded {q.qsize()} proxies to check")
except FileNotFoundError:
    print("Error: proxy_list.txt not found!")
    exit(1)
        
def check_proxies():
    global q, valid_proxies
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json", 
                             proxies={"http": proxy, "https": proxy},
                             timeout=10)
            if res.status_code == 200:
                print(f"✓ Valid proxy: {proxy}")
                valid_proxies.append(proxy)
        except:
            pass  
        finally:
            q.task_done()


print("Starting proxy validation...")
threads = []
for _ in range(50):
    t = threading.Thread(target=check_proxies)
    t.start()
    threads.append(t)


for t in threads:
    t.join()


if valid_proxies:
    with open("valid_proxies", "w") as f:
        for proxy in valid_proxies:
            f.write(proxy + "\n")
    print(f"\n Found and saved {len(valid_proxies)} valid proxies to 'valid_proxies' file")
else:
    print("\n No valid proxies found")

print("Proxy checking complete!")