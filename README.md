# NDC-US56
A Items.db file will be required to run this, structure as follows:

SQLite format
CREATE TABLE "Post_Item" (
	"item_Id" INTEGER NOT NULL, 
	title VARCHAR, 
	address VARCHAR, 
	"application_Type" VARCHAR, 
	PRIMARY KEY ("item_Id")

There is also a known issue where at least one row must exist on the table before the service will function.
