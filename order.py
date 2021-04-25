import logging
import json
import inspect

log = logging.getLogger(__name__)



class Order(object):
    """
    Represents an order made on Coinbase.
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
        "created_at": "2021-03-17T07:34:01.972518Z",
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
        if id:
            self.id_ = id
            del id
        else:
            self.id_ = id_
        self.product_id = product_id
        self.profile_id = profile_id
        self.side = side
        self.funds = funds
        self.specified_funds = specified_funds
        if type:
            self.type_ = type
            del type
        else:
            self.type_ = type_
        self.post_only = post_only
        self.created_at = created_at
        self.done_at = done_at
        self.done_reason = done_reason
        self.fill_fees = fill_fees
        self.filled_size = filled_size
        self.executed_value = executed_value
        self.status = status
        self.settled = settled

    def __repr__(self):
        return self._asdict()

    def _asdict(self):
        return {
            # should dict key be "id" or "_id"?
            "id": self.id_,
            "product_id": self.product_id,
            "profile_id": self.profile_id, 
            "side": self.side,
            "funds": self.funds,
            "specified_funds": self.specified_funds,
            # should key be "type" or "_type"?
            "type": self.type_,
            "post_only": self.post_only,
            "created_at": self.created_at,
            "done_at": self.done_at, 
            "done_reason": self.done_reason, 
            "fill_fees": self.fill_fees, 
            "filled_size": self.filled_size,  
            "executed_value": self.executed_value, 
            "status": self.status, 
            "settled": self.settled
        }

    def commit(self):
        # db.write
        """Save order to db"""
        pass

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