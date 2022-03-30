.Phony: install uninstall

install:
	install -d /usr/local/bin
	install dvd2mkv.py /usr/local/bin/dvd2mk4
	install dvd2mkv.conf /etc/
	install -d /usr/lib/systemd/system
	install dvd2mkv.service /usr/lib/systemd/system
	install dvd2mkv.timer /usr/lib/systemd/system
	systemctl daemon-reload
	systemctl enable dvd2mkv.timer
	systemctl start dvd2mkv.timer
