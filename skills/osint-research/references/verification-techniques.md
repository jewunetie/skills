# Verification Techniques

Methods for verifying claims, geolocating content, determining when events occurred, and fact-checking.

## Geolocation from Images/Video

### Systematic Process

1. **Analyze context**: Language on signs, architecture style, vegetation, vehicle types
2. **Identify landmarks**: Unique buildings, monuments, geographic features
3. **Extract visual clues**: Road markings, utility poles, license plates, sun position
4. **Narrow search area**: Region → City → Neighborhood
5. **Match against mapping tools**: Satellite and street view
6. **Verify**: Confirm 3+ reference points align

### Visual Clue Categories

| Category | What to Look For |
|----------|------------------|
| Architecture | Building styles, roofing materials, window designs |
| Signage | Language, font styles, road sign designs, business names |
| Vegetation | Tree species, crops, seasonal indicators |
| Infrastructure | Power line styles, road markings, sidewalk patterns |
| Vehicles | License plate format, driving side, common makes |
| Terrain | Mountains, water bodies, elevation, soil color |
| Weather | Cloud patterns, visibility, precipitation |

### Geolocation Tools

| Tool | URL | Description |
|------|-----|-------------|
| Google Earth Pro | google.com/earth | Free desktop app, historical imagery slider |
| Google Street View | maps.google.com | Street-level imagery |
| Yandex Maps | yandex.com/maps | Better coverage in Russia/CIS |
| Mapillary | mapillary.com | Crowdsourced street imagery |
| OpenStreetMap | openstreetmap.org | Detailed mapping, rural area coverage |
| Wikimapia | wikimapia.org | User-annotated locations |
| SunCalc | suncalc.org | Sun position calculator for shadow analysis |
| GeoSpy.ai | geospy.ai | AI-powered geolocation from images |

### Shadow Analysis for Direction

Sun position indicates cardinal directions:
- Shadows point opposite to sun
- In Northern Hemisphere: sun is south, shadows point north at solar noon
- Shadow length + sun angle = time estimation
- Use SunCalc to model sun position for location/date/time

## Chronolocation (When Did This Happen?)

### Methods

**Shadow Analysis**
1. Geolocate the image first
2. Identify clear shadows with known object heights
3. Calculate shadow ratio (length ÷ height)
4. Determine sun azimuth (opposite of shadow direction)
5. Use SunCalc: adjust date/time until shadows match

**Weather Verification**
Cross-reference visible weather against historical records:

| Tool | URL | Description |
|------|-----|-------------|
| Weather Underground History | wunderground.com/history | Historical weather by location/date |
| NOAA Climate Data | ncdc.noaa.gov | Official US weather records |
| WorldWeatherOnline | worldweatheronline.com/weather-history | Global historical weather |
| Ogimet | ogimet.com | SYNOP weather data |

**Metadata**
- EXIF data from original images (creation timestamp, GPS)
- File system timestamps (can be misleading if copied)
- Platform upload timestamps
- Note: Timestamps can be manipulated; use as corroboration, not proof

**Contextual Clues**
- Event banners, dated signs, newspaper headlines in frame
- Seasonal indicators (foliage, snow, holiday decorations)
- Construction state of known buildings/projects
- Vehicle model years

## Fact-Checking Methodology

### First Draft's Five Pillars

| Pillar | Question |
|--------|----------|
| Provenance | Is this the original content? |
| Source | Who created/uploaded it? |
| Date | When was it created? |
| Location | Where was it captured? |
| Motivation | Why was it created/shared? |

### Verification Workflow

1. **Check if already debunked**: Search claim + "fact check", "debunked", "false"
2. **Find original source**: Trace back through shares to first appearance
3. **Verify source identity**: Is account real? History consistent?
4. **Check for manipulation**: Reverse image search, metadata analysis
5. **Corroborate with other sources**: Independent confirmation
6. **Check date alignment**: Does timeline make sense?

### Fact-Checking Resources

