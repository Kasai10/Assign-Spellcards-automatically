import fitz  # PyMuPDF
import os
import re
import shutil
import glob
import sys

arguments = sys.argv



def copy_to_target_location(path, is_Spellcards):
    # Destination path
    destination = dnd_folder_path
    if is_Spellcards:
        shutil.copy(path, destination)
    elif not is_Spellcards:
        shutil.copy(path, character_sheets_dir)

if("-edit" in arguments):
    dnd_folder_path = input("Input the path to your dnd folder: ")
    with open("Dndpath.txt", "w") as file:
        file.write(dnd_folder_path)
try:
    with open("Dndpath.txt", "r") as file:
        dnd_folder_path = file.readline()
except:
    print("Use -edit the first time you start in order to provide a dnd folder path.")
    quit()
character_sheets_dir = os.path.join(dnd_folder_path, "CharacterSheets")
character_name = ""
try:
    characters = os.listdir(character_sheets_dir)
    for i in range(len(characters)):
        characters[i] = characters[i].replace(".pdf", "")


        while(True):
            print("Press 'a' if you want to add a character to the directory!") 
            character_name = input(f"Input character name, the following files are present in the directory: {characters}: ")
            if character_name == "a":
                path_to_charactersheet = input("Input the path to the charactersheet here: ")
                try:
                    copy_to_target_location(path_to_charactersheet, False)
                    continue
                except:
                    print("Sheet not found. Please try again!")
                    continue
            spells_for_character = os.path.join(dnd_folder_path, "Spellcards " + character_name)
            if character_name in characters:
                break
            else:
                print("Please input a valid character")
except:
    print("Making directories now...")

    

spellcards_folder = os.path.join(dnd_folder_path, "Spell Cards")

def make_spellcard_folder(character_name):
    # Create dnd_folder_path if it doesn't exist
    if not os.path.exists(dnd_folder_path):
        os.makedirs(dnd_folder_path)
        print(dnd_folder_path + " successfully created")
    
    # Create character_sheets_dir if it doesn't exist
    if not os.path.exists(character_sheets_dir):
        os.makedirs(character_sheets_dir)
        print(character_sheets_dir + " successfully created")
    
    # Create spells_for_character if it doesn't exist
    try:
        if not os.path.exists(spells_for_character):
            os.makedirs(spells_for_character)
            print(spells_for_character + " successfully created")
        else:
            print("Character already exists")
    except:
        spellcards_path = input("Path to Spellcards folder: ")
        copy_to_target_location(spellcards_path, True)
        character_sheet_location = input("Location of character sheet: ")
        copy_to_target_location(character_sheet_location, False)
        print(f"Directories were successfully created")
        make_spellcard_folder()
    
    get_character_sheet_text(character_name)

def get_character_sheet_text(character_name):
    character_sheet_path = os.path.join(character_sheets_dir, character_name + ".pdf")
    if not os.path.exists(character_sheet_path):
        print("The character sheet you provided does not exist within " + character_sheets_dir)
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
            spell.strip()
            # Remove the leading 'O' and strip any whitespace
            cleaned_spell = spell[1:].strip()
            cleaned_spells.append(cleaned_spell)

    # Print the cleaned spells
    double_cleaned_spells = []
    for spell in cleaned_spells:
        if spell.startswith("O"):
            spell.strip()
            # Remove the leading 'O' and strip any whitespace
            cleaned_spell = spell[1:].strip()
            double_cleaned_spells.append(cleaned_spell)
        else:
            double_cleaned_spells.append(spell)
    
    copy_spells_in_spellfolder(double_cleaned_spells)

    
def clean_file_name(file_name):
    # Remove any leading or trailing whitespace
    file_name = file_name.strip()
    # Remove any additional characters that may be causing the discrepancy
    file_name = file_name.replace("  ", " ")  # Replace double spaces with single space
    # Optionally, you can remove any other unwanted characters or patterns
    
    return file_name

def copy_spells_in_spellfolder(potential_spells):
    spellcards_folder = os.path.join(dnd_folder_path, "Spell Cards")
    spells_for_character = os.path.join(dnd_folder_path, f"Spellcards {character_name}")

    # Create the spells_for_character folder if it doesn't exist
    if not os.path.exists(spells_for_character):
        os.makedirs(spells_for_character)
        print(f"{spells_for_character} successfully created")

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
            # If PNG files are found, copy the first one (assuming unique file names)
            source_path = png_files[0]
            file_name = os.path.basename(source_path)
            destination_path = os.path.join(spells_for_character, file_name)
            shutil.copy(source_path, destination_path)
            print(f"Copied {file_name} to {spells_for_character}")
        else:
            print(f"No PNG file found for {spell_name}")

    print("Spell images copied successfully.")

make_spellcard_folder(character_name)
