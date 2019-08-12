## Filebeat Notes
- filebeat.inputs.paths param only accepts absolute path

filebeat -e -v -c /etc/filebeat.yml -d '*'
filebeat -e -v -c filebeat.yml -d '*'


filebeat -e -v -c /Users/sammiebae/Desktop/data-infra-notes/filebeats/filebeat.yml -d '*'