CREATE TABLE MarvelCharacters1(
id INTEGER PRIMARY KEY AUTOINCREMENT,
page_id INTEGER,
name TEXT,
urlslug TEXT,
EYE TEXT,
HAIR TEXT,
SEX TEXT,
GSM TEXT,
ALIVE TEXT,
APPEARANCES TEXT,
FIRST_APPEARANCES TEXT,
Year INTEGER
);

insert into MarvelCharacters1(page_id, name, urlslug, EYE, HAIR, SEX, GSM, ALIVE, APPEARANCES, FIRST_APPEARANCES, Year) values (1678, "Spider-Man (Peter Parker)",	"\/Spider-Man_(Peter_Parker)", "Hazel Eyes","Brown Hair","Male Characters",	"Secret Identity","Living Characters",4043,	"Aug-62", 1962);
select * from MarvelCharacters1;