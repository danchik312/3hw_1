CREATE_USER_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS telegramm_users(
id INTEGER PRIMARY KEY,
first_name TEXT,
tg_id INTEGER,
UNIQUE(tg_id))'''
INSERT_USER = '''INSERT OR IGNORE INTO telegramm_users VALUES (?, ?, ?)'''

SELECT_USER = '''SELECT * FROM telegramm_users'''