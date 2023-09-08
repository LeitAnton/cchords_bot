CREATE TABLE IF NOT EXISTS user
(
    user_id  INT PRIMARY KEY,
    username VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS song
(
    song_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_name VARCHAR(255),
    song_name   VARCHAR(255),
    link        TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS un_song_id ON song (artist_name, song_name);


CREATE TABLE IF NOT EXISTS favorite
(
    favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    song_id     INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (user_id),
    FOREIGN KEY (song_id) REFERENCES song (song_id)
);
CREATE UNIQUE INDEX IF NOT EXISTS un_fav_id ON favorite (user_id, song_id);

CREATE TABLE IF NOT EXISTS history
(
    history_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id           INTEGER NOT NULL,
    song_id           INTEGER NOT NULL,
    viewing_timestamp VARCHAR(26),
    FOREIGN KEY (user_id) REFERENCES user (user_id),
    FOREIGN KEY (song_id) REFERENCES song (song_id)
);
CREATE UNIQUE INDEX IF NOT EXISTS un_his_id ON history (user_id, song_id);

CREATE TABLE IF NOT EXISTS temporary_buffer
(
    temporary_id INTEGER PRIMARY KEY NOT NULL,
    artist_name  VARCHAR(255),
    song_name    VARCHAR(255),
    link         TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS un_tem_id ON temporary_buffer (artist_name, song_name);
