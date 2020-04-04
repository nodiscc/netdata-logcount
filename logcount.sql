#
# @synopsis: level-count
# @description: Print out the number of log messages from the past 5 minutes and broken down by log level
# @reference: https://github.com/tstack/lnav/issues/721
#

;WITH level_counts AS
    (SELECT log_level, count(*) AS total
       FROM all_logs
       WHERE log_time >= timeslice(datetime(CURRENT_TIMESTAMP, 'localtime'), '300sec')
       GROUP BY log_level)
   SELECT 'total' AS log_level, sum(total) AS total FROM level_counts
   UNION
   SELECT * FROM level_counts
:write-csv-to -

