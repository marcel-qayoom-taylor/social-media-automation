# TO RUN PROGRAM

# 1. Open terminal
# 2. Run the following command: python main.py
# 3. Fill in the required fields
# 4. Click the "Submit" button
# 5. Run python 'py test_runner.py'
# 6. Check the output of the tests and do manual entry where needed

# TO-DO

# Check why facebook didn't run last time
# Check facebook flow
# Find a way to announce next human step when hitting page.pause()
# Find a way to communicate next planned action of the program to the user
# Add a way to have confirmation of what platforms have been completed
# Ensure linkedin_article_link is being saved and used in other platforms
# Get reposting to work
# Try get Medium to work
# Add bold and italics to to disclaimer
# Automatically set default paragraph spacing for body content in post data



import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
import json
import subprocess

# Fonts
font_heading = ("Arial", 13, "bold")
font_subheading = ("Arial", 10, "bold")

image_path = ""  # Global variable to store the image path
static_data = {} # Global variable to store the static data

try:
    with open('./config.json', 'r') as file:
        config = json.load(file)
        print("Config loaded: ", config)
except FileNotFoundError:
    print("config.json file not found.")
    config = {}  # Initialize an empty config if file doesn't exist
except json.JSONDecodeError:
    print("Error decoding JSON from config.json.")
    config = {}  # Initialize an empty config if there's a JSON decoding error


def load_static_data_from_json():
    try:
        with open('staticData.json', 'r') as file:
            rawData = json.load(file)
            data = {}
            data['tags'] = rawData.get('tags', [])
            data['general_disclaimer'] = rawData.get('general_disclaimer', "")
            data['historic_disclaimer'] = rawData.get('historic_disclaimer', "")
            return data
    except FileNotFoundError:
        print("staticData.json file not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from staticData.json.")
        return []

def update_char_count(*args):
    char_count = 280 - len(txt_twt_desc.get("1.0", "end-1c"))
    lbl_char_count.config(text=f"{char_count} characters remaining")

def imageUploader():
    global image_path
    fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    path = filedialog.askopenfilename(filetypes=fileTypes)
    # if file is selected
    if path:
        print('found path: ', path)
        image_path = path  # Store the path in the global variable
        lbl_image_path.config(text=f"Image path: {path}")
    else:
        print("No file is chosen !! Please choose a file.")

def submit_data():
    global image_path
    global static_data
    # Get the tags as a list
    tags = [tag.strip() for tag in txt_tags.get("1.0", END).strip().split(',')]
    
    # Prepare disclaimers list
    disclaimers = []
    if useGeneralDisclaimer.get():
        disclaimers.append(static_data['general_disclaimer'])
    if useHistoricDisclaimer.get():
        disclaimers.append(static_data['historic_disclaimer'])
    
    # Load existing config
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {}

    # Update only the postingPlatforms section
    if 'postingPlatforms' not in config:
        config['postingPlatforms'] = {}
    
    config['postingPlatforms'] = {
        "mailchimp": {"enabled": postToMailchimp.get()},
        "linkedIn": {"enabled": postToLinkedIn.get()},
        "facebook": {"enabled": postToFacebook.get()},
        "instagram": {"enabled": postToInstagram.get()},
        "squarespace": {"enabled": postToSquarespace.get()},
        "twitter": {"enabled": postToTwitter.get()}
    }

    # Write updated config back to file
    try:
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        print("Config successfully written to config.json")
    except Exception as e:
        print(f"An error occurred while writing to config.json: {e}")
    
    # Structure the data for postData.json
    data = {
        "article": {
            "title": ent_title.get(),
            "body": txt_body.get("1.0", END).strip(),
            "intro": txt_intro.get("1.0", END).strip(),
            "image_path": image_path,
            "tags": tags,
            "disclaimers": disclaimers,
            "twitter_post": txt_twt_desc.get("1.0", END).strip(),
            "linkedin_article_link": "",
            "linkedin_post_link": "",
            "facebook_post_link": ""
        }
    }    

    # Write the data to postData.json
    try:
        with open("postData.json", "w") as json_file:
            json.dump(data, json_file, indent=2)
        print("Data successfully written to postData.json")
    except Exception as e:
        print(f"An error occurred while writing to postData.json: {e}")

    # Print the data for verification
    print("Submitted data:", json.dumps(data, indent=2))

    # Run the test_runner.py script
    try:
        subprocess.run(['py', 'test_runner.py'], check=True)
        print("test_runner.py executed successfully")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running test_runner.py: {e}")
    except FileNotFoundError:
        print("test_runner.py not found. Make sure it's in the same directory as this script.")

    
