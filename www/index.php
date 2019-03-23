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


echo "<table><form action='settings.php' method='POST'>
		<tr><td>Bitte Passwort eingeben: </td><td><input type='password' name='fpassw'></td></tr>
		</table><p>
		<input type='submit' value='Login' id='button'>
	</form><p>

	<h3>Neues Passwort</h3>

	<table><form action='' method='POST'>
		<tr><td>Passwort eingeben: </td><td><input type='password' name='fpasswalt'></td></tr>
		<tr><td>Neues Passwort eingeben: </td><td><input type='password' name='fpasswneu1'></td></tr>
		<tr><td>Neues Passwort wiederholen: </td><td><input type='password' name='fpasswneu2'></td></tr>
		</table><p>
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
