# netdata-logcount

Check/graph the number of syslog messages, by level over time.

![](https://gitlab.com/nodiscc/toolbox/-/raw/master/DOC/SCREENSHOTS/FQqBT7o.png)

This is a `python.d` plugin for [netdata](https://my-netdata.io/). It parses output from [lnav](https://lnav.org/).

Maximum acceptable number of error/warning/info log messages over the configured time period can be configured, alarms will be raised if log message counts exceed this level.


## Installation

This plugin expects the CSV output of a [lnav](https://lnav.org/) [script](logcount.sql) at `/var/cache/logcount`

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
netdata_install_prefix="/opt/netdata" # if netdata is installed from binary/.run script
netdata_install_prefix="" # if netdata is installed from OS packages
sudo cp netdata-logcount/logcount.sql /opt/netdata-logcount/logcount.sql
sudo cp netdata-logcount/cron.d_logcount /etc/cron.d/logcount
sudo cp netdata-logcount/logcount.chart.py $netdata_install_prefix/usr/libexec/netdata/python.d/
sudo cp netdata-logcount/python.d_logcount.conf $netdata_install_prefix/etc/netdata/python.d/logcount.conf
sudo cp netdata-logcount/health.d_logcount.conf $netdata_install_prefix/etc/netdata/health.d/logcount.conf

# generate the initial lgocount file
sudo lnav -n -f /opt/netdata-logcount/logcount.sql > /var/cache/logcount
sudo chgrp netdata /var/cache/logcount
sudo chmod g+r /var/cache/logcount

# restart netdata
systemctl restart netdata

```

You can also install this module using the [`nodiscc.xsrv.monitoring` ansible role](https://gitlab.com/nodiscc/xsrv/-/tree/master/roles/monitoring).


## Configuration

- Change log parsing interval in `/etc/cron.d/logcount /opt/netdata-logcount/logcount.sql`
- Chart refresh time/common `python.d` plugin options can be changed in [`$netdata_install_prefix/etc/netdata/python.d/logcount.conf`](python.d_logcount.conf)
- Alarm settings can be changed in [`$netdata_install_prefix/etc/netdata/health.d/logcount.conf`](health.d_logcount.conf) (see [Netdata health alarm configuration](https://learn.netdata.cloud/docs/monitor/configure-alarms)). For example, set `to: silent` to prevent sending mail notifications for an alarm.

Browse logs by running `sudo lnav` from a terminal, and read the [documentation](https://lnav.readthedocs.io/en/latest/)


## Debug

To debug this plugin:

```bash
$ sudo su -s /bin/bash netdata
$ $netdata_install_prefix/usr/libexec/netdata/plugins.d/python.d.plugin 1  debug trace logcount
```

Due to the way the plugins works (parse lnav output generated each X minutes, for messages over last X minutes), message counts shown in the graph represent counts over **the previous period**.

## License

[GNU GPLv3](LICENSE)

## Mirrors

- https://github.com/nodiscc/netdata-logcount
- https://gitlab.com/nodiscc/netdata-logcount

