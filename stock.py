#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, Workflow, fields
from trytond.pyson import Eval
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.modules.stock import StockMixin

__all__ = ['Lot']
__metaclass__ = PoolMeta

class Lot():
    __name__ = 'stock.lot'

    used_lot = fields.Char('Used')

    @classmethod
    def __setup__(cls):
        super(Lot, cls).__setup__()

    @staticmethod
    def default_used_lot():
        return 'no_used'
