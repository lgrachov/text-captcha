.PHONY: start cleanup

start:
	make cleanup
	python3 app.py

cleanup:
	rm -f img_* && echo "Removed all images"