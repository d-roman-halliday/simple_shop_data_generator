# simple_shop_data_generator
Python generator for a simple shop model for data testing, original code created by ChatGPT.

This is meant as an example for an approach, rather than a general tool (although there is no reason it can't be extended as such).
## Configuration
Use the [config.yaml](config.yaml) File for connections, either giving a whole URL, or by configureing the various required parts.

## View data
```
SELECT sci.id,
       sci.cart_id,
       sc.created_at,
       p.name          AS product_name,
       c.name          AS customer_name
  FROM shopping_cart_items sci  
    INNER JOIN shopping_carts sc ON sci.cart_id = sc.id
    INNER JOIN products        p ON p.id = sci.product_id   
    INNER JOIN customers       c ON sc.customer_id = c.id
;
```


# Testing & Configuration Notes

## Executed in Ubuntu
```
git clone git@github.com:d-roman-halliday/simple_shop_data_generator.git
python -m venv venv
source venv/bin/activate

cd simple_shop_data_generator/

pip install --upgrade pip
pip install -r requirements.txt

vi config.yaml

python simple_shop_data_generator.py

```
