#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, Workflow, fields
from trytond.pyson import Eval
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.modules.stock import StockMixin

__all__ = ['Lot', 'Move', 'SplitMove']
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

class Move():
    __name__ = 'stock.move'

    num_lot = fields.Char('Series')

    @classmethod
    def __setup__(cls):
        super(Move, cls).__setup__()

class SplitMove():
    'Split Move'
    __name__ = 'stock.move.split'

    def default_start(self, fields):
        pool = Pool()
        Move = pool.get('stock.move')
        default = {}
        move = Move(Transaction().context['active_id'])
        default['uom'] = move.uom.id
        default['unit_digits'] = move.unit_digits
        default['uom_category'] = move.uom.category.id
        default['count'] = move.purchase_quantity
        default['quantity'] = 1
        return default
