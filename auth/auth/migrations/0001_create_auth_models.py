from yoyo import step

step(
    "CREATE TABLE IF NOT EXISTS profileuser( \
        id SERIAL NOT NULL PRIMARY KEY, \
        username VARCHAR(32) NOT NULL UNIQUE, \
        email VARCHAR(128) UNIQUE, \
        full_name VARCHAR(128), \
        phone VARCHAR(32), \
        password VARCHAR(128) NOT NULL, \
        address VARCHAR(128) \
    )",
    "DROP TABLE profileuser",
)

step(
    "INSERT INTO profileuser(id, username, email, full_name, password) \
    VALUES(1, 'Ivan', 'ivan@mail.ru', 'Петров Иван Сергеевич', '$2b$12$VMhRsWfY0zagDclPtY/N2.GdkKPyQLikJu3bhLFGWt77ynOHkzQNm')"
)

step(
    "INSERT INTO profileuser(id, username, email, full_name, password) \
    VALUES(2, 'Petr', 'petr@yandex.ru', 'Васин Петр Сергеевич', '$2b$12$DZBeh0mfviXYE90kZQeUyeFKLY6.SidgrjHFG.OrahBpH.AiiZaLq')"
)

step(
    "INSERT INTO profileuser(id, username, password) \
    VALUES(3, 'user', '$2b$12$/moQbWO7fj5kO/jDGRdAuOqIJ9MJC7OnFsOr8aq32BmXPwsW4Tgni')"
)
