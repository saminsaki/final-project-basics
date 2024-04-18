import argparse
import os
import json
import shutil
import datetime

working_dir_file = 'path.json'
log_file = 'logs.log'

def setup():
    parser = argparse.ArgumentParser(description="File manipulation and directory navigation CLI tool")
    parser.add_argument("command", help="Command to execute (ls, cd, mkdir, rmdir, rm, cp, mv, find, cat)")
    parser.add_argument("path", nargs='?', default='.', help="Path for the command, defaults to current directory")
    parser.add_argument("destination", nargs='?', help="Destination path for cp, mv commands")
    parser.add_argument("-p", "--pattern", help="Pattern for the find command")
    parser.add_argument("-r", "--recursive", help="Recursive option for rm command")
    parser.add_argument("-f", "--file", help="File name for cat command")
    parser.add_argument("-a", "--all", action="store_true", help="Show all files and dirs.")
    return parser

def is_valid_path(path):
    if not os.path.exists(path):
        print(f"Error: The path '{path}' does not exist.")
        return False
    if not os.access(path, os.R_OK):
        print(f"Error: The path '{path}' is not accessible.")
        return False
    return True

def log_command(command, status, error_message=None):
    with open(log_file, 'a') as log:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log.write(f"{timestamp} - Command: {command}, Status: {status}")
        if error_message:
            log.write(f", Error: {error_message}")
        log.write('\n')

def load_working_directory():
    if os.path.exists(working_dir_file):
        with open(working_dir_file, 'r') as f:
            data = json.load(f)
            return data.get('cwd', os.getcwd())
    return os.getcwd()

def save_working_directory(path):
    with open(working_dir_file, 'w') as f:
        json.dump({'cwd': path}, f)

def list_directory(path, show_hidden=False):
    cwd = load_working_directory()
    full_path = os.path.join(cwd, path)
    if not is_valid_path(full_path):
        return

    try:
        for item in os.listdir(full_path):
            if show_hidden or not item.startswith('.'):
                print(item)
    except FileNotFoundError:
        print(f"Error: The directory '{cwd}' was not found.")

def change_directory(path):
	if not is_valid_path(full_path):
		return

    save_working_directory(path)

def create_directory(name):
    cwd = load_working_directory()
    full_path = os.path.join(cwd, name)
    if not is_valid_path(full_path):
        return

    try:
        os.makedirs(full_path, exist_ok=True)
    except OSError as e:
        print(f"Error: Could not create directory '{full_path}'. {e}")

def remove_empty_directory(path):
    cwd = load_working_directory()
    full_path = os.path.join(cwd, path)
    if not is_valid_path(full_path):
        return

    try:
        os.rmdir(full_path)
        print(f"Empty directory '{full_path}' removed successfully.")
    except OSError as e:
        print(f"Error: Could not remove empty directory '{full_path}'. {e}")

def remove_directory(path):
    cwd = load_working_directory()
    full_path = os.path.join(cwd, path)
    if not is_valid_path(full_path):
        return

    try:
        shutil.rmtree(full_path)
        print(f"Directory '{full_path}' and its contents removed recursively.")
    except OSError as e:
        print(f"Error: Could not remove directory '{full_path}'. {e}")


def remove_file(path):
    cwd = load_working_directory()
    full_path = os.path.join(cwd, path)
    if not is_valid_path(full_path):
        return

    try:
        os.remove(full_path)
        print(f"File '{full_path}' removed successfully.")
    except OSError as e:
        print(f"Error: Could not remove file '{full_path}'. {e}")

def copy_file(source, destination):
    cwd = load_working_directory()
    source_path = os.path.join(cwd, source)
    destination_path = os.path.join(cwd, destination)
    print(source_path, destination_path)
    if not is_valid_path(source_path):
        return
    if not is_valid_path(destination_path):
        return

    try:
        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)
            print(f"Directory '{source_path}' copied to '{destination_path}'.")
        else:
            shutil.copy2(source_path, destination_path)
            print(f"File '{source_path}' copied to '{destination_path}'.")
    except OSError as e:
        print(f"Error: Could not copy '{source_path}' to '{destination_path}'. {e}")

def move_file(source, destination):
    cwd = load_working_directory()
    source_path = os.path.join(cwd, source)
    destination_path = os.path.join(cwd, destination)
    if not is_valid_path(source_path):
        return
    if not is_valid_path(destination_path):
        return

    try:
        shutil.move(source_path, destination_path)
        print(f"Moved '{source_path}' to '{destination_path}'.")
    except OSError as e:
        print(f"Error: Could not move '{source_path}' to '{destination_path}'. {e}")


def find_matching_files(full_path, pattern):
	matching_files = []
	for root, _, filenames in os.walk(full_path):
	    for filename in filenames:
	        if pattern in filename:
	            matching_files.append(os.path.join(root, filename))
	return matching_files

def find_files(path, pattern):
	cwd = load_working_directory()
	full_path = os.path.join(cwd, path)
    if not is_valid_path(full_path):
        return

	if not os.path.exists(full_path) or not os.path.isdir(full_path):
	    print(f"Error: The directory '{full_path}' does not exist.")
	    return

	matches = find_matching_files(full_path, pattern)

	if matches:
	    print("Matching files/directories:")
	    for match in matches:
	        print(match)
	else:
	    print(f"No files/directories matching the pattern '{pattern}' found.")

def view_logs():
    if os.path.exists(log_file):
        with open(log_file, 'r') as log:
            print(log.read())
    else:
        print("No logs available.")

def cat_file(file_path):
    cwd = load_working_directory()
    full_path = os.path.join(cwd, file_path)
    if not is_valid_path(full_path):
        return

    try:
        with open(full_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"Error: File '{full_path}' not found.")
    except Exception as e:
        print(f"Error: Could not read file '{full_path}'. {e}")

def main():
	parser = setup()
	args = parser.parse_args()
	try:
	    if args.command == 'ls':
	        if args.all:
	            list_directory(args.path, show_hidden=True)
	        else:
	            list_directory(args.path)
	    elif args.command == 'mkdir':
	        create_directory(args.path)
	    elif args.command == 'cd':
	        change_directory(args.path)
	    elif args.command == 'rmdir':
	        remove_empty_directory(args.path)
	    elif args.command == 'rm':
	        if args.recursive:
	        	remove_directory(args.recursive)
	        else:
	            remove_file(args.path)
	    elif args.command == 'cp':
	        copy_file(args.path, args.destination)
	    elif args.command == 'mv':
	        move_file(args.path, args.destination)
	    elif args.command == 'find':
	    	print(args.pattern)
	    	find_files(args.path, args.pattern)
	    elif args.command == "logs":
	    	view_logs()
	    elif args.command == "cat":
	    	cat_file(args.file)
	    else:
	    	log_command(args.command, "Error", "Invalid command")
	    	print("Invalid Command!")
	    log_command(args.command, "Success")
	except Exception as e:
	    print(f"Error: {e}")
	    log_command(args.command, "Error", str(e))

if __name__ == "__main__":
    main()