static_data = load_static_data_from_json()

# Create the main window
window = ttk.Window(themename="superhero")
window.title("Social Media Poster")
window.grid_columnconfigure(0, weight=1, minsize=200)
window.grid_columnconfigure(1, weight=1, minsize=200)

style = ttk.Style()
style.configure("Heading.TLabel", font=("Verdana", 16, "bold"))
style.configure("TLabel", font=("Verdana", 10))


# Article Frame -------------------------------------------------------------
frm_article = ttk.Frame(window, padding=20, borderwidth=1, relief="solid")
lbl_article_frame_title = ttk.Label(frm_article, text="Article Details", style="Heading.TLabel")

# Title label and entry
lbl_title = ttk.Label(frm_article, text="Enter article title:", style="TLabel")
ent_title = ttk.Entry(frm_article, width=50, style="TEntry")

# Body label and text box
lbl_body = ttk.Label(frm_article, text="Enter article body:", style="TLabel")
txt_body = ttk.Text(frm_article, width=70, height=20, wrap="word")

# Body label and text box
lbl_intro = ttk.Label(frm_article, text="Enter article intro:", style="TLabel")
txt_intro = ttk.Text(frm_article, width=70, height=10, wrap="word")

# Disclaimer checkboxes
frm_disclaimers = ttk.Frame(frm_article, padding=5)
useGeneralDisclaimer = ttk.BooleanVar(value=True)
useHistoricDisclaimer = ttk.BooleanVar(value=False)
chk_general_disclaimer = ttk.Checkbutton(frm_disclaimers, text="Include general disclaimer", onvalue=True, offvalue=False, variable=useGeneralDisclaimer)
chk_historic_disclaimer = ttk.Checkbutton(frm_disclaimers, text="Include historic disclaimer", onvalue=True, offvalue=False, variable=useHistoricDisclaimer)

# Tags label and entry
lbl_tags = ttk.Label(frm_article, text="Enter tags (seperated by commas):", style="TLabel")
txt_tags = ttk.Text(frm_article, width=70, height=1, wrap="word")

txt_tags.insert(0.0, ", ".join(static_data['tags'])) # Prefill the text input field

# Add image
lbl_image = ttk.Label(frm_article, text="Add an image", style="TLabel")
lbl_image_path = ttk.Label(frm_article, text="Image path: ")
btn_image = ttk.Button(frm_article, text="Upload Image", command=imageUploader, style="TButton")

# Positioning
frm_article.grid(row=0, column=0, padx=10, pady=5, sticky='n')
lbl_article_frame_title.grid(row=0, column=0, sticky='w', pady=5)
lbl_title.grid(row=1, column=0, sticky='w', pady=5)
ent_title.grid(row=2, column=0, sticky='w', pady=5)
lbl_body.grid(row=3, column=0, sticky='w', pady=5)
txt_body.grid(row=4, column=0, sticky='w', pady=5)
lbl_intro.grid(row=5, column=0, sticky='w', pady=5)
txt_intro.grid(row=6, column=0, sticky='w', pady=5)
frm_disclaimers.grid(row=7, column=0, sticky='w')
chk_general_disclaimer.grid(row=0, column=0, sticky='w')
chk_historic_disclaimer.grid(row=0, column=1, sticky='w', padx=5)
lbl_tags.grid(row=8, column=0, sticky='w', pady=5)
txt_tags.grid(row=9, column=0, sticky='w', pady=5)
lbl_image.grid(row=10, column=0, sticky='w', pady=5)
lbl_image_path.grid(row=11, column=0, sticky='w', pady=5)
btn_image.grid(row=12, column=0, sticky='w', pady=5)
# End of Article Frame -------------------------------------------------------------
# Extras Frame ---------------------------------------------------------------------
frm_extras = ttk.Frame(window, padding=20, borderwidth=1, relief="solid")
lbl_extras_frame_title = ttk.Label(frm_extras, text="Extra Details", style="Heading.TLabel")

