#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval

__all__ = ['SaleLine']
__metaclass__ = PoolMeta


class SaleLine:
    __name__ = 'sale.line'

    @classmethod
    def __setup__(cls):
        super(SaleLine, cls).__setup__()

    def get_move(self, shipment_type):
        move = super(SaleLine, self).get_move(shipment_type)

        if move and self.lot:
            for lote in self.lot:
                if lote.lot:
                    move.lot = lote.lot
                    lot = lote.lot
                    lot.used_lot = 'used'
                    lot.save()
        return move
