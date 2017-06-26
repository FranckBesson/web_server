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

DROP TABLE RECIPE_POSSESSION CASCADE;

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
    ITEM_ID             SERIAL          NOT NULL,
    ITEM_KIND           VARCHAR(5)      NOT NULL,
    ITEM_INFLUENCE      REAL            NOT NULL,
    ITEM_OWNER          VARCHAR(255)    NOT NULL,
    ITEM_X_COORDINATE   REAL            NOT NULL,
    ITEM_Y_COORDINATE   REAL            NOT NULL,

    CONSTRAINT PK_ITEM PRIMARY KEY(ITEM_ID),
    CONSTRAINT CK_ITEM CHECK (ITEM_KIND IN ('STAND', 'AD'))
);



--==== PLAYER Table ====
-- Create a PLAYER table
CREATE TABLE PLAYER (
    PLAYER_NAME         VARCHAR(255)    NOT NULL,
    PLAYER_BUDGET       MONEY           NOT NULL,
    PLAYER_INFLUENCE    REAL            NOT NULL,
    
    CONSTRAINT PK_PLAYER PRIMARY KEY(PLAYER_NAME)
);

--==== RECIPE Table ====
-- Create a RECIPE table, a recip is also an ingredient
CREATE TABLE RECIPE (
    RECIPE_NAME     VARCHAR(255)    NOT NULL,
    RECIPE_PRICE    MONEY           NOT NULL,
    RECIPE_ALCOHOL  BOOLEAN         NOT NULL,
    RECIPE_COLD     BOOLEAN         NOT NULL,

    CONSTRAINT PK_RECIPE PRIMARY KEY(RECIPE_NAME)
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

--==== COMPOSE Table ====
-- Create a COMPOSE relation table
-- CK_COMPOSE_RECIPECEPTION because a recipe can't be made by itself
CREATE TABLE COMPOSE (
    COMPOSE_RECIPE_NAME               VARCHAR(255)    NOT NULL,
    COMPOSE_INGREDIENT_RECIPE_NAME    VARCHAR(255)    NOT NULL,

    CONSTRAINT PK_COMPOSE PRIMARY KEY(COMPOSE_RECIPE_NAME, COMPOSE_INGREDIENT_RECIPE_NAME),
    CONSTRAINT CK_COMPOSE_RECIPECEPTION CHECK (COMPOSE_RECIPE_NAME != COMPOSE_INGREDIENT_RECIPE_NAME)
);

--==== SALE Table ====
-- Create a SALE relation table
CREATE TABLE SALE (
    SALE_DAY_NUMBER   INT           NOT NULL,
    SALE_RECIPE_NAME    VARCHAR(255)          NOT NULL,
    SALE_PLAYER_NAME  VARCHAR(255)  NOT NULL,
    SALE_NUMBER       INT           NOT NULL,
    SALE_PRODUCE      INT           NOT NULL,

    CONSTRAINT PK_SALE PRIMARY KEY(SALE_DAY_NUMBER, SALE_RECIPE_NAME, SALE_PLAYER_NAME),
    CONSTRAINT CK_SALE_NUMBER CHECK (SALE_NUMBER <= SALE_PRODUCE),
    CONSTRAINT CK_SALE_PRODUCE CHECK (SALE_PRODUCE >= 0)
);

--==== RECIPE_POSSESSION ====
-- Create a RECIPE_POSSESSION relation table
CREATE TABLE RECIPE_POSSESSION (
    RECIPE_POSSESSION_PLAYER_NAME  VARCHAR(255)    NOT NULL,
    RECIPE_POSSESSION_RECIPE_NAME    VARCHAR(255)             NOT NULL,

    CONSTRAINT PK_RECIPE_POSSESSION PRIMARY KEY(RECIPE_POSSESSION_PLAYER_NAME, RECIPE_POSSESSION_RECIPE_NAME)
);

-- ============================================================================
-- File             : lomonade_TD.sql
-- Author           : Franck BESSON
-- Date             : June 2017
-- Role             : Create tables dependencies
-- ============================================================================

--==== COMPOSE dependencies ====

ALTER TABLE COMPOSE
ADD CONSTRAINT FK_COMPOSE_RECIPE_NAME FOREIGN KEY (COMPOSE_RECIPE_NAME) REFERENCES RECIPE (RECIPE_NAME);

ALTER TABLE COMPOSE
ADD CONSTRAINT FK_COMPOSE_INGREDIENT_RECIPE_NAME FOREIGN KEY (COMPOSE_INGREDIENT_RECIPE_NAME) REFERENCES RECIPE (RECIPE_NAME);

--==== SALE dependencies ====

ALTER TABLE SALE
ADD CONSTRAINT FK_SALE_DAY_NUMBER FOREIGN KEY (SALE_DAY_NUMBER) REFERENCES DAY (DAY_NUMBER);

ALTER TABLE SALE
ADD CONSTRAINT FK_SALE_RECIPE_NAME FOREIGN KEY (SALE_RECIPE_NAME) REFERENCES RECIPE (RECIPE_NAME);

ALTER TABLE SALE
ADD CONSTRAINT FK_SALE_PLAYER_NAME FOREIGN KEY (SALE_PLAYER_NAME) REFERENCES PLAYER (PLAYER_NAME);

--==== ITEM dependencies ====

ALTER TABLE ITEM
ADD CONSTRAINT FK_ITEM_OWNER FOREIGN KEY (ITEM_OWNER) REFERENCES PLAYER (PLAYER_NAME);

--==== RECIPE_POSSESSION dependencies ====

ALTER TABLE RECIPE_POSSESSION
ADD CONSTRAINT FK_RECIPE_POSSESSION_PLAYER_NAME FOREIGN KEY (RECIPE_POSSESSION_PLAYER_NAME) REFERENCES PLAYER (PLAYER_NAME);

ALTER TABLE RECIPE_POSSESSION
ADD CONSTRAINT FK_RECIPE_POSSESSION_RECIPE_NAME FOREIGN KEY (RECIPE_POSSESSION_RECIPE_NAME) REFERENCES RECIPE (RECIPE_NAME);

-- ============================================================================
-- File             : lomonade_jeux_de_test.sql
-- Author           : Franck BESSON
-- Date             : June 2017
-- Role             : Créer un jeux d'essaie
-- ============================================================================

-- Insert
INSERT INTO PLAYER VALUES('Franck',5,5);
INSERT INTO PLAYER VALUES('Martin',8,7);
INSERT INTO PLAYER VALUES('Louis',15,8);

-- Mes item
INSERT INTO ITEM(ITEM_KIND, ITEM_INFLUENCE, ITEM_OWNER, ITEM_X_COORDINATE, ITEM_Y_COORDINATE) VALUES('STAND',1,'Franck',3,2);
INSERT INTO ITEM(ITEM_KIND, ITEM_INFLUENCE, ITEM_OWNER, ITEM_X_COORDINATE, ITEM_Y_COORDINATE) VALUES('AD',1,'Franck',5,2);
INSERT INTO ITEM(ITEM_KIND, ITEM_INFLUENCE, ITEM_OWNER, ITEM_X_COORDINATE, ITEM_Y_COORDINATE) VALUES('AD',2,'Franck',4,2);
INSERT INTO ITEM(ITEM_KIND, ITEM_INFLUENCE, ITEM_OWNER, ITEM_X_COORDINATE, ITEM_Y_COORDINATE) VALUES('AD',1,'Franck',3,3);
INSERT INTO ITEM(ITEM_KIND, ITEM_INFLUENCE, ITEM_OWNER, ITEM_X_COORDINATE, ITEM_Y_COORDINATE) VALUES('STAND',2,'Martin',3,5);
INSERT INTO ITEM(ITEM_KIND, ITEM_INFLUENCE, ITEM_OWNER, ITEM_X_COORDINATE, ITEM_Y_COORDINATE) VALUES('AD',1,'Martin',3,1);

-- Mes recette
INSERT INTO RECIPE(RECIPE_NAME, RECIPE_PRICE, RECIPE_ALCOHOL, RECIPE_COLD) VALUES('lemonade',5,false,true);
INSERT INTO RECIPE(RECIPE_NAME, RECIPE_PRICE, RECIPE_ALCOHOL, RECIPE_COLD) VALUES('ricard (with water)',2,true,true);

-- Mes ingredients
INSERT INTO RECIPE(RECIPE_NAME, RECIPE_PRICE, RECIPE_ALCOHOL, RECIPE_COLD) VALUES('lemon',0.8,false,false);
INSERT INTO RECIPE(RECIPE_NAME, RECIPE_PRICE, RECIPE_ALCOHOL, RECIPE_COLD) VALUES('water',0.3,false,false);
INSERT INTO RECIPE(RECIPE_NAME, RECIPE_PRICE, RECIPE_ALCOHOL, RECIPE_COLD) VALUES('ice',0.2,false,true);
INSERT INTO RECIPE(RECIPE_NAME, RECIPE_PRICE, RECIPE_ALCOHOL, RECIPE_COLD) VALUES('ricard',1.2,true,false);

-- Composition d'une limonade
INSERT INTO COMPOSE VALUES('lemonade','lemon');
INSERT INTO COMPOSE VALUES('lemonade','water');
INSERT INTO COMPOSE VALUES('lemonade','ice');

-- Composition d'un ricard
INSERT INTO COMPOSE VALUES('ricard (with water)','ricard');
INSERT INTO COMPOSE VALUES('ricard (with water)','water');
INSERT INTO COMPOSE VALUES('ricard (with water)','ice');

-- Attribution de recette
INSERT INTO RECIPE_POSSESSION VALUES('Franck','lemonade');
INSERT INTO RECIPE_POSSESSION VALUES('Franck','ricard (with water)');
INSERT INTO RECIPE_POSSESSION VALUES('Martin','lemonade');

-- Inserion de deux jours
INSERT INTO DAY VALUES(1,'SUNNY');
INSERT INTO DAY VALUES(2,'CLOUDY');

-- Création des sales d'un joueur
INSERT INTO SALE VALUES(1,'lemonade','Franck',5,5);
INSERT INTO SALE VALUES(1,'ricard (with water)','Franck',2,3);

INSERT INTO SALE VALUES(1,'lemonade','Martin',2,5);
INSERT INTO SALE VALUES(1,'ricard (with water)','Martin',6,10);

-- Création de la map
INSERT INTO MAP(MAP_CENTER_X, MAP_CENTER_Y, MAP_SPAN_X, MAP_SPAN_Y) VALUES(5,5,10,10);

-- Insertion du temps
INSERT INTO TIME VALUES(21);