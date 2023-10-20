## Folder Structure

- data_read.py: 
    - used in milestone 2
    - read kafka data of 24 hours time period
    - parameters are as follows:

```
# read from last x hours
# example of data file name: kafka_ratings_1681235685000_1h.csv
> python3 data_read.py hours x

# read from yesterday 00:00 - 23:59
> python3 data_read.py day

# read from the given day 00:00 - 23:59
> python3 data_read.py day 2023-03-24

# read from x days before today 00:00-23:59
# for example, set x=3 at 2022/04/11 will get the data from 2022/04/08 to 2022/04/10
# the data file will be named as kafka_ratings_20220408_20220410.csv
> python3 data_read.py days x
```

- scripts_archive:
    - data processing codes for milestone 1


