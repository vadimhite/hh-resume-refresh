build:
	docker build -t hh-resume-refresh .
run:
	docker run -v "$(CURDIR):/app" --rm --name hh-resume-refresh hh-resume-refresh python ./main.py
auth:
	docker run -it -v "$(CURDIR):/app" --rm --name hh-resume-refresh hh-resume-refresh python ./auth.py
