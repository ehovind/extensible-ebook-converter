echo "Testing eecon-fetcher.py"
./eecon_fetcher.py --source "http://runeberg.org/download.pl?mode=txtzip&work=karlekt"
./eecon_fetcher.py --title karlekt --auto-utf8
./eecon_fetcher.py --title karlekt --auto-populate
./eecon_fetcher.py --title karlekt --auto-markup
echo "----------------------------------------------------"
echo "Testing eecon-analyzer.py"
./eecon_analyzer.py --title karlekt --lang sv
./eecon_analyzer.py --title karlekt --markup lxml --lang sv
echo "----------------------------------------------------"
echo "Testing eecon-converter.py"
./eecon_converter.py --title karlekt

sleep 2

echo "Testing eecon-fetcher.py"
./eecon_fetcher.py --source "http://runeberg.org/download.pl?mode=txtzip&work=herrgard"
./eecon_fetcher.py --title herrgard --auto-utf8
./eecon_fetcher.py --title herrgard --auto-markup
echo "----------------------------------------------------"
echo "Testing eecon-analyzer.py"
./eecon_analyzer.py --title herrgard --lang sv
./eecon_analyzer.py --title herrgard --markup lxml --lang sv
echo "----------------------------------------------------"
echo "Testing eecon-converter.py"
./eecon_converter.py --title herrgard
