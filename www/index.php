<!DOCTYPE html>
<!-- Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-11-23
   - Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

   - Dies ist die INDEX HTML-Datei. -->

<html>
<head>
<title>Raspi Smart-Home</title>
<link rel="stylesheet" type="text/css" href="format.css" />
<meta http-equiv="content-type" content="text/html; charset=utf-8">

</head>
<body>
	<p> <h1>Ihre Smart-Home Steuerung für unterwegs.</h1> </p>
	
<?php
// Läd XML und erstellt für jedes /devices/device einen Button.

echo "<form action='' method='POST'><p>
	Einschaltzeit eingeben: <input type='text' name='fanfz' value=".$_POST['fanfz']."><br>
	Ausschaltzeit eingeben: <input type='text' name='fendz' value=".$_POST['fendz']."></p><p>";

$xml = simplexml_load_file('status.xml');

if(isset($_POST['submit'])){
	//echo "Submitted";
	
	//Schreibt Werte die in Chekcboxen ausgewählt wurden in $xml
	foreach($xml->device as $device1){
		$indent = "fcheck".$device1['id'];

		If(isset($_POST[$indent])){
			$device1->status = 'on';

			If(isset($_POST['fanfz'])){
				$xml->device->timer->on = strtotime($_POST['fanfz']);
			}

			If(isset($_POST['fendz'])){
				$xml->device->timer->off = strtotime($_POST['fendz']);
			}
		}

		else{
			$device1->status = 'off';
		}
	}

	If(isset($_POST['holiday'])){
		$xml->holiday = 'on';
	}

	else{
		$xml->holiday = 'off';
	}

	$anfz=$_POST['fanfz'];
	$endz=$_POST['fendz'];

	//Speichert $xml in Datei
	file_put_contents('status.xml', $xml->asXML());
}

//Erzeuge Checkbox für jedes Gerät
foreach($xml->device as $device){
	echo $device->name."<input type='checkbox' id='check' name='fcheck".$device['id']."'";

	If($device->status == 'on'){
		echo "checked";
	}

	echo "><br>";
}

echo "Urlaubsmodus <input type='checkbox' name='holiday'";

if($xml->holiday == 'on'){
	echo "checked";
}

echo "></p><input type='submit' name='submit' value='OK'></form>";

//print_r($_POST);

?>

	<form action="settings.php" target="_self">
		<input type="submit" value="Einstellungen">
	</form>
</body>
</html>