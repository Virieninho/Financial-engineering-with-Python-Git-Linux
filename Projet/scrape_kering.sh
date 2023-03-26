#!/bin/bash

echo "$(date +'%Y-%m-%d %H:%M:%S'),$(curl -s https://www.tradingsat.com/kering-FR0000121485/ | grep '<span class="price">' | sed 's/.*>\([^<]*\)<.*/\1/')" >> kering_price.csv
