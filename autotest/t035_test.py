"""
Test zonbud utility
"""
import os
import numpy as np
from flopy.utils import ZoneBudget

pth = '../examples/data/zonbud_examples'
cbc_f = 'freyberg.gitcbc'

nrow, ncol = 40, 20
zon = np.zeros((1, nrow, ncol), np.int)
zon[0, :20, :10] = 1
zon[0, :20, 10:] = 2
zon[0, 20:, :10] = 3
zon[0, 20:, 10:] = 4
zon = np.random.randint(5, size=(1, 40, 20))


def test_zonbud_write_csv_kstpkper():

    zb = ZoneBudget(os.path.join(pth, cbc_f))
    zbud = zb.get_budget(zon, kstpkper=zb.get_kstpkper()[-1])
    zbud.to_csv(os.path.join(pth, 'zbud.csv'), write_format='zonbud')
    zbud.to_csv(os.path.join(pth, 'zbud_pandas.csv'), write_format='pandas')
    return


def test_zonbud_write_csv_totim():

    zb = ZoneBudget(os.path.join(pth, cbc_f))
    zbud = zb.get_budget(zon, totim=zb.get_times()[-1])
    zbud.to_csv(os.path.join(pth, 'zbud.csv'), write_format='zonbud')
    zbud.to_csv(os.path.join(pth, 'zbud_pandas.csv'), write_format='pandas')
    return


def test_zonbud_budget():

    zb = ZoneBudget(os.path.join(pth, cbc_f))
    zbud = zb.get_budget(zon, kstpkper=zb.get_kstpkper()[-1])

    recs = zbud.get_records()
    if recs.shape[0] == 0:
        raise Exception('No records returned.')
    recordlist = [('IN', 'CONSTANT HEAD'), ('IN', 'FROM ZONE 1')]
    recs = zbud.get_records(recordlist=recordlist, zones=[1, 3])
    if recs.shape[0] == 0:
        raise Exception('No records returned.')
    return


def test_zonbud_mass_balance():

    zb = ZoneBudget(os.path.join(pth, cbc_f))
    zbud = zb.get_budget(zon, kstpkper=zb.get_kstpkper()[-1])

    recs = zbud.get_mass_balance()
    if recs.shape[0] == 0:
        raise Exception('No records returned.')
    recs = zbud.get_total_outflow(zones=3)
    if recs.shape[0] == 0:
        raise Exception('No records returned.')
    recs = zbud.get_total_inflow(zones=(1, 2))
    if recs.shape[0] == 0:
        raise Exception('No records returned.')
    recs = zbud.get_percent_error()
    if recs.shape[0] == 0:
        raise Exception('No records returned.')
    return


def test_zonbud_aliases():

    zb = ZoneBudget(os.path.join(pth, cbc_f))

    aliases = {1: 'Trey', 2: 'Mike', 4: 'Page', 0: 'Carini'}
    zbud = zb.get_budget(zon, kstpkper=zb.get_kstpkper()[-1], aliases=aliases)
    zbud.to_csv(os.path.join(pth, 'zbud_aliases.csv'), write_format='zonbud')
    recs = zbud.get_records()
    if recs.shape[0] == 0:
        raise Exception('No records returned.')
    print(recs.dtype)
    print(recs)
    recordlist = [('IN', 'FROM Mike')]
    recs = zbud.get_records(recordlist=recordlist, zones=['Trey', 3])
    print(recs.dtype)
    print(recs)
    return


if __name__ == '__main__':

    test_zonbud_write_csv_kstpkper()
    test_zonbud_write_csv_totim()
    test_zonbud_aliases()
    test_zonbud_budget()
    test_zonbud_mass_balance()
