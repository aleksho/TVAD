SELECT S.id, A.id, A.type, D.name, V.folder_name, S.second, S.video_id, V.start_write_file,D.place, DAYOFYEAR(V.start_write_file) as day_of_year, V.channel_id
FROM vsilence AS S
INNER JOIN vvideo as V
    ON S.video_id=V.id
INNER JOIN dinfo as D
    ON V.device_id=D.id
INNER JOIN adcatalog as A
    ON S.found_ad_id=A.ad_id
where
YEAR(V.start_write_file) = 2021
and DAYOFYEAR(V.start_write_file)  BETWEEN {start} AND {end}
and A.type = '{label}'
and S.image_status = 2
LIMIT {limit};