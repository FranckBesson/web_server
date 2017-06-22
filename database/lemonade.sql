-- ============================================================================
-- File             : lemonade.sql
-- Author           : Franck BESSON
-- Date             : June 2017
-- Role             : Create data tables
-- ============================================================================

--======== DATA TABLES ========

--==== ITEM Table ====
-- Create an ITEM, a item can be a stand or an ad panel
-- The item_kind value can be "STAND" or "AD" only
CREATE TABLE ITEM (
    ITEM_ID             SERIAL      NOT NULL,
    ITEM_KIND           VARCHAR(5)  NOT NULL,
    ITEM_INFLUENCE      REAL        NOT NULL,
    ITEM_X_COORDINATE   REAL        NOT NULL,
    ITEM_Y_COORDINATE   REAL        NOT NULL,

    CONSTRAINT PK_ITEM PRIMARY KEY(ITEM_ID),
    CONSTRAINT CK_ITEM CHECK (ITEM_KIND IN ('STAND', 'AD'))
);



--==== PLAYER Table ====
-- Create a PLAYER table
CREATE TABLE PLAYER (
    PLAYER_ID           SERIAL          NOT NULL,
    PLAYER_BUDGET       MONEY           NOT NULL,
    PLAYER_INFLUENCE    REAL            NOT NULL,
    PLAYER_NAME         VARCHAR(255)    NOT NULL,

    CONSTRAINT PK_PLAYER PRIMARY KEY(PLAYER_ID),
    CONSTRAINT UQ_PLAYER_NAME UNIQUE (PLAYER_NAME))
);

--==== RECIPE Table ====
-- Create a RECIPE table, a recip is also an ingredient
CREATE TABLE RECIPE (
    RECIPE_ID       SERIAL          NOT NULL,
    RECIPE_NAME     VARCHAR(255)    NOT NULL,
    RECIPE_PRICE    MONEY           NOT NULL,
    RECIPE_ALCOHOL  BOOLEAN         NOT NULL,
    RECIPE_COLD     BOOLEAN         NOT NULL,

    CONSTRAINT PK_RECIPE PRIMARY KEY(RECIPE_ID)
);

--==== DAY Table ====
-- Create a DAY table
-- The day_weather value can be "RAINY", "CLOUDY", "SUNNY", "HEATWAVE" or "THUNDERSTORM" only
CREATE TABLE DAY (
    DAY_NUMBER  SMALLINT    NOT NULL,
    DAY_WEATHER VARCHAR(12) NOT NULL,

    CONSTRAINT PK_DAY PRIMARY KEY(DAY_NUMBER),
    CONSTRAINT CK_DAY_NUMBER CHECK (DAY_NUMBER >= 0)),
    CONSTRAINT CK_DAY CHECK (DAY_WEATHER IN ('RAINY', 'CLOUDY', 'SUNNY', 'HEATWAVE', 'THUNDERSTORM'))
);

--==== TIME Table ====
-- create a TIME table who represent the current time of the game
CREATE TABLE TIME (
    TIME_HOUR   INT    NOT NULL,

    CONSTRAINT PK_TIME PRIMARY KEY(TIME_HOUR),
    CONSTRAINT CK_TIME_HOUR CHECK (TIME_HOUR >= 0)
);

