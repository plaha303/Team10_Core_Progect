# Проєктне завдання команди DO-IT.

Команда №10

GOIT > Курс > Python Developer > Python core > Проектна робота

# Персональний помічник

Проєкт створення “персонального помічника” з інтерфейсом командного рядка.

Наш “Персональний помічник” є консольним ботом, який спілкується з користувачем за допомогою командного рядка, отримуючи команди, та виконуючи потрібні дії.

“Персональний помічник” вміє:

- зберігає контакти з іменами, адресами, номерами телефонів, email та днями народження до книги контактів;
- виводить список контактів, у яких день народження через задану кількість днів від поточної дати;
- перевіряє правильність введеного номера телефону та email під час створення або редагування запису та повідомляє - користувачеві у разі некоректного введення;
- здійснює пошук контактів серед контактів книги;
- редагує та видаляє записи з книги контактів;
- зберігає нотатки з текстовою інформацією;
- проводить пошук за нотатками;
- редагує та видаляє нотатки;
- додає в нотатки "теги", ключові слова, що описують тему чи предмет запису;
- здійснює пошук та сортування нотаток за ключовими словами (тегами);
- бот вміє аналізувати введений текст та вгадує, що хоче від нього користувач і пропонує найближчу команду для виконання
- вміє сортувати файли у зазначеній папці за категоріями (зображення, документи, відео та ін.).

# Примітка

“Персональний помічник” - сортує файли у зазначеній папці за такими категоріями:

CATEGORIES = 
      "Audio": [".mp3", ".aiff", ".wav", ".aac", ".flac"]
      "Documents": [".docx", ".doc", ".txt", ".pdf", ".xls", ".xlsx", ".pptx", ".rtf"]
      "Video": [".avi", ".mp4", ".mov", ".mkv", ".mpeg"],
      "Image": [".jpeg", ".png", ".pcd", ".jpg", ".svg", ".tiff", ".raw", ".gif", ".bmp"]
      "Archive": [".zip", ".7-zip", ".7zip", ".rar", ".gz", ".tar"]
      "Book": [".fb2", ".mobi"]


Всі інші файли будуть розподілені у категорію "Other".

## Використання

Додаток підтримує наступні команди:

         hello  -> відображає вітальне повідомлення.
         add -> додає новий контакт.
         add birthday -> додати день народження до контакту
         add note -> додати нову примітку
         add tag -> додати новий тег до нотатки.
         edit birthday -> змінює існуюче значення дня народження контакту
         days to birthday -> показує, скільки днів залишилося до дня народження
         show birthday -> показати список контактів, чий день народження є вказаним числом днів від поточної дати                               
         edit phone -> змінює номер телефону наявного контакту.
         del phone -> видалити номер із контакту.
         del note -> видалити примітку.
         add phone -> додає телефон до існуючого контакту
         change phone -> замінити старий номер на новий
         change note -> змінити існуючу примітку.
         show all -> відображає всі контакти та їхні номери телефонів.
         show notes -> показати всі нотатки.
         search by name -> шукає контакти, в яких ім'я збігається
         search by phone -> пошук контактів із відповідним номером телефону
         search note by tag -> шукати нотатку з тегом.
         search note -> Пошук примітки в тексті
         sort folder -> сортувати файли за категоріями видаляє порожні папки в шляху до папки, указаному користувачем              
         help -> відображає список доступних команд.
         exit, close, good bye -> вихід з програми.

## Особливості роботи
		 

Проєкт збережений в окремому репозиторії та  загальнодоступний https://github.com/plaha303/Team10_Core_Progect
Проєкт містить докладну інструкцію щодо встановлення та використання;
Проєкт встановлюється як Python-пакет та може бути викликаний у будь-якому місці системи відповідною командою після встановлення;
Персональний помічник зберігає інформацію на жорсткому диску в папці користувача і може бути перезапущений без втрати даних.

## Опис роботи

Клас AddressBook унаслідується від UserDict, та відповідає за логіку пошуку за записами до цього класу та 
клас Record, який відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name.

Записи Record в AddressBook зберігаються як значення у словнику. Як ключі використовується значення Record.name.value.
Record зберігає об'єкт Name та список об'єктів Phone в окремому атрибуті.
Record реалізує методи для додавання/видалення/редагування об'єктів Phone.
AddressBook реалізує метод add_record, який додає Record у self.data.

Додано пагінацію (посторінкове виведення) для AddressBook для ситуацій, коли книга дуже велика і потрібно показати вміст частинами, а не все одразу. Реалізуємо це через створення ітератора за записами.


## Створення та встановлення “Персонального помічника”

Щоб встановити програму потрібно зайти у теку де знаходиться установчий пакет та у командному рядку ввести  'pip install Address-Book' . (або python setup.py install, потрібні права адміністратора).

Коли пакет встановлений в системі, скрипт можна викликати у будь-якому місці з консолі командою book.

 ## Команда проекта”

 
     Евгеній Плахотін - Team-lead
     Сергій Андрейко - Scrum master
     Влад Кірілов
     Леонід Шершун
     Дулін Сергій
 
