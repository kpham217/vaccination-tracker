-- check the tables
select* from prj.general;

select * from prj.counties;

-- denormalised table by adding density to general table 
select g.id, g.clinicName, g.gisX, g.gisY, g.counties, c.density
from prj.general as g
left join prj.counties as c
on g.counties = c.counties;

-- check tables
select * from prj.denormalised_data;

select * from prj.halifax_density as h;

-- count the number of clinics
select d.counties,count(*) as c
from prj.denormalised_data as d
group by counties
order by c desc;

-- replace Halifax density
select n.id, n.clinicName, n.counties, h.density
from prj.general as n
left join prj.halifax_density as h
on n.id = h.clinicID
where n.counties='Halifax'
order by h.density; 

-- select the Cabe Breton information
select * from prj.denormalised_data
where counties='Cape Breton';


-- select the counties where density > 10 and density < 10
select counties
from prj.denormalised_data as d
where d.density > 10
group by counties;

select counties
from prj.denormalised_data as d
where d.density < 10
group by counties;

-- find the clinic with id
select *
from prj.denormalised_data
where id = '6a88e3d9-49fd-462f-b6dc-6415058f74e3';
