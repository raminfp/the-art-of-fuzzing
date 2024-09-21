<?php
$dom = new DomDocument;
$dom->loadXML('<root></root>');
$e = $dom->createElement('e');
$e->appendChild($dom);
