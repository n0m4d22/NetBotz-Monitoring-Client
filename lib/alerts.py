"""UI and audio alert setup."""

import tkinter as tk
import winsound 

# play the alarm sound
def play_alert():
    # Play the alarm sound until the button 'Silence' is pressed
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)

# silence the alarm sound
def silence_alert():
    # Silence the alarm
    winsound.PlaySound(None, winsound.SND_PURGE)

# alert definition that adapts based on "type"
def alert(node, type):
    # windows config
    window = tk.Tk()
    window.title(f"Alert: {type}")
    window.geometry("350x200")
    window.resizable(False, False)
            
    # labels and ui elements
    status_label = tk.Label(window, text=f"CRITICAL: {node.label} {type}: {node.temperature}", fg="red", font=("Arial", 11, "bold"))
    status_label.pack(pady=20)
    
    # silence button config
    silence_button = tk.Button(window, text="Silence", command=silence_alert, bg="white", fg="black", font=("Arial", 10, "bold"), width=15, height=2)
    silence_button.pack(pady=10)
            
    window.after(100, play_alert)
            
    window.mainloop()