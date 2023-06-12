variacao = """
SELECT 
	a.moeda,
	vlanter,
	vlatual,
	CAST(percent AS float) as percent,
	CASE WHEN b.MOEDA is not null then 'S' ELSE 'N' END AS FAVORITA
 FROM MARKETANTIG a
 LEFT JOIN FAVORITAS b ON a.moeda = b.moeda
GROUP BY a.moeda,vlanter,vlatual,percent
ORDER BY 4 DESC
"""

favoritas = """
SELECT * FROM (
SELECT 
	a.moeda,
	vlanter,
	vlatual,
	CAST(percent AS float) as percent,
	CASE WHEN b.MOEDA is not null then 'S' ELSE 'N' END AS FAVORITA
 FROM MARKETANTIG a
 LEFT JOIN FAVORITAS b ON a.moeda = b.moeda
GROUP BY a.moeda,vlanter,vlatual,percent
ORDER BY 4 DESC) T0
WHERE T0.FAVORITA = 'S'
"""

utlimaatualiz = """
select 
strftime('%d/%m/%Y às %H:%M',
	datetime(starttime/1000, 'unixepoch', '-3 hours')) 
from MARKETANTIG group by starttime
"""

checkmoeda = "SELECT COUNT(1) FROM FAVORITAS WHERE MOEDA = '{}'"