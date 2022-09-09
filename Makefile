build:
	docker build -t hh-resume-refresh .
run:
	docker run -it -d --restart unless-stopped --name hh-resume-refresh hh-resume-refresh
