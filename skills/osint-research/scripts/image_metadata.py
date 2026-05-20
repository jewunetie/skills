#!/usr/bin/env python3
"""
Image metadata extraction for OSINT research.
Extracts EXIF data including camera info, timestamps, and GPS coordinates.
Requires: pip install exifread (add --break-system-packages if needed)

Usage:
    python image_metadata.py <image_path_or_url> [--json]
    
Examples:
    python image_metadata.py photo.jpg
    python image_metadata.py /path/to/image.jpg --json
    python image_metadata.py https://example.com/photo.jpg
    
GPS coordinates are converted to decimal format with Google Maps links.
"""

import json
import sys
import io
import urllib.request
from pathlib import Path
from typing import Optional, Union

# Check for exifread dependency
try:
    import exifread
except ImportError:
    print("Error: exifread library required")
    print("Install with: pip install exifread --break-system-packages")
    sys.exit(1)


def dms_to_decimal(dms_values, ref: str) -> Optional[float]:
    """
    Convert GPS coordinates from degrees/minutes/seconds to decimal degrees.
    
    Args:
        dms_values: List of exifread Ratio values [degrees, minutes, seconds]
        ref: Reference direction ('N', 'S', 'E', 'W')
    
    Returns:
        Decimal degrees (negative for S/W)
    """
    try:
        d = float(dms_values[0].num) / float(dms_values[0].den)
        m = float(dms_values[1].num) / float(dms_values[1].den)
        s = float(dms_values[2].num) / float(dms_values[2].den)
        
        decimal = d + m / 60 + s / 3600
        
        if ref.upper() in ["S", "W"]:
            decimal = -decimal
        
        return round(decimal, 6)
    except (AttributeError, ZeroDivisionError, IndexError):
        return None


