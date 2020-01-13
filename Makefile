work:
	python -u server.py |tee ser.log
clean:
	rm -f  *.o

cleanall: clean
	rm -f  y.* lex.yy.c mu

