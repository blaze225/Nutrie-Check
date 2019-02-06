drop table if exists products;
drop table if exists product_ingredients;
drop table if exists safety_ratings;

create table products (
	barcode text primary key not null,
	product_type text not null
);

create table product_ingredients (
	barcode text not null,
	ingredient_name text not null,
	primary key (barcode, ingredient_name) 
);

create table safety_ratings (
	product_type text not null,
	ingredient_name text not null,
	safety integer not null,
	primary key (product_type, ingredient_name) 
);
