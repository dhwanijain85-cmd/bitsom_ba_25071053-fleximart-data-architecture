# NoSQL Analysis Report - FlexiMart Product Catalog

## Section A: Limitations of RDBMS (150 words)

The current relational database faces significant challenges when handling FlexiMart's diverse product catalog:

**1. Products with Different Attributes**
In MySQL, all products share the same table structure. A laptop needs columns for RAM, processor, and screen size, while shoes need size and color. This forces us to either create many NULL columns (sparse data problem) or build complex multi-table structures with product-specific attribute tables. Both approaches make queries complicated and slow.

**2. Frequent Schema Changes**
Adding a new product type like "Smart Watches" requires ALTER TABLE commands to add new columns. In production, schema changes can lock tables, cause downtime, and require application code updates. Each new product category means database migrations.

**3. Storing Nested Data (Reviews)**
Customer reviews with ratings, comments, and replies don't fit naturally in flat tables. We need separate tables (products, reviews, replies) with JOIN operations. Fetching a product with all its reviews requires multiple queries, impacting performance.


## Section B: NoSQL Benefits (150 words)

MongoDB addresses these limitations effectively:

**1. Flexible Schema (Document Structure)**
Each product is stored as a JSON-like document with its own unique fields. A laptop document can have `{ram: "16GB", processor: "i7"}` while a shoe document has `{size: 42, color: "black"}`. No NULL columns, no wasted space. New product types require zero schema changes - just insert documents with new fields.

**2. Embedded Documents (Reviews Within Products)**
Reviews can be stored directly inside the product document as an array:
```json
{
  "product_name": "Laptop",
  "reviews": [
    {"user": "Rahul", "rating": 5, "comment": "Great!"},
    {"user": "Priya", "rating": 4, "comment": "Good value"}
  ]
}
```
One query fetches everything - no JOINs needed.

**3. Horizontal Scalability**
MongoDB distributes data across multiple servers (sharding). As FlexiMart grows to millions of products, we add more servers instead of upgrading one expensive machine. This provides better availability and faster read/write operations.


## Section C: Trade-offs (100 words)

**Disadvantage 1: No ACID Transactions Across Documents**
MongoDB doesn't guarantee strong consistency for operations spanning multiple documents like MySQL does. If FlexiMart needs to update inventory and create an order atomically, MySQL's transactions are more reliable. MongoDB's multi-document transactions exist but have performance overhead.

**Disadvantage 2: No JOIN Operations**
MongoDB lacks native JOIN support. If we need to analyze "all orders for products in Electronics category," we must either duplicate data (denormalization) or run multiple queries and merge results in application code. This increases complexity and storage requirements.
