#Задание 1
select ALIVE, count(*)
from MarvelCharacters
where ALIVE is not null
group by ALIVE
;

#Задание 2
select EYE, avg(APPEARANCES)
from MarvelCharacters
where eye is not null
group by EYE
;

#Задание 3
select EYE, max(APPEARANCES)
from MarvelCharacters
where eye is not null
group by EYE
;

#Задание 4
select identify, min(APPEARANCES)
from MarvelCharacters
where eye is not null identify in "Public Identity"
group by identify
;

#Задание 5
select SEX, count(*)
from MarvelCharacters
where SEX is not null
group by SEX
order by count(*) desc;
;

#Задание 6
select identify, avg(Year)
from MarvelCharacters
where identify is not null
group by identify
;

#Задание 7
select eye, count(*)
from MarvelCharacters
where eye is not null and  ALIVE = "Living Characters"
group by eye
order by count(*) desc
;

#Задание 8
select eye, min(APPEARANCES), max(APPEARANCES)
from MarvelCharacters
where eye is not null
group by eye
;

#Задание 9
select identify, count(*)
from MarvelCharacters
where identify is not null and ALIVE = "Deceased Characters"
group by identify
;

#Задание 10
select eye, avg(Year)
from MarvelCharacters
where eye is not null
group by eye
order by avg(Year) desc
;

#Задание 11
select name, APPEARANCES
from MarvelCharacters
where APPEARANCES = (
    select max(APPEARANCES)
    from MarvelCharacters
);


#Задание 12
select name, Year, APPEARANCES
from MarvelCharacters
where Year = (
    select year
    from MarvelCharacters
    where APPEARANCES = (
        select max(APPEARANCES)
        from MarvelCharacters
    )
);

#Задание 13
select name, APPEARANCES, ALIVE
from MarvelCharacters
where ALIVE = "Living Characters" and APPEARANCES = (
    select min(APPEARANCES)
    from MarvelCharacters
);

#Задание 14
select name, hair, appearances
from MarvelCharacters
where hair = "Blond Hair" and APPEARANCES = (
    select max(appearances)
    from MarvelCharacters
    where hair = "Blond Hair"
);

#Задание 15
select name, identify, appearances
from MarvelCharacters
where identify = "Public Identity" and APPEARANCES = (
    select min(appearances)
    from MarvelCharacters
);