import logging
import logging.config
import os
import yaml

def find_logging_config(filename='custom_logging.yaml'):
    # Define possible locations for the logging configuration file
    possible_locations = [
        os.getcwd(),  # Current working directory
        os.path.join(os.getcwd(), 'config'),  # config directory in current working directory
        os.path.expanduser('~'),  # User's home directory
        os.path.join(os.path.expanduser('~'), 'config'),  # config directory in user's home directory
    ]

    # Check each possible location for the configuration file
    for location in possible_locations:
        config_path = os.path.join(location, filename)
        print(f"Checking {config_path}")
        if os.path.exists(config_path):
            print(f"Found logging configuration at: {config_path}")
            return config_path

    return None
def setup_logging(default_path='custom_logging.yaml', default_level=logging.INFO):
    config_path = find_logging_config(default_path)

    if config_path:
        print(f"Loading logging configuration from: {config_path}")
        with open(config_path, 'rt') as f:
            config = yaml.safe_load(f.read())
        print(f"Loaded configuration: {config}")
        try:
            logging.config.dictConfig(config)
            print("Logging configured successfully.")
        except Exception as e:
            print(f"Error configuring logging: {e}")
            logging.basicConfig(level=default_level)
    else:
        print(f"Configuration file not found. Using default logging configuration.")
        logging.basicConfig(level=default_level)
