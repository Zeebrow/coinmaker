import logging
import json
import inspect
import CONSTANTS as C

log = logging.getLogger(__name__)



class Order(object):
    """
    My description of an order made on Coinbase.
    Let's keep instance attributes explicit since they are crucial to get right.
    """
    ex_order = {
        "id": "74130f08-baac-4430-b1ec-5aee0df98379",
        "product_id": "ETH-USD",
        "profile_id": "bce73511-6c46-48fd-83c1-31002ed36d93", 
        "side": "buy",
        "funds": "9.9502487500000000",
        "specified_funds": "10.0000000000000000",
        "type": "market",
        "post_only": "false",
        # "created_at": "2021-03-17T07:34:01.972518Z",
        "created_at": "2021-03-17T07:34:01.972518",
        "done_at": "2021-03-17T07:34:01.982Z", 
        "done_reason": "filled", 
        "fill_fees": "0.0497512000275000", 
        "filled_size": "0.00558165",  
        "executed_value": "9.9502400055000000", 
        "status": "done", 
        "settled": "true"
    }

    def __init__(self, product_id, profile_id,
        side, funds, specified_funds, post_only, 
        created_at, done_at, done_reason, fill_fees, filled_size,
        executed_value, status, settled, 
        type_=None, id_=None, id=None, type=None):
        self.id_ = id if id else id_
        self.product_id = product_id
        self.profile_id = profile_id
        self.side = side
        self.funds = funds
        self.specified_funds = specified_funds
        self.type_ = type if type else type_
        self.post_only = post_only
        self.created_at = created_at
        self.done_at = done_at
        self.done_reason = done_reason
        self.fill_fees = fill_fees
        self.filled_size = filled_size
        self.executed_value = executed_value
        self.status = status
        self.settled = settled

    def __str__(self):
        return json.dumps(self._asdict(), indent=C.DEFAULT_JSON_INDENT)

    def __repr__(self):
        return self._asdict()

    def _asdict(self):
        return {
            # should dict key be "id" or "_id"?
            "id": self.id_,
            "product_id": self.product_id,
            "profile_id": self.profile_id, 
            "side": self.side,
            "funds": float(self.funds),
            "specified_funds": float(self.specified_funds),
            # should key be "type" or "_type"?
            "type": self.type_,
            "post_only": self.post_only,
            "created_at": self.created_at,
            "done_at": self.done_at, 
            "done_reason": self.done_reason, 
            "fill_fees": float(self.fill_fees), 
            "filled_size": float(self.filled_size),  
            "executed_value": float(self.executed_value), 
            "status": self.status, 
            "settled": self.settled
        }

    def commitable(self):
        # db.write
        """Save order to db"""
        return self._map_for_commit(measurement=self.product_id)

    def _map_for_commit(self, measurement):
        """See XYZ for format"""
        return [{
            "measurement": measurement,
            # "tags": {**self._asdict()},
            "tags": {"Will_this_work": "question_mark"},
            "time": self.done_at,
            "fields":{
                **self._asdict()
            }
        }]
#         return [
#     {
#         "measurement": "cpu_load_short",
#         "tags": {
#             "host": "server01",
#             "region": "us-west"
#         },
#         "time": "2009-11-10T23:00:00Z",
#         "fields": {
#             "value": 0.64
#         }
#     }
# ]
    def save(self, out_file, indent=None):
        """write (append) to file"""
        with open(out_file, 'a') as f:
            f.write(json.dumps(self.__dict__, indent=indent))


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' ))
    logger.addHandler(sh)
    logger.info("order.py")

    Test_Order = {
        "id": "74130f08-baac-4430-b1ec-5aee0df98379",
        "product_id": "ETH-USD",
        "profile_id": "bce73511-6c46-48fd-83c1-31002ed36d93", 
        "side": "buy",
        "funds": "9.9502487500000000",
        "specified_funds": "10.0000000000000000",
        "type": "market",
        "post_only": "false",
        "created_at": "2021-03-17T07:34:01.972518Z",
        "done_at": "2021-03-17T07:34:01.982Z", 
        "done_reason": "filled", 
        "fill_fees": "0.0497512000275000", 
        "filled_size": "0.00558165",  
        "executed_value": "9.9502400055000000", 
        "status": "done", 
        "settled": "true"
    }
    o = Order(**Test_Order)
    print(o.__dict__)
    o.save('order.json')
    print(o._asdict())