-- todo
-- Is ON DELETE NO ACTION still needed?
-- Should ON UPDATE NO ACTION needed to be added?
-- Use? ON DELETE CASCADE ON UPDATE NO ACTION
-- reject any incomplete input. club-results/268011/details/211798.data.sql
-- reject any NULL instances which have a few instances. A few files appear incomplete and have many different columns of NULL instances. Only some are commented on below.
-- concerned that over-zelous rejecting can lead to problematic consistency issues. e.g. non-INT player numbers. Better to accept most but validate and ignore in code?

PRAGMA journal_mode=WAL;

DROP TABLE IF EXISTS "events";

CREATE TABLE "events" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NOT NULL,
"club_tournament_id" INT NULL,
"name" VARCHAR NOT NULL,
"organization" VARCHAR NOT NULL,
"club_name" VARCHAR NOT NULL,
"club_id_number" INT NOT NULL,
"type" VARCHAR NOT NULL,
"rating" INT NOT NULL,
"number_of_sessions" INT NOT NULL,
"start_date" VARCHAR NOT NULL,
"end_date" VARCHAR NOT NULL,
-- reject a few NULL board_scoring_method instances.
"board_scoring_method" VARCHAR NOT NULL,
"stratification_type" VARCHAR NOT NULL,
"winner_type" INT NULL,
"transaction_id" VARCHAR NULL,
"club_class" INT NOT NULL,
"number_of_restrictions" INT NOT NULL,
"sanction" VARCHAR NULL,
"top_override" VARCHAR NULL,
"match_scoring_method" VARCHAR NULL,
"acbl_handicap_type" VARCHAR NULL,
"acbl_board_top" INT NULL,
"deleted_at" VARCHAR NULL,
"deleted_by" VARCHAR NULL,
"rule_engine" INT NULL,
"concurrent_limited_tables" REAL NULL,
"bbo_event_description" VARCHAR NULL,
"bbo_tournament_id" VARCHAR NULL,
"bbo_unix_timestamp" INT NULL,
"maxRoundNumber" INT NULL,
"rounds" VARCHAR NULL,
"program_name" VARCHAR NULL,
-- reject a few NULL tb_count e.g. club-results/106880/details/339368.data.sql
"tb_count" REAL NOT NULL,
"hasOverallStrats" BOOL NULL,
"hasSectionStrats" BOOL NULL,
"hashandicapScore" BOOL NULL,
"resultExists" BOOL NULL,
"olExists" BOOL NULL,
"contractExists" BOOL NULL,
"movieExists" BOOL NULL,
-- accept the many NULL maxBoardsCount instances. deprecated?
"maxBoardsCount" INT NULL,
-- reject 3000 NULL bboGameLinks?
"bboGameLinks" VARCHAR NULL,
"authCheck" BOOL NOT NULL,
"employee" BOOL NULL,
"mpc_test" BOOL NULL,
"ff_rule_engine" BOOL NULL,
"canAccessGameFile" BOOL NULL,
"document_id" VARCHAR NOT NULL,
"hasPbn" BOOL NOT NULL,
"mp_engine" VARCHAR NOT NULL,
"hr_delay" BOOL NOT NULL,
"bwsfileExists" BOOL NOT NULL,
-- accept the many NULL files instances. deprecated?
"files" VARCHAR NULL,
"board_sort" INT NOT NULL,
"from_score" BOOL NOT NULL,
"club" INT NOT NULL,
-- reject 250 NULL club_session instances.
"club_session" VARCHAR NOT NULL,
"env" VARCHAR NOT NULL ,
"stratvalues" VARCHAR NOT NULL,
"mpLimits" VARCHAR NOT NULL,
"club_director_name" VARCHAR NULL,
"mobile" BOOL NULL,
"sort_by_pair" BOOL NULL,
"game_type" INT NOT NULL,
"strats" VARCHAR NOT NULL,
"uploads" VARCHAR NOT NULL,
"sessions" VARCHAR NOT NULL,
-- list of VARCHAR
FOREIGN KEY ("rounds") REFERENCES "rounds"(id) ON DELETE NO ACTION,
-- list of VARCHAR
FOREIGN KEY ("bboGameLinks") REFERENCES "bboGameLinks"(id) ON DELETE NO ACTION,
-- single INT
FOREIGN KEY ("club") REFERENCES "club"(id) ON DELETE NO ACTION,
-- list of VARTYPE
FOREIGN KEY ("stratvalues") REFERENCES "stratvalues"(id) ON DELETE NO ACTION,
-- list of INTs
FOREIGN KEY ("files") REFERENCES "files"(id) ON DELETE NO ACTION
-- single INT
FOREIGN KEY ("game_type") REFERENCES "game_type"(id) ON DELETE NO ACTION,
-- list of INTs
FOREIGN KEY ("strats") REFERENCES "strats"(id) ON DELETE NO ACTION,
-- list of INTs
FOREIGN KEY ("uploads") REFERENCES "uploads"(id) ON DELETE NO ACTION,
-- list of INTs
FOREIGN KEY ("sessions") REFERENCES "sessions"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "awards";

