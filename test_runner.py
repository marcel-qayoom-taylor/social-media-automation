import json
import subprocess

# Read and parse the config.json file
try:
    with open('config.json', 'r') as file:
        config = json.load(file)
except FileNotFoundError:
    print("config.json file not found.")
    config = {"postingPlatforms": {}}
except json.JSONDecodeError:
    print("Error decoding JSON from config.json.")
    config = {"postingPlatforms": {}}

# Determine which platforms are enabled
enabled_platforms = [platform for platform, settings in config['postingPlatforms'].items() if settings['enabled']]

# Map platforms to test files
platform_tests = {
    'mailchimp': 'tests/PostMailchimpArticle.py',
    'linkedIn': 'tests/PostLinkedinArticle.py',
    'squarespace': 'tests/PostSquarespaceArticle.py',
    'medium': 'tests/PostMediumArticle.py',
    'facebook': 'tests/PostFacebookArticle.py',
    'instagram': 'tests/PostInstagramArticle.py',
    'twitter': 'tests/PostTwitterArticle.py',
}

# Filter the tests to run based on enabled platforms
tests_to_run = [platform_tests[platform] for platform in enabled_platforms if platform in platform_tests]

print("tests to run are: ", tests_to_run)

# Run the tests using pytest
if tests_to_run:
    test_command = ['pytest'] + tests_to_run
    result = subprocess.run(test_command, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
else:
    print('No platforms are enabled for testing.')