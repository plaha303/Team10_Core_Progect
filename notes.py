def save_note():
    title = input("Введіть заголовок нотатки: ")
    content = input("Введіть текстову інформацію: ")
    tags = input("Введіть теги через кому (необов'язково): ").split(',')

    with open("notes.txt", "a") as file:
        file.write(f"{title}\n{content}\n{' '.join(tags)}\n")
    print("Нотатка збережена.")


def search_notes():
    keyword = input("Введіть ключове слово для пошуку: ")

    with open("notes.txt", "r") as file:
        notes = file.read().split("\n\n")

    found = False
    for note in notes:
        title, content, tags = note.split("\n", 2)
        if keyword.lower() in title.lower() or keyword.lower() in content.lower() or keyword.lower() in tags.lower():
            print(f"\nЗаголовок: {title}\nТекст: {content}\nТеги: {tags}")
            found = True

    if not found:
        print("За вашим запитом нічого не знайдено.")


def edit_note():
    title_to_edit = input("Введіть заголовок нотатки, яку бажаєте редагувати: ")

    with open("notes.txt", "r") as file:
        notes = file.read().split("\n\n")

    found = False
    for i, note in enumerate(notes):
        title, content, tags = note.split("\n", 2)
        if title == title_to_edit:
            found = True
            new_title = input("Введіть новий заголовок нотатки: ")
            new_content = input("Введіть нову текстову інформацію: ")
            new_tags = input("Введіть нові теги через кому (необов'язково): ").split(',')
            notes[i] = f"{new_title}\n{new_content}\n{' '.join(new_tags)}"
            break

    if not found:
        print("Нотатку з таким заголовком не знайдено.")
        return

    with open("notes.txt", "w") as file:
        file.write("\n\n".join(notes))
    print("Нотатку змінено.")


def delete_note():
    title_to_delete = input("Введіть заголовок нотатки, яку бажаєте видалити: ")

    with open("notes.txt", "r") as file:
        notes = file.read().split("\n\n")

    found = False
    for i, note in enumerate(notes):
        title, _, _ = note.split("\n", 2)
        if title == title_to_delete:
            found = True
            del notes[i]
            break

    if not found:
        print("Нотатку з таким заголовком не знайдено.")
        return

    with open("notes.txt", "w") as file:
        file.write("\n\n".join(notes))
    print("Нотатку видалено.")


if __name__ == "__main__":
    while True:
        print("\nМеню:")
        print("1. Зберегти нотатку")
        print("2. Пошук нотатки")
        print("3. Редагувати нотатку")
        print("4. Видалити нотатку")
        print("5. Вийти")

        choice = input("Виберіть опцію (1/2/3/4/5): ")

        if choice == "1":
            save_note()
        elif choice == "2":
            search_notes()
        elif choice == "3":
            edit_note()
        elif choice == "4":
            delete_note()
        elif choice == "5":
            break
        else:
            print("Введена некоректна опція. Спробуйте ще раз.")
