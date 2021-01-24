-- upgrade --
CREATE TABLE IF NOT EXISTS "content" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" VARCHAR(5) NOT NULL  DEFAULT 'Movie',
    "title" VARCHAR(400) NOT NULL,
    "date_added" DATE NOT NULL,
    "release_year" INT,
    "rating" VARCHAR(8) NOT NULL  DEFAULT 'NR',
    "duration" INT NOT NULL,
    "description" TEXT
);
COMMENT ON COLUMN "content"."type" IS 'Either ``\"Show\"`` or ``\"Movie\"``';
COMMENT ON COLUMN "content"."rating" IS 'TV or MPAA Rating';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" TEXT NOT NULL
);
