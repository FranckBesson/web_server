-- ============================================================================
-- File             : lomonade_DELETE.sql
-- Author           : Franck BESSON
-- Date             : June 2017
-- Role             : Delete tables
-- ============================================================================

DROP TABLE ITEM CASCADE;

DROP TABLE PLAYER CASCADE;

DROP TABLE RECIPE CASCADE;

DROP TABLE DAY CASCADE;

DROP TABLE TIME CASCADE;

DROP TABLE MAP CASCADE;

DROP TABLE ITEM_POSSESSION CASCADE;

DROP TABLE COMPOSE CASCADE;

DROP TABLE SALE CASCADE;

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
    CONSTRAINT UQ_PLAYER_NAME UNIQUE (PLAYER_NAME)
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
    CONSTRAINT CK_DAY_NUMBER CHECK (DAY_NUMBER >= 0),
    CONSTRAINT CK_DAY CHECK (DAY_WEATHER IN ('RAINY', 'CLOUDY', 'SUNNY', 'HEATWAVE', 'THUNDERSTORM'))
);

--==== TIME Table ====
-- create a TIME table who represent the current time of the game
CREATE TABLE TIME (
    TIME_HOUR   INT    NOT NULL,

    CONSTRAINT PK_TIME PRIMARY KEY(TIME_HOUR),
    CONSTRAINT CK_TIME_HOUR CHECK (TIME_HOUR >= 0)
);

--==== MAP Table ====
-- create a MAP table
CREATE TABLE MAP (
    MAP_ID          SERIAL  NOT NULL,
    MAP_CENTER_X    REAL    NOT NULL,
    MAP_CENTER_Y    REAL    NOT NULL,
    MAP_SPAN_X      REAL    NOT NULL,
    MAP_SPAN_Y      REAL    NOT NULL,

    CONSTRAINT PK_MAP PRIMARY KEY(MAP_ID)
);


-- ============================================================================
-- File             : lomonade_RT.sql
-- Author           : Franck BESSON
-- Date             : June 2017
-- Role             : Create relation tables
-- ============================================================================

--======== RELATION TABLES ========

--==== ITEM_POSSESSION Table ====
-- Create a ITEM_POSSESSION relation table
CREATE TABLE ITEM_POSSESSION (
    ITEM_POSSESSION_PLAYER_ID   INT    NOT NULL,
    ITEM_POSSESSION_ITEM_ID     INT    NOT NULL,

    CONSTRAINT PK_ITEM_POSSESSION PRIMARY KEY(ITEM_POSSESSION_PLAYER_ID, ITEM_POSSESSION_ITEM_ID)
);

--==== COMPOSE Table ====
-- Create a COMPOSE relation table
-- CK_COMPOSE_RECIPECEPTION because a recipe can't be made by itself
CREATE TABLE COMPOSE (
    COMPOSE_RECIPE_ID               INT    NOT NULL,
    COMPOSE_INGREDIENT_RECIPE_ID    INT    NOT NULL,

    CONSTRAINT PK_COMPOSE PRIMARY KEY(COMPOSE_RECIPE_ID, COMPOSE_INGREDIENT_RECIPE_ID),
    CONSTRAINT CK_COMPOSE_RECIPECEPTION CHECK (COMPOSE_RECIPE_ID != COMPOSE_INGREDIENT_RECIPE_ID)
);

--==== SALE Table ====
-- Create a SALE relation table
CREATE TABLE SALE (
    SALE_DAY_NUMBER INT    NOT NULL,
    SALE_RECIPE_ID  INT    NOT NULL,
    SALE_NUMBER     INT    NOT NULL,

    CONSTRAINT PK_SALE PRIMARY KEY(SALE_DAY_NUMBER, SALE_RECIPE_ID),
    CONSTRAINT CK_SALE_NUMBER CHECK (SALE_NUMBER >= 0)
);

-- ============================================================================
-- File             : lomonade_TD.sql
-- Author           : Franck BESSON
-- Date             : June 2017
-- Role             : Create tables dependencies
-- ============================================================================

--==== ITEM_POSSESSION dependencies ====

ALTER TABLE ITEM_POSSESSION
ADD CONSTRAINT FK_ITEM_POSSESSION_PLAYER_ID FOREIGN KEY (ITEM_POSSESSION_PLAYER_ID) REFERENCES PLAYER (PLAYER_ID);

ALTER TABLE ITEM_POSSESSION
ADD CONSTRAINT FK_ITEM_POSSESSION_ITEM_ID FOREIGN KEY (ITEM_POSSESSION_ITEM_ID) REFERENCES ITEM (ITEM_ID);

--==== COMPOSE dependencies ====

ALTER TABLE COMPOSE
ADD CONSTRAINT FK_COMPOSE_RECIPE_ID FOREIGN KEY (COMPOSE_RECIPE_ID) REFERENCES RECIPE (RECIPE_ID);

ALTER TABLE COMPOSE
ADD CONSTRAINT FK_COMPOSE_INGREDIENT_RECIPE_ID FOREIGN KEY (COMPOSE_INGREDIENT_RECIPE_ID) REFERENCES RECIPE (RECIPE_ID);

--==== SALE dependencies ====

ALTER TABLE SALE
ADD CONSTRAINT FK_SALE_DAY_NUMBER FOREIGN KEY (SALE_DAY_NUMBER) REFERENCES DAY (DAY_NUMBER);

ALTER TABLE SALE
ADD CONSTRAINT FK_SALE_RECIPE_ID FOREIGN KEY (SALE_RECIPE_ID) REFERENCES RECIPE (RECIPE_ID);

