<?php
	header("Content-Type:application/xml");
	echo '<?xml version="1.0" encoding="utf-8"?><korisnici>';

	$korisnik = $_GET['korisnik'];
	$korisnici = json_decode(file_get_contents('korisnici.json'));
	$found = 0;
	foreach($korisnici as $k) {
		if ($k->korisnicko_ime == $korisnik) {
			$found = 1;
		} 
	}
	echo "<korisnik>$found</korisnik>";
	echo "</korisnici>";
	
	
?>