'''Fetches Ubuntu cloud images metadata and extracts relevant image URLs.'''
import argparse
import json
import logging
import os
from typing import Callable

import requests
import toml


# Configure logging
log = logging.getLogger(__name__)


def lazy_ic_import() -> Callable:
    '''Import icecream only when needed.'''
    # global ic
    from icecream import ic  # pylint: disable=import-outside-toplevel
    ic.configureOutput(includeContext=True)
    ic.configureOutput(prefix='ic| ')
    return ic


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Fetch and save Ubuntu cloud images metadata.")
    parser.add_argument("-c", "--config",
                        default="./etc/config.toml",
                        help="Path to the configuration file.")
    return parser.parse_args()


def load_config(config_path: str) -> dict:
    """Loads configuration from a TOML file."""
    if not os.path.exists(config_path):
        log.error("❌ Configuration file not found: %s", config_path)
        return {}
    if not os.access(config_path, os.R_OK):
        log.error("❌ Permission denied to read configuration file: %s", config_path)
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return toml.load(f)
    except toml.TomlDecodeError:
        log.error("❌ Failed to decode TOML file: %s", config_path)
        return {}
    except IOError as e:
        log.error("❌ Failed to open configuration file: %s - %d: %s",
                  config_path, e.errno, e.strerror)
        return {}


def validate_config(config: dict) -> bool:
    """Validates the configuration file."""
    required_sections = ['image_urls', 'files']
    for section in required_sections:
        if section not in config:
            log.error("❌ Missing required section in configuration file: %s", section)
            return False
    return True


def fetch_ubuntu_metadata(ubuntu_json_url: str) -> dict:
    """Fetches Ubuntu cloud images metadata and extracts relevant image URLs."""
    log.info("Fetching metadata from %s...", ubuntu_json_url)
    try:
        response = requests.get(ubuntu_json_url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    except requests.RequestException as e:
        log.error("❌ An error occurred while fetching metadata: %s", e)
        return {}

    try:
        return_content = response.json()
    except ValueError as e:
        log.error("❌ Failed to parse JSON response: %s", e)
        return {}

    return return_content


def extract_image_data(metadata: dict, base_url) -> dict:
    """Extracts image details from the fetched JSON data."""
    images = {}

    for product, details in metadata.get("products", {}).items():
        if details.get("arch") != "amd64":
            continue  # Skip non-amd64 architectures
        release = details.get("release", "unknown")
        version = details.get("version", "unknown")
        versions = details.get("versions", {})

        if not versions:
            log.info("⚠️ Skipping %s: No available builds", product)
            continue

        latest_version = max(versions.keys())  # Find latest available build
        disk_data = versions[latest_version]["items"].get("disk1.img", {})

        if not disk_data:
            log.info("⚠️ Skipping %s: No disk1.img found", product)
            continue

        # Get the download and checksum URLs
        image_url = base_url + disk_data.get("path", "")
        sha256_hash = disk_data.get("sha256", "unknown")

        log.info("✅ Found %s %s %s %s %s",
                 product, release, version, latest_version, image_url)

        images[product] = {
            "release": release,
            "version": version,
            "build_date": latest_version,
            "image_url": image_url,
            "sha256": sha256_hash
        }

    log.info("✅ Extracted %s images", len(images))
    return images


def save_metadata(metadata: dict, output_file: str) -> None:
    """Saves extracted metadata to a local JSON file."""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)
        log.info("✅ Saved metadata to %s", output_file)
    except PermissionError:
        log.error("❌ Permission denied when trying to save metadata to %s", output_file)
    except IOError as e:
        errno = e.errno if e.errno is not None else "Unknown"
        strerror = e.strerror if e.strerror is not None else "Unknown error"
        log.error("❌ Failed to save metadata to %s - %s: %s", output_file, errno, strerror)
    except TypeError as e:
        log.error("❌ Failed to serialize metadata to JSON: %s", e)


def main():
    '''Main entry point of the script.'''
    log.info("Starting the script...")
    args = parse_args()
    config = load_config(args.config)
    if not config or not validate_config(config):
        return

    ubuntu_json_url = (config['image_urls']['ubuntu_base_url'] +
                       config['image_urls']['ubuntu_metadata_url'])
    output_file = config['files']['output_file']
    metadata = fetch_ubuntu_metadata(ubuntu_json_url)
    if not metadata:
        return

    image_data = extract_image_data(metadata,
                                    config['image_urls']['ubuntu_base_url'])
    save_metadata(image_data, output_file)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
