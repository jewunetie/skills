# People Research Techniques

Techniques and tools for investigating individuals using publicly accessible sources.

## Social Media Investigation

### Platform-Specific Approaches

**LinkedIn**
- Native search limited for free accounts; use Google dorks: `site:linkedin.com/in/ "name" "company"`
- Profile URLs often contain username: `linkedin.com/in/[username]`
- Check activity: posts, comments, articles, group memberships
- Employment history provides timeline and network connections

**Twitter/X**
- Advanced search: `twitter.com/search-advanced`
- Key operators: `from:username`, `since:YYYY-MM-DD`, `until:YYYY-MM-DD`, `geocode:lat,long,radius`
- Search replies and mentions, not just posts
- Check following/followers for network mapping

**Facebook**
- Direct search limited; use Google: `site:facebook.com "name" "location"`
- Check public posts, group memberships, tagged photos
- Friends lists often partially visible

**Instagram**
- Browse without account via picuki.com
- Check tagged locations, tagged users, story highlights
- Posting times reveal timezone/routine

**Reddit**
- User history at `reddit.com/user/[username]`
- Comments reveal interests, expertise, opinions, location hints
- Check cake day and karma for account age/activity level

**TikTok**
- Profile at `tiktok.com/@username`
- Video content, sounds used, duets reveal interests and connections

### Social Media Tools

| Tool | URL | Description |
|------|-----|-------------|
| WhatsMyName | whatsmyname.app | Web-based username search across 500+ sites |
| Sherlock | github.com/sherlock-project/sherlock | CLI tool, 400+ sites, low false positives |
| Maigret | github.com/soxoj/maigret | Sherlock fork, 2000+ sites |
| Social Searcher | social-searcher.com | Multi-platform search |
| Picuki | picuki.com | Instagram viewer without account |

## Username and Email OSINT

### Username Enumeration
1. Start with known username
2. Search across platforms using tools above
3. Try variations: appending numbers, underscores, dots
4. Check for consistent avatar images across platforms

### Email Investigation

| Tool | URL | Description |
|------|-----|-------------|
| Hunter.io | hunter.io | Find emails by domain, verify deliverability |
| Have I Been Pwned | haveibeenpwned.com | Check if email in data breaches (reveals which services used) |
| Epieos | epieos.com | Email to identity - finds associated Google profiles |
| Holehe | github.com/megadose/holehe | Check which sites have accounts for an email |

Email components to investigate:
- Username portion → search as username
- Domain → if custom domain, who owns it?
- Format pattern → try variations (firstname.lastname, flastname, etc.)

## Phone Number Research

| Tool | URL | Description |
|------|-----|-------------|
| Truecaller | truecaller.com | Global crowdsourced caller ID |
| NumLookup | numlookup.com | Free carrier/line type lookup |
| CallerID Test | calleridtest.com | CNAM lookup for subscriber name |
| Sync.me | sync.me | Reverse phone lookup |

Information obtainable:
- Subscriber name (CNAM)
- Carrier/provider
- Line type (mobile, landline, VoIP)
- Geographic region from area code

## Public Records (US-focused)

### Court Records

| Source | URL | Description |
|--------|-----|-------------|
| CourtListener | courtlistener.com | Free federal cases via RECAP project |
| PACER | pacer.uscourts.gov | Federal court records (fee-based but often waived) |
| State Courts | Varies by state | Each state has own search portal |

### Property and Business Records
- County assessor/recorder websites for property ownership
- State Secretary of State for business filings
- Voter registration (public in most states): name, address, DOB, party, voting history

### Other Public Records
- Marriage/divorce records (county clerk)
- Professional licenses (state licensing boards)
- Campaign contributions (fec.gov)

## Image and Visual OSINT

### Reverse Image Search

| Tool | URL | Description |
|------|-----|-------------|
| Google Images | images.google.com | General reverse search |
| Yandex Images | yandex.com/images | Best for faces and Eastern European content |
| TinEye | tineye.com | Finding image origins and modifications |
| FaceCheck.ID | facecheck.id | Face search across social media |

### EXIF Metadata

| Tool | URL | Description |
|------|-----|-------------|
| ExifTool | exiftool.org | CLI gold standard, most comprehensive |
| Jimpl | jimpl.com | Web-based with map display for GPS |
| FotoForensics | fotoforensics.com | EXIF + error level analysis for manipulation |

EXIF can reveal: camera make/model, capture date/time, GPS coordinates, editing software. Note: Most social media strips EXIF on upload; original files via messaging may retain it.

## Archived and Deleted Content

| Tool | URL | Description |
|------|-----|-------------|
| Wayback Machine | web.archive.org | 800+ billion archived pages since 1996 |
| Archive.today | archive.today | Manual archiving, good for social media |
| CachedView | cachedview.com | Aggregates multiple cache sources |

Search pattern for Wayback: `web.archive.org/web/*/example.com/path/*`

## People Search Aggregators

These aggregate public records, phone directories, social profiles, and data broker information:

| Tool | URL | Description |
|------|-----|-------------|
| TruePeopleSearch | truepeoplesearch.com | Free, US-focused |
| FastPeopleSearch | fastpeoplesearch.com | Free, US-focused |
| That's Them | thatsthem.com | Free, includes email/phone lookup |
| Webmii | webmii.com | Free people search aggregator |
| PeekYou | peekyou.com | Free, aggregates social profiles |

Caution: Aggregator data can be months or years outdated. Always verify key findings from primary sources.