CREATE TABLE "awards" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"player_id" INT NOT NULL,
"comp_group_id" INT NOT NULL,
-- reject 47,000 non-INT id_number e.g. NM, NA, HARR, HI, tmp:...?
"id_number" INT NULL,
"type" VARCHAR NOT NULL,
"final" INT NOT NULL,
"rank" VARCHAR NOT NULL,
"locus" VARCHAR NOT NULL,
"total" REAL NOT NULL,
-- NULL or list of always length 1 of INT? Why is this a list?
"pigment" VARCHAR NULL UNIQUE,
FOREIGN KEY ("pigment") REFERENCES "pigment"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "awards_score";

CREATE TABLE "awards_score" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"player_id" INT NOT NULL,
"total" REAL NOT NULL,
"type" VARCHAR NOT NULL,
"final" BOOL NOT NULL,
-- list of always length 1 of INT? Why is this a list?
"pigment" VARCHAR NOT NULL UNIQUE,
FOREIGN KEY ("pigment") REFERENCES "pigment"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "bboGameLinks";

CREATE TABLE "bboGameLinks" (
-- id is composed of <event(id)>-<list num>
"id" VARCHAR NOT NULL PRIMARY KEY,
"events" INT NOT NULL,
"n" VARCHAR NULL,
"s" VARCHAR NULL,
"e" VARCHAR NULL,
"w" VARCHAR NULL,
"d" VARCHAR NULL,
"v" VARCHAR NULL,
"b" VARCHAR INT NULL,
"a" VARCHAR NULL,
"tbt" VARCHAR NOT NULL,
"p" VARCHAR NULL,
FOREIGN KEY ("events") REFERENCES "events"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "board_results";

CREATE TABLE "board_results" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"board_id" INT NOT NULL,
"round_number" INT NULL,
"table_number" INT NULL,
"ns_pair" INT NOT NULL,
"ew_pair" INT NOT NULL,
"ns_score" VARCHAR NOT NULL,
"ew_score" VARCHAR NOT NULL,
"contract" VARCHAR NULL,
"declarer" VARCHAR NULL,
"ew_match_points" REAL NULL,
"ns_match_points" REAL NULL,
"opening_lead" VARCHAR NULL,
"result" VARCHAR NULL,
"tricks_taken" INT NULL,
-- board_results_add_ons are INT but many are NULL
"board_results_add_ons" INT NULL,
-- board_results_addons are INT but many are NULL
"board_results_addons" INT NULL,
FOREIGN KEY ("board_results_add_ons") REFERENCES "board_results_add_ons"(id) ON DELETE NO ACTION,
FOREIGN KEY ("board_results_addons") REFERENCES "board_results_addons"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "board_results_addons";

CREATE TABLE "board_results_addons" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NOT NULL,
"board_results_id" INT NOT NULL UNIQUE,
-- reject NULL bbo_movie?
"bbo_movie" VARCHAR NULL
);

DROP TABLE IF EXISTS "board_results_add_ons";

