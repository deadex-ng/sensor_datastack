with traffic_data as (
    select * from public.traffic_data
),
I80_stations as (
  select * from public.i80_stations
),
final as (
    select 
        i80_stations.ID,
        i80_stations.Name,
        traffic_data.utc_time_id,
        traffic_data.avg_travel_time
        from i80_stations
        inner join traffic_data on traffic_data.source_id = i80_stations.id 
        where traffic_data.avg_travel_time = 71 order by utc_time_id
)
select 
  * 
from final 
