with traffic_data as (
    select * from public.traffic_data
),
i80_stations as (
  select * from public.i80_stations
),
station_summary as (
  select * from public.station_summary
),
final as (
    select 
        i80_stations.ID,
        i80_stations.Name,
        traffic_data.utc_time_id,
        traffic_data.avg_travel_time,
        station_summary.flow_max
        from i80_stations
        inner join station_summary 
        on station_summary.ID = i80_stations.id  
        inner join traffic_data 
        on station_summary.ID = traffic_data.source_id
        where traffic_data.utc_time_id = '03/01/2016 16:18'
)
select 
  * 
from final
