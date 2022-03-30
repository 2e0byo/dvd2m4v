.Phony: install uninstall

dist/dvd2m4v*.whl: dvd2m4v.py
	poetry build

install:
	install -d /usr/local/bin
	pip3 install dist/*.whl
	install dvd2m4v.conf /etc/
	install -d /usr/lib/systemd/system
	install dvd2m4v.service /usr/lib/systemd/system
	install dvd2m4v.timer /usr/lib/systemd/system
	systemctl daemon-reload
	systemctl enable dvd2m4v.timer
	systemctl start dvd2m4v.timer

uninstall:
	pip3 uninstall dvd2m4v
	rm -f /etc/dvd2m4v
	rmdir /usr/local/bin || echo "Not removing dir /usr/local/bin as not empty"
	systemctl stop dvd2m4v.timer
	systemctl disable dvd2m4v.timer
	rm -f /usr/lib/systemd/system/dvd2m4v.service
	rm -f /usr/lib/systemd/system/dvd2m4v.timer
	rmdir /usr/lib/systemd/system || echo "Not removing dir /usr/lib/systemd/system as not empty"
	systemctl daemon-reload
