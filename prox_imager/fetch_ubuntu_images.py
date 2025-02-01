'''Fetches Ubuntu cloud images metadata and extracts relevant image URLs.'''
import argparse
import json
import requests
import toml


def load_config(config_path: str) -> dict:
    """Loads configuration from a TOML file."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return toml.load(f)
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        return {}
    except PermissionError:
        print(f"❌ Permission denied to open configuration file: {config_path}")
        return {}
    except toml.TomlDecodeError:
        print(f"❌ Failed to decode TOML file: {config_path}")
        return {}
    except IOError as e:
        print(f"❌ Failed to open configuration file: {config_path} - {e.errno}: {e.strerror}")
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
    return_content = {}
    print(f"fetching metadata from {ubuntu_json_url}...")
    response = requests.get(ubuntu_json_url, timeout=10)
    if response.status_code != 200:
        print("❌ Failed to fetch metadata!")
    else:
        return_content = response.json()
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
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    print(f"✅ Saved metadata to {output_file}")


def main():
    '''Main entry point of the script.'''
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
    main()
