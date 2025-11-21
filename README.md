# PwnEnum

PwnEnum is a combined Subdomain Enumeration and Directory Bruteforcing toolkit designed for penetration testers, security analysts, and red team operators. It aims to provide a unified, optimized, and flexible enumeration workflow with support for:
- Subdomain bruteforcing using user‑defined wordlists
- Directory/content discovery on web servers
- Filtering options (status codes, sizes, keywords)
- Progress indicators for real‑time visibility
- Threading for faster enumeration
- Rate‑limit handling with retries and delays
- Proxy support (global or per‑request)
- Random User‑Agents to reduce fingerprinting
- Output exporting to save results

## Features

### 🔎 Subdomain Enumeration
- Brute-force subdomains using a wordlist
- Filters for valid responses
- Respects wildcard DNS
- Progress display
- Proxy and UA randomization

### 📁 Directory Enumeration
- Scans for valid paths on a target domain
- Supports file extension permutations
- Filters by status code, size, keyword
- Automatic rate-limit handling

## Installation
`git clone https://github.com/yourrepo/pwnenum.git`

`cd pwnenum`

`pip3 install -r requirements.txt`

## Usage
### Subdomain Enumeration
`python3 PwnEnum.py sub -d example.com -w wordlist.txt -t 50 -o output.txt`

### Directory Enumeration
`python3 PwnEnum.py dir -u https://example.com -w dirs.txt -t 50 -o results.txt`
    
## Supported Options
### General
- -w, --wordlist: Path to the wordlist file.

- -t, --threads: Number of threads to use.

- -o, --output: Save results to an output file.

- --proxy: Set a proxy (HTTP/S).

- --rate-limit: Delay between requests in seconds.

### Subdomain Enumeration

- sub: Enter subdomain enumeration mode.

- -d, --domain: Target domain.

- -sc, --status-codes: Filter allowed HTTP status codes.

### Directory Enumeration

- dir: Enter directory enumeration mode.

- -u, --url: Base URL for directory scanning.

- -sc, --status-codes: Filter allowed HTTP status codes.