| Tool | URL | Description |
|------|-----|-------------|
| Google Fact Check Explorer | toolbox.google.com/factcheck/explorer | Search fact-checks across organizations |
| Snopes | snopes.com | Long-running fact-check site |
| PolitiFact | politifact.com | Political claims |
| FactCheck.org | factcheck.org | Political claims |
| AFP Fact Check | factcheck.afp.com | International coverage |
| Reuters Fact Check | reuters.com/fact-check | News-focused |
| Full Fact | fullfact.org | UK-focused |

## Image/Video Verification

### Manipulation Detection

| Tool | URL | Description |
|------|-----|-------------|
| FotoForensics | fotoforensics.com | Error level analysis, metadata, JPEG quality |
| Forensically | 29a.ch/photo-forensics | Clone detection, error level analysis |
| TinEye | tineye.com | Find image modifications and origins |

### Red Flags for Manipulation
- Inconsistent lighting/shadows across image
- Irregular edges around subjects
- Repeated patterns (clone stamp artifacts)
- Misaligned perspective
- JPEG quality inconsistencies
- Missing/inconsistent metadata

### Video-Specific Tools

| Tool | URL | Description |
|------|-----|-------------|
| InVID WeVerify | weverify.eu/verification-plugin | Browser extension, keyframe extraction, reverse search |
| YouTube DataViewer | citizenevidence.amnestyusa.org | Extract upload time, thumbnails |
| Downsub | downsub.com | Download video subtitles for analysis |

## Satellite Imagery Analysis

| Tool | URL | Description |
|------|-----|-------------|
| Google Earth Pro | google.com/earth | Historical imagery with time slider |
| Sentinel Hub EO Browser | apps.sentinel-hub.com/eo-browser | Free 10m resolution, 5-day refresh |
| USGS Earth Explorer | earthexplorer.usgs.gov | Landsat imagery since 1972 |
| NASA Worldview | worldview.earthdata.nasa.gov | Near real-time imagery, 600+ layers |
| Zoom Earth | zoom.earth | Recent satellite imagery, weather |

Resolution limitations:
- Sentinel-2: 10m (cannot identify vehicles/individuals)
- Landsat: 30m (broad area analysis only)
- Google Earth: ~15cm in urban areas (varies)

## Social Media Content Verification

### Platform-Specific Checks

**Twitter/X**
- Account creation date (new accounts less reliable)
- Follower/following ratio
- Post history consistency
- Check if account is verified (though less reliable post-2023)

**Facebook**
- Profile creation date
- Friend network (fake profiles often have sparse networks)
- Activity patterns
- Check if profile photo appears elsewhere (reverse image search)

**YouTube**
- Channel creation date
- Upload history
- View/subscriber patterns
- Comments (often contain corrections/context)

### Bot/Fake Account Indicators
- High posting frequency (hundreds/day)
- Coordinated timing across accounts
- Generic profile photos (stock images, AI-generated)
- Username patterns: adjective+noun+numbers
- Non-human posting hours
- Identical or templated content across accounts

## Document Verification

### Authenticity Checks
- Consistent formatting with known authentic documents
- Correct logos, headers, signatures for stated organization
- Metadata matches claimed origin
- Language/terminology consistent with organization
- Cross-reference information against other sources

### PDF Metadata

| Tool | URL | Description |
|------|-----|-------------|
| ExifTool | exiftool.org | Comprehensive metadata extraction |
| PDF Examiner | pdfexaminer.com | Online PDF analysis |
| Peepdf | github.com/jesparza/peepdf | PDF security analysis |

PDF metadata can reveal: creation software, author, creation/modification dates, edit history.

## Corroboration Standards

| Confidence Level | Requirements |
|------------------|--------------|
| Confirmed | 3+ independent, reliable sources agree |
| High | 2 reliable sources, consistent details |
| Medium | Single reliable source |
| Low | Unverified single source |
| Conflicting | Sources disagree, note the conflict |

Independence means sources did not derive information from each other. Wire services and outlets that pick up stories are not independent of the original source.
