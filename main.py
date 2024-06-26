import tkinter as tk
import os
import functools


class NotesApp:
    def __init__(self, master):
        # Initialize the app
        self.master = master
        self.master.title("Notes App")
        self.master.geometry("400x200")  # Set initial window size
        # Initialize variables
        self.user_folder = None
        self.course_folder = None
        self.course_notes = []
        self.chapter_count = 1
        self.paragraph_count = 1
        # Create GUI elements
        self.create_gui_elements()

    def create_gui_elements(self):
        # Create GUI elements
        self.create_labels_and_entries()
        self.create_buttons()

    def create_labels_and_entries(self):
        # Create labels and entry for username
        self.welcome_label = tk.Label(self.master, text="Notes App!", font=("Helvetica", 20))
        self.welcome_label.pack(pady=(20, 0))  # Push the welcome label down
        self.username_prompt_label = tk.Label(self.master, text="Enter username to view folders:")
        self.username_prompt_label.pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack(pady=30)

    def create_buttons(self):
        # Create buttons for New and Load
        button_frame = tk.Frame(self.master)
        button_frame.pack()
        self.new_button = tk.Button(button_frame, text="New", command=self.create_username)
        self.new_button.pack(side=tk.LEFT, padx=5)
        self.load_button = tk.Button(button_frame, text="Load", command=self.load_folders)
        self.load_button.pack(side=tk.LEFT, padx=5)

    def create_username(self):
        # Create a username and proceed to create a new course
        username = self.username_entry.get()
        if username:
            self.user_folder = f"User_{username}"
            os.makedirs(self.user_folder, exist_ok=True)
            self.new_course_window()
        else:
            self.display_message("Please enter a username.")

    def load_folders(self):
        # Load existing folders for the entered username
        username = self.username_entry.get()
        if username:
            self.user_folder = f"User_{username}"
            if os.path.isdir(self.user_folder):
                self.course_folders = [f for f in os.listdir(self.user_folder) if os.path.isdir(os.path.join(self.user_folder, f))]
                if self.course_folders:
                    self.display_folders()
                else:
                    self.display_message("No folders found.")
            else:
                self.display_message("User folder not found.")
        else:
            self.display_message("Please enter a username.")

    def display_folders(self):
        # Display course folders
        self.folders_window = tk.Toplevel(self.master)
        self.folders_window.title("Courses")
        self.folders_window.geometry("400x300")  # Set the size of the window
        self.course_prompt_label = tk.Label(self.folders_window, text="Click on a course to open notes, or create a new course")
        self.course_prompt_label.pack(pady=10)
        # Create a frame to contain the listbox and scrollbar
        frame = tk.Frame(self.folders_window)
        frame.pack(fill=tk.BOTH, expand=True)
        # Create a listbox to display the course folders
        self.course_listbox = tk.Listbox(frame)
        self.course_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Create a scrollbar and attach it to the listbox
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.course_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.course_listbox.config(yscrollcommand=scrollbar.set)
        # Populate the listbox with course folders
        for folder_name in self.course_folders:
            self.course_listbox.insert(tk.END, folder_name)
        # Bind double-click event to open the selected course folder
        self.course_listbox.bind("<Double-Button-1>", self.open_course_folder)
        # Create a frame for the "New Course" button
        button_frame = tk.Frame(self.folders_window)
        button_frame.pack(side=tk.BOTTOM)
        # Place the "New Course" button in the button frame
        new_course_button = tk.Button(button_frame, text="New", command=self.new_course_window)
        new_course_button.pack(pady=10)

    def open_course_folder(self, event):
        # Open the selected course folder
        selection = self.course_listbox.curselection()
        if selection:
            folder_index = selection[0]
            folder_name = self.course_listbox.get(folder_index)
            notes_window = tk.Toplevel(self.folders_window)
            notes_window.title(f"{folder_name} Notes")
            notes_window.geometry("600x300")
            self.load_notes(folder_name, notes_window)

    def load_notes(self, folder_name, notes_window):
        # Load notes for the selected course folder
        self.course_notes = os.listdir(os.path.join(self.user_folder, folder_name))
        if self.course_notes:
            # Display notes in a listbox
            frame = tk.Frame(notes_window)
            frame.pack(fill=tk.BOTH, expand=True)
            prompt_label = tk.Label(frame, text="Double click a note to view, or 'continue' to take more notes")
            prompt_label.pack(pady=5)
            notes_listbox_frame = tk.Frame(frame)
            notes_listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            notes_listbox = tk.Listbox(notes_listbox_frame)
            notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=notes_listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            notes_listbox.config(yscrollcommand=scrollbar.set)
                
            # Bind double-click event to open the selected note
            def open_selected_note(event):
                selected_index = notes_listbox.curselection()
                if selected_index:
                    selected_note_name = notes_listbox.get(selected_index[0])
                    self.open_note(None, folder_name, selected_note_name)
            
            # Populate the listbox with note names
            for note_name in self.course_notes:
                notes_listbox.insert(tk.END, note_name)
            
            # Bind double-click event to open the selected note
            notes_listbox.bind("<Double-Button-1>", open_selected_note)
            
            continue_button = tk.Button(notes_window, text="Continue", command=lambda: self.open_highest_note(folder_name))
            continue_button.pack(pady=10)
        else:
            self.display_message(f"No notes found for {folder_name}.")
            new_note_button = tk.Button(notes_window, text="Create New Note", command=lambda: self.open_note(folder_name, "New_Note.txt"))
            new_note_button.pack(pady=10)


    def display_all_notes(self):
        # Create a new window to display all notes
        all_notes_window = tk.Toplevel(self.master)
        all_notes_window.title("All Notes")
        all_notes_window.geometry("800x600")

        # Create a text widget to display all notes
        all_notes_text = tk.Text(all_notes_window, wrap=tk.WORD, height=30, width=100)
        all_notes_text.pack(fill=tk.BOTH, expand=True)

        # Get the directory path for the selected course code
        course_notes_dir = os.path.join(self.user_folder, self.selected_course)

        # Iterate over note files in the selected course folder
        for note_file in os.listdir(course_notes_dir):
            with open(os.path.join(course_notes_dir, note_file), 'r') as f:
                note_content = f.read()
                all_notes_text.insert(tk.END, f"Note: {note_file}\n\n")
                all_notes_text.insert(tk.END, note_content)
                all_notes_text.insert(tk.END, "\n\n")

        # Disable editing in the text widget
        all_notes_text.config(state=tk.DISABLED)

    def open_course_folder(self, event):
        # Open the selected course folder
        selection = self.course_listbox.curselection()
        if selection:
            folder_index = selection[0]
            self.selected_course = self.course_listbox.get(folder_index)
            folder_name = self.selected_course
            notes_window = tk.Toplevel(self.folders_window)
            notes_window.title(f"{folder_name} Notes")
            notes_window.geometry("600x300")
            self.load_notes(folder_name, notes_window)

        # Add a button to view all notes
        view_all_button = tk.Button(notes_window, text="View All Notes", command=self.display_all_notes)
        view_all_button.pack(pady=10)

    def open_note_by_name(self, folder_name, note_name):
        # Helper function to open a note by name
        self.open_note(folder_name, note_name)

