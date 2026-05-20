#!/usr/bin/env python3
"""
Domain reconnaissance script for OSINT research.
Combines DNS lookups, WHOIS data, and subdomain discovery using only public APIs.
No external dependencies required (stdlib only).

Usage:
    python domain_recon.py <domain> [--json]
    
Examples:
    python domain_recon.py anthropic.com
    python domain_recon.py example.com --json
"""

import json
import urllib.request
import urllib.error
import re
import sys
from typing import Optional


def dns_lookup(domain: str) -> dict:
    """
    Perform DNS lookups using Google's DNS-over-HTTPS API.
    Returns A, AAAA, MX, NS, and TXT records.
    """
    results = {}
    record_types = ["A", "AAAA", "MX", "NS", "TXT"]
    
    for rtype in record_types:
        url = f"https://dns.google/resolve?name={domain}&type={rtype}"
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/dns-json"})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                if "Answer" in data:
                    records = [ans.get("data") for ans in data["Answer"] if ans.get("data")]
                    if records:
                        results[rtype] = records
        except Exception:
            continue
    
    return results


def whois_lookup(domain: str) -> dict:
    """
    Perform WHOIS lookup using RDAP (Registration Data Access Protocol).
    RDAP is the official successor to WHOIS with structured JSON responses.
    """
    # Determine TLD and select appropriate RDAP server
    tld = domain.split(".")[-1].lower()
    
    rdap_servers = {
        "com": "https://rdap.verisign.com/com/v1/domain/",
        "net": "https://rdap.verisign.com/net/v1/domain/",
        "org": "https://rdap.publicinterestregistry.org/rdap/domain/",
        "io": "https://rdap.nic.io/domain/",
        "co": "https://rdap.nic.co/domain/",
    }
    
    # Try TLD-specific server first, then generic fallback
    urls = []
    if tld in rdap_servers:
        urls.append(rdap_servers[tld] + domain)
    urls.append(f"https://rdap.org/domain/{domain}")
    
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/rdap+json"})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode())
                
                result = {}
                
                # Extract registration dates
                for event in data.get("events", []):
                    action = event.get("eventAction")
                    date = event.get("eventDate")
                    if action == "registration" and date:
                        result["creation_date"] = date
                    elif action == "expiration" and date:
                        result["expiration_date"] = date
                    elif action == "last changed" and date:
                        result["updated_date"] = date
                
                # Extract nameservers
                nameservers = [ns.get("ldhName") for ns in data.get("nameservers", []) if ns.get("ldhName")]
                if nameservers:
                    result["nameservers"] = nameservers
                
                # Extract status
                status = data.get("status", [])
                if status:
                    result["status"] = status
                
                # Extract registrar from entities
                for entity in data.get("entities", []):
                    roles = entity.get("roles", [])
                    if "registrar" in roles:
                        # Try to get registrar name from vcard
                        vcard = entity.get("vcardArray", [])
                        if len(vcard) > 1:
                            for field in vcard[1]:
                                if field[0] == "fn":
                                    result["registrar"] = field[3]
                                    break
                        # Fallback to handle
                        if "registrar" not in result and entity.get("handle"):
                            result["registrar"] = entity.get("handle")
                
                return result
                
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
        except Exception:
            continue
    
    return {"error": "Could not retrieve WHOIS data"}


def subdomain_discovery(domain: str, timeout: int = 30) -> dict:
    """
    Discover subdomains using Certificate Transparency logs via crt.sh.
    Returns unique subdomains found in SSL/TLS certificates.
    """
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode())
            
            subdomains = set()
            # Pattern for valid hostnames
            hostname_pattern = re.compile(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]*[a-z0-9])?)*$")
            
            for entry in data:
                name_value = entry.get("name_value", "")
                for line in name_value.split("\n"):
                    subdomain = line.strip().lower()
                    # Filter: must end with domain, no wildcards, valid format
                    if (subdomain.endswith(domain) and 
                        not subdomain.startswith("*") and 
                        "@" not in subdomain and
                        hostname_pattern.match(subdomain)):
                        subdomains.add(subdomain)
            
            return {
                "count": len(subdomains),
                "subdomains": sorted(subdomains)
            }
            
    except Exception as e:
        return {"error": str(e)}


def full_recon(domain: str) -> dict:
    """
    Perform full domain reconnaissance combining all methods.
    """
    results = {
        "domain": domain,
        "dns": {},
        "whois": {},
        "subdomains": {}
    }
    
    # DNS lookup
    dns_results = dns_lookup(domain)
    if dns_results:
        results["dns"] = dns_results
    
    # WHOIS lookup
    whois_results = whois_lookup(domain)
    if whois_results:
        results["whois"] = whois_results
    
    # Subdomain discovery
    subdomain_results = subdomain_discovery(domain)
    if subdomain_results:
        results["subdomains"] = subdomain_results
    
    return results


def print_results(results: dict, as_json: bool = False):
    """Print results in human-readable or JSON format."""
    if as_json:
        print(json.dumps(results, indent=2))
        return
    
    domain = results.get("domain", "Unknown")
    print(f"\n{'='*60}")
    print(f"Domain Reconnaissance: {domain}")
    print(f"{'='*60}")
    
    # DNS Records
    dns = results.get("dns", {})
    if dns:
        print(f"\n[DNS Records]")
        for rtype, records in dns.items():
            print(f"  {rtype}:")
            for record in records[:5]:
                print(f"    - {record}")
            if len(records) > 5:
                print(f"    ... and {len(records) - 5} more")
    else:
        print(f"\n[DNS Records] No records found")
    
    # WHOIS
    whois = results.get("whois", {})
    if whois and "error" not in whois:
        print(f"\n[WHOIS Information]")
        field_labels = {
            "registrar": "Registrar",
            "creation_date": "Created",
            "expiration_date": "Expires",
            "updated_date": "Updated",
            "nameservers": "Nameservers",
            "status": "Status"
        }
        for field, label in field_labels.items():
            if field in whois:
                value = whois[field]
                if isinstance(value, list):
                    print(f"  {label}:")
                    for v in value[:3]:
                        print(f"    - {v}")
                    if len(value) > 3:
                        print(f"    ... and {len(value) - 3} more")
                else:
                    print(f"  {label}: {value}")
    else:
        print(f"\n[WHOIS Information] {whois.get('error', 'Not available')}")
    
    # Subdomains
    subs = results.get("subdomains", {})
    if subs and "error" not in subs:
        count = subs.get("count", 0)
        subdomains = subs.get("subdomains", [])
        print(f"\n[Subdomains] Found {count} via Certificate Transparency")
        for sub in subdomains[:15]:
            print(f"    - {sub}")
        if count > 15:
            print(f"    ... and {count - 15} more")
    else:
        print(f"\n[Subdomains] {subs.get('error', 'Not available')}")
    
    print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    domain = sys.argv[1].lower().strip()
    as_json = "--json" in sys.argv
    
    # Basic domain validation
    if not re.match(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]*[a-z0-9])?)+$", domain):
        print(f"Error: Invalid domain format: {domain}")
        sys.exit(1)
    
    results = full_recon(domain)
    print_results(results, as_json)


if __name__ == "__main__":
    main()
