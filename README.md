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
    
