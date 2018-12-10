<!DOCTYPE html>
<!-- Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-12-10
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
	Einschaltzeit eingeben: <input type='text' name='fanfz' value='".@$_POST['fanfz']."'><br>
	Ausschaltzeit eingeben: <input type='text' name='fendz' value='".@$_POST['fendz']."'></p>
	<p>";

$xml = simplexml_load_file('status.xml');

if(isset($_POST['submit'])){
	//echo "Submitted";
	
	//Schreibt Werte die in Chekcboxen ausgewählt wurden in $xml
	foreach($xml->device as $device1){
		$indent = "fcheck".$device1['id'];
		$indentvis = "fcheck_vis".$device1['id'];

		If(isset($_POST[$indentvis])){
			$device1->status = 'on';
			$device1->holiday = 'on';

			If(!empty($_POST['fanfz'])){
				$device1->timer->on = strtotime($_POST['fanfz']);
			}

			else{
				$device1->timer->on = 0;
			}

			If(!empty($_POST['fendz'])){
				$device1->timer->off = strtotime($_POST['fanfz']);
			}

			else{
				$device1->timer->off = 0;
			}
		}

		elseif(isset($_POST[$indent])){
			$device1->status = $_POST[$indent];
			$device1->holiday = $_POST[$indent];
		}

		else{
			$device1->status = 'off';
			$device1->holiday = 'off';
		}
	}

	If(isset($_POST['holiday'])){
		$xml->holiday->status = 'on';
	}

	else{
		$xml->holiday->status = 'off';
	}

	$anfz=$_POST['fanfz'];
	$endz=$_POST['fendz'];

	//Speichert $xml in Datei
	file_put_contents('status.xml', $xml->asXML());
}

//Erzeuge Checkbox für jedes Gerät
foreach($xml->device as $device){
	echo $device->name."<label class='switch'><input type='checkbox' name='fcheck_vis".$device['id']."' ";

	If($device->status == 'on'){
		echo "checked ";
	}
	If($xml->holiday->status == 'on'){
		echo "disabled><span class='slider round'>
		<input type='hidden' name='fcheck".$device['id']."' value='".$device->status."'>";
	}
	else{
		echo "><span class='slider round'>";
	}
	echo "</label><br>
		";
}

echo "Urlaubsmodus <label class='switch'>
	<input type='checkbox' name='holiday' id='holidaychk' ";

if($xml->holiday->status == 'on'){
	echo "checked";
}

echo "><span class='slider round'></span></label>
	</p><input type='submit' name='submit' value='OK' id='button'></form><p>";

//print_r($_POST);

?>

	<form action="settings.php" target="_self">
		<input type="submit" value="Einstellungen" id="button">
	</form>
</body>
</html>