CREATE TABLE "board_results_add_ons" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NOT NULL,
"board_results_id" INT NOT NULL UNIQUE,
-- reject NULL bbo_movie?
"bbo_movie" VARCHAR NULL
);

DROP TABLE IF EXISTS "boards";

CREATE TABLE "boards" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"section_id" INT NOT NULL,
"board_number" INT NOT NULL,
"resultExists" BOOL NOT NULL,
"olExists" BOOL NOT NULL,
"contractExists" BOOL NOT NULL,
-- Many instances of NULL. single INT
"movieExists" INT NULL,
-- list of INTs
"board_results" VARCHAR NULL UNIQUE,
FOREIGN KEY ("movieExists") REFERENCES "movieExists"(id) ON DELETE NO ACTION,
FOREIGN KEY ("board_results") REFERENCES "board_results"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "club";

CREATE TABLE "club" (
"id" INT NOT NULL PRIMARY KEY,
"name" VARCHAR NOT NULL,
"is_subscribed" BOOL NULL,
"unit_no" INT NOT NULL,
"district_no" INT NOT NULL,
"manager_no" INT NOT NULL,
"directory" INT NOT NULL,
"type" VARCHAR NULL,
"operation_type" VARCHAR NOT NULL,
"owner" VARCHAR NULL,
"status_type" VARCHAR NOT NULL,
"status_date" VARCHAR NULL,
-- A few NULL fee_paid. Reject? club-results/277400/details/266365.data.sql
"fee_paid" VARCHAR NULL,
"established" VARCHAR NULL,
"alias" VARCHAR NOT NULL,
"new_results" INT NOT NULL,
"club_enrolled" VARCHAR NULL,
"results_preference" INT NOT NULL,
"payment_preference" INT NOT NULL,
"confirm_sanction" INT NOT NULL,
"upload_game" INT NOT NULL,
"update_club" INT NOT NULL,
-- A few NULL updated_by: club-results/904847/details/53032.data.sql, 99408, 99409
"updated_by" INT NULL,
"deleted_at" VARCHAR NULL,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NOT NULL,
"live_enrolled_at" VARCHAR NULL
);

DROP TABLE IF EXISTS "files";

-- files deprecated?
CREATE TABLE "files" (
"id" INT NOT NULL PRIMARY KEY,
"events" INT NOT NULL,
"text" VARCHAR NOT NULL,
"title" VARCHAR NOT NULL,
"file" VARCHAR NOT NULL,
"link" VARCHAR NOT NULL,
FOREIGN KEY ("events") REFERENCES "events"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "game_type";

CREATE TABLE "game_type" (
"id" INT NOT NULL PRIMARY KEY,
"rating" INT NOT NULL,
"type_code" VARCHAR NULL,
"type_name" VARCHAR NULL,
"fee_table" INT NULL,
"fee_reduced" REAL NULL,
"fee_add" REAL NULL,
"is_editable" BOOL NULL,
"is_cbf" BOOL NULL,
"is_local" BOOL NULL,
"level" VARCHAR NOT NULL,
"active_at" VARCHAR NULL,
"expired_at" VARCHAR NULL,
"user_id" INT NOT NULL,
"deleted_at" VARCHAR NULL,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NOT NULL,
"sanction_required" BOOL NULL
);

DROP TABLE IF EXISTS "hand_records";

CREATE TABLE "hand_records" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"board" INT NOT NULL,
-- voids are empty string or ----- (5 -) but never NULL
"north_spades" VARCHAR NOT NULL,
"north_hearts" VARCHAR NOT NULL,
"north_diamonds" VARCHAR NOT NULL,
"north_clubs" VARCHAR NOT NULL,
"east_spades" VARCHAR NOT NULL,
"east_hearts" VARCHAR NOT NULL,
"east_diamonds" VARCHAR NOT NULL,
"east_clubs" VARCHAR NOT NULL,
"south_spades" VARCHAR NOT NULL,
"south_hearts" VARCHAR NOT NULL,
"south_diamonds" VARCHAR NOT NULL,
"south_clubs" VARCHAR NOT NULL,
"west_spades" VARCHAR NOT NULL,
"west_hearts" VARCHAR NOT NULL,
"west_diamonds" VARCHAR NOT NULL,
"west_clubs" VARCHAR NOT NULL,
"board_record_hash" VARCHAR NOT NULL,
"board_record_string" VARCHAR NOT NULL,
"hand_record_set_id" INT NOT NULL,
"dealer" VARCHAR NOT NULL,
"vulnerability" VARCHAR NOT NULL,
-- double dummy, par, auction, comment, notes, points can all be NULL
"double_dummy_ew" VARCHAR NULL,
"double_dummy_ns" VARCHAR NULL,
"par" VARCHAR NULL,
"auction" VARCHAR NULL,
"comment" VARCHAR NULL,
"notes" VARCHAR NULL,
-- NULL or (always?) single INT? Why is this a list? Should be INT?
"points" VARCHAR NULL,
FOREIGN KEY ("points") REFERENCES "points"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "movieExists";

CREATE TABLE "movieExists" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NOT NULL,
"board_results_id" INT NOT NULL,
-- reject NULL bbo_movie?
"bbo_movie" VARCHAR NULL
);

