create table if not exists shop_unit(
"id" uuid,
"date" timestamp not null,
"name" text not null,
"price" integer,
"type" text not null,
CONSTRAINT "K2" PRIMARY KEY ("id")
);

create table if not exists childrens(
"children_id" uuid,
"parent_id" uuid,
CONSTRAINT "K3" PRIMARY KEY ("children_id", "parent_id"),
CONSTRAINT "C2" FOREIGN KEY ("children_id")
    REFERENCES "shop_unit" ("id") ON DELETE CASCADE,
CONSTRAINT "C3" FOREIGN KEY ("parent_id")
    REFERENCES "shop_unit" ("id") ON DELETE CASCADE
);

CREATE TABLE statistic(
"id" uuid,
"name" text,
"date" timestamp,
"parent_id" uuid,
"price" integer,
"type" text,
CONSTRAINT "C4" FOREIGN KEY ("id")
    REFERENCES "shop_unit" ("id") ON DELETE CASCADE
);