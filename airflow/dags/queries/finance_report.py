base_records = """
    INSERT INTO base_records
    with 
        sold_products_with_country as (
            select 
            a.license_plate,
            a.status,
            a.platform,
            a.platform_fee,
            a.sold_price,
            a.sold_price * 0.10 as buybay_fee,
            CASE    
                WHEN b.transport_cost is null and a.country is not null
                    THEN 'OTHER'
                ELSE a.country
            END AS country
            from sold_products a 
            left join transport_cost b
                using(country)
        ),
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
            from sold_products_with_country a join last_update_dim l_dim
                on UPPER(a.license_plate) = UPPER(l_dim.license_plate)
            join graded_products b
                on UPPER(a.license_plate) = UPPER(b.license_plate)
            join grading_fees c
                on UPPER(b.grading_cat) = UPPER(c.grading_cat)
            left join transport_cost d
                on UPPER(a.country) = UPPER(d.country)
            left join platform_fees e
                on UPPER(a.platform) = UPPER(e.platform)
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
            where status = 'shipped'
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
