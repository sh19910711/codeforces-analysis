FROM apache/zeppelin:0.7.3

RUN cd lib && curl -O https://s3.amazonaws.com/athena-downloads/drivers/JDBC/SimbaAthenaJDBC_2.0.2/AthenaJDBC42_2.0.2.jar
ADD config/zeppelin-site.xml /zeppelin/conf/zeppelin-site.xml
