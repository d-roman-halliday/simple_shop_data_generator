# simple_shop_data_generator
Python generator for a simple shop model for data testing, original code created by ChatGPT.

This is meant as an example for an approach, rather than a general tool (although there is no reason it can't be extended as such).
## Configuration
Use the [config.yaml](config.yaml) File for connections, either giving a whole URL, or by configureing the various required parts.

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
