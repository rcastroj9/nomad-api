drop table ifexists users;
create table users (
    id integer primary key autoincrement,
    name text not null,
    email text not null, 
    password text not null
    )
    
drop table ifexists trips;
create table trips (
    name text not null,
    cost double not null, 
    destination text not null,
    travel_date integer not null,
    saving_plan text not null
    )