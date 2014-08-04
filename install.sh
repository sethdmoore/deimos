rm -rf /usr/local/lib/python2.7/deimos
/root/deimos/setup.py bdist_egg
easy_install /root/deimos/dist/deimos-0.4.3-py2.7.egg
restart mesos-slave
