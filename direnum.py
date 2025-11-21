import requests
import threading
import time
import random
from queue import Queue

# Random UA pool
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 11)",
    "Mozilla/5.0 (Windows NT 10.0; WOW64)"
]

lock = threading.Lock()


# ---------------------------------------------------------
#  Try HTTPS then HTTP fallback
# ---------------------------------------------------------
def make_request(url, proxy):
    """Try a directory path on HTTPS, fall back to HTTP if needed."""

    schemes = []
    if url.startswith("http://") or url.startswith("https://"):
        schemes = [url]  # already a full URL
    else:
        schemes = [
            f"https://{url}",
            f"http://{url}"
        ]

    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }

    proxies = {"http": proxy, "https": proxy} if proxy else None

    for attempt in schemes:
        try:
            r = requests.get(attempt, headers=headers, proxies=proxies, timeout=4)
            return r.status_code
        except:
            continue

    return None


# ---------------------------------------------------------
#  Worker Thread
# ---------------------------------------------------------
def worker(queue, base_url, results, proxy, status_filter, progress, total):
    while not queue.empty():
        path = queue.get()

        # Ensure proper formatting
        if base_url.endswith("/"):
            full = base_url + path
        else:
            full = f"{base_url}/{path}"

        status = make_request(full, proxy)

        with lock:
            progress[0] += 1
            percent = (progress[0] / total) * 100
            print(f"\rProgress: {percent:.2f}% ({progress[0]}/{total})", end="")

        if status:
            if (status_filter and status in status_filter) or (not status_filter):
                with lock:
                    results.append(f"{full} [{status}]")
                    print(f"\nFOUND: {full} [{status}]")

        queue.task_done()


# ---------------------------------------------------------
#  Run Directory Enumeration
# ---------------------------------------------------------
def run_directory_enum(base_url, wordlist, threads, output, proxy, status_filter):

    print(f"\n[+] Starting Directory Enumeration on: {base_url}")
    print(f"[+] Words loaded: {len(wordlist)}")
    if proxy:
        print(f"[+] Using Proxy: {proxy}")
    print("--------------------------------------------------")

    queue = Queue()
    results = []
    progress = [0]
    total = len(wordlist)

    # Load queue
    for word in wordlist:
        queue.put(word)

    # Start threads
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(
            target=worker,
            args=(queue, base_url, results, proxy, status_filter, progress, total)
        )
        t.start()
        thread_list.append(t)

    # Wait for finish
    for t in thread_list:
        t.join()

    print("\n\n[+] Scan Complete!")
    print(f"[+] Total Found: {len(results)}")

    # Save results
    if output:
        with open(output, "w") as f:
            for r in results:
                f.write(r + "\n")
        print(f"[+] Saved to: {output}")

    return results
