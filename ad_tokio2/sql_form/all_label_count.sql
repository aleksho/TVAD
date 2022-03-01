SELECT YEAR(V.start_write_file) as year, DAYOFYEAR(V.start_write_file) as day_of_year, A.type, count(*)
FROM vsilence AS S
INNER JOIN vvideo as V
    ON S.video_id=V.id
INNER JOIN dinfo as D
    ON V.device_id=D.id
INNER JOIN adcatalog as A
    ON S.found_ad_id=A.ad_id
-- where
--     A.type in ('no_ad', 'ad')

group by 1, 2, 3;