        with cte_actions_with_min_ts as (
            select * 
                , row_number() over() as row_num 
                , min(timestamp) over(partition by userId, action_date, action_hour, lvl_3_cat) as first_ts
            from default.lab05_events_join_catalog_v
            where action in ('favAdd', 'favRemove') 
            and action_year = {start.year}
            and action_month = {start.month}
            and action_day = {start.day}
            --and action_year = 2020
            --and action_month = 11
            --and action_day = 25
        ) 
        , cte_with_actrion_rn as (
            select * 
                , row_number() over(partition by userId, action_date, action_hour, lvl_3_cat, itemId order by row_num) as rn_over_cat3
            from cte_actions_with_min_ts
        )
        , cte_with_score as (
            select * 
                ,case 
                    when action = 'favRemove' and rn_over_cat3 = 1 then 0
                    when action = 'favAdd' then 1 
                    when action = 'favRemove' then -1
                end as score
            from cte_with_actrion_rn
        )
        , cte as (
            select 
                userId
                , action_date
                , action_hour
                , lvl_3_cat
                , sum(score) as score_sum
                , count(case when action = 'favAdd' then 1 else null end) as add_cnt  --???
                , min(case when action = 'favAdd' then timestamp end) as first_ts
                --, min(timestamp) as first_ts
            from cte_with_score
            group by userId, action_date, action_hour, lvl_3_cat
        )
        ,cte_with_rn as (
            select 
                cte.*
                , row_number() over(partition by userId, action_date, action_hour order by score_sum desc, first_ts) as rn
            from cte 
            where add_cnt > 0
        )
        select 
            userId, action_hour, lvl_3_cat
        from cte_with_rn 
        where 1=1
            and rn <= 5
            --and userId = toUUID('7c60cc8b-fe2d-468a-9388-4919754e405a')
            --and action_hour = 18
        order by userId, action_hour, rn



/*

select lvl_3_cat, timestamp,  action
from default.lab05_events_join_catalog_v
where 1=1 
    and action in ('favAdd', 'favRemove')   
    and action_year = 2020
    and action_month = 11
    and action_day = 25
    and userId = toUUID('7c60cc8b-fe2d-468a-9388-4919754e405a')
    and action_hour = 18
order by timestamp


*/