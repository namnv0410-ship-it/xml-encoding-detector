xml-encoding-detector

Lightweight XML encoding detector for Python.



Features

UTF-8 BOM detection

UTF-16 LE/BE BOM detection

UTF-32 LE/BE BOM detection

XML declaration parsing

Encoding alias normalization

Installation

pip install xml-encoding-detector

Usage

from xml\_encoding\_detector import (

&#x20;   detect\_encoding,

)



xml = (

&#x20;   b'<?xml version="1.0" '

&#x20;   b'encoding="Shift\_JIS"?>'

)



result = detect\_encoding(xml)



print(result.encoding)

print(result.confidence)

print(result.source)

Example Output

shift\_jis

0.9

xml-declaration

