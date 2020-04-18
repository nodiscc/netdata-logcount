# netdata-logcount

Check/graph the number of syslog messages, by level over time.

<!-- TODO SCREENSHOT ![](https://i.imgur.com/ebD2MTW.png) -->

This is a `python.d` plugin for [netdata](https://my-netdata.io/). It parses output from [lnav](https://lnav.org/).

Maximum acceptable number of error/warning/info log messages over the configured time period can be configured, alarms will be raised if log message counts exceed this level.


## Installation

This plugin expects the CSV output of this [lnav script](logcount.sql) at `/var/log/logcount.log`

```bash
# install lnav
apt install lnav
# clone the repository
git clone https://gitlab.com/nodiscc/netdata-logcount

# edit configuration values in these files, notably the periodicity of logcount file generation,
# update interval for the chart and alarms, and warning/critical thresholds for number of log messages
nano netdata-logcount/health.d_logcount.conf
nano netdata-logcount/cron.d_logcount
nano netdata-logcount/logcount.sql

# copy files in place
sudo mkdir /opt/netdata-logcount
sudo cp netdata-logcount/opt_netdata-logcount_logcount.sql /opt/netdata-logcount/logcount.sql
sudo cp netdata-logcount/cron.d_logcount /etc/cron.d/logcount
sudo cp netdata-logcount/logcount.chart.py /opt/netdata/usr/libexec/netdata/python.d/
sudo cp netdata-logcount/python.d_logcount.conf /opt/netdata/etc/netdata/python.d/
sudo cp netdata-logcount/health.d_logcount.conf /opt/netdata/etc/netdata/health.d/logcount.conf

# generate the initial lgocount file
sudo lnav -n -f /opt/netdata-logcount/logcount.sql > /var/log/logcount.log

# restart netdata
systemctl restart netdata

```

## Configuration

- Change log parsing interval in `/etc/cron.d/logcount /opt/netdata-logcount/logcount.sql`
- Chart refresh time/common `python.d` plugin options can be changed in [`/opt/netdata/etc/netdata/health.d/logcount.conf`](python.d_logcount.conf)
- Alarm settings can be changed in [`health.d_logcount.conf`](health.d_logcount.conf)

Browse logs by running `sudo lnav` from a terminal, and read the [documentation](https://lnav.readthedocs.io/en/latest/)


## Debug

To debug this plugin:

```bash
$ sudo su -s /bin/bash netdata
$ /opt/netdata/usr/libexec/netdata/plugins.d/python.d.plugin 1  debug trace logcount
```


## License

[GNU GPLv3](LICENSE)

## Mirrors

- https://github.com/nodiscc/netdata-logcount
- https://gitlab.com/nodiscc/netdata-logcount

