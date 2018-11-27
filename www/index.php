<!DOCTYPE html>
<!-- Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-11-23
   - Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

   - Dies ist die INDEX HTML-Datei. -->

<html>
<head>

<title>
Raspi Smart-Home
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
echo "<form action='' method='POST'>
	<input type='button' value='Urlaubsmdous' name='holiday' onclick='1'>
	<input type='text' name='fanfz' value=".$_POST['fanfz'].">
	<input type='text' name='fendz' value=".$_POST['fendz']."><p>";
$anfz=$_POST['fanfz'];
$endz=$_POST['fendz'];

	foreach ($xml->device as $device){
	echo $device->name."<input type='checkbox' id='check' name='fcheck".$device['id']."'><br>";
	}

echo "<input type='submit' value='ok'></form>";
//print_r($_POST);

	foreach($xml->device as $device1){
	$indent = "fcheck".$device1['id'];
	//echo $indent."&nbsp";

		If($_POST[$indent]){
		$device1->status = 'on';
		//echo $device1->name.$device1->status."<br>";
		}

		else{
		$device1->status = 'off';
		//echo $device1->name.$device1->status."<br>";
		}
	}

//print_r($xml);
?>
<form action="settings.php" target="_self">
<input type="submit" value="Einstellungen">
</form>



</body>
</html>
