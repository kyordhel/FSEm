PREFIX  = practica
SILENT  = @
JOB     = "FSEm - $(PREFIX) 08"
RUBBER  = rubber
RFLAGS  = --pdf --force

ASPELL  = aspell --lang=en_GB --mode=tex \
          --extra-dicts=./extra-dict.pws list <
TEMP	= *.aux *.blg *.log *.out *.tmp *.synctex.gz
RMFILES = $(TEMP) *~ *.toc *.idx *.ilg *.ind *.log *.lot *.lof \
          *.adx *.and *.abb *.ldx .temp* *.tar mergedfile.pdf


%.pdf: %.tex
	$(SILENT) $(RUBBER) $(RFLAGS) $@

all:
	$(SILENT) make -s build
	$(SILENT) make -s clean
#	 $(SILENT) make -s warnspell
	$(SILENT) make -s launch

build:
	$(SILENT) rm -f $(TEMP)
	$(SILENT) rubber --pdf --force --jobname=$(JOB) $(PREFIX).tex
# 	$(SILENT) rubber --pdf --force $(PREFIX).tex

clean:
	$(SILENT) rubber --clean $(PREFIX).tex
	$(SILENT) rubber --clean --jobname=$(JOB) $(PREFIX).tex
# 	$(SILENT) rm -f figures/*-converted-to.pdf
	$(SILENT) rm -f $(TEMP)

launch:
# 	$(SILENT) gnome-open $(PREFIX).pdf &> /dev/null
	$(SILENT) xdg-open $(JOB).pdf &> /dev/null

warnspell:
	./warnspell.sh
