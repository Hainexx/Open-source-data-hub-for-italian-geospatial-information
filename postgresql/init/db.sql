-- POSTGIS Extension
CREATE EXTENSION IF NOT EXISTS postgis;

------------------------------------------------------
--						TABLES						--
------------------------------------------------------

CREATE TABLE tb_nations (
    id SERIAL,
    name text NOT NULL,
    pretty_name text NULL,
	geometry geometry(MultiPolygon, 4326) NOT NULL
);

CREATE UNIQUE INDEX ix_nations on tb_nations (id);

CREATE TABLE tb_regions (
    id SERIAL,
	id_nation int NOT NULL,
    name text NOT NULL,
    pretty_name text NULL,
	geometry geometry(MultiPolygon, 4326) NOT NULL
);

CREATE UNIQUE INDEX ix_regions on tb_regions (id);

ALTER TABLE tb_regions ADD CONSTRAINT id_nation_fk
	FOREIGN KEY (id_nation) REFERENCES tb_nations(id);

CREATE TABLE tb_cities (
    id SERIAL,
	id_region int NOT NULL,
    name text NOT NULL,
    pretty_name text NULL,
	geometry geometry(MultiPolygon, 4326) NOT NULL
);

CREATE UNIQUE INDEX ix_cities on tb_cities (id);

ALTER TABLE tb_cities ADD CONSTRAINT id_region_fk
	FOREIGN KEY (id_region) REFERENCES tb_regions(id);

CREATE TABLE tb_buildings_footprints (
    id SERIAL,
	id_city int NOT NULL,
    geometry geometry(MultiPolygon, 4326) NOT NULL
);

CREATE UNIQUE INDEX ix_building_footprints on tb_buildings_footprints (id);

ALTER TABLE tb_buildings_footprints ADD CONSTRAINT id_city_fk
	FOREIGN KEY (id_city) REFERENCES tb_cities(id);


