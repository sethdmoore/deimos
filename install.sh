rm -rf /usr/local/lib/python2.7/deimos
/root/deimos/setup.py bdist_egg
easy_install /root/deimos/dist/deimos-0.4.3-py2.7.egg
rm -f /tmp/mesos/meta/slaves/latest
for i in $(docker ps | awk '{print $1}'); do docker kill $i; done
killall -9 deimos
restart mesos-slave
