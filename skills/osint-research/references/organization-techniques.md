# Organization Research Techniques

Techniques and tools for investigating companies, nonprofits, and other organizations using publicly accessible sources.

## Corporate Registry Databases

### United States

Companies register at state level. Key portals:

| State | URL | Notes |
|-------|-----|-------|
| Delaware | icis.corp.delaware.gov | Most US corporations registered here |
| Florida | sunbiz.org | Notably transparent records |
| California | bizfileonline.sos.ca.gov | Large business database |
| New York | appext20.dos.ny.gov/corp_public | Corporation search |
| Texas | mycpa.cpa.state.tx.us/coa | Comptroller lookup |

Information typically available: company name, registration number, status (active/dissolved), formation date, registered agent, officers/directors.

### International

| Jurisdiction | URL | Description |
|--------------|-----|-------------|
| UK Companies House | find-and-update.company-information.service.gov.uk | Free, comprehensive: officers, filings, PSC (beneficial owners) |
| OpenCorporates | opencorporates.com | Aggregates 235M+ companies from 145+ jurisdictions |
| EU Business Registers | e-justice.europa.eu | Links to all EU member state registries |

### Global Aggregator

**OpenCorporates** is the primary tool for cross-jurisdictional searches. Searchable by company name, officer name, registration number, or address. Free tier provides basic data; API free for journalists/NGOs/academics.

## SEC and Financial Disclosures

### EDGAR Database

SEC filings at sec.gov/edgar/search. Key form types:

| Form | Purpose | Intelligence Value |
|------|---------|-------------------|
| 10-K | Annual report | Financials, risk factors, business description, competition |
| 10-Q | Quarterly report | Recent performance, material changes |
| 8-K | Current report | M&A, leadership changes, material contracts |
| DEF 14A | Proxy statement | Executive compensation, board members, voting matters |
| Form 4 | Insider transactions | Stock purchases/sales by officers |
| 13-F | Institutional holdings | Who owns significant stakes |
| S-1 | IPO registration | Comprehensive pre-IPO disclosure |

**10-K Item 1A (Risk Factors)** is especially valuable - management must disclose concerns and vulnerabilities.

### International Equivalents

| Country | Source | URL |
|---------|--------|-----|
| UK | Companies House | companieshouse.gov.uk |
| Canada | SEDAR+ | sedarplus.ca |
| Australia | ASX | asx.com.au |

## Business Intelligence Sources

| Tool | URL | Description |
|------|-----|-------------|
| Crunchbase | crunchbase.com | Company profiles, funding rounds, key people, news (free tier available) |
| Owler | owler.com | Competitive intelligence, company profiles |
| Craft.co | craft.co | Company profiles, supply chain data |
| LinkedIn | linkedin.com/company | Company pages, employee data, job postings |

## Domain and Website Investigation

### Domain Registration

| Tool | URL | Description |
|------|-----|-------------|
| ICANN Lookup | lookup.icann.org | Official WHOIS (often redacted post-GDPR) |
| Whois.com | whois.com | Free WHOIS lookup |
| ViewDNS | viewdns.info | WHOIS, reverse IP, DNS tools |
| Whoxy | whoxy.com | WHOIS history, reverse searches (limited free) |

### DNS and Infrastructure

| Tool | URL | Description |
|------|-----|-------------|
| SecurityTrails | securitytrails.com | Historical DNS, subdomains, IP history (50 free queries/mo) |
| DNSDumpster | dnsdumpster.com | DNS recon, subdomain enumeration |
| crt.sh | crt.sh | Certificate Transparency logs - reveals subdomains |
| Shodan | shodan.io | Internet-connected device search |
| Censys | search.censys.io | Host and certificate search |

### Website Technology

| Tool | URL | Description |
|------|-----|-------------|
| Wappalyzer | wappalyzer.com | Browser extension detecting CMS, frameworks, analytics |
| BuiltWith | builtwith.com | Technology profiler with historical data |
| SimilarWeb | similarweb.com | Traffic estimates, audience insights |

## Job Postings as Intelligence

Job listings reveal organizational intelligence:
- **Technologies used**: Required skills indicate tech stack
- **Expansion plans**: New location hiring
- **Team structure**: Role titles and reporting lines
- **Financial health**: Hiring volume indicates growth
- **Strategic priorities**: New AI/ML roles indicate direction

Primary sources: LinkedIn Jobs, Indeed, Glassdoor, company career pages.

Search pattern: `site:linkedin.com/jobs "company name"` or `site:greenhouse.io "company name"`

## Patent and Trademark Research

| Source | URL | Description |
|--------|-----|-------------|
| Google Patents | patents.google.com | US, EPO, WIPO patents, user-friendly interface |
| USPTO | ppubs.uspto.gov | US patents from 1790-present |
| Espacenet | worldwide.espacenet.com | 140M+ docs from 90+ authorities |
| USPTO TESS | tmsearch.uspto.gov | US trademark search |
| WIPO Global Brand | branddb.wipo.int | International trademark database |

Patents reveal R&D focus, technology direction, and key inventors.

## Government Contracts and Grants

| Source | URL | Description |
|--------|-----|-------------|
| USAspending | usaspending.gov | All federal spending: contracts, grants, loans |
| SAM.gov | sam.gov | Contract opportunities, entity registration |
| FPDS | fpds.gov | Federal procurement data |
| Grants.gov | grants.gov | Federal grant opportunities |

Search by recipient name, NAICS code, agency, or location.

## Nonprofit Research

| Source | URL | Description |
|--------|-----|-------------|
| ProPublica Nonprofit Explorer | projects.propublica.org/nonprofits | Searchable Form 990s |
| GuideStar/Candid | candid.org | Nonprofit profiles, financials |
| Charity Navigator | charitynavigator.org | Ratings and financials |
| IRS Tax Exempt Search | apps.irs.gov/app/eos | Official exempt org database |

**Form 990** reveals: revenue, expenses, officers, board members, highest-paid employees, major donors (Schedule B for private foundations), program descriptions.

## Supply Chain and Trade Data

| Tool | URL | Description |
|------|-----|-------------|
| ImportYeti | importyeti.com | Free import data, supplier search |
| US Census Trade Data | usatrade.census.gov | Official US trade statistics |
| UN Comtrade | comtradeplus.un.org | International trade database |

Trade data reveals suppliers, shipping volumes, sourcing countries, and business relationships.

## News and Press

| Source | URL | Description |
|--------|-----|-------------|
| Google News | news.google.com | News aggregation with date filtering |
| Business Wire | businesswire.com | Press releases |
| PR Newswire | prnewswire.com | Press releases |
| SEC EDGAR | sec.gov/cgi-bin/browse-edgar | 8-K filings often contain press releases |

Use date operators: `"company name" after:2024-01-01` to find recent coverage.

## LinkedIn Company Research

- Company pages: `linkedin.com/company/[company-name]`
- Employee search: `site:linkedin.com/in/ "company name"`
- Employee count, growth trends, job postings
- "People also viewed" for competitors
- Employee tenure patterns indicate culture/turnover
