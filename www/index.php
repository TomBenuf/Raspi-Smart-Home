<!DOCTYPE html>
<!-- Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-11-08
   - Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

   - Dies ist die INDEX HTML-Datei. -->

<html>
<head>

</head>
<body>
	<h3> IT WORKS! </h3>
	This is the example index.html for the raspi-smart-home project.<br>
	Plus it has some php now :O
	<p>

<?php

/* Läd XML und erstellt für jedes /devices/device einen Button.
 * Bis jetzt aber noch ohne Aktion */

$xml = simplexml_load_file('status.xml');

echo "<form action='' method='POST'>";

foreach ($xml->device as $device){
	echo "<input type='button' value=".$device->name.">";
	}
echo "</form>";

?>
</body>
</html>
