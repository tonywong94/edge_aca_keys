from astropy.table import Table
from astropy.coordinates import SkyCoord

t = Table.read('ACAonly_updated.csv')

with open('target_definitions_new.txt','w') as f:
    for row in t:
        c = SkyCoord(ra=row['RA'], dec=row['DE'], frame='fk5', unit=('deg','deg'))
        f.write(' '.join([row['Name'], c.to_string(style='hmsdms'), '{0}'.format(row['Vlsr']),' 800\n']))

f.close()
