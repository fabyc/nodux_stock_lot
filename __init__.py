#This file is part of Tryton.  The COPYRIGHT file at the top level of this
#repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from .stock import *
from .sale import *


def register():
    Pool.register(
        Lot,
        SaleLine,
        module='nodux_stock_lot', type_='model')
