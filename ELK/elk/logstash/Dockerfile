FROM docker.elastic.co/logstash/logstash:6.8.23

# Add your logstash plugins setup here
RUN logstash-plugin install logstash-filter-prune
RUN logstash-plugin install logstash-output-clickhouse