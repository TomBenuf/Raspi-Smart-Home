<!DOCTYPE html>
<!-- Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-11-23
   - Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

   - Dies ist die INDEX HTML-Datei. -->

<html>
<head>

<title>
Raspi Smar-tHome
</title>
<link rel="stylesheet" type="text/css" href="format.css" />
<meta http-equiv="content-type" content="text/html; charset=utf-8">

</head>
<body>
	<p> <h1>Ihre Smart-Home Steuerung für unterwegs.</h1> </p>
<?php


/* Läd XML und erstellt für jedes /devices/device einen Button.
 * Bis jetzt aber noch ohne Aktion */


 $xml = simplexml_load_file('status.xml');

echo "<form action='' method='POST'>";
	echo "<input type='text' name='fanfz' value=".$_POST['fanfz'].">";
	echo "<input type='text' name='fendz' value=".$_POST['fendz'].">";
	$anfz=$_POST['fanfz'];
	$endz=$_POST['fendz'];
	foreach ($xml->device as $device)
		{
		echo "<input type='button' value=".$device->name."id='button1' name='f".$device->name."'onclick='1'>";
		//$_POST['f'.$device->name.''];

			If($_POST['f'.$device->name.'']==1)
			{$device->name=$_POST['f'.$device->name.''];
			}
		}
$daten='$device->name'.'$anfz'.'$endz';
echo "</form>";
$send=fopen('status.xml');
fwrite($send,$daten);
fclose($send);
?>
<form action="settings.php" target="_self">
<input type="submit" value="Einstellungen">
</form>



</body>
</html>
