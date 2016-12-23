#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
import operator
import itertools
import datetime
from sql import Table
from sql.functions import Overlay, Position
from sql.aggregate import Max
from sql.operators import Concat

from trytond.model import Workflow, ModelView, ModelSQL, fields
from trytond.modules.company import CompanyReport
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond import backend
from trytond.pyson import Eval, Not, Equal, If, Or, And, Bool, In, Get, Id
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond.tools import reduce_ids, grouped_slice

__all__ = ['ShipmentIn', 'ShipmentInternal']
__metaclass__ = PoolMeta

class ShipmentIn():
    "Supplier Shipment"
    __name__ = 'stock.shipment.in'

    @classmethod
    def __setup__(cls):
        super(ShipmentIn, cls).__setup__()

    @classmethod
    @ModelView.button
    @Workflow.transition('received')
    def receive(cls, shipments):
        Move = Pool().get('stock.move')
        Lot = Pool().get('stock.lot')
        lots = None

        for shipment in shipments:
            for move in shipment.moves:
                if move.num_lot :
                    lots = Lot.search([('number', '=', move.num_lot), ('product', '=', move.product)])

                    if lots:
                        for lot in lots:
                            move.lot = lot
                            move.save()
                    else:
                        lot = Lot()
                        lot.number = move.num_lot
                        lot.product = move.product.id
                        lot.save()
                        move.lot = lot
                        move.save()

                    lot = Lot()
                    lot.number = move.num_lot
                    lot.product = move.product.id
                    lot.save()
                    move.lot = lot
                    move.save()
        Move.do([m for s in shipments for m in s.incoming_moves])

        cls.create_inventory_moves(shipments)

class ShipmentInternal():
    "Internal Shipment"
    __name__ = 'stock.shipment.internal'

    @classmethod
    @ModelView.button
    @Workflow.transition('waiting')
    def wait(cls, shipments):
        Move = Pool().get('stock.move')
        Lot = Pool().get('stock.lot')
        lots = None

        # First reset state to draft to allow update from and to location
        Move.draft([m for s in shipments for m in s.moves])
        for shipment in shipments:
            for move in shipment.moves:
                if move.num_lot :
                    lots = Lot.search([('number', '=', move.num_lot), ('product', '=', move.product)])
                    if lots:
                        for lot in lots:
                            move.lot = lot
                            move.save()
                    else:
                        lot = Lot()
                        lot.number = move.num_lot
                        lot.product = move.product.id
                        lot.save()
                        move.lot = lot
                        move.save()
                    print "pasa hasta aqui" , lot, move

            Move.write([m for m in shipment.moves
                    if m.state != 'done'], {
                    'from_location': shipment.from_location.id,
                    'to_location': shipment.to_location.id,
                    'planned_date': shipment.planned_date,
                    })
