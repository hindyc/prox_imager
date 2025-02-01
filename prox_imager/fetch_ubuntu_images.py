'''Fetches Ubuntu cloud images metadata and extracts relevant image URLs.'''
import argparse
import json
import logging
import os
import requests
import toml


# Configure logging
log = logging.getLogger(__name__)


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


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Fetch and save Ubuntu cloud images metadata.")
    parser.add_argument("-c", "--config",
                        default="./etc/config.toml",
                        help="Path to the configuration file.")
    return parser.parse_args()


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


def extract_image_data(metadata: dict) -> dict:
    """Extracts image details from the fetched JSON data."""
    images = {}

    for product, details in metadata.get("products", {}).items():
        release = details.get("release", "unknown")
        arch = details.get("arch", "unknown")
        version = details.get("version", "unknown")

        # Get the download and checksum URLs
        image_url = details.get("url")
        sha256_url = details.get("sha256")

        if image_url and sha256_url:
            images[product] = {
                "release": release,
                "arch": arch,
                "version": version,
                "image_url": image_url,
                "sha256_url": sha256_url
            }

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

    ubuntu_json_url = config['urls']['ubuntu_json_url']
    output_file = config['files']['output_file']
    metadata = fetch_ubuntu_metadata(ubuntu_json_url)
    if not metadata:
        return

    image_data = extract_image_data(metadata)
    save_metadata(image_data, output_file)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