def extract_metadata(source: Union[str, Path]) -> dict:
    """
    Extract EXIF metadata from an image file or URL.
    
    Args:
        source: File path or URL to image
        
    Returns:
        Dictionary with structured metadata
    """
    result = {
        "source": str(source),
        "camera": {},
        "capture": {},
        "gps": {},
        "software": {},
        "raw_tags": {}
    }
    
    data = None
    try:
        # Handle URL vs file path
        if str(source).startswith(("http://", "https://")):
            req = urllib.request.Request(
                str(source), 
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                data = io.BytesIO(response.read())
                result["source_type"] = "url"
        else:
            path = Path(source)
            if not path.exists():
                return {"source": str(source), "error": f"File not found: {source}"}
            data = open(path, "rb")
            result["source_type"] = "file"
            result["filename"] = path.name
        
        # Extract EXIF tags
        tags = exifread.process_file(data, details=False)
        
        if not tags:
            result["warning"] = "No EXIF data found (may have been stripped)"
            return result
        
        # Camera information
        camera_tags = {
            "Image Make": "make",
            "Image Model": "model",
            "EXIF LensModel": "lens",
            "EXIF LensMake": "lens_make",
            "Image ImageDescription": "description"
        }
        for tag, key in camera_tags.items():
            if tag in tags:
                result["camera"][key] = str(tags[tag])
        
        # Capture settings
        capture_tags = {
            "EXIF DateTimeOriginal": "datetime_original",
            "EXIF DateTimeDigitized": "datetime_digitized",
            "Image DateTime": "datetime_modified",
            "EXIF ExposureTime": "exposure",
            "EXIF FNumber": "aperture",
            "EXIF ISOSpeedRatings": "iso",
            "EXIF FocalLength": "focal_length",
            "EXIF Flash": "flash",
            "EXIF WhiteBalance": "white_balance",
            "EXIF ExposureProgram": "exposure_program",
            "EXIF MeteringMode": "metering_mode",
            "Image Orientation": "orientation",
            "EXIF ExifImageWidth": "width",
            "EXIF ExifImageLength": "height"
        }
        for tag, key in capture_tags.items():
            if tag in tags:
                value = str(tags[tag])
                # Clean up aperture display
                if key == "aperture" and "/" in value:
                    try:
                        num, den = value.split("/")
                        value = f"f/{float(num)/float(den):.1f}"
                    except:
                        pass
                result["capture"][key] = value
        
        # GPS data
        gps_lat = tags.get("GPS GPSLatitude")
        gps_lat_ref = tags.get("GPS GPSLatitudeRef")
        gps_lon = tags.get("GPS GPSLongitude")
        gps_lon_ref = tags.get("GPS GPSLongitudeRef")
        
        if gps_lat and gps_lat_ref:
            lat = dms_to_decimal(gps_lat.values, str(gps_lat_ref))
            if lat is not None:
                result["gps"]["latitude"] = lat
                result["gps"]["latitude_ref"] = str(gps_lat_ref)
        
        if gps_lon and gps_lon_ref:
            lon = dms_to_decimal(gps_lon.values, str(gps_lon_ref))
            if lon is not None:
                result["gps"]["longitude"] = lon
                result["gps"]["longitude_ref"] = str(gps_lon_ref)
        
        # Generate map links if we have coordinates
        if result["gps"].get("latitude") and result["gps"].get("longitude"):
            lat = result["gps"]["latitude"]
            lon = result["gps"]["longitude"]
            result["gps"]["google_maps"] = f"https://maps.google.com/?q={lat},{lon}"
            result["gps"]["openstreetmap"] = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=15"
        
        # Additional GPS info
        gps_extra = {
            "GPS GPSAltitude": "altitude",
            "GPS GPSTimeStamp": "timestamp",
            "GPS GPSDateStamp": "datestamp",
            "GPS GPSImgDirection": "direction"
        }
        for tag, key in gps_extra.items():
            if tag in tags:
                result["gps"][key] = str(tags[tag])
        
        # Software/processing info
        software_tags = {
            "Image Software": "software",
            "Image ProcessingSoftware": "processing_software",
            "EXIF ColorSpace": "color_space",
            "Image Copyright": "copyright",
            "Image Artist": "artist"
        }
        for tag, key in software_tags.items():
            if tag in tags:
                result["software"][key] = str(tags[tag])
        
        # Store all raw tags (excluding thumbnails)
        for tag, value in tags.items():
            if tag not in ("JPEGThumbnail", "TIFFThumbnail"):
                result["raw_tags"][tag] = str(value)
        
        # Clean up empty sections
        result = {k: v for k, v in result.items() if v or k in ["source", "source_type"]}
        
        return result
        
    except urllib.error.HTTPError as e:
        return {"source": str(source), "error": f"HTTP error: {e.code}"}
    except urllib.error.URLError as e:
        return {"source": str(source), "error": f"URL error: {e.reason}"}
    except Exception as e:
        return {"source": str(source), "error": str(e)}
    finally:
        if data is not None and hasattr(data, "close"):
            data.close()


def print_results(results: dict, as_json: bool = False):
    """Print results in human-readable or JSON format."""
    if as_json:
        print(json.dumps(results, indent=2))
        return
    
    source = results.get("source", "Unknown")
    
    print(f"\n{'='*60}")
    print(f"Image Metadata: {source}")
    print(f"{'='*60}")
    
    if "error" in results:
        print(f"\nError: {results['error']}")
        return
    
    if "warning" in results:
        print(f"\nWarning: {results['warning']}")
        return
    
    # Camera info
    camera = results.get("camera", {})
    if camera:
        print(f"\n[Camera]")
        if camera.get("make") or camera.get("model"):
            print(f"  Device: {camera.get('make', '')} {camera.get('model', '')}".strip())
        if camera.get("lens"):
            print(f"  Lens: {camera.get('lens')}")
    
    # Capture settings
    capture = results.get("capture", {})
    if capture:
        print(f"\n[Capture Settings]")
        if capture.get("datetime_original"):
            print(f"  Date/Time: {capture['datetime_original']}")
        settings = []
        if capture.get("exposure"):
            settings.append(f"{capture['exposure']}s")
        if capture.get("aperture"):
            settings.append(capture["aperture"])
        if capture.get("iso"):
            settings.append(f"ISO {capture['iso']}")
        if capture.get("focal_length"):
            settings.append(f"{capture['focal_length']}mm")
        if settings:
            print(f"  Settings: {', '.join(settings)}")
        if capture.get("width") and capture.get("height"):
            print(f"  Dimensions: {capture['width']} x {capture['height']}")
    
    # GPS
    gps = results.get("gps", {})
    if gps:
        print(f"\n[GPS Location]")
        if gps.get("latitude") and gps.get("longitude"):
            print(f"  Coordinates: {gps['latitude']}, {gps['longitude']}")
            if gps.get("altitude"):
                print(f"  Altitude: {gps['altitude']}")
            if gps.get("google_maps"):
                print(f"  Google Maps: {gps['google_maps']}")
            if gps.get("openstreetmap"):
                print(f"  OpenStreetMap: {gps['openstreetmap']}")
    
    # Software
    software = results.get("software", {})
    if software:
        print(f"\n[Software/Attribution]")
        for key, value in software.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Summary stats
    raw_tags = results.get("raw_tags", {})
    if raw_tags:
        print(f"\n[Summary]")
        print(f"  Total EXIF tags: {len(raw_tags)}")
    
    print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    source = sys.argv[1]
    as_json = "--json" in sys.argv
    
    results = extract_metadata(source)
    print_results(results, as_json)


if __name__ == "__main__":
    main()
