-- Создание таблицы Запись на услуги
create table if not exists sign_up_for_services(
    id integer primary key autoincrement,
    name text not null,
    phone text not null,
    data datetime default (datetime('now', 'localtime')),
    master_id integer,
    status text default "waiting...",
    foreign key (master_id) references masters(id)
);

-- Создание таблицы Мастера
create table if not exists masters(
    id integer primary key autoincrement,
    first_name text not null,
    last_name text not null,
    middle_name text,
    phone text  not null
);

--Создание таблицы Услуги
create table if not exists services(
    id integer primary key autoincrement,
    title text unique not null,
    description text not null,
    price integer not null
);

--Создание таблицы masters_services
create table if not exists masters_services(
    master_id integer,
    service_id integer,
    foreign key (master_id) references masters(id),
    foreign key (service_id) references services(id)
);

--Создание таблицы appointments_services
create table if not exists appointments_services(
    appointment_id integer,
    service_id integer,
    foreign key (service_id) references services(id)
);

--Добавление мастера в таблицу Мастера
insert into masters (first_name, last_name, middle_name, phone)
values ("Марина", "Мандаринова", "Капибаровна", "89282282282");

--Добавление мастера в таблицу Мастера
insert into masters (first_name, last_name, middle_name, phone)
values ("Женечка", "Поляков", "Вовчикович", "89282282282");

--Добавление услуги в таблицу Услуги
insert into services (title, description, price)
values ("теплый нос", "Наращивание волос на носу", 600);

--Добавление услуги в таблицу Услуги
insert into services (title, description, price)
values ("теплое ухо", "Наращивание волос на ухе. Стоит в два раза больше, чем теплый нос, потому что нос 1, а ух 2", 1200);

--Добавление услуги в таблицу Услуги
insert into services (title, description, price)
values ("теплые зубы", "Наращивание волос всех зубах. Мы не стоматология, но во рот что-нибудь да засунем", 15000);

--Добавление услуги в таблицу Услуги
insert into services (title, description, price)
values ("холодная подмышка", "Побрить волосы на подмышке", 1800);

--Добавление услуги в таблицу Услуги
insert into services (title, description, price)
values ("холодные ноги", "Побрить волосы на ногах", 600);


--Соответствие мастера и услуг в таблице masters_services
insert into masters_services (master_id, service_id)
values (1, 2);

--Соответствие мастера и услуг в таблице masters_services
insert into masters_services (master_id, service_id)
values (1, 3);

--Соответствие мастера и услуг в таблице masters_services
insert into masters_services (master_id, service_id)
values (1, 4);

--Соответствие мастера и услуг в таблице masters_services
insert into masters_services (master_id, service_id)
values (2, 1);

--Соответствие мастера и услуг в таблице masters_services
insert into masters_services (master_id, service_id)
values (2, 3);

--Соответствие мастера и услуг в таблице masters_services
insert into masters_services (master_id, service_id)
values (2, 5);

--Добавление записи на услуги в таблицу Запись на услуги
insert into sign_up_for_services (name, phone, master_id)
values ("Павел", "8989898989", 1);

--Добавление записи на услуги в таблицу Запись на услуги
insert into sign_up_for_services (name, phone, master_id)
values ("Александр", "1212121212", 2);

--Добавление записи на услуги в таблицу Запись на услуги
insert into sign_up_for_services (name, phone, master_id)
values ("Яна", "5445455445", 2);

--Добавление записи на услуги в таблицу Запись на услуги
insert into sign_up_for_services (name, phone, master_id)
values ("Полина", "54124513662", 1);

--Соответствие записи на услугу с услугами в таблице appointments_services
insert into appointments_services (appointment_id, service_id)
values (1, 3);

--Соответствие записи на услугу с услугами в таблице appointments_services
insert into appointments_services (appointment_id, service_id)
values (1, 4);

--Соответствие записи на услугу с услугами в таблице appointments_services
insert into appointments_services (appointment_id, service_id)
values (2, 1);

--Соответствие записи на услугу с услугами в таблице appointments_services
insert into appointments_services (appointment_id, service_id)
values (2, 3);

--Соответствие записи на услугу с услугами в таблице appointments_services
insert into appointments_services (appointment_id, service_id)
values (2, 5);

--Соответствие записи на услугу с услугами в таблице appointments_services
insert into appointments_services (appointment_id, service_id)
values (3, 3);

--Соответствие записи на услугу с услугами в таблице appointments_services
insert into appointments_services (appointment_id, service_id)
values (4, 2);

--Соответствие записи на услугу с услугами в таблице appointments_services
insert into appointments_services (appointment_id, service_id)
values (4, 4);