# Twitter description
frm_twitter = ttk.Frame(frm_extras, padding=5)

lbl_twt_desc = ttk.Label(frm_twitter, text="Enter Twitter description:", style="TLabel")
txt_twt_desc = ttk.Text(frm_twitter, width=70, height=6, wrap="word")
txt_twt_desc.bind("<KeyRelease>", update_char_count)

# Character count label
lbl_char_count = ttk.Label(frm_twitter, text="280 chars remaining", style="TLabel")

# Platforms
lbl_platforms = ttk.Label(frm_extras, text="Post to:", style="Heading.TLabel")

frm_platforms = ttk.Frame(frm_extras, padding=5)
postToLinkedIn = ttk.BooleanVar(value=True)
postToFacebook = ttk.BooleanVar(value=True)
postToInstagram = ttk.BooleanVar(value=True)
postToSquarespace = ttk.BooleanVar(value=True)
postToTwitter = ttk.BooleanVar(value=True)
postToMailchimp = ttk.BooleanVar(value=True)  # New variable for Mailchimp

chk_mailchimp = ttk.Checkbutton(frm_platforms, text="Mailchimp", onvalue=True, offvalue=False, variable=postToMailchimp)  # New checkbox for Mailchimp
chk_linkedin = ttk.Checkbutton(frm_platforms, text="LinkedIn", onvalue=True, offvalue=False, variable=postToLinkedIn)
chk_facebook = ttk.Checkbutton(frm_platforms, text="Facebook", onvalue=True, offvalue=False, variable=postToFacebook)
chk_instagram = ttk.Checkbutton(frm_platforms, text="Instagram", onvalue=True, offvalue=False, variable=postToInstagram)
chk_squarespace = ttk.Checkbutton(frm_platforms, text="Squarespace", onvalue=True, offvalue=False, variable=postToSquarespace)
chk_twitter = ttk.Checkbutton(frm_platforms, text="Twitter", onvalue=True, offvalue=False, variable=postToTwitter)

# Positioning
frm_extras.grid(row=0, column=1, padx=10, pady=5, sticky='n')

lbl_extras_frame_title.grid(row=0, column=0, sticky='w', pady=5)
frm_twitter.grid(row=1, column=0, sticky='w', pady=5)
lbl_twt_desc.grid(row=0, column=0, sticky='w', pady=5)
txt_twt_desc.grid(row=1, column=0, sticky='w', pady=5)
lbl_char_count.grid(row=2, column=0, sticky='w', pady=5, padx=5)

lbl_platforms.grid(row=3, column=0, sticky='w', pady=5)
frm_platforms.grid(row=4, column=0, sticky='w', pady=5)
chk_mailchimp.grid(row=0, column=0, sticky='w', padx=(0,5))
chk_linkedin.grid(row=0, column=1, sticky='w', padx=(0,5))
chk_facebook.grid(row=0, column=2, sticky='w', padx=(0,5))
chk_instagram.grid(row=0, column=3, sticky='w', padx=(0,5))
chk_squarespace.grid(row=0, column=4, sticky='w', padx=(0,5))
chk_twitter.grid(row=0, column=5, sticky='w', padx=(0,5))

# End of Extras Frame ---------------------------------------------------------------------

# Create the submit button
btn_submit = ttk.Button(window, text="Submit", command=submit_data, style="TButton")
btn_submit.grid(row=10, column=0, columnspan=2, pady=10)

# Add some padding to the main window
window.geometry("1100x1000")  # Set a fixed size for the window
#window["padding"] = (20, 20)  # Add padding to the main window

# Adjust the grid layout
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
frm_article.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
frm_extras.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

# Run the main loop
window.mainloop()

