base_records = """
    INSERT INTO base_records
    with 
        base_table as (
            select
                a.license_plate,
                a.status,
                a.platform,
                l_dim.last_update,
                date_trunc('day',l_dim.last_update)::date as last_update_day,
                a.sold_price,
                a.sold_price * 0.10  as buybay_fee,
                c.cost as grading_fee,
                d.transport_cost as transport_fee,
                CASE 
                    WHEN a.platform_fee is null 
                        THEN (a.sold_price * e.platform_fee) / 100
                    ELSE a.platform_fee
                END AS platform_fee
            from sold_products a join last_update_dim l_dim
            on a.license_plate = l_dim.license_plate            
            join graded_products b
            on a.license_plate = b.license_plate
            join grading_fees c
            on b.grading_cat = c.grading_cat
            join transport_cost d
            on a.country = d.country
            left join platform_fees e
            on a.platform = e.platform
    )
    select
        *,
        sold_price - buybay_fee - transport_fee - platform_fee - grading_fee as partner_payout
    from base_table;
    """
finance_report ="""
    INSERT INTO finance_report
    with 
        aggregatted_fees as (
            select
                platform,
                last_update_day,
                sum(sold_price) total_income,
                sum(buybay_fee) total_buybay_fee,
                sum(grading_fee) total_grading_fee,
                sum(platform_fee) total_platform_fee,
                sum(transport_fee) total_transport_fee,
                sum(partner_payout) total_partner_payout
            from base_records
            group by platform, last_update_day
        )
        select
            platform,
            last_update_day,
            total_income,
            total_buybay_fee,
            total_grading_fee,
            total_transport_fee,
            total_partner_payout,
            (total_buybay_fee + total_grading_fee + total_platform_fee) total_fees
        from aggregatted_fees
    order by total_income desc;
"""
