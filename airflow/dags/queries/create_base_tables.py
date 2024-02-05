graded_products_tb = """
            CREATE TABLE IF NOT EXISTS graded_products (
            License_plate VARCHAR PRIMARY KEY,
            grading_cat VARCHAR NULL,
            grading_time VARCHAR NULL
            );
            """
grading_fees_tb = """
            CREATE TABLE IF NOT EXISTS grading_fees (
            grading_cat VARCHAR PRIMARY KEY,
            cost REAL NULL
            );
            """
sold_products_tb = """
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
transport_cost_tb = """
            CREATE TABLE IF NOT EXISTS transport_cost (
            country VARCHAR PRIMARY KEY,
            transport_cost REAL NULL
            );
            """
platform_fees_tb = """
            CREATE TABLE IF NOT EXISTS platform_fees (
            platform VARCHAR PRIMARY KEY,
            platform_fee REAL NULL
            );
            """

base_records_tb = """
            CREATE TABLE IF NOT EXISTS base_records (
            license_plate VARCHAR PRIMARY KEY,
            status VARCHAR NULL,
            platform VARCHAR NULL,
            last_update TIMESTAMP,
            last_update_day DATE NULL,
            sold_price REAL NULL,
            buybay_fee REAL NULL,
            grading_fee REAL NULL,
            transport_fee REAL NULL,
            platform_fee REAL NULL,
            partner_payout REAL NULL
            );
            """

finance_report_tb = """
            CREATE TABLE IF NOT EXISTS finance_report (
            platform VARCHAR NULL,
            shipped_at_day DATE NULL,
            total_income REAL NULL,
            total_buybay_fee REAL NULL,
            total_grading_fee REAL NULL,
            total_transport_fee REAL NULL,
            total_partner_payout REAL NULL,
            total_fees REAL NULL
            );
            """

last_update_dim = """
            CREATE TABLE IF NOT EXISTS last_update_dim (
            license_plate VARCHAR PRIMARY KEY,
            last_update TIMESTAMP
            );
            """
