<!DOCTYPE html>
<!-- Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-11-08
   - Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

   - Dies ist die INDEX HTML-Datei. -->

<html>
<head>

<title>
Raspi SmartHome
</title>
<link rel="stylesheet" type="text/css" href="format.css" />
<meta http-equiv="content-type" content="text/html; charset=utf-8">

</head>
<body>
	<p>
	Ihre Smart-Home Steuerung für unterwegs.</p>
<?php
     

/* Läd XML und erstellt für jedes /devices/device einen Button.
 * Bis jetzt aber noch ohne Aktion */


 $xml = simplexml_load_file('status.xml');

echo "<form action='' method='POST'>";
foreach ($xml->device as $device){
	echo "<input type='button' value=".$device->name.">";
	}
	echo "<input type='button' name='ferstellen' value='Erstellen' onClick=1>";
	if($_POST['ferstellen']=1)
	{echo "<input type='text' name='fneuname'>
	       <input type='password' name='fpass'>";
		   $neuname=$_POST['fneuname'];
		   $pass=$_POST['fpass'];  
		}
	if($pass="")
	{echo"<input type='button' value='$neuname'>";
		
	}		
echo "</form>";

?>



</body>
</html>
