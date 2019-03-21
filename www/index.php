<!DOCTYPE html>
<!-- Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2019-03-21
   - Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

   - Dies ist die INDEX HTML-Datei. -->

<html>
<head>
<title>Raspi Smart-Home</title>
<link rel="stylesheet" type="text/css" href="format.css" />
<meta http-equiv="content-type" content="text/html; charset=utf-8">

</head>
<body>
	<p><h1>Ihre Smart-Home Steuerung <br> für unterwegs</h1> </p>

<?php


echo "<form action='settings.php' method='POST'>
		Bitte Passwort eingeben: <input type='password' name='fpassw'><p>
		<input type='submit' value='Login' id='button'>
	</form><p>

	<h3>Neues Passwort</h3>

	<form action='' method='POST'>
		Passwort eingeben: <input type='password' name='fpasswalt'><br>
		Neues Passwort eingeben: <input type='password' name='fpasswneu1'><br>
		Neues Passwort wiederholen: <input type='password' name='fpasswneu2'><p>
		<input type='submit' name='fsubmit' value='OK' id='button'>
	</form>";

if(@$_POST['fsubmit']){

	$xml = simplexml_load_file('status.xml');

	if(hash('sha256',@$_POST['fpasswalt']) == $xml->passw){

		if(@$_POST['fpasswneu1'] == @$_POST['fpasswneu2']){

			$xml->passw = hash('sha256',@$_POST['fpasswneu1']);
			file_put_contents('status.xml', $xml->asXML());
			echo "Passwort erfolgreich geändert!";
		}

		else echo "Die Eingaben stimmen nicht überein!";
	}

	else echo "Das alte Passwort ist falsch!";
}
?>
</body>
</html>
