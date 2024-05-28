from tkinter import *

def submit_data():
  # Get the data from the entry field
  data = entry.get()
  # Process the data (replace with your logic)
  print("You entered:", data)

# Create the main window
window = Tk()
window.title("Input Form")
window.grid_columnconfigure(0, weight=1, minsize=75)
window.grid_columnconfigure(1, weight=1, minsize=200)

# Article Frame
frm_article = Frame(master=window, padx=10, pady=5)

# Article Title Frame
frm_article_title = Frame(master=frm_article, pady=10)
  # Title label and entry
lbl_title = Label(master=frm_article_title, text="Enter article title:")
ent_title = Entry(master=frm_article_title, width=50)

# Article Body Frame
frm_article_body = Frame(master=frm_article, pady=10)
  # Body label and text box
lbl_body = Label(master=frm_article_body, text="Enter article body:")
txt_body = Text(master=frm_article_body, width=70, height=20)

# Article Body Frame
frm_article_intro = Frame(master=frm_article, pady=10)
  # Body label and text box
lbl_intro = Label(master=frm_article_intro, text="Enter article intro:")
txt_intro = Text(master=frm_article_intro, width=70, height=10)

# Positioning
frm_article.grid(row=0, column=0, padx=10, pady=5)
lbl_title.grid(row=0, column=0, sticky='w')
ent_title.grid(row=1, column=0)
lbl_body.grid(row=2, column=0, sticky='w')
txt_body.grid(row=3, column=0)
lbl_intro.grid(row=4, column=0, sticky='w')
txt_intro.grid(row=5, column=0)

frm_article_title.pack(fill=BOTH, expand=True)
frm_article_body.pack(fill=BOTH, expand=True)
frm_article_intro.pack(fill=BOTH, expand=True)

# Extras Frame
frm_extras = Frame(master=window)
frm_extras.grid(row=0, column=1, padx=10, pady=5)

# Article Title Frame
frm_extra_title = Frame(master=frm_extras, height=2, width=50)
  # Title label and entry
lbl_title2 = Label(master=frm_extra_title, text="Enter extra title:")
lbl_title2.grid(row=0, column=1)

ent_title2 = Entry(master=frm_extra_title)
ent_title2.grid(row=1, column=1)

frm_extra_title.pack(fill=BOTH, expand=True)

# Create the submit button
btn_submit = Button(window, text="Submit", command=submit_data)
btn_submit.grid(row=10, column=0, columnspan=2, pady=10)

# Run the main loop
window.mainloop()
