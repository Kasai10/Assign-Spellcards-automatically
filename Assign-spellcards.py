import fitz  # PyMuPDF
import os
import re
import shutil
import glob
import sys

#kekse
arguments = sys.argv

def copy_to_target_location(path, is_Spellcards):
    # Destination path
    destination = dnd_folder_path
    if is_Spellcards:
        shutil.copy(path, destination)
    else:
        shutil.copy(path, character_sheets_dir)

if "-edit" in arguments:
    dnd_folder_path = input("Input the path to your dnd folder: ")
    with open("Dndpath.txt", "w") as file:
        file.write(dnd_folder_path)
try:
    with open("Dndpath.txt", "r") as file:
        dnd_folder_path = file.readline().strip()
except FileNotFoundError:
    print("Use -edit the first time you start in order to provide a dnd folder path.")
    quit()

character_sheets_dir = os.path.join(dnd_folder_path, "CharacterSheets")
character_name = ""
try:
    characters = os.listdir(character_sheets_dir)
    characters = [filename.replace(".pdf", "") for filename in characters]
    while True:
        print("Press 'a' if you want to add a character to the directory!") 
        character_name = input(f"Input character name, the following files are present in the directory: {characters}: ")
        if character_name == "a":
            path_to_charactersheet = input("Input the path to the charactersheet here: ")
            try:
                copy_to_target_location(path_to_charactersheet, False)
                continue
            except FileNotFoundError:
                print("Sheet not found. Please try again!")
                continue
        spells_for_character = os.path.join(dnd_folder_path, f"Spellcards {character_name}")
        if character_name in characters:
            break
        else:
            print("Please input a valid character")
except FileNotFoundError:
    print("Making directories now...")

# Use the directory where the script is located for spellcards_folder
spellcards_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Spell Cards")

def make_spellcard_folder(character_name):
    # Create dnd_folder_path if it doesn't exist
    if not os.path.exists(dnd_folder_path):
        os.makedirs(dnd_folder_path)
        print(f"{dnd_folder_path} successfully created")
    
    # Create character_sheets_dir if it doesn't exist
    if not os.path.exists(character_sheets_dir):
        os.makedirs(character_sheets_dir)
        print(f"{character_sheets_dir} successfully created")
    
    # Create spells_for_character if it doesn't exist
    if not os.path.exists(spells_for_character):
        os.makedirs(spells_for_character)
        print(f"{spells_for_character} successfully created")
    else:
        print("Character already exists")
    
    get_character_sheet_text(character_name)

def get_character_sheet_text(character_name):
    character_sheet_path = os.path.join(character_sheets_dir, f"{character_name}.pdf")
    if not os.path.exists(character_sheet_path):
        print(f"The character sheet you provided does not exist within {character_sheets_dir}")
        return

    character_sheet = fitz.open(character_sheet_path)
    last_page = character_sheet[-1]  # Get the last page
    character_sheet_text = last_page.get_text("text")  # Extract text from the last page

    # Define the regular expression pattern to match spells
    spell_pattern = re.compile(r'O\s+[\w\s]+')

    # Find all matches of the spell pattern in the text
    spells = spell_pattern.findall(character_sheet_text)

    # Print the found spells
    cleaned_spells = []
    for spell in spells:
        if spell.startswith("O"):
            spell = spell.strip()
            # Remove the leading 'O' and strip any whitespace
            cleaned_spell = spell[1:].strip()
            cleaned_spells.append(cleaned_spell)

    # Print the cleaned spells
    copy_spells_in_spellfolder(cleaned_spells)

def copy_spells_in_spellfolder(potential_spells):
    spells_for_character = os.path.join(dnd_folder_path, f"Spellcards {character_name}")

    # Create the spells_for_character folder if it doesn't exist
    if not os.path.exists(spells_for_character):
        os.makedirs(spells_for_character)
        print(f"{spells_for_character} successfully created")

    # Store the names of copied files to avoid duplication
    copied_files = set()

    # Iterate through potential_spells and search for corresponding PNG files
    for spell_name in potential_spells:
        # Construct the expected PNG file name pattern for the spell
        png_file_pattern = os.path.join(spellcards_folder, f"{spell_name}*")
        
        # Use glob to search for PNG files matching the pattern
        png_files = glob.glob(png_file_pattern)

        if not png_files:
            # If no PNG files are found, try searching using only the first word of the spell name
            first_word = spell_name.split()[0]
            png_file_pattern = os.path.join(spellcards_folder, f"{first_word}*")
            png_files = glob.glob(png_file_pattern)

        if png_files:
            # Copy the first PNG file found
            for png_file in png_files:
                file_name = os.path.basename(png_file)
                # Ensure the file hasn't been copied already
                if file_name not in copied_files:
                    destination_path = os.path.join(spells_for_character, file_name)
                    shutil.copy(png_file, destination_path)
                    copied_files.add(file_name)
                    print(f"Copied {file_name} to {spells_for_character}")
        else:
            print(f"No PNG file found for {spell_name}")

    print("Spell images copied successfully.")

make_spellcard_folder(character_name)
