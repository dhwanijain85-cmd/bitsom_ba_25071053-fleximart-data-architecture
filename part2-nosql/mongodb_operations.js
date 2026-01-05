// ============================================================================
// FlexiMart MongoDB Operations
// ============================================================================
// This file contains MongoDB operations for the product catalog
// Run these operations in MongoDB shell (mongosh) or MongoDB Compass
// ============================================================================

// ----------------------------------------------------------------------------
// Operation 1: Load Data (1 mark)
// Import the provided JSON file into collection 'products'
// ----------------------------------------------------------------------------

// Method 1: Using mongoimport command (run in terminal)
// mongoimport --db fleximart --collection products --file products_catalog.json --jsonArray

// Method 2: Using mongosh (paste the JSON data)
use fleximart;

db.products.drop();  // Clear existing data if any

db.products.insertMany([
    // Paste contents of products_catalog.json here
    // Or use mongoimport command above
]);

// Verify data loaded
db.products.countDocuments();  // Should return 12


// ----------------------------------------------------------------------------
// Operation 2: Basic Query (2 marks)
// Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock
// ----------------------------------------------------------------------------

db.products.find(
    {
        category: "Electronics",
        price: { $lt: 50000 }
    },
    {
        name: 1,
        price: 1,
        stock: 1,
        _id: 0
    }
);

// Expected output:
// { name: "Sony WH-1000XM5 Headphones", price: 29990, stock: 200 }
// { name: "Dell 27-inch 4K Monitor", price: 32999, stock: 60 }
// { name: "OnePlus Nord CE 3", price: 26999, stock: 180 }


// ----------------------------------------------------------------------------
// Operation 3: Review Analysis (2 marks)
// Find all products that have average rating >= 4.0
// Use aggregation to calculate average from reviews array
// ----------------------------------------------------------------------------

db.products.aggregate([
    {
        $project: {
            name: 1,
            category: 1,
            avg_rating: { $avg: "$reviews.rating" }
        }
    },
    {
        $match: {
            avg_rating: { $gte: 4.0 }
        }
    },
    {
        $sort: { avg_rating: -1 }
    }
]);

// Expected output: All 12 products (all have avg rating >= 4.0)


// ----------------------------------------------------------------------------
// Operation 4: Update Operation (2 marks)
// Add a new review to product "ELEC001"
// Review: {user: "U999", rating: 4, comment: "Good value", date: ISODate()}
// ----------------------------------------------------------------------------

db.products.updateOne(
    { product_id: "ELEC001" },
    {
        $push: {
            reviews: {
                user_id: "U999",
                username: "NewUser",
                rating: 4,
                comment: "Good value",
                date: new Date().toISOString().split('T')[0]
            }
        }
    }
);

// Verify the update
db.products.findOne(
    { product_id: "ELEC001" },
    { name: 1, reviews: 1 }
);


// ----------------------------------------------------------------------------
// Operation 5: Complex Aggregation (3 marks)
// Calculate average price by category
// Return: category, avg_price, product_count
// Sort by avg_price descending
// ----------------------------------------------------------------------------

db.products.aggregate([
    {
        $group: {
            _id: "$category",
            avg_price: { $avg: "$price" },
            product_count: { $sum: 1 }
        }
    },
    {
        $project: {
            _id: 0,
            category: "$_id",
            avg_price: { $round: ["$avg_price", 2] },
            product_count: 1
        }
    },
    {
        $sort: { avg_price: -1 }
    }
]);

// Expected output:
// { category: "Electronics", avg_price: 70830.67, product_count: 6 }
// { category: "Fashion", avg_price: 5214.83, product_count: 6 }