DROP TABLE IF EXISTS "pair_summaries";

CREATE TABLE "pair_summaries" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"section_id" INT NOT NULL,
"event_pair_type" INT NULL,
"pair_type_id" INT NULL,
"pair_number" INT NOT NULL,
"direction" VARCHAR NULL,
-- a few instances of NULL strat: club-results/101402/details/29993.data.sql
"strat" INT NULL,
"boards_played" INT NULL,
"score" REAL NOT NULL,
"percentage" REAL NULL,
"adjustment" REAL NULL,
"handicap" REAL NULL,
"raw_score" REAL NULL,
"is_eligible" BOOL NULL,
-- list of INTs
"strat_place" VARCHAR NULL,
-- NULL or (always?) list of length 1? Why is this a list? Should be INT?
"session_scores" VARCHAR NULL,
-- list of INTs
"players" VARCHAR NOT NULL UNIQUE,
FOREIGN KEY ("strat_place") REFERENCES "strat_place"(id) ON DELETE NO ACTION,
FOREIGN KEY ("session_scores") REFERENCES "session_scores"(id) ON DELETE NO ACTION,
FOREIGN KEY ("players") REFERENCES "players"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "pigment";

CREATE TABLE "pigment" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
-- award_id is sometimes not unique
"award_id" INT NOT NULL,
"amount" REAL NOT NULL,
"color" VARCHAR NOT NULL
);

DROP TABLE IF EXISTS "players";

CREATE TABLE "players" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"pair_summary_id" INT NOT NULL,
-- reject non-INT id_number?
-- NULL case: club-results/130948/details/105902.data.sql
"id_number" VARCHAR NULL,
"rateable" BOOL NOT NULL,
"name" VARCHAR NOT NULL,
"city" VARCHAR NULL,
"state" VARCHAR NULL,
"country" VARCHAR NULL,
"mp_total" REAL NULL,
"lifemaster" BOOL NULL,
"is_valid_member" BOOL NOT NULL,
"bbo_playernumber" INT NULL,
"bbo_username" VARCHAR NULL,
"awards_count" INT NOT NULL,
"awards_score_count" INT NOT NULL,
-- NULL or list of length 1 of INT? Why is this a list? Should be INT?
"awards_score" VARCHAR NULL,
-- NULL or list of length 1 of INT? Why is this a list? Should be INT?
"awards" VARCHAR NULL,
FOREIGN KEY ("awards_score") REFERENCES "awards_score"(id) ON DELETE NO ACTION,
FOREIGN KEY ("awards") REFERENCES "awards"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "points";

CREATE TABLE "points" (
"id" INT NOT NULL PRIMARY KEY,
"hand_records" INT NOT NULL UNIQUE,
"N" INT NOT NULL,
"W" INT NOT NULL,
"E" INT NOT NULL,
"S" INT NOT NULL,
FOREIGN KEY ("hand_records") REFERENCES "hand_records"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "remaining_teams";

CREATE TABLE "remaining_teams" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"session_id" INT NOT NULL,
"round_number" INT NOT NULL,
"team" INT NOT NULL,
"opposing_team" INT NOT NULL,
"team_score" REAL NOT NULL,
"opposing_team_score" REAL NOT NULL
);

