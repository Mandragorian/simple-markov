TEST_DIR = tests
TESTS = $(wildcard $(TEST_DIR)/*_test.py)

clean:
	rm -rf *.pyc

test: clean $(TESTS)
	for test in $(TESTS); do\
		python3 -m unittest $$test ;\
	done

.PHONY: test
.PHONY: clean
