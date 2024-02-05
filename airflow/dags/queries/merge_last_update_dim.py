merge_last_update_dim = """
                    MERGE INTO last_update_dim ca
                    USING sold_products t
                    ON t.license_plate = ca.license_plate
                    WHEN MATCHED AND t.shipped_at is NOT NULL AND t.shipped_at != ca.last_update THEN
                        UPDATE SET last_update = t.shipped_at
                    WHEN NOT MATCHED AND t.shipped_at is NOT NULL THEN
                        INSERT (license_plate, last_update)
                        VALUES (t.license_plate, t.shipped_at)
                    WHEN NOT MATCHED THEN
                        INSERT (license_plate, last_update)
                        VALUES (t.license_plate, t.created_at);    
                    """