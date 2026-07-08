import os
import shutil
import psutil
import datetime


def menu():
    print("=====SYSTEM AUTOMATOR====")
    print("1. File organizer")
    print("2. System health monitor")
    print("3. Create backup")
    print("4. Large files finder")
    print("5. Exit")


def file_organizer():
    timestamp1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    folder = input(
        "Enter folder path to organize in this format 'c/folder_path'")
    videos = os.path.join(folder, "Videos")
    music = os.path.join(folder, "Music")
    document = os.path.join(folder, "Documents")
    picture = os.path.join(folder, "Pictures")
    others = os.path.join(folder, "Others")
    if not os.path.exists(folder):
        print("Path provided do not exist")
    else:
        for destination in [videos, music, document, picture]:
            if not os.path.exists(destination):
                os.makedirs(destination)
        files = os.listdir(folder)
        for file in files:
            full_path = os.path.join(folder, file)

            if os.path.isfile(full_path):
                result = os.path.splitext(file)
                ext = result[1]
                ext = ext.lower()
                try:
                    if ext in [".txt", ".doc", ".pdf", ".txt", ".csv"]:
                        shutil.move(full_path, document)
                        with open("organizer.log", "a") as f:
                            f.write(f"{file} was moved to {document}\n")
                        print(f"{timestamp1} - {file} was moved to {document}")

                    elif ext in [".mp3", ".wav"]:
                        shutil.move(full_path, music)
                        with open("organizer.log", "a") as f:
                            f.write(
                                f"{timestamp1} - {file} was moved to {music}\n")
                        print(f"{file} was moved to {music}")

                    elif ext == ".mp4":
                        shutil.move(full_path, videos)
                        with open("organizer.log", "a") as f:
                            f.write(
                                f"{timestamp1} - {file} was moved to {videos}\n")
                        print(f"{file} was moved to {videos}")

                    elif ext in [".jpg", ".jpeg", ".png", ".webp"]:
                        shutil.move(full_path, picture)
                        with open("organizer.log", "a") as f:
                            f.write(
                                f"{timestamp1} - {file} was moved to {picture}\n")
                        print(f"{file} was moved to {picture}")

                    else:
                        shutil.move(full_path, others)
                        with open("organizer.log", "a") as f:
                            f.write(
                                f"{timestamp1} - {file} was moved to {others}\n")

                        print(f"{file} was moved to {others}")
                except FileNotFoundError:
                    print(f"Error, file not found: {file}")
                except FileExistsError:
                    if ext in [".txt", ".doc", ".pdf", ".txt", ".csv"]:
                        print(f"{file} already exists in {document}")
                    elif ext in [".mp3", ".wav"]:
                        print(f"{file} already exists in {music}")
                    elif ext == ".mp4":
                        print(f"{file} already exists in {videos}")
                    elif ext in [".jpg", ".jpeg", ".png", ".webp"]:
                        print(f"{file} already exists in {picture}")
                    else:
                        print(f"{file} already exists in {others} ")
                except Exception as e:
                    print(f"Error: {e} occured")


def system_health_monitor():
    cpu = None
    ram = None
    mem = None
    timestamp2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cpu = psutil.cpu_percent(interval=1)
        cpu = f"CPU usage: {cpu}%"
    except Exception as e:
        print(f"Error {e} occured")
    try:
        ram = psutil.virtual_memory().percent
        ram = f"RAM usage: {ram}%"
    except Exception as e:
        print(f"Error {e} occured")
    try:
        mem = psutil.disk_usage("/").percent
        mem = f"Disk usage: {mem}%"
    except Exception as e:
        print(f"Error {e} occured")
    log2 = f"{timestamp2}- {cpu} | {ram} | {mem}"
    with open("health_data.log", "a") as f:
        f.write(log2)
    return cpu, ram, mem


def backup_with_limit():
    main_folder = input(
        "Enter folder path to backup: ").strip().strip('"')
    main_folder = main_folder.rstrip('\\/')

    if not os.path.isdir(main_folder):
        print(f"{main_folder} is not a folder path")
        return

    parent_path = os.path.dirname(main_folder)
    folder_name = os.path.basename(main_folder)
    max_backups = 2
    prefix = f"{folder_name}_backup_"
    backups = []

    for item in os.listdir(parent_path):
        full_item_path = os.path.join(parent_path, item)
        if os.path.isdir(full_item_path) and item.startswith(prefix):
            backups.append(item)

    backups.sort(reverse=True)

    if len(backups) >= max_backups:
        for old in backups[max_backups:]:
            old_path = os.path.join(parent_path, old)
            print(f"Deleting {old_path}")
            shutil.rmtree(old_path)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M-%S")
    backup_name = f"{folder_name}_backup_{timestamp}"
    backup_path = os.path.join(parent_path, backup_name)

    shutil.copytree(main_folder, backup_path)
    return f"Backup created:  {backup_path}"


def large_file_finder():
    find_folder = input("Enter folder path to find file: ")
    results = []
    if not os.path.exists(find_folder):
        print(f"{find_folder} is not a folder")
        return

    for root, dir, filenames in os.walk(find_folder):
        for file in filenames:
            file_find_path = os.path.join(root, file)
            file_size = 0
            try:
                file_size = os.path.getsize(file_find_path)
            except Exception as e:
                print(f"Error {e} occured")
                continue

            if file_size >= 50 * 1024 * 1024:
                size = file_size / (1024 * 1024)
                size = round(size, 2)
                results.append((f"{file_find_path}, {size}MB"))

    if len(results) == 0:
        return []
    return results


def main():
    while True:
        choice = None
        menu()
        try:
            choice = int(input("Pick an option from above: "))
        except ValueError:
            print(f"Only integars are allowed, try again")
            continue
        except KeyboardInterrupt:
            print("Program closed by user")
            break
        except Exception as e:
            print(f"Error {e} occured")
            continue

        if choice == 1:
            file_organizer()
            print("Choose option from 1-5")

        elif choice == 2:
            shm = system_health_monitor()
            for shms in shm:
                print(shms)
            print("Choose option from 1-5")

        elif choice == 3:
            backup = backup_with_limit()
            print(backup)
            print("Choose option from 1-5")

        elif choice == 4:
            finding = large_file_finder()
            if not finding:
                print("No file above 50MB was found")
            else:
                for item in finding:
                    print(item)
            print("Choose option from 1-5")

        elif choice == 5:
            break

        else:
            print("Wrong input, try 1-5")
            continue


if __name__ == "__main__":
    main()
