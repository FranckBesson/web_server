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
    CONSTRAINT CK_COMPOSE_RECIPECEPTION CHECK (COMPOSE_RECIPE_ID != COMPOSE_INGREDIENT_RECIPE_ID))
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

