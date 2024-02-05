with 
base_table as (
    select
        a.platform,
        date_trunc('day',a.shipped_at)::date as shipped_at_day,
        a.sold_price,
        a.sold_price * 0.10  as buybay_fee,
        a.sold_price * (c.cost/100) as grading_fee,
        d.transport_cost as transport_fee
    from sold_products a join graded_products b
    on a.license_plate = b.license_plate
    join grading_fees c
    on b.grading_cat = c.grading_cat
    join transport_cost d
    on a.country = d.country
    left join platform_fees e
    on a.platform = e.platform
    where a.status = 'shipped'
),
partners_payout as (
    select
        *,
        sold_price - buybay_fee - transport_fee - platform_fee - grading_fee as partner_payout
    from base_table a
),
aggregatted_fees as (
    select
        platform,
        shipped_at_day,
        sum(sold_price) total_income,
        sum(buybay_fee) total_buybay_fee,
        sum(grading_fee) total_grading_fee,
        sum(platform_fee) total_platform_fee,
        sum(transport_fee) total_transport_fee,
        sum(partner_payout) total_partner_payout
    from partners_payout
    group by platform, shipped_at_day
)
select
    platform,
    shipped_at_day,
    total_income,
    total_buybay_fee,
    total_grading_fee,
    (total_buybay_fee + total_grading_fee + total_platform_fee) total_fees,
    total_transport_fee,
    total_partner_payout
from aggregatted_fees;