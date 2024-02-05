graded_products = """
            CREATE TABLE IF NOT EXISTS graded_products (
            License_plate VARCHAR PRIMARY KEY,
            grading_cat VARCHAR NULL,
            grading_time VARCHAR NULL
            );
            """
grading_fees = """
            CREATE TABLE IF NOT EXISTS grading_fees (
            grading_cat VARCHAR PRIMARY KEY,
            cost REAL NULL
            );
            """
sold_products = """
            CREATE TABLE IF NOT EXISTS sold_products (
            License_plate VARCHAR PRIMARY KEY,
            status VARCHAR NULL,
            platform VARCHAR NULL,
            created_at TIMESTAMP NULL,
            shipped_at TIMESTAMP NULL,
            sold_price REAL NULL,
            country VARCHAR NULL,
            channel_ref VARCHAR NULL,
            platform_fee REAL NULL
            );
            """
transport_cost = """
            CREATE TABLE IF NOT EXISTS transport_cost (
            country VARCHAR PRIMARY KEY,
            transport_cost REAL NULL
            );
            """
platform_fees = """
            CREATE TABLE IF NOT EXISTS platform_fees (
            platform VARCHAR PRIMARY KEY,
            platform_fee REAL NULL
            );
            """