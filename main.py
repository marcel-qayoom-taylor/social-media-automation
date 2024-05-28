from tkinter import *

# Fonts
font_heading = ("Arial", 13, "bold")
font_subheading = ("Arial", 10, "")

def submit_data():
  # Get the data from the entry field
  data = entry.get()
  # Process the data (replace with your logic)
  print("You entered:", data)

# Create the main window
window = Tk()
window.title("Social Media Poster")
window.grid_columnconfigure(0, weight=1, minsize=75)
window.grid_columnconfigure(1, weight=1, minsize=200)

# Article Frame -------------------------------------------------------------
frm_article = Frame(master=window, padx=10, pady=5)
lbl_frame_title = Label(master=frm_article, text="Article Details", font=font_heading)

# Title label and entry
lbl_title = Label(master=frm_article, text="Enter article title:", font=font_subheading)
ent_title = Entry(master=frm_article, width=50)

# Body label and text box
lbl_body = Label(master=frm_article, text="Enter article body:", font=font_subheading)
txt_body = Text(master=frm_article, width=70, height=20)

# Body label and text box
lbl_intro = Label(master=frm_article, text="Enter article intro:", font=font_subheading)
txt_intro = Text(master=frm_article, width=70, height=10)

# Disclaimer checkboxes
frm_disclaimers = Frame(master=frm_article, pady=5)
useGeneralDisclaimer = BooleanVar(value=True)
useHistoricDisclaimer = BooleanVar(value=False)
chk_general_disclaimer = Checkbutton(master=frm_disclaimers, text="Include general disclaimer", onvalue=True, offvalue=False, variable=useGeneralDisclaimer)
chk_historic_disclaimer = Checkbutton(master=frm_disclaimers, text="Include historic disclaimer", onvalue=True, offvalue=False, variable=useHistoricDisclaimer)

# Positioning
frm_article.grid(row=0, column=0, padx=10, pady=5)
lbl_frame_title.grid(row=0, column=0, sticky='w', pady=5)
lbl_title.grid(row=1, column=0, sticky='w', pady=5)
ent_title.grid(row=2, column=0, sticky='w', pady=5)
lbl_body.grid(row=3, column=0, sticky='w', pady=5)
txt_body.grid(row=4, column=0, sticky='w', pady=5)
lbl_intro.grid(row=5, column=0, sticky='w', pady=5)
txt_intro.grid(row=6, column=0, sticky='w', pady=5)
frm_disclaimers.grid(row=7, column=0, sticky='w')
chk_general_disclaimer.grid(row=0, column=0, sticky='w')
chk_historic_disclaimer.grid(row=0, column=1, sticky='w')

# End of Article Frame -------------------------------------------------------------

# Extras Frame ---------------------------------------------------------------------
frm_extras = Frame(master=window)
frm_extras.grid(row=0, column=1, padx=10, pady=5)

# Title label and entry
lbl_title2 = Label(master=frm_extras, text="Enter extra title:")
lbl_title2.grid(row=0, column=1)

ent_title2 = Entry(master=frm_extras)
ent_title2.grid(row=1, column=1)
# End of Extras Frame ---------------------------------------------------------------------


# Create the submit button
btn_submit = Button(window, text="Submit", command=submit_data)
btn_submit.grid(row=10, column=0, columnspan=2, pady=10)

# Run the main loop
window.mainloop()
