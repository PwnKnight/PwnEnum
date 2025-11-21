#!/usr/bin/env python3
import argparse
import threading
import requests
import time
import random
import sys
import os
from queue import Queue

# ---------------------------------------------------------
#   MODULE PATH INJECTION (Option C)
# ---------------------------------------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))
from subenum import run_subdomain_enum
from direnum import run_directory_enum

# ---------------------------------------------------------
#   RANDOM USER-AGENTS
# ---------------------------------------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 11)",
    "Mozilla/5.0 (Windows NT 10.0; WOW64)"
]

# ---------------------------------------------------------
#   BANNER
# ---------------------------------------------------------
def banner():
    print(r"""
██████╗ ██╗    ██╗███╗   ██╗███████╗███╗   ██╗██╗   ██╗███╗   ███╗
██╔══██╗██║    ██║████╗  ██║██╔════╝████╗  ██║██║   ██║████╗ ████║
██████╔╝██║ █╗ ██║██╔██╗ ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║
██╔═══╝ ██║███╗██║██║╚██╗██║██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║
██║     ╚███╔███╔╝██║ ╚████║███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║
╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝
                                                                  

                  PwnEnum — Enumeration Suite
       Developed by: Emilio Pancubit — PwnKnight
============================================================
""")

# ---------------------------------------------------------
#   WORDLIST LOADER
# ---------------------------------------------------------
def load_wordlist(path):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        print(f"[ERROR] Could not load wordlist: {path}")
        sys.exit(1)

# ---------------------------------------------------------
#   MODE-SPECIFIC HELP
# ---------------------------------------------------------
def show_sub_help():
    print("""
Subdomain Mode Usage:
  python3 PwnEnum.py sub -d example.com -w wordlist.txt [options]

Options:
  -d, --domain      Target domain (required)
  -w, --wordlist    Subdomain wordlist
  -t, --threads     Number of threads (default: 10)
  -o, --output      Output file
  -sc, --status     Filter allowed HTTP status codes (comma separated)
  --proxy           Proxy (e.g., http://127.0.0.1:8080)
""")


def show_dir_help():
    print("""
Directory Mode Usage:
  python3 PwnEnum.py dir -u https://example.com -w wordlist.txt [options]

Options:
  -u, --url         Base URL (required)
  -w, --wordlist    Directory wordlist
  -t, --threads     Number of threads (default: 10)
  -o, --output      Output file
  -sc, --status     Filter allowed HTTP status (comma separated)
  --proxy           Proxy (e.g., http://127.0.0.1:8080)
""")

# ---------------------------------------------------------
#   MAIN
# ---------------------------------------------------------
def main():
    banner()

    parser = argparse.ArgumentParser(
        description="PwnEnum Enumeration Tool",
        add_help=True
    )

    parser.add_argument(
        "mode",
        help="Mode: sub / dir",
        choices=["sub", "dir"]
    )

    parser.add_argument("-w", "--wordlist", help="Wordlist path")
    parser.add_argument("-d", "--domain", help="Target domain for subdomain enumeration")
    parser.add_argument("-u", "--url", help="Target URL for directory enumeration")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Threads")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--proxy", help="Proxy (http://127.0.0.1:8080)")
    parser.add_argument("-sc", "--status", help="Allowed status codes (comma separated)")

    args = parser.parse_args()

    # Parse status code filters
    status_filter = None
    if args.status:
        status_filter = [int(x) for x in args.status.split(",")]

    # ------------------------------
    # MODE: SUBDOMAIN
    # ------------------------------
    if args.mode == "sub":

        if not args.domain or not args.wordlist:
            show_sub_help()
            sys.exit(1)

        # Reject invalid input like api.example.com
        if "." in args.domain.split(".")[0]:
            print(f"[ERROR] Invalid domain for subdomain enumeration: {args.domain}")
            print("       Do NOT include subdomains here.")
            sys.exit(1)

        words = load_wordlist(args.wordlist)

        run_subdomain_enum(
            domain=args.domain,
            wordlist=words,
            threads=args.threads,
            output=args.output,
            proxy=args.proxy,
            status_filter=status_filter
        )
        return

    # ------------------------------
    # MODE: DIRECTORY
    # ------------------------------
    if args.mode == "dir":
        if not args.url or not args.wordlist:
            show_dir_help()
            sys.exit(1)

        words = load_wordlist(args.wordlist)

        run_directory_enum(
            base_url=args.url,
            wordlist=words,
            threads=args.threads,
            output=args.output,
            proxy=args.proxy,
            status_filter=status_filter
        )
        return


if __name__ == "__main__":
    main()
