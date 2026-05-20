#!/usr/bin/env python3
"""
Wayback Machine archive checker for OSINT research.
Check if URLs have been archived and retrieve snapshot information.
No external dependencies required (stdlib only).

Usage:
    python wayback_check.py <url> [--json] [--list]
    
Arguments:
    url      URL to check (with or without protocol)
    --json   Output as JSON
    --list   List available snapshots (may be blocked in some environments)
    
Examples:
    python wayback_check.py example.com
    python wayback_check.py https://anthropic.com/blog --json
    python wayback_check.py example.com --json

Note: The --list option uses the CDX API which may be rate-limited or blocked.
If --list fails, the basic availability check (without --list) usually works.
"""

import json
import urllib.request
import urllib.parse
import sys
from datetime import datetime


def check_availability(url: str) -> dict:
    """
    Check if a URL has been archived in the Wayback Machine.
    Returns the closest available snapshot if it exists.
    """
    # Normalize URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    api_url = f"https://archive.org/wayback/available?url={urllib.parse.quote(url, safe='')}"
    
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            
            result = {"url": url, "archived": False}
            
            snapshots = data.get("archived_snapshots", {})
            closest = snapshots.get("closest", {})
            
            if closest.get("available"):
                result["archived"] = True
                result["snapshot_url"] = closest.get("url")
                result["timestamp"] = closest.get("timestamp")
                result["status"] = closest.get("status")
                
                # Parse timestamp to human-readable format
                ts = closest.get("timestamp", "")
                if len(ts) >= 14:
                    try:
                        dt = datetime.strptime(ts[:14], "%Y%m%d%H%M%S")
                        result["snapshot_date"] = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
                    except ValueError:
                        pass
            
            return result
            
    except Exception as e:
        return {"url": url, "error": str(e)}


def list_snapshots(url: str, limit: int = 100) -> dict:
    """
    List available snapshots for a URL using the CDX API.
    Returns timestamps and snapshot URLs.
    
    Note: The CDX API may be rate-limited or blocked in some environments.
    Use check_availability() as a fallback.
    """
    # Normalize URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    # CDX API for listing snapshots
    api_url = (
        f"https://web.archive.org/cdx/search/cdx"
        f"?url={urllib.parse.quote(url, safe='')}"
        f"&output=json"
        f"&limit={limit}"
        f"&fl=timestamp,statuscode,mimetype,original"
    )
    
    try:
        req = urllib.request.Request(api_url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; OSINT-research/1.0)",
            "Accept": "application/json"
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode()
            
            # Check for access denied
            if "Access denied" in content or "Forbidden" in content:
                return {
                    "url": url, 
                    "error": "CDX API access restricted. Use basic availability check instead.",
                    "fallback_suggestion": "Run without --list flag for basic check"
                }
            
            data = json.loads(content)
            
            if not data or len(data) < 2:
                return {"url": url, "snapshots": [], "count": 0}
            
            # First row is headers
            headers = data[0]
            snapshots = []
            
            for row in data[1:]:
                entry = dict(zip(headers, row))
                timestamp = entry.get("timestamp", "")
                
                snapshot = {
                    "timestamp": timestamp,
                    "status": entry.get("statuscode"),
                    "mimetype": entry.get("mimetype"),
                    "original_url": entry.get("original"),
                    "archive_url": f"https://web.archive.org/web/{timestamp}/{entry.get('original', url)}"
                }
                
                # Parse timestamp
                if len(timestamp) >= 14:
                    try:
                        dt = datetime.strptime(timestamp[:14], "%Y%m%d%H%M%S")
                        snapshot["date"] = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        pass
                
                snapshots.append(snapshot)
            
            # Calculate date range
            result = {
                "url": url,
                "count": len(snapshots),
                "snapshots": snapshots
            }
            
            if snapshots:
                result["first_snapshot"] = snapshots[-1].get("date", snapshots[-1].get("timestamp"))
                result["last_snapshot"] = snapshots[0].get("date", snapshots[0].get("timestamp"))
            
            return result
            
    except urllib.error.HTTPError as e:
        if e.code in (403, 429):
            return {
                "url": url,
                "error": f"CDX API access restricted (HTTP {e.code}). Use basic availability check instead.",
                "fallback_suggestion": "Run without --list flag for basic check"
            }
        return {"url": url, "error": f"HTTP error: {e.code}"}
    except Exception as e:
        return {"url": url, "error": str(e)}


def print_results(results: dict, as_json: bool = False, show_list: bool = False):
    """Print results in human-readable or JSON format."""
    if as_json:
        print(json.dumps(results, indent=2))
        return
    
    url = results.get("url", "Unknown")
    
    if "error" in results:
        print(f"\nError checking {url}: {results['error']}")
        return
    
    if show_list:
        # List view
        count = results.get("count", 0)
        print(f"\n{'='*60}")
        print(f"Wayback Machine Snapshots: {url}")
        print(f"{'='*60}")
        
        if count == 0:
            print("\nNo snapshots found.")
            return
        
        print(f"\nFound {count} snapshots")
        if results.get("first_snapshot"):
            print(f"First: {results['first_snapshot']}")
        if results.get("last_snapshot"):
            print(f"Last:  {results['last_snapshot']}")
        
        print(f"\nRecent snapshots:")
        for snap in results.get("snapshots", [])[:20]:
            date = snap.get("date", snap.get("timestamp", "Unknown"))
            status = snap.get("status", "?")
            print(f"  [{status}] {date}")
            print(f"       {snap.get('archive_url', '')}")
        
        if count > 20:
            print(f"\n  ... and {count - 20} more snapshots")
    else:
        # Simple availability check
        print(f"\n{'='*60}")
        print(f"Wayback Machine: {url}")
        print(f"{'='*60}")
        
        if results.get("archived"):
            print(f"\n✓ Archived")
            print(f"  Snapshot date: {results.get('snapshot_date', results.get('timestamp', 'Unknown'))}")
            print(f"  Status: {results.get('status', 'Unknown')}")
            print(f"  Archive URL: {results.get('snapshot_url', 'Unknown')}")
        else:
            print(f"\n✗ Not archived (or no snapshots available)")
    
    print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    url = sys.argv[1]
    as_json = "--json" in sys.argv
    show_list = "--list" in sys.argv
    
    if show_list:
        results = list_snapshots(url)
    else:
        results = check_availability(url)
    
    print_results(results, as_json, show_list)


if __name__ == "__main__":
    main()
