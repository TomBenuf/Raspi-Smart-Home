<!DOCTYPE html>
<!-- Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2019-03-23
   - Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

   - Dies ist die INDEX HTML-Datei. -->

<html>
<head>
<title>Raspi Smart-Home</title>
<link rel="stylesheet" type="text/css" href="format.css" />
<meta http-equiv="content-type" content="text/html; charset=utf-8">

</head>
<body>
	<p><h1>Ihre Smart-Home Steuerung</h1> </p>

<?php
// Läd XML und erstellt für jedes /devices/device einen Button.


$xml = simplexml_load_file('status.xml');

//print_r($_POST);
//print(hash('sha256',$_POST['fpassw']));
//echo "<br>";
//print($xml->passw);

if(hash('sha256',@$_POST['fpassw']) == $xml->passw){

echo "<table><form action='' method='POST'>
	<input type='hidden' name='fpassw' value=".@$_POST['fpassw'].">
	<tr><td>Einschaltzeit eingeben: </td><td><input type='text' name='fanfz'></td></tr>
	<tr><td>Ausschaltzeit eingeben: </td><td><input type='text' name='fendz'></td></td>
	</table><p><table>";

if(isset($_POST['submit'])){
	//echo "Submitted";
	
	//Schreibt Werte die in Chekcboxen ausgewählt wurden in $xml
	foreach($xml->device as $device1){
		$indent = "fcheck".$device1['id'];
		$indentvis = "fcheck_vis".$device1['id'];

		If(isset($_POST[$indentvis])){
			$device1->holiday = 'on';

			if(!empty($_POST['fanfz'])){
				$device1->status = 'off';
				$device1->timer->on = strtotime($_POST['fanfz']);
			}

			elseif(!empty($_POST['fendz'])){
				$device1->status = 'on';
				$device1->timer->off = strtotime($_POST['fendz']);
			}

			else{
				$device1->status = 'on';
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

	//Speichert $xml in Datei und erstellt .lock datei während schreibvorgang
	$lock = fopen('status.lock','w');
	fclose($lock);
	file_put_contents('status.xml', $xml->asXML());
	unlink('status.lock');
}

//Erzeuge Checkbox für jedes Gerät
foreach($xml->device as $device){
	echo "<tr><td>".$device->name."</td><td><label class='switch'><input type='checkbox' name='fcheck_vis".$device['id']."' ";

	If($device->status == 'on' and empty($_POST['anfz'])){
		echo "checked ";
	}
	If($xml->holiday->status == 'on'){
		echo "disabled><span class='slider round'>
		<input type='hidden' name='fcheck".$device['id']."' value='".$device->status."'>";
	}
	else{
		echo "><span class='slider round'>";
	}
	echo "</label></td></tr>";
}

echo "<tr><td>Urlaubsmodus </td><td><label class='switch'>
	<input type='checkbox' name='holiday' id='holidaychk' ";

if($xml->holiday->status == 'on'){
	echo "checked";
}

echo "><span class='slider round'></span></label></td></tr></table>
	</p><input type='submit' name='submit' value='OK' id='button'></form><p>";
}
else echo "Passwort falsch!<p>";
//print_r($_POST);

?>
<input type='button' onclick="location.href='index.php'" value='Zurück' id='button'>
</body>
</html>