#double clicking a file opens largest file

    def open_highest_note(self, folder_name):
        # Open the note with the highest chapter and paragraph count
        highest_chapter = 0
        highest_paragraph = 0
        highest_note = None
        for note_name in self.course_notes:
            chapter, paragraph = self.extract_chapter_paragraph(note_name)
            if chapter > highest_chapter or (chapter == highest_chapter and paragraph > highest_paragraph):
                highest_chapter = chapter
                highest_paragraph = paragraph
                highest_note = note_name
        if highest_note:
            self.open_note(folder_name, highest_note)

    def extract_chapter_paragraph(self, note_name):
        # Extract chapter and paragraph from note name
        parts = note_name.split('_')
        chapter = int(parts[1])
        paragraph = int(parts[3].split('.')[0])  # Remove the '.txt' extension
        return chapter, paragraph

    def open_note(self, event, folder_name, note_name):
        # Construct the file path
        filepath = os.path.join(self.user_folder, folder_name, note_name)
        # Check if the file exists
        if not os.path.exists(filepath):
            # If the file doesn't exist, create it
            chapter, paragraph = 1, 1
            new_note_name = f"Chapter_{chapter}_Paragraph_{paragraph}.txt"
            filepath = os.path.join(self.user_folder, folder_name, new_note_name)
            with open(filepath, 'w') as file:
                pass  # This creates an empty file
        # Open the file for reading
        with open(filepath, 'r') as file:
            note_content = file.read()
        note_window = tk.Toplevel(self.master)  # Use self.master instead of self.folders_window
        note_window.title(f"{note_name} Notes")
        note_window.geometry("600x300")

        # Create a text widget to display the note content
        note_text = tk.Text(note_window, wrap=tk.WORD, height=15, width=70)
        note_text.pack(fill=tk.BOTH, expand=True)

        # Insert the note content into the text widget
        note_text.insert(tk.END, note_content)

        # Create buttons for next chapter, next paragraph, and save
        button_frame = tk.Frame(note_window)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        next_chapter_button = tk.Button(button_frame, text="Next Chapter", command=lambda: self.next_chapter(folder_name, note_name, note_window))
        next_chapter_button.pack(side=tk.LEFT)

        next_paragraph_button = tk.Button(button_frame, text="Next Paragraph", command=lambda: self.next_paragraph(folder_name, note_name, note_window))
        next_paragraph_button.pack(side=tk.LEFT)

        save_button = tk.Button(button_frame, text="Save", command=lambda: self.save_notes(folder_name, note_name, note_text))
        save_button.pack(side=tk.RIGHT)

        # Set the position of the note window relative to the root window
        note_window.geometry("+{}+{}".format(self.master.winfo_x() + 50, self.master.winfo_y() + 50))


    def create_course_folder(self):
        # Create a new course folder
        course_code = self.course_entry.get()
        if course_code:
            self.course_folder = os.path.join(self.user_folder, course_code)
            os.makedirs(self.course_folder, exist_ok=True)
            # Determine the new note title
            new_note_title = self.determine_new_note_title(course_code)
            # Open a window for taking notes with the new note title
            self.open_note(None, course_code, new_note_title)
        else:
            self.display_message("Please enter a course code.")

    def determine_new_note_title(self, course_code):
        # Determine the title for the new note based on existing notes
        chapter = 1
        paragraph = 1
        while True:
            new_note_name = f"Chapter_{chapter}_Paragraph_{paragraph}.txt"
            if not os.path.exists(os.path.join(self.course_folder, new_note_name)):
                break
            # If the note already exists, increment the chapter and paragraph counts
            paragraph += 1
        return f"Chapter_{chapter}_Paragraph_{paragraph}.txt"



    def new_course_window(self):
        # Create a new course window
        self.course_window = tk.Toplevel(self.master)
        self.course_window.title("Course Code")
        
        self.course_label = tk.Label(self.course_window, text="Course Code:")
        self.course_label.pack()
        
        self.course_entry = tk.Entry(self.course_window)
        self.course_entry.pack()

        self.next_button = tk.Button(self.course_window, text="Next", command=self.create_course_folder)
        self.next_button.pack()


    def next_chapter(self, folder_name, note_name, notes_window):
        # Open the next chapter
        chapter, _ = self.extract_chapter_paragraph(note_name)
        chapter += 1
        paragraph = 1
        new_note_name = f"Chapter_{chapter}_Paragraph_{paragraph}.txt"
        self.create_empty_note_file(folder_name, new_note_name)
        self.open_note(None, folder_name, new_note_name)
        # Close the current note window
        notes_window.destroy()

    def next_paragraph(self, folder_name, note_name, notes_window):
        # Open the next paragraph
        chapter, paragraph = self.extract_chapter_paragraph(note_name)
        paragraph += 1
        new_note_name = f"Chapter_{chapter}_Paragraph_{paragraph}.txt"
        self.create_empty_note_file(folder_name, new_note_name)
        self.open_note(None, folder_name, new_note_name)
        # Close the current note window
        notes_window.destroy()


               

    def create_empty_note_file(self, folder_name, note_name):
        # Create an empty note file if it doesn't exist
        filepath = os.path.join(self.user_folder, folder_name, note_name)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as file:
                pass


    def save_notes(self, folder_name, note_name, note_text):
        # Save the notes to the appropriate file
        notes = note_text.get('1.0', tk.END)
        filename = os.path.join(self.user_folder, folder_name, note_name)
        with open(filename, 'w') as f:
            f.write(notes)

    def display_message(self, message):
        # Display a message window
        message_window = tk.Toplevel(self.master)
        tk.Label(message_window, text=message).pack()
        tk.Button(message_window, text="OK", command=message_window.destroy).pack()

def main():
    # Main function to initialize the app
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
