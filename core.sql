BEGIN;
--
-- Create model AccessRecord
--
CREATE TABLE "core_accessrecord" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "user_count" integer NOT NULL, "view_count" integer NOT NULL);
--
-- Create model Page
--
CREATE TABLE "core_page" ("id" char(32) NOT NULL PRIMARY KEY, "code" varchar(64) NOT NULL UNIQUE, "name" varchar(64) NOT NULL, "pre_page" char(32) NULL, "next_page" char(32) NULL);
--
-- Create model PageResource
--
CREATE TABLE "core_pageresource" ("id" char(32) NOT NULL PRIMARY KEY, "type" varchar(2) NOT NULL, "resource" varchar(100) NOT NULL, "page_id" char(32) NOT NULL REFERENCES "core_page" ("id"));
--
-- Create model Roll
--
CREATE TABLE "core_roll" ("id" char(32) NOT NULL PRIMARY KEY, "code" varchar(64) NOT NULL UNIQUE, "name" varchar(64) NOT NULL, "page_count" integer NULL, "start_page" char(32) NULL, "end_page" char(32) NULL, "qianziwen" varchar(8) NULL, "remark" text NULL);
--
-- Create model Series
--
CREATE TABLE "core_series" ("id" char(32) NOT NULL PRIMARY KEY, "code" varchar(64) NOT NULL UNIQUE, "name" varchar(64) NOT NULL, "type" varchar(2) NOT NULL, "volume_count" integer NULL, "sutra_count" integer NULL, "dynasty" varchar(64) NULL, "historic_site" varchar(64) NULL, "publish_name" varchar(64) NULL, "publish_date" date NULL, "publish_edition" smallint NULL, "publish_prints" smallint NULL, "publish_ISBN" varchar(64) NULL, "remark" text NULL);
--
-- Create model Sutra
--
CREATE TABLE "core_sutra" ("id" char(32) NOT NULL PRIMARY KEY, "code" varchar(64) NOT NULL UNIQUE, "name" varchar(64) NOT NULL, "type" varchar(2) NOT NULL, "clazz" varchar(64) NULL, "dynasty" varchar(64) NULL, "historic_site" varchar(64) NULL, "roll_count" integer NULL, "start_page" char(32) NULL, "end_page" char(32) NULL, "qianziwen" varchar(8) NULL, "remark" text NULL, "series_id" char(32) NULL REFERENCES "core_series" ("id"));
--
-- Create model Translator
--
CREATE TABLE "core_translator" ("id" char(32) NOT NULL PRIMARY KEY, "name" varchar(64) NOT NULL, "type" varchar(2) NOT NULL, "remark" text NULL);
--
-- Create model Volume
--
CREATE TABLE "core_volume" ("id" char(32) NOT NULL PRIMARY KEY, "code" varchar(64) NOT NULL UNIQUE, "name" varchar(64) NOT NULL, "start_page" char(32) NULL, "end_page" char(32) NULL, "remark" text NULL, "series_id" char(32) NULL REFERENCES "core_series" ("id"));
--
-- Add field translator to sutra
--
ALTER TABLE "core_sutra" RENAME TO "core_sutra__old";
CREATE TABLE "core_sutra" ("id" char(32) NOT NULL PRIMARY KEY, "code" varchar(64) NOT NULL UNIQUE, "name" varchar(64) NOT NULL, "type" varchar(2) NOT NULL, "clazz" varchar(64) NULL, "dynasty" varchar(64) NULL, "historic_site" varchar(64) NULL, "roll_count" integer NULL, "start_page" char(32) NULL, "end_page" char(32) NULL, "qianziwen" varchar(8) NULL, "remark" text NULL, "series_id" char(32) NULL REFERENCES "core_series" ("id"), "translator_id" char(32) NULL REFERENCES "core_translator" ("id"));
INSERT INTO "core_sutra" ("series_id", "end_page", "roll_count", "dynasty", "historic_site", "clazz", "qianziwen", "type", "code", "start_page", "id", "translator_id", "name", "remark") SELECT "series_id", "end_page", "roll_count", "dynasty", "historic_site", "clazz", "qianziwen", "type", "code", "start_page", "id", NULL, "name", "remark" FROM "core_sutra__old";
DROP TABLE "core_sutra__old";
CREATE INDEX "core_pageresource_page_id_b4179094" ON "core_pageresource" ("page_id");
CREATE INDEX "core_volume_series_id_94c6ff67" ON "core_volume" ("series_id");
CREATE INDEX "core_sutra_series_id_62f05234" ON "core_sutra" ("series_id");
CREATE INDEX "core_sutra_translator_id_d55eb245" ON "core_sutra" ("translator_id");
--
-- Add field series to roll
--
ALTER TABLE "core_roll" RENAME TO "core_roll__old";
CREATE TABLE "core_roll" ("id" char(32) NOT NULL PRIMARY KEY, "code" varchar(64) NOT NULL UNIQUE, "name" varchar(64) NOT NULL, "page_count" integer NULL, "start_page" char(32) NULL, "end_page" char(32) NULL, "qianziwen" varchar(8) NULL, "remark" text NULL, "series_id" char(32) NULL REFERENCES "core_series" ("id"));
INSERT INTO "core_roll" ("series_id", "end_page", "page_count", "id", "qianziwen", "name", "remark", "code", "start_page") SELECT NULL, "end_page", "page_count", "id", "qianziwen", "name", "remark", "code", "start_page" FROM "core_roll__old";
DROP TABLE "core_roll__old";
CREATE INDEX "core_roll_series_id_439211d5" ON "core_roll" ("series_id");
--
-- Add field sutra to roll
--
ALTER TABLE "core_roll" RENAME TO "core_roll__old";
CREATE TABLE "core_roll" ("id" char(32) NOT NULL PRIMARY KEY, "code" varchar(64) NOT NULL UNIQUE, "name" varchar(64) NOT NULL, "page_count" integer NULL, "start_page" char(32) NULL, "end_page" char(32) NULL, "qianziwen" varchar(8) NULL, "remark" text NULL, "series_id" char(32) NULL REFERENCES "core_series" ("id"), "sutra_id" char(32) NULL REFERENCES "core_sutra" ("id"));
INSERT INTO "core_roll" ("sutra_id", "series_id", "end_page", "page_count", "id", "qianziwen", "name", "remark", "code", "start_page") SELECT NULL, "series_id", "end_page", "page_count", "id", "qianziwen", "name", "remark", "code", "start_page" FROM "core_roll__old";
DROP TABLE "core_roll__old";
CREATE INDEX "core_roll_series_id_439211d5" ON "core_roll" ("series_id");
CREATE INDEX "core_roll_sutra_id_f09dc575" ON "core_roll" ("sutra_id");
--
-- Add field roll to page
--
ALTER TABLE "core_page" RENAME TO "core_page__old";
CREATE TABLE "core_page" ("id" char(32) NOT NULL PRIMARY KEY, "code" varchar(64) NOT NULL UNIQUE, "name" varchar(64) NOT NULL, "pre_page" char(32) NULL, "next_page" char(32) NULL, "roll_id" char(32) NULL REFERENCES "core_roll" ("id"));
INSERT INTO "core_page" ("next_page", "id", "pre_page", "name", "code", "roll_id") SELECT "next_page", "id", "pre_page", "name", "code", NULL FROM "core_page__old";
DROP TABLE "core_page__old";
CREATE INDEX "core_page_roll_id_e9714047" ON "core_page" ("roll_id");
--
-- Add field series to page
--
ALTER TABLE "core_page" RENAME TO "core_page__old";
CREATE TABLE "core_page" ("id" char(32) NOT NULL PRIMARY KEY, "code" varchar(64) NOT NULL UNIQUE, "name" varchar(64) NOT NULL, "pre_page" char(32) NULL, "next_page" char(32) NULL, "roll_id" char(32) NULL REFERENCES "core_roll" ("id"), "series_id" char(32) NULL REFERENCES "core_series" ("id"));
INSERT INTO "core_page" ("series_id", "next_page", "id", "pre_page", "name", "code", "roll_id") SELECT NULL, "next_page", "id", "pre_page", "name", "code", "roll_id" FROM "core_page__old";
DROP TABLE "core_page__old";
CREATE INDEX "core_page_roll_id_e9714047" ON "core_page" ("roll_id");
CREATE INDEX "core_page_series_id_7cecce9e" ON "core_page" ("series_id");
--
-- Add field sutra to page
--
ALTER TABLE "core_page" RENAME TO "core_page__old";
CREATE TABLE "core_page" ("id" char(32) NOT NULL PRIMARY KEY, "code" varchar(64) NOT NULL UNIQUE, "name" varchar(64) NOT NULL, "pre_page" char(32) NULL, "next_page" char(32) NULL, "roll_id" char(32) NULL REFERENCES "core_roll" ("id"), "series_id" char(32) NULL REFERENCES "core_series" ("id"), "sutra_id" char(32) NULL REFERENCES "core_sutra" ("id"));
INSERT INTO "core_page" ("sutra_id", "series_id", "next_page", "id", "pre_page", "name", "code", "roll_id") SELECT NULL, "series_id", "next_page", "id", "pre_page", "name", "code", "roll_id" FROM "core_page__old";
DROP TABLE "core_page__old";
CREATE INDEX "core_page_roll_id_e9714047" ON "core_page" ("roll_id");
CREATE INDEX "core_page_series_id_7cecce9e" ON "core_page" ("series_id");
CREATE INDEX "core_page_sutra_id_a7e182d3" ON "core_page" ("sutra_id");
--
-- Add field volume to page
--
ALTER TABLE "core_page" RENAME TO "core_page__old";
CREATE TABLE "core_page" ("id" char(32) NOT NULL PRIMARY KEY, "code" varchar(64) NOT NULL UNIQUE, "name" varchar(64) NOT NULL, "pre_page" char(32) NULL, "next_page" char(32) NULL, "roll_id" char(32) NULL REFERENCES "core_roll" ("id"), "series_id" char(32) NULL REFERENCES "core_series" ("id"), "sutra_id" char(32) NULL REFERENCES "core_sutra" ("id"), "volume_id" char(32) NULL REFERENCES "core_volume" ("id"));
INSERT INTO "core_page" ("sutra_id", "series_id", "next_page", "volume_id", "id", "pre_page", "name", "code", "roll_id") SELECT "sutra_id", "series_id", "next_page", NULL, "id", "pre_page", "name", "code", "roll_id" FROM "core_page__old";
DROP TABLE "core_page__old";
CREATE INDEX "core_page_roll_id_e9714047" ON "core_page" ("roll_id");
CREATE INDEX "core_page_series_id_7cecce9e" ON "core_page" ("series_id");
CREATE INDEX "core_page_sutra_id_a7e182d3" ON "core_page" ("sutra_id");
CREATE INDEX "core_page_volume_id_a7147cf8" ON "core_page" ("volume_id");
COMMIT;
