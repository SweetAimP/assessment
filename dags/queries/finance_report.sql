select
    a.platform,
    date_trunc('day',a.shipped_at)::date as shipped_at_day,
    a.platform,
    sum(a.sold_price) as total_income,
    sum(a.sold_price * 0.10 ) as buybay_fee,
    sum(a.sold_price * (c.cost/100)  ) as grading_fee,
    sum(d.transport_cost ) as transport_fee
from sold_products a join graded_products b
on a.license_plate = b.license_plate
join grading_fees c
on b.grading_cat = c.grading_cat
join transport_cost d
on a.country = d.country
where a.status = 'shipped' and date_trunc('day',a.shipped_at)::date = '2022-10-03'
group by platform, date_trunc('day',a.shipped_at)
order by 2 desc, platform;