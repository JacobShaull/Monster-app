from data import Database  # Replace 'data' with the actual name of your python file containing the Database class

def main():
    # Create a database instance
    db = Database()

    # Test the count method
    initial_count = db.count()
    print(f"Initial document count: {initial_count}")

    # Test the seed method
    db.seed(10)  # Adds 10 random documents
    print(f"Document count after seeding: {db.count()}")

    # Test the reset method
    db.reset()
    print(f"Document count after reset: {db.count()}")

if __name__ == "__main__":
    main()