DROP TABLE IF EXISTS "rounds";

CREATE TABLE "rounds" (
"id" INT NOT NULL PRIMARY KEY,
"events" INT NOT NULL,
"opposing_team" INT NOT NULL,
"score" REAL NOT NULL,
FOREIGN KEY ("events") REFERENCES "events"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "score_awards";

CREATE TABLE "score_awards" (
"id" VARCHAR NOT NULL PRIMARY KEY,
"team_summaries" INT NOT NULL,
"amount" REAL NOT NULL,
"color" VARCHAR NOT NULL,
"type" VARCHAR NOT NULL,
FOREIGN KEY ("team_summaries") REFERENCES "team_summaries"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "sections";

CREATE TABLE "sections" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"session_id" INT NOT NULL,
"name" VARCHAR NOT NULL,
"has_bws" BOOL NOT NULL,
"boards_per_round" INT NULL,
"number_of_rounds" INT NULL,
"overallrankCount" INT NOT NULL,
"sectionrankCount" INT NOT NULL,
"hashandicapScore" BOOL NULL,
-- list of INTs
"pair_summaries" VARCHAR NOT NULL UNIQUE,
-- boards is sometimes non-unique. e.g. club-results/108571/details/74222.data.sql
-- list of INTs
"boards" VARCHAR NULL UNIQUE,
FOREIGN KEY ("pair_summaries") REFERENCES "pair_summaries"(id) ON DELETE NO ACTION,
FOREIGN KEY ("boards") REFERENCES "boards"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "session_scores";

CREATE TABLE "session_scores" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"session_id" INT NOT NULL,
"pair_summary_id" INT NOT NULL UNIQUE,
"factored_score" REAL NOT NULL,
"score" REAL NOT NULL,
"percentage" REAL NULL
);

DROP TABLE IF EXISTS "sessions";

CREATE TABLE "sessions" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"event_id" INT NOT NULL,
"number" INT NOT NULL,
"number_of_sections" INT NOT NULL,
-- hand_record_id can be "SHUFFLE". 10% are NULL.
"hand_record_id" VARCHAR NULL,
"cross_section_scoring" VARCHAR NULL,
"processing_status" INT NOT NULL,
"acbl_hand_record_file" VARCHAR NULL,
"club_session_id" INT NOT NULL,
"game_date" VARCHAR NOT NULL,
-- hand_records_sets is unknown
"hand_records_sets" VARCHAR NULL,
"has_hand_record" BOOL NULL,
"generated_hand_record_file" VARCHAR NULL,
-- teamMatches, team_matches, remaining_teams, team_summaries, hand_records, sections
-- are all NULLable lists of INTs
"teamMatches" VARCHAR NULL,
"team_matches" VARCHAR NULL,
"remaining_teams" VARCHAR NULL,
"team_summaries" VARCHAR NULL,
"hand_records" VARCHAR NULL,
"sections" VARCHAR NULL,
FOREIGN KEY ("teamMatches") REFERENCES "teamMatches"(id) ON DELETE NO ACTION,
FOREIGN KEY ("team_matches") REFERENCES "team_matches"(id) ON DELETE NO ACTION,
FOREIGN KEY ("remaining_teams") REFERENCES "remaining_teams"(id) ON DELETE NO ACTION,
FOREIGN KEY ("team_summaries") REFERENCES "team_summaries"(id) ON DELETE NO ACTION,
FOREIGN KEY ("hand_records") REFERENCES "hand_records"(id) ON DELETE NO ACTION,
FOREIGN KEY ("sections") REFERENCES "sections"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "stratValues";

CREATE TABLE "stratValues" (
"id" INT NOT NULL PRIMARY KEY,
"events" INT NOT NULL,
"label" VARCHAR NOT NULL,
"limit" INT NOT NULL,
FOREIGN KEY ("events") REFERENCES "events"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "strat_place";

CREATE TABLE "strat_place" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"pair_summary_id" INT NOT NULL,
"strat_number" INT NOT NULL,
"rank" INT NOT NULL,
"type" VARCHAR NOT NULL
);

DROP TABLE IF EXISTS "strats";

CREATE TABLE "strats" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"event_id" INT NOT NULL,
"number" INT NOT NULL,
"label" VARCHAR NOT NULL,
"limit" INT NOT NULL
);

