import threading
import datetime
import os
import csv
import docx
from typing import Callable, Dict, Any, List
from ai_assistant import chat_with_mistral # Currently unused, but kept for context
from calendar_sync import add_event, check_reminders
from text_to_speech import speak_text
from email_helper import suggest_email_template, autocomplete_sentence # Currently unused
from file_handler import process_file  # Assuming this handles generic file reading/parsing
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuration & Helpers ---

# Define the log/output file path for visuals
VISUAL_OUTPUT_PATH = "staplr_output"
os.makedirs(VISUAL_OUTPUT_PATH, exist_ok=True)

def start_reminder_thread():
    """Starts the calendar reminder check in a separate thread."""
    print("Starting reminder service...")
    reminder_thread = threading.Thread(target=check_reminders, daemon=True)
    reminder_thread.start()

# --- Core Functionality ---

def perform_eda(file_path: str) -> str:
    """Performs basic EDA on the given CSV file and returns a summary."""
    try:
        df = pd.read_csv(file_path)
        numeric_df = df.select_dtypes(include=['number'])

        if numeric_df.empty:
            return "⚠️ No numeric data available for EDA."

        summary = numeric_df.describe().to_string()
        missing_values = df.isnull().sum().to_string()
        correlation_matrix = numeric_df.corr()

        # Save heatmap to the dedicated output folder
        heatmap_path = os.path.join(VISUAL_OUTPUT_PATH, "eda_correlation_heatmap.png")
        
        plt.figure(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Heatmap")
        plt.tight_layout() # Ensures everything fits
        plt.savefig(heatmap_path)
        plt.close()

        return (
            f"📊 **EDA Summary for '{os.path.basename(file_path)}':**\n\n{summary}\n\n"
            f"🔍 **Missing Values:**\n{missing_values}\n\n"
            f"✅ Correlation heatmap saved as '{heatmap_path}'"
        )

    except FileNotFoundError:
        return "⚠️ Error: File not found. Please check the path."
    except Exception as e:
        return f"⚠️ Error performing EDA: {type(e).__name__}: {str(e)}"

# --- Query Processor ---

def handle_eda_request(query_args: List[str]) -> str:
    """Handles the 'perform eda' command."""
    # Note: Using tkinter's filedialog is often not ideal for CLI assistants, 
    # but kept here to match the original requirement.
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return "⚠️ No file selected."
    return perform_eda(file_path)

def handle_reminder(query_args: List[str]) -> str:
    """Handles the 'remind me of' command."""
    # Expected format: <event> at <HH:MM>
    full_arg = " ".join(query_args)
    
    # Use a more robust split logic
    if ' at ' not in full_arg:
        return "⚠️ Invalid format. Try: 'Remind me of <event> at <HH:MM>'"
    
    description, time_str = [p.strip() for p in full_arg.split(" at ", 1)]

    try:
        # Validate time_str format (e.g., ensure it's HH:MM)
        datetime.datetime.strptime(time_str, "%H:%M") 
        
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        duration = "30 mins"
        add_event(date, time_str, duration, description, reminder=True)
        return f"✅ Reminder set for '{description}' at {time_str} today."
    except ValueError:
        return "⚠️ Invalid time format. Please use HH:MM (e.g., 14:30)."
    except Exception as e:
        return f"❌ Error setting reminder: {e}"

def handle_add_event(query_args: List[str]) -> str:
    """Handles the 'add event' command (similar to reminder, but not a loud reminder)."""
    full_arg = " ".join(query_args)

    if ' at ' not in full_arg:
        return "⚠️ Invalid format. Try: 'Add event <description> at <HH:MM>'"

    description, time_str = [p.strip() for p in full_arg.split(" at ", 1)]

    try:
        datetime.datetime.strptime(time_str, "%H:%M") 
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        duration = "30 mins"
        add_event(date, time_str, duration, description, reminder=False)
        return f"✅ Event '{description}' added at {time_str} today."
    except ValueError:
        return "⚠️ Invalid time format. Please use HH:MM (e.g., 14:30)."
    except Exception as e:
        return f"❌ Error adding event: {e}"

def handle_speak(query_args: List[str]) -> str:
    """Handles the 'speak' or 'repeat after me' command."""
    text_to_speak = " ".join(query_args).strip()
    if text_to_speak:
        # Use threading to prevent TTS from blocking the main loop
        threading.Thread(target=speak_text, args=(text_to_speak,), daemon=True).start()
        return f"🎤 Speaking: {text_to_speak}"
    return "⚠️ No text provided to speak."

def handle_read_file(query_args: List[str]) -> str:
    """Handles general file reading command (e.g., 'read file <path>')."""
    # Note: Since the original file functions were simple, 
    # this re-implements that simple file reading logic for consistency.
    file_path = query_args[0] if query_args else None
    if not file_path:
        return "⚠️ Please provide a file path to read."
    
    try:
        _, ext = os.path.splitext(file_path.lower())
        
        if ext == '.docx':
             # Use the original function logic
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text if text.strip() else f"The DOCX file '{os.path.basename(file_path)}' is empty."
        
        elif ext == '.csv':
            # Use the original function logic
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                data = "\n".join([", ".join(row) for row in reader])
            return data if data.strip() else f"The CSV file '{os.path.basename(file_path)}' is empty."

        else:
            # Fallback for other files (using the imported process_file is a good idea here)
            return process_file(file_path) # Assuming process_file handles generic text files
            
    except FileNotFoundError:
        return f"⚠️ Error: File not found at path '{file_path}'."
    except Exception as e:
        return f"❌ Error reading file: {type(e).__name__}: {e}"

# Map commands to their handler functions
COMMAND_MAP: Dict[str, Callable[[List[str]], str]] = {
    "perform eda on this file": handle_eda_request,
    "remind me of": handle_reminder,
    "add event": handle_add_event,
    "speak": handle_speak,
    "repeat after me": handle_speak,
    "read file": handle_read_file # New command to replace dedicated file readers
}

def process_staplr_query(query: str) -> str:
    """Analyzes user query and dispatches to the appropriate handler."""
    query_lower = query.lower().strip()

    if query_lower == "exit":
        return "👋 Exiting Staplr."

    # Look for command prefix in the map
    for command, handler in COMMAND_MAP.items():
        if query_lower.startswith(command):
            # Extract arguments by removing the command part
            args_str = query[len(command):].strip()
            # Split arguments for the handler (simple space split for flexibility)
            query_args = args_str.split() if args_str else [] 
            
            # Special handling for commands that need the argument string intact
            if command in ["remind me of", "add event"]:
                 query_args = [args_str] # Pass the full remaining string
            elif command in ["speak", "repeat after me"]:
                 query_args = [args_str] # Pass the full remaining string
            
            return handler(query_args)

    return "⚠️ I can only assist with predefined functions."

# Main function to run Staplr in terminal mode
def main():
    start_reminder_thread()
    print("\n--- Staplr AI Assistant ---")
    print("Available commands: perform eda on this file, remind me of <event> at <HH:MM>, add event <desc> at <HH:MM>, speak <text>, read file <path>, exit")

    while True:
        try:
            user_input = input("\nAsk Staplr: ").strip()
            if not user_input:
                continue
                
            response = process_staplr_query(user_input)
            
            print(response)

            if response == "👋 Exiting Staplr.":
                break
        
        except KeyboardInterrupt:
            print("\n👋 Exiting Staplr.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Removed the redundant file reading functions (read_word_document, read_csv_file)
    # as they are re-implemented within handle_read_file or should be handled by process_file.
    
    main()
