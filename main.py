from tkinter import *

def submit_data():
  # Get the data from the entry field
  data = entry.get()
  # Process the data (replace with your logic)
  print("You entered:", data)

# Create the main window
window = Tk()
window.title("Input Form")

# Create the label and entry widget
label = Label(window, text="Enter your data:")
label.pack()

entry = Entry(window)
entry.pack()

# Create the submit button
submit_button = Button(window, text="Submit", command=submit_data)
submit_button.pack()

# Run the main loop
window.mainloop()