DROP TABLE IF EXISTS "teamMatches";

CREATE TABLE "teamMatches" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"session_id" INT NOT NULL,
"round_number" INT NOT NULL,
"team" INT NOT NULL,
"opposing_team" INT NOT NULL,
"team_score" REAL NOT NULL,
"opposing_team_score" REAL NOT NULL
);

DROP TABLE IF EXISTS "team_matches";

CREATE TABLE "team_matches" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"session_id" INT NOT NULL,
"round_number" INT NOT NULL,
"team" INT NOT NULL,
"opposing_team" INT NOT NULL,
"team_score" REAL NOT NULL,
"opposing_team_score" REAL NOT NULL
);

DROP TABLE IF EXISTS "team_players";

CREATE TABLE "team_players" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"team_summary_id" INT NOT NULL,
-- reject 100+ non-INT id_number?
"id_number" VARCHAR NULL,
"rateable" BOOL NOT NULL,
"name" VARCHAR NOT NULL,
"city" VARCHAR NULL,
"state" VARCHAR NULL,
"country" VARCHAR NULL,
"mp_total" REAL NULL,
"lifemaster" BOOL NULL,
"matches_played" INT NULL,
"number_of_wins" INT NULL,
"is_valid_member" BOOL NOT NULL,
-- bbo_playernumber, bbo_username can be NULL
"bbo_playernumber" VARCHAR NULL,
"bbo_username" VARCHAR NULL
);

DROP TABLE IF EXISTS "team_strat_places";

CREATE TABLE "team_strat_places" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"team_summary_id" INT NOT NULL,
"strat_number" INT NOT NULL,
"rank" INT NOT NULL,
"type" VARCHAR NOT NULL
);

DROP TABLE IF EXISTS "team_summaries";

CREATE TABLE "team_summaries" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NULL,
"updated_at" VARCHAR NULL,
-- seating type is unknown
"seating" INT NULL,
"total_score" REAL NOT NULL,
"rank" VARTYPE NOT NULL,
-- NULL case: club-results/231159/details/120293.data.sql
"number_of_wins" REAL NULL,
"adjustment" INT NULL,
-- NULL case: club-results/231159/details/120293.data.sql
"matches_played" INT NULL,
"session_id" INT NOT NULL,
"strat" INT NOT NULL,
"team_id" INT NOT NULL,
"team_name" VARCHAR NULL,
"is_eligible" BOOL NULL,
-- score_awards,, team_players, team_strat_places are all lists of INTs
-- score_awards can be NULL
"score_awards" VARCHAR NULL UNIQUE,
"team_players" VARCHAR NOT NULL UNIQUE,
-- NULL case: club-results/118489/details/227.data.sql
"team_strat_places" VARCHAR NULL UNIQUE,
FOREIGN KEY ("score_awards") REFERENCES "score_awards"(id) ON DELETE NO ACTION,
FOREIGN KEY ("team_players") REFERENCES "team_players"(id) ON DELETE NO ACTION,
FOREIGN KEY ("team_strat_places") REFERENCES "team_strat_places"(id) ON DELETE NO ACTION
);

DROP TABLE IF EXISTS "uploads";

CREATE TABLE "uploads" (
"id" INT NOT NULL PRIMARY KEY,
"created_at" VARCHAR NOT NULL,
"updated_at" VARCHAR NULL,
"event_id" INT NOT NULL,
"program_name" VARCHAR NOT NULL,
"program_version" VARCHAR NOT NULL,
"document_id" VARCHAR NOT NULL,
"correction" BOOL NULL
);
