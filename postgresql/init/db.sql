-- POSTGIS Extension
CREATE EXTENSION IF NOT EXISTS postgis;

------------------------------------------------------
--						TABLES						--
------------------------------------------------------

CREATE TABLE tb_nations (
    id SERIAL,
    name text NOT NULL,
    pretty_name text NULL,
	geometry geometry(MultiPolygon, 4326) NULL
);

CREATE UNIQUE INDEX ix_nations on tb_nations (name);

CREATE TABLE tb_regions (
    id SERIAL,
	id_nation int NOT NULL,
    name text NOT NULL,
    pretty_name text NULL,
	geometry geometry(MultiPolygon, 4326) NULL
);

CREATE UNIQUE INDEX ix_regions on tb_regions (name);

ALTER TABLE tb_regions ADD CONSTRAINT id_nation_fk
	FOREIGN KEY (id_nation) REFERENCES tb_nations(id);

CREATE TABLE tb_cities (
    id SERIAL,
	id_region int NULL,
    name text NOT NULL,
    pretty_name text NULL,
	geometry geometry(MultiPolygon, 4326) NULL
);

CREATE UNIQUE INDEX ix_cities on tb_cities (name);

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


CREATE TABLE stg_buildings_footprints (
    id text NOT NULL,
    city_id INT NOT NULL,
    city_name text NOT NULL,
    geometry text NOT NULL
);

CREATE VIEW vw_buildings_footprints AS

    SELECT c.name, bf.id, ST_AsText(bf.geometry)
    FROM tb_buildings_footprints bf
    INNER JOIN tb_cities c on c.id = bf.id_city;

CREATE FUNCTION fn_stg_to_tb_buildings_footprint() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	INSERT INTO tb_cities (name) VALUES (NEW.city_name)
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO tb_buildings_footprints(id_city, geometry) 
    SELECT (SELECT id from tb_cities WHERE name = NEW.city_name), 
            ST_SetSRID( ST_Multi(ST_Force2D(ST_GeomFromText(NEW.geometry))), 4326);
 
    RETURN NEW;
END
$$;

CREATE TRIGGER tr_stg_to_tb_buildings_footprint
BEFORE INSERT OR UPDATE ON stg_buildings_footprints
FOR EACH ROW EXECUTE PROCEDURE fn_stg_to_tb_buildings_footprint();

COPY stg_buildings_footprints FROM '/files/raw_data/geoportale_lombardia/complete_dataset.csv' DELIMITER ',' CSV HEADER;

INSERT INTO tb_nations(name, pretty_name) VALUES ('italy', 'Italy');
INSERT INTO tb_regions(name, pretty_name, id_nation) VALUES ('lombardy', 'Lombardy', 1);