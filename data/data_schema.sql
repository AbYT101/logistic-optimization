CREATE TABLE "delivery_requests" (
  "id" integer PRIMARY KEY,
  "order_id" integer,
  "driver_id" integer,
  "driver_action" varchar,
  "lat" float,
  "lng" float,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "completed_orders" (
  "Trip_ID" integer PRIMARY KEY,
  "Trip_Origin" varchar,
  "Trip_Destination" varchar,
  "Trip_Start_Time" timestamp,
  "Trip_End_Time" timestamp
);

CREATE TABLE "weather" (
  "date" date PRIMARY KEY,
  "temperature" float,
  "rain" float
);

CREATE TABLE "calendar" (
  "date" date PRIMARY KEY,
  "name" varchar,
  "type" varchar
);

ALTER TABLE "delivery_requests" ADD FOREIGN KEY ("order_id") REFERENCES "completed_orders" ("Trip_ID");

ALTER TABLE "completed_orders" ADD FOREIGN KEY ("Trip_Start_Time") REFERENCES "weather" ("date");

ALTER TABLE "completed_orders" ADD FOREIGN KEY ("Trip_Start_Time") REFERENCES "calendar" ("date");
