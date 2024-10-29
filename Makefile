
.PHONY: run
run:
	cd db && make build && make run && cd .. && \
	cd migrations && make build && make run && cd .. && \
	cd api && make build && make run && cd ..
