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
            cost MONEY NULL
            );
            """
sold_products_tb = """
            CREATE TABLE IF NOT EXISTS sold_products (
            License_plate VARCHAR PRIMARY KEY,
            status VARCHAR NULL,
            platform VARCHAR NULL,
            created_at TIMESTAMP NULL,
            shipped_at TIMESTAMP NULL,
            sold_price MONEY NULL,
            country VARCHAR NULL,
            channel_ref VARCHAR NULL,
            platform_fee MONEY NULL
            );
            """
transport_cost_tb = """
            CREATE TABLE IF NOT EXISTS transport_cost (
            country VARCHAR PRIMARY KEY,
            transport_cost MONEY NULL
            );
            """
platform_fees_tb = """
            CREATE TABLE IF NOT EXISTS platform_fees (
            platform VARCHAR PRIMARY KEY,
            platform_fee MONEY NULL
            );
            """

base_records_tb = """
            CREATE TABLE IF NOT EXISTS base_records (
            license_plate VARCHAR PRIMARY KEY,
            status VARCHAR NULL,
            platform VARCHAR NULL,
            shipped_at_day DATE NULL,
            sold_price MONEY NULL,
            buybay_fee MONEY NULL,
            grading_fee MONEY NULL,
            transport_fee MONEY NULL,
            platform_fee MONEY NULL,
            partner_payout MONEY NULL
            );
            """

finance_report_tb = """
            CREATE TABLE IF NOT EXISTS finance_report (
            platform VARCHAR NULL,
            shipped_at_day DATE NULL,
            total_income MONEY NULL,
            total_buybay_fee MONEY NULL,
            total_grading_fee MONEY NULL,
            total_transport_fee MONEY NULL,
            total_partner_payout MONEY NULL,
            total_fees MONEY NULL
            """