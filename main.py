from tkinter import *
from tkinter import Label
from tkinter import filedialog
import json

# Fonts
font_heading = ("Arial", 13, "bold")
font_subheading = ("Arial", 10, "bold")

image_path = ""  # Global variable to store the image path
static_data = {} # Global variable to store the static data

with open('./config.json', 'r') as file:
    try: 
        config = json.load(file)
        print("Config loaded: ", config)
    except FileNotFoundError:
        print("staticData.json file not found.")

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

# image uploader function
# def imageUploader():
#     fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
#     path = filedialog.askopenfilename(filetypes=fileTypes)
#     # if file is selected
#     if len(path):
#       print('found path: ', path)
#       lbl_image_path = Label(frm_article, text="Image path: Not selected", font=font_subheading)
#       lbl_image_path.grid(row=12, column=0, sticky='w', pady=5)
#       lbl_image_path.insert(text="Image path")
#     else:
#         print("No file is chosen !! Please choose a file.")

def update_char_count(*args):
    print("text changed")
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
        disclaimers.append(static_data['general_disclaimer'])  # Replace with your actual general disclaimer text
    if useHistoricDisclaimer.get():
        disclaimers.append(static_data['historic_disclaimer'])  # Replace with your actual historic disclaimer text

    # Structure the data
    data = {
        "article": {
            "title": ent_title.get(),
            "body": txt_body.get("1.0", END).strip(),
            "intro": txt_intro.get("1.0", END).strip(),
            "image_path": image_path,
            "tags": tags,
            "disclaimers": disclaimers,
            "linkedin_article_link": "",
            "linkedin_post_link": "",
            "facebook_post_link": ""
        }
    }    

    # Write the data to a JSON file
    try:
        with open("postData.json", "w") as json_file:
            json.dump(data, json_file, indent=2)
        print("Data successfully written to postData.json")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

    # Print the data for verification
    print("Submitted data:", json.dumps(data, indent=2))
    
static_data = load_static_data_from_json()

# Create the main window
window = Tk()
window.title("Social Media Poster")
window.grid_columnconfigure(0, weight=1, minsize=200)
window.grid_columnconfigure(1, weight=1, minsize=200)

# Article Frame -------------------------------------------------------------
frm_article = Frame(window, padx=10, pady=5)
lbl_article_frame_title = Label(frm_article, text="Article Details", font=font_heading)

# Title label and entry
lbl_title = Label(frm_article, text="Enter article title:", font=font_subheading)
ent_title = Entry(frm_article, width=50)

# Body label and text box
lbl_body = Label(frm_article, text="Enter article body:", font=font_subheading)
txt_body = Text(frm_article, width=70, height=20)

# Body label and text box
lbl_intro = Label(frm_article, text="Enter article intro:", font=font_subheading)
txt_intro = Text(frm_article, width=70, height=10)

# Disclaimer checkboxes
frm_disclaimers = Frame(frm_article, pady=5)
useGeneralDisclaimer = BooleanVar(value=True)
useHistoricDisclaimer = BooleanVar(value=False)
chk_general_disclaimer = Checkbutton(frm_disclaimers, text="Include general disclaimer", onvalue=True, offvalue=False, variable=useGeneralDisclaimer)
chk_historic_disclaimer = Checkbutton(frm_disclaimers, text="Include historic disclaimer", onvalue=True, offvalue=False, variable=useHistoricDisclaimer)

# Tags label and entry
lbl_tags = Label(frm_article, text="Enter tags (seperated by commas):", font=font_subheading)
txt_tags = Text(frm_article, width=70, height=1)

txt_tags.insert(0.0, ", ".join(static_data['tags'])) # Prefill the text input field

# Add image
lbl_image = Label(frm_article, text="Add an image", font=font_subheading)
lbl_image_path = Label(frm_article, text="Image path: ")
btn_image = Button(frm_article, text="Upload Image", command=imageUploader)

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
chk_historic_disclaimer.grid(row=0, column=1, sticky='w')
lbl_tags.grid(row=8, column=0, sticky='w', pady=5)
txt_tags.grid(row=9, column=0, sticky='w', pady=5)
lbl_image.grid(row=10, column=0, sticky='w', pady=5)
lbl_image_path.grid(row=11, column=0, sticky='w', pady=5)
btn_image.grid(row=12, column=0, sticky='w', pady=5)
# End of Article Frame -------------------------------------------------------------
# Extras Frame ---------------------------------------------------------------------
frm_extras = Frame(window, padx=10, pady=5)
lbl_extras_frame_title = Label(frm_extras, text="Extra Details", font=font_heading)

# Twitter description
frm_twitter = Frame(frm_extras, pady=5)

lbl_twt_desc = Label(frm_twitter, text="Enter Twitter description:", font=font_subheading)
txt_twt_desc = Text(frm_twitter, width=70, height=6)
txt_twt_desc.bind("<KeyRelease>", update_char_count)

# Character count label
lbl_char_count = Label(frm_twitter, text="280 chars remaining", font=font_subheading)

# Platforms
lbl_platforms = Label(frm_extras, text="Post to:", font=font_heading)

frm_platforms = Frame(frm_extras, pady=5)
postToLinkedIn = BooleanVar(value=True)
postToFacebook = BooleanVar(value=True)
postToInstagram = BooleanVar(value=True)
postToSquarespace = BooleanVar(value=True)
postToTwitter = BooleanVar(value=True)

chk_linkedin = Checkbutton(frm_platforms, text="LinkedIn", onvalue=True, offvalue=False, variable=postToLinkedIn)
chk_facebook = Checkbutton(frm_platforms, text="Facebook", onvalue=True, offvalue=False, variable=postToFacebook)
chk_instagram = Checkbutton(frm_platforms, text="Instagram", onvalue=True, offvalue=False, variable=postToInstagram)
chk_squarespace = Checkbutton(frm_platforms, text="Squarespace", onvalue=True, offvalue=False, variable=postToSquarespace)
chk_twitter = Checkbutton(frm_platforms, text="Twitter", onvalue=True, offvalue=False, variable=postToTwitter)

# Positioning
frm_extras.grid(row=0, column=1, padx=10, pady=5, sticky='n')
lbl_extras_frame_title.grid(row=0, column=0, sticky='w', pady=5)
frm_twitter.grid(row=1, column=0, sticky='w', pady=5)
lbl_twt_desc.grid(row=0, column=0, sticky='w', pady=5)
txt_twt_desc.grid(row=1, column=0, sticky='w', pady=5)
lbl_char_count.grid(row=2, column=0, sticky='w', pady=5, padx=5)

lbl_platforms.grid(row=3, column=0, sticky='w', pady=5)
frm_platforms.grid(row=4, column=0, sticky='w', pady=5)
chk_linkedin.grid(row=0, column=0, sticky='w', padx=(0,5))
chk_facebook.grid(row=0, column=1, sticky='w', padx=(0,5))
chk_instagram.grid(row=0, column=2, sticky='w', padx=(0,5))
chk_squarespace.grid(row=0, column=3, sticky='w', padx=(0,5))
chk_twitter.grid(row=0, column=4, sticky='w', padx=(0,5))

# End of Extras Frame ---------------------------------------------------------------------

# Create the submit button
btn_submit = Button(window, text="Submit", command=submit_data)
btn_submit.grid(row=10, column=0, columnspan=2, pady=10)

# Run the main loop
window.mainloop()
