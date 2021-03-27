#Coinmaker

##Market Buy (not settled)
{
  "id": "74130f08-baac-4430-b1ec-5aee0df98379",
  "product_id": "ETH-USD",
  "side": "buy",
  "stp": "dc", <----------------------------------------------------- #not gonna use this
  "funds": "9.95024875",
  "specified_funds": "10",
  "type": "market",
  "post_only": false,
  "created_at": "2021-03-17T07:34:01.972518Z",
  "fill_fees": "0",
  "filled_size": "0",
  "executed_value": "0",
  "status": "pending",
  "settled": false
}

##Market Buy (settled)
{
  "id": "74130f08-baac-4430-b1ec-5aee0df98379",
  "product_id": "ETH-USD",
  "profile_id": "bce73511-6c46-48fd-83c1-31002ed36d93", <-----------------------------------------------------
  "side": "buy",
  "funds": "9.9502487500000000",
  "specified_funds": "10.0000000000000000",
  "type": "market",
  "post_only": false,
  "created_at": "2021-03-17T07:34:01.972518Z",
  "done_at": "2021-03-17T07:34:01.982Z", <-----------------------------------------------------
  "done_reason": "filled", <-----------------------------------------------------
  "fill_fees": "0.0497512000275000", 
  "filled_size": "0.00558165",  
  "executed_value": "9.9502400055000000", 
  "status": "done", 
  "settled": true
}

##Limit Buy
{
  "id": "345adc70-6020-45e3-be73-fc57d812a5a4",
  "price": "1100.00000000",
  "size": "0.01000000",
  "product_id": "ETH-USD",
  "profile_id": "bce73511-6c46-48fd-83c1-31002ed36d93",
  "side": "buy",
  "type": "limit",
  "time_in_force": "GTC",
  "post_only": true,
  "created_at": "2021-03-27T02:59:14.132209Z",
  "fill_fees": "0.0000000000000000",
  "filled_size": "0.00000000",
  "executed_value": "0.0000000000000000",
  "status": "open",
  "settled": false
}

##Limit Sell
{
  "id": "50017be0-dd85-439f-938d-6903ffdcfa5c",
  "price": "1800.00000000",
  "size": "0.00100000",
  "product_id": "ETH-USD",
  "profile_id": "bce73511-6c46-48fd-83c1-31002ed36d93",
  "side": "sell",
  "type": "limit",
  "time_in_force": "GTC",
  "post_only": true,
  "created_at": "2021-03-27T02:58:23.460517Z",
  "fill_fees": "0.0000000000000000",
  "filled_size": "0.00000000",
  "executed_value": "0.0000000000000000",
  "status": "open",
  "settled": false
}


