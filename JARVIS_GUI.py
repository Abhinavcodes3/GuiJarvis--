import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import speech_recognition as sr


def start_listening():
    """Start speech recognition and update the GUI with recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_chat_display("Listening for your command...\n")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            update_chat_display(f"You said: {command}\n")
            handle_command(command)  # Process the command
        except sr.UnknownValueError:
            update_chat_display("Sorry, I could not understand that.\n")
        except sr.RequestError:
            update_chat_display("Speech recognition service is unavailable.\n")


def handle_command(command):
    """Process the recognized command and perform actions."""
    if "hello" in command.lower():
        update_chat_display("Jarvis says: Hello!\n")
    elif "how are you" in command.lower():
        update_chat_display("Jarvis says: I'm just a program, but I'm functioning well!\n")
    elif "lights" in command.lower():
        update_chat_display("Jarvis says: Lights turned on!\n")
    elif "music" in command.lower():
        update_chat_display("Jarvis says: Playing music now!\n")
    else:
        update_chat_display("Jarvis says: Command not recognized.\n")


def update_chat_display(message):
    """Update the chat display text box with the given message."""
    chat_display.config(state="normal")  # Enable editing
    chat_display.insert(tk.END, message)  # Insert message
    chat_display.config(state="disabled")  # Disable editing
    chat_display.see(tk.END)  # Scroll to the end


def update_loading_gif():
    """Animate the loading.gif in the top-left corner."""
    global loading_frames, loading_frame_index

    loading_frame = loading_frames[loading_frame_index]
    loading_label.configure(image=loading_frame)
    loading_frame_index = (loading_frame_index + 1) % len(loading_frames)

    root.after(100, update_loading_gif)  # Update every 100 ms


def create_gui():
    """Create the GUI window."""
    global chat_display, loading_label, root, loading_frames, loading_frame_index

    # Main window (set size to 16:9 aspect ratio)
    root = tk.Tk()
    window_width = 1280  # 16:9 aspect ratio width
    window_height = 720  # 16:9 aspect ratio height
    root.geometry(f"{window_width}x{window_height}")
    root.title("Jarvis GUI")
    root.resizable(False, False)  # Disable resizing for consistent layout

    # Load the background GIF (jarvis.gif)
    jarvis_gif = Image.open("jarvis.gif")
    frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(jarvis_gif)]

    # Create a Label widget for the animated background
    background_label = tk.Label(root)
    background_label.place(relwidth=1, relheight=1)  # Make it cover the entire window

    # Function to animate the background GIF
    def update_background(index=0):
        background_label.configure(image=frames[index])
        root.after(100, update_background, (index + 1) % len(frames))

    update_background()  # Start the animation



    # Textbox for Chat (bottom overlay)
    chat_display = tk.Text(root, font=("Arial", 12), bg="black", fg="white", wrap=tk.WORD, state="disabled")
    chat_display.place(relx=0.5, rely=0.85, anchor="center", width=window_width - 40, height=100)

    # Start Listening Button (directly above the chat box)
    listen_button = tk.Button(root, text="Start Listening", command=start_listening, font=("Arial", 14), bg="#007BFF", fg="white")
    listen_button.place(relx=0.5, rely=0.78, anchor="center")

    root.mainloop()


# Call to create the GUI
create_gui()

