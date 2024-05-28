from tkinter import *

# Fonts
font_heading = ("Arial", 13, "bold")
font_subheading = ("Arial", 10)

def update_char_count(*args):
    print("text changed")
    char_count = 280 - len(txt_twt_desc.get("1.0", "end-1c"))
    lbl_char_count.config(text=f"{char_count} characters remaining")

def submit_data():
  # Get the data from the entry field
  data = entry.get()
  # Process the data (replace with your logic)
  print("You entered:", data)

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

# Positioning
frm_extras.grid(row=0, column=1, padx=10, pady=5, sticky='n')
lbl_extras_frame_title.grid(row=0, column=1, sticky='w', pady=5)
frm_twitter.grid(row=1, column=1, sticky='w', pady=5)
lbl_twt_desc.grid(row=0, column=0, sticky='w', pady=5)
txt_twt_desc.grid(row=1, column=0, sticky='w', pady=5)
lbl_char_count.grid(row=1, column=1, sticky='w', pady=5, padx=5)
# End of Extras Frame ---------------------------------------------------------------------

# Create the submit button
btn_submit = Button(window, text="Submit", command=submit_data)
btn_submit.grid(row=10, column=0, columnspan=2, pady=10)

# Run the main loop
window.mainloop()
