from bot import Bot
from bot import *
from AddressBook import *
from rich.console import Console
from classes import *
from note_tag import *
import difflib

# for package install
VERSION = "0.9.0"

COMMANDS = {
    add_command: ("add", "+", "2","adding","append"),
    change_command: ("change", "зміни", "3"),
    exit_command: ("bye", "exit", "end","GoodBye", "0"),
    delete_contact_command:("del","8", "delete"),
    find_command: ("find", "4"),
    show_all_command: ("show-all", "5", "show","showing"),
    hello_command:("hello", "1"),
    edit_name_command: ("edit", "7","rename"),
    change_birthday_command: ("change-bday", "6","change-birthday", "changebday","changebirthday"),
    change_email_command: ("change-email", "9", "change-mail", "changemail", "changeemail"),
    change_address_command: ("change-address", "10","changeaddress"),
    sort_files: ("sort","sorting"),
    contacts_in_period: ("period", "bdays","congrats"),
    help_command: ("help"),
    show_notes: ("show-notes", "n5"),
    make_note: ("make-notes", "add-notes", "+n"),
    bot_add_teg: ("add-tag","+t"),
    bot_change_teg: ("change-tag","=t"),
    bot_add_text_note: ("add-text"),
    bot_change_text_note: ("change-text","=text"),
    delete_note_by_number: ("delete-note","-n"),
    search_notes: ("search-n","search-notes","search-tag","fnt")
        
}

def get_closest_matches(user_input, commands, n=3, cutoff=0.6):
    user_input_lower = user_input.lower()
    closest_matches = []
    for cmd, kwds in commands.items():
        for kwd in kwds:
            if kwd in user_input_lower:
                closest_matches.append(kwd)
    if not closest_matches:
        user_words = user_input_lower.split()
        for cmd, kwds in commands.items():
            for kwd in kwds:
                for word in user_words:
                    similarity = difflib.SequenceMatcher(None, word, kwd).ratio()
                    if similarity >= 0.5:  # Поріг схожості, можна налаштувати під свої потреби
                        closest_matches.append(kwd)
                        break
    return closest_matches

def parser(text: str):
    text_lst = text.split(" ")
    for cmd, kwds in COMMANDS.items():
        kwd = text_lst[0]
        if len(text_lst) and kwd in kwds:
            data = text[len(kwd):].strip().split()
            return cmd, data

    matches = get_closest_matches(text, COMMANDS)
    if matches:
        return closest_matches_suggestion, (matches,)

    return unknown_command, [text]
        
        # for kwd in kwds:
        #     if text.lower().startswith(kwd):
        #         data = text[len(kwd):].strip().split()
        #         if cmd in [change_command, edit_name_command]:
        #             if len(data) < 3:
        #                 data.append(None)
        #         return cmd, data


def closest_matches_suggestion(matches):
    return f"Did you mean one of the following commands: {', '.join(matches)}?"

def unknown_command(text):
    return f"Unknown command: '{text}'. Type 'help' to see the list of available commands."

def main():
    print('Hello. I am your contact-assistant.\nWhat can I do for you?')
    
    while True:
        user_input = input("enter your choices--->>> ")

        cmd, data = parser(user_input)

        if cmd == exit_command:
            print("Goodbye!")
            break

        result = cmd(*data)  # Оброблюємо команду та отримуємо результат

        if cmd == closest_matches_suggestion:
            print(result)  # Виводимо повідомлення з пропозиціями варіантів команд
        elif cmd == unknown_command:
            print(result)  # Виводимо повідомлення про невідому команду
        else:
            if isinstance(result, str):
                print(result)
            else:
                console = Console()
                console.print(result)

       
 

if __name__ == "__main__":
    bot = Bot()
    main()
