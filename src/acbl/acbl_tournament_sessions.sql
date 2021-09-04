PRAGMA journal_mode=WAL;

DROP TABLE IF EXISTS "sessions";

CREATE TABLE "sessions" (
"acbl_number_session_id" VARCHAR NOT NULL PRIMARY KEY,
"acbl_number" VARCHAR NULL,
"mp_won" VARCHAR NULL,
"mp_color" VARCHAR NULL,
"percentage" VARCHAR NULL,
"score" VARCHAR NULL,
"sanction" VARCHAR NULL,
"event_id" VARCHAR NULL,
"session_id" VARCHAR NULL,
"trax_master_event_code" VARCHAR NULL,
"score_tournament_name" VARCHAR NULL,
"score_event_name" VARCHAR NULL,
"score_session_number" VARCHAR NULL,
"score_session_time_description" VARCHAR NULL,
"score_event_type" VARCHAR NULL,
"score_score_type" VARCHAR NULL,
"section" VARCHAR NULL,
"results_last_updated" VARCHAR NULL,
"session" VARCHAR NULL,
"_id" VARCHAR NULL,
"_event_id" VARCHAR NULL,
"id" VARCHAR NULL,
"session_number" VARCHAR NULL,
"start_date" VARCHAR NULL,
"start_time" VARCHAR NULL,
"description" VARCHAR NULL,
"event" VARCHAR NULL,
"tournament" VARCHAR NULL,
"date" VARCHAR NULL,
-- list of VARCHAR
FOREIGN KEY ("event") REFERENCES "event"(id) ON DELETE NO ACTION,
-- list of VARCHAR
FOREIGN KEY ("tournament") REFERENCES "tournament"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "tournament_chair";

CREATE TABLE "session" (
"_id" VARCHAR NULL,
"id" INT NOT NULL PRIMARY KEY,
"_event_id" VARCHAR NULL,
"sessions" VARCHAR NULL,
"session_number" VARCHAR NULL,
"start_date" VARCHAR NULL,
"start_time" VARCHAR NULL,
"description" VARCHAR NULL,
-- list of VARCHAR
FOREIGN KEY ("sessions") REFERENCES "sessions"(session_id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "event";

CREATE TABLE "event" (
"sanction" VARCHAR NULL,
"_id" VARCHAR NULL,
"_schedule_id" VARCHAR NULL,
"id" INT NOT NULL PRIMARY KEY,
"name" VARCHAR NULL,
"event_code" VARCHAR NULL,
"start_date" VARCHAR NULL,
"start_time" VARCHAR NULL,
"game_type" VARCHAR NULL,
"event_type" VARCHAR NULL,
"mp_limit" VARCHAR NULL,
"mp_color" VARCHAR NULL,
"mp_rating" VARCHAR NULL,
"is_charity" VARCHAR NULL,
"is_juniors" VARCHAR NULL,
"is_mixed" VARCHAR NULL,
"is_playthrough" VARCHAR NULL,
"is_seniors" VARCHAR NULL,
"is_side_game" VARCHAR NULL,
"is_womens" VARCHAR NULL,
"session_count" VARCHAR NULL
);

DROP TABLE IF EXISTS "tournament";

CREATE TABLE "tournament" (
"id" INT NOT NULL PRIMARY KEY,
"sessions" VARCHAR NULL,
"_schedule_id" VARCHAR NULL,
"sanction" VARCHAR NULL,
"alt_sanction" VARCHAR NULL,
"name" VARCHAR NULL,
"start_date" VARCHAR NULL,
"end_date" VARCHAR NULL,
"district" VARCHAR NULL,
"unit" VARCHAR NULL,
"category" VARCHAR NULL,
"type" VARCHAR NULL,
"mp_restrictions" VARCHAR NULL,
"allowed_conventions" VARCHAR NULL,
"schedule_pdf" VARCHAR NULL,
"schedule_link" VARCHAR NULL,
"last_updated" VARCHAR NULL,
"schedule_available" VARCHAR NULL,
"cancelled" VARCHAR NULL,
"contacts" VARCHAR NULL,
"locations" VARCHAR NULL,
-- list of VARCHAR
FOREIGN KEY ("sessions") REFERENCES "sessions"(session_id) ON DELETE NO ACTION,
-- list of VARCHAR
FOREIGN KEY ("contacts") REFERENCES "contacts"(id) ON DELETE NO ACTION,
-- list of VARCHAR
FOREIGN KEY ("locations") REFERENCES "locations"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "contacts";

CREATE TABLE "contacts" (
"id" INT NOT NULL PRIMARY KEY,
"sessions" VARCHAR NULL,
"tournament_chair" VARCHAR NULL,
"partnership_chair" VARCHAR NULL,
"director_in_charge" VARCHAR NULL,
-- list of VARCHAR
FOREIGN KEY ("sessions") REFERENCES "sessions"(session_id) ON DELETE NO ACTION,
-- list of VARCHAR
FOREIGN KEY ("tournament_chair") REFERENCES "tournament_chair"(id) ON DELETE NO ACTION,
-- list of VARCHAR
FOREIGN KEY ("partnership_chair") REFERENCES "partnership_chair"(id) ON DELETE NO ACTION,
-- list of VARCHAR
FOREIGN KEY ("director_in_charge") REFERENCES "director_in_charge"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "tournament_chair";

CREATE TABLE "tournament_chair" (
"id" INT NOT NULL PRIMARY KEY,
"sessions" VARCHAR NULL,
"first_name" VARCHAR NULL,
"last_name" VARCHAR NULL,
"email" VARCHAR NULL,
-- list of VARCHAR
FOREIGN KEY ("sessions") REFERENCES "sessions"(session_id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "partnership_chair";

CREATE TABLE "partnership_chair" (
"id" INT NOT NULL PRIMARY KEY,
"sessions" VARCHAR NULL,
"first_name" VARCHAR NULL,
"last_name" VARCHAR NULL,
"email" VARCHAR NULL,
-- list of VARCHAR
FOREIGN KEY ("sessions") REFERENCES "sessions"(session_id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "director_in_charge";

CREATE TABLE "director_in_charge" (
"id" INT NOT NULL PRIMARY KEY,
"sessions" VARCHAR NULL,
"first_name" VARCHAR NULL,
"last_name" VARCHAR NULL,
-- list of VARCHAR
FOREIGN KEY ("sessions") REFERENCES "sessions"(session_id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "locations";

CREATE TABLE "locations" (
"id" INT NOT NULL PRIMARY KEY,
"sessions" VARCHAR NULL,
"sanction" VARCHAR NULL,
"_id" VARCHAR NULL,
"name" VARCHAR NULL,
"address_1" VARCHAR NULL,
"address_2" VARCHAR NULL,
"city" VARCHAR NULL,
"state" VARCHAR NULL,
"country" VARCHAR NULL,
"postal" VARCHAR NULL,
"phone" VARCHAR NULL,
-- list of VARCHAR
FOREIGN KEY ("sessions") REFERENCES "sessions"(session_id) ON DELETE NO ACTION
);

