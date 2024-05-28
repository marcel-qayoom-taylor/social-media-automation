from tkinter import *

def submit_data():
  # Get the data from the entry field
  data = entry.get()
  # Process the data (replace with your logic)
  print("You entered:", data)

# Create the main window
window = Tk()
window.title("Input Form")
window.grid_columnconfigure(2, weight=1, minsize=75)

# Article Frame
frm_article = Frame(master=window)
frm_article.grid(row=0, column=0, padx=10, pady=5)

# Article Title Frame
frm_article_title = Frame(master=frm_article, height=2, width=50)
  # Title label and entry
lbl_title = Label(master=frm_article_title, text="Enter article title:").pack()
ent_title = Entry(master=frm_article_title)
ent_title.pack()

frm_article_title.pack(fill=BOTH, expand=True)

# Article Body Frame
frm_article_body = Frame(master=frm_article, height=5, width=50)
  # Body label and text box
lbl_body = Label(master=frm_article_body, text="Enter article body:").pack()
txt_body = Text(master=frm_article_body)
txt_body.pack()

frm_article_body.pack(fill=BOTH, expand=True)

# Article Body Frame
frm_article_intro = Frame(master=frm_article, height=5, width=50)
  # Body label and text box
lbl_intro = Label(master=frm_article_intro, text="Enter article intro:").pack()
txt_intro = Text(master=frm_article_intro)
txt_intro.pack()

frm_article_intro.pack(fill=BOTH, expand=True)

# Create the submit button
btn_submit = Button(frm_article, text="Submit", command=submit_data).pack()


frm_extras = Frame(master=window, bg="blue")
frm_extras.grid(row=0, column=1, padx=10, pady=5)

# Article Title Frame
frm_extra_title = Frame(master=frm_extras, height=2, width=50)
  # Title label and entry
lbl_title2 = Label(master=frm_extra_title, text="Enter extra title:")
lbl_title2.grid(row=0, column=1)

ent_title2 = Entry(master=frm_extra_title)
ent_title2.grid(row=1, column=1)

label2 = Label(text="B")
label2.grid(row=3, column=2)

# Run the main loop
window.mainloop()